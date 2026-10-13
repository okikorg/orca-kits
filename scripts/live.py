"""Runs a published kit live, as a new user would, in the test organization,
then deletes everything the run created.

    ORCA_PROD_TEST_API_KEY=... python scripts/live.py <slug> [--docs <orca-docs dir>]

It copies the kit with `orca kits copy <link> --yes`, reads the agent with
`orca agents get`, runs the kit's steps below (an `orca chat` question, or
the kit's run.py and run.ts), and, for Scout with --docs, the start page's
own scout.py and scout.ts. Then it deletes the sessions the run opened and
the agents, skills and templates the copy created, and lists any it could
not delete. The CLI runs with its own config directory, so the run never
touches the caller's login.

Set ORCA_CLI to the orca binary to use (default: orca on PATH).
"""

import json
import os
import pathlib
import re
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request

import kitlib

ORIGIN = "https://api.orcapods.ai"

# What each kit is asked, through `orca chat <agent> <question>`.
QUESTIONS = {
    "scout": ["What's new in the latest Python release? Cite your sources."],
}


class Run:
    def __init__(self, key, workdir):
        self.key = key
        self.env = {
            **os.environ,
            "ORCA_API_KEY": key,
            "ORCA_API_URL": ORIGIN,
            "ORCA_CONFIG_DIR": str(workdir / "config"),
            "ORCA_NO_UPDATE_CHECK": "1",
        }
        self.cli = os.environ.get("ORCA_CLI", "orca")
        self.failures = []

    def sh(self, *args, cwd=None, show=True):
        print(f"\n$ {' '.join(args)}", flush=True)
        result = subprocess.run(args, env=self.env, cwd=cwd, capture_output=True, text=True)
        if show and result.stdout:
            print(result.stdout.rstrip())
        if result.returncode:
            print(result.stderr.rstrip(), file=sys.stderr)
            self.failures.append(f"{' '.join(args)} exited {result.returncode}")
        return result

    def orca(self, *args, **kwargs):
        return self.sh(self.cli, *args, **kwargs)

    def api(self, method, path):
        request = urllib.request.Request(ORIGIN + path, method=method, headers={"Authorization": f"Bearer {self.key}"})
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                return json.load(response)
        except urllib.error.HTTPError as error:
            if error.code == 404 and method == "DELETE":
                return None
            raise


def page_programs(docs):
    """The start page's scout.py and scout.ts code blocks."""
    page = (pathlib.Path(docs) / "start-here.mdx").read_text()
    blocks = dict(re.findall(r"^```\w+ (scout\.(?:py|ts))\n(.*?)^```", page, re.DOTALL | re.MULTILINE))
    return blocks


def main(argv):
    docs = argv[argv.index("--docs") + 1] if "--docs" in argv[:-1] else None
    names = [a for a in argv if not a.startswith("--") and a != docs]
    if len(names) != 1:
        sys.exit(__doc__)
    folder = kitlib.KITS / names[0]
    public_id = kitlib.published(folder).get("public_id") or sys.exit(f"kits/{folder.name} is not published yet")
    key = os.environ.get("ORCA_PROD_TEST_API_KEY") or sys.exit("set ORCA_PROD_TEST_API_KEY")
    link = f"https://app.orcapods.ai/kits/{public_id}"

    with tempfile.TemporaryDirectory(prefix="orca-live-") as tmp:
        run = Run(key, pathlib.Path(tmp))
        before = {s["id"] for s in run.api("GET", "/v1/agents/sessions?limit=100")["data"]}
        copied = run.orca("--json", "kits", "copy", link, "--yes", show=False)
        created = json.loads(copied.stdout).get("created", []) if copied.returncode == 0 else []
        print(json.dumps(created, indent=2))
        try:
            agent = next((c for c in created if c["kind"] == "agent"), None)
            if agent:
                run.orca("agents", "get", agent["name"])
                for question in QUESTIONS.get(folder.name, []):
                    run.orca("chat", agent["name"], question)
                for program in ("run.py", "run.ts"):
                    if (folder / program).exists():
                        runner = [sys.executable] if program.endswith(".py") else ["node", "--experimental-strip-types"]
                        run.sh(*runner, str(folder / program), cwd=folder)
                if folder.name == "scout" and docs:
                    for name, code in sorted(page_programs(docs).items()):
                        # Written inside the repo, so scout.ts resolves the pinned openai.
                        path = kitlib.ROOT / f".live-{name}"
                        path.write_text(code)
                        runner = [sys.executable] if name.endswith(".py") else ["node", "--experimental-strip-types"]
                        try:
                            run.sh(*runner, str(path), cwd=kitlib.ROOT)
                        finally:
                            path.unlink()
        finally:
            leftovers = []
            after = run.api("GET", "/v1/agents/sessions?limit=100")["data"]
            for session in after:
                if session["id"] not in before:
                    run.api("DELETE", f"/v1/agents/sessions/{session['id']}")
                    print(f"deleted session {session['id']}")
            paths = {"agent": "/v1/agents/", "skill": "/v1/skills/", "template": "/v1/agents/environments/templates/"}
            for item in reversed(created):
                try:
                    run.api("DELETE", paths[item["kind"]] + item["id"])
                    print(f"deleted {item['kind']} {item['id']}")
                except urllib.error.HTTPError as error:
                    leftovers.append(f"{item['kind']} {item['id']}: HTTP {error.code}")
            for session in run.api("GET", "/v1/agents/sessions?limit=100")["data"]:
                if session["id"] not in before:
                    leftovers.append(f"session {session['id']}")
            for leftover in leftovers:
                print(f"LEFT BEHIND: {leftover}", file=sys.stderr)
        if run.failures or leftovers:
            for failure in run.failures:
                print(f"FAILED: {failure}", file=sys.stderr)
            sys.exit(1)
        print(f"\nlive run of kits/{folder.name} passed; nothing left behind")


if __name__ == "__main__":
    main(sys.argv[1:])
