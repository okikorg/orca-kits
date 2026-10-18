"""Updates one kit's draft in the Orca kits organization. It never publishes:
only the operator does, at the server container's shell (orca-design
kit-trust D5.13).

    ORCA_KITS_API_KEY=... python scripts/publish.py <slug> [--allow-new] [--first]

ORCA_KITS_API_KEY is the publish key: a Member key of the Orca kits
organization whose id is in the server's ORCA_KIT_PUBLISHER_KEYS.

1. Refuses a dirty tree, or a HEAD not on origin/main (unless --first, the
   kit's first draft from its pull request), so what is published is what
   was reviewed on main. Runs check.py on the folder.
2. Updates each resource by the id in published.json, from the Python
   definitions: the agent, each skill (a new default version) and the
   template. A resource with no id is created only with --allow-new, and its
   id written to published.json at once, so a new id always lands in a PR.
3. Creates the draft kit the first time, then sets its words, its selection,
   its README as written, and its source: the link to its folder on main,
   which the kit's page shows as a GitHub icon.
4. Prints the operator line that publishes the draft, with the public id
   from published.json, or none for a kit's first publish, which mints one.
"""

import io
import json
import os
import subprocess
import sys
import urllib.error
import urllib.request
import zipfile

import check
import kitlib

NULLABLE_AGENT_FIELDS = sorted(check.AGENT_FIELDS - {"model"})


def fail(message):
    sys.exit(f"publish: {message}")


class Api:
    def __init__(self, key, origin):
        self.key, self.origin = key, origin.rstrip("/")

    def call(self, method, path, body=None):
        request = urllib.request.Request(
            self.origin + path,
            method=method,
            data=None if body is None else json.dumps(body).encode(),
            headers={"Authorization": f"Bearer {self.key}", "Content-Type": "application/json"},
        )
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                warning = response.headers.get("orca-warning")
                if warning:
                    print(f"warning: {warning}")
                return json.load(response)
        except urllib.error.HTTPError as error:
            fail(f"{method} {path}: HTTP {error.code} {error.read().decode(errors='replace')}")


def skill_zip(folder):
    data = io.BytesIO()
    with zipfile.ZipFile(data, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(folder.rglob("*")):
            if path.is_file():
                archive.write(path, f"{folder.name}/{path.relative_to(folder)}")
    return (f"{folder.name}.zip", data.getvalue(), "application/zip")


def operator_line(ids):
    """The server command that publishes the draft after its review, its diff
    and a typed yes. --public-id keeps the kit's link."""
    line = f"orca-agent-server kits publish --kit {ids['kit']}"
    return line + (f" --public-id {ids['public_id']}" if ids.get("public_id") else "")


def main(argv):
    from openai import OpenAI

    flags = {a for a in argv if a.startswith("--")}
    names = [a for a in argv if not a.startswith("--")]
    if len(names) != 1 or flags - {"--allow-new", "--first"}:
        sys.exit(__doc__)
    folder = kitlib.KITS / names[0]
    if not folder.is_dir():
        fail(f"no folder kits/{names[0]}")
    key = os.environ.get("ORCA_KITS_API_KEY") or fail("set ORCA_KITS_API_KEY, the publish key: a member key of the Orca kits organization whose id is in ORCA_KIT_PUBLISHER_KEYS")
    origin = os.environ.get("ORCA_ORIGIN", "https://api.orcapods.ai")

    if kitlib.git("status", "--porcelain"):
        fail("the tree has uncommitted changes; publish only what is committed and reviewed")
    commit = kitlib.git("rev-parse", "HEAD")
    if "--first" not in flags:
        kitlib.git("fetch", "--quiet", "origin", "main")
        if subprocess.run(["git", "merge-base", "--is-ancestor", commit, "origin/main"], cwd=kitlib.ROOT).returncode:
            fail(f"{commit[:7]} is not on origin/main; publish from main (or --first, for a kit's first publish from its PR)")
    problems = check.Problems()
    check.check_kit(folder, problems)
    if problems:
        fail("the folder does not pass check.py:\n" + "\n".join(problems))

    ids = kitlib.published(folder)
    allow_new = "--allow-new" in flags

    def record(field, value):
        ids[field] = value
        (folder / "published.json").write_text(json.dumps(ids, indent=2) + "\n")

    def need_new(what):
        if not allow_new:
            fail(f"{what} has no id in published.json; create it locally with --allow-new and commit published.json")

    client = OpenAI(api_key=key, base_url=f"{origin}/v1")
    templates = client.beta.agents.environments.templates

    # Skills first: the template names them by id.
    skill_ids = dict(ids.get("skills", {}))
    for skill in kitlib.skill_dirs(folder):
        bundle = skill_zip(skill)
        if skill.name in skill_ids:
            version = client.skills.versions.create(skill_ids[skill.name], files=[bundle], default=True)
            print(f"skill {skill.name}: version {version.version}")
        else:
            need_new(f"skill {skill.name}")
            created = client.skills.create(files=[bundle])
            skill_ids[skill.name] = created.id
            record("skills", dict(skill_ids))
            print(f"skill {skill.name}: created {created.id}")

    bodies = kitlib.python_bodies(folder, skill_ids)
    agent = bodies["agent"]
    if ids.get("agent"):
        resets = {field: None for field in NULLABLE_AGENT_FIELDS if field not in agent}
        client.beta.agents.update(ids["agent"], **resets, **agent)
        print(f"agent {agent['name']}: updated {ids['agent']}")
    else:
        need_new(f"agent {agent['name']}")
        record("agent", client.beta.agents.create(**agent).id)
        print(f"agent {agent['name']}: created {ids['agent']}")

    if "template" in bodies:
        if ids.get("template"):
            templates.update(ids["template"], **bodies["template"])
            print(f"template: updated {ids['template']}")
        else:
            need_new("the template")
            record("template", templates.create(**bodies["template"]).id)
            print(f"template: created {ids['template']}")

    words = kitlib.words(folder)
    kit_body = {
        **words,
        "readme": (folder / "README.md").read_text().rstrip(),
        "source": f"https://github.com/okikorg/orca-kits/tree/main/kits/{folder.name}",
        "selection": {
            "agents": [ids["agent"]],
            "skills": [skill_ids[s.name] for s in kitlib.skill_dirs(folder)],
            "templates": [ids["template"]] if ids.get("template") else [],
        },
    }
    api = Api(key, origin)
    if ids.get("kit"):
        api.call("PATCH", f"/api/kits/{ids['kit']}", kit_body)
    else:
        need_new("the kit")
        kit = api.call("POST", "/api/kits", kit_body)
        record("kit", kit["id"])
        print(f"kit: created {kit['id']} (draft)")

    print(f"kit {ids['kit']}: draft updated from {commit[:7]}, not published")
    print("To publish it, run this at the server container's shell (orca-agent-server docs/kits-publishing.md):")
    print(operator_line(ids))
    if not ids.get("public_id"):
        print("Then add the public id it prints to published.json, with the README's Add it lines, in a pull request.")


if __name__ == "__main__":
    main(sys.argv[1:])
