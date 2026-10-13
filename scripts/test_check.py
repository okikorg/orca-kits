"""Proves check.py refuses each shape the server refuses, and passes the real
kits. Each case is a copy of kits/scout with one thing broken.

    python scripts/test_check.py
"""

import json
import pathlib
import shutil
import sys
import tempfile

import check
import kitlib

SCOUT = kitlib.KITS / "scout"

TEMPLATE_PY = '''
def define(templates, skills):
    return templates.create(name="t", skills=[{"type": "skill_reference", "skill_id": skills["%s"]}]%s)
'''
TEMPLATE_TS = '''
export function define(templates: any, skills: any) {
  return templates.create({ name: 't', skills: [{ type: 'skill_reference', skill_id: skills['%s'] }]%s });
}
'''
SKILL = "---\nname: %s\ndescription: A test skill.\n---\nDo the thing.\n"


def edit(folder, name, old, new):
    path = folder / name
    text = path.read_text()
    assert old in text, (name, old)
    path.write_text(text.replace(old, new))


def both(folder, old_py, new_py, old_ts, new_ts):
    edit(folder, "agent.py", old_py, new_py)
    edit(folder, "agent.ts", old_ts, new_ts)


def add_template(folder, skill_folder, skill_name, named, extra_py="", extra_ts=""):
    (folder / "skills" / skill_folder).mkdir(parents=True)
    (folder / "skills" / skill_folder / "SKILL.md").write_text(SKILL % skill_name)
    (folder / "template.py").write_text(TEMPLATE_PY % (named, extra_py))
    (folder / "template.ts").write_text(TEMPLATE_TS % (named, extra_ts))


CASES = {
    "unknown agent field": (
        lambda f: both(f, 'name="scout",', 'name="scout", files=[],', "name: 'scout',", "name: 'scout', files: [],"),
        "fields the server refuses",
    ),
    "Python and TypeScript differ": (
        lambda f: edit(f, "agent.ts", "name: 'scout'", "name: 'scouts'"),
        "definitions differ",
    ),
    "another model": (
        lambda f: both(f, "gpt-5.6-luna", "gpt-5.6", "gpt-5.6-luna", "gpt-5.6"),
        "Orca credit model",
    ),
    "remote MCP": (
        lambda f: both(
            f,
            '[{"type": "web_search"}]',
            '[{"type": "mcp", "server_label": "x"}]',
            "[{ type: 'web_search' }]",
            "[{ type: 'mcp', server_label: 'x' } as any]",
        ),
        "remote MCP is blocked",
    ),
    "skill name differs from its folder": (
        lambda f: add_template(f, "notes", "other", "notes"),
        "matches its folder",
    ),
    "template names a skill outside the kit": (
        lambda f: add_template(f, "notes", "notes", "missing"),
        "not in skills/",
    ),
    "template mounts an uploaded file": (
        lambda f: add_template(
            f, "notes", "notes", "notes",
            ', files=[{"type": "file_id", "file_id": "file_1", "path": "/x"}]',
            ", files: [{ type: 'file_id', file_id: 'file_1', path: '/x' }]",
        ),
        "mounts an uploaded file",
    ),
    "template sets environment values": (
        lambda f: add_template(f, "notes", "notes", "notes", ', env={"TOKEN": "x"}', ", env: { TOKEN: 'x' }"),
        "environment values",
    ),
    "skills without a template": (
        lambda f: ((f / "skills" / "notes").mkdir(parents=True), (f / "skills" / "notes" / "SKILL.md").write_text(SKILL % "notes")),
        "through a template",
    ),
    "run.py without run.ts": (
        lambda f: (f / "run.py").write_text("print(1)\n"),
        "come together",
    ),
    "extra word in kit.json": (
        lambda f: (f / "kit.json").write_text(json.dumps({**kitlib.words(f), "tags": []})),
        "holds exactly",
    ),
    "amount in the README": (
        lambda f: edit(f, "README.md", "See [pricing]", "It costs $0.01 a search. See [pricing]"),
        "names an amount",
    ),
    "relative link in the README": (
        lambda f: edit(f, "README.md", "](https://github.com/okikorg/orca-kits/blob/main/kits/scout/agent.py)", "](agent.py)"),
        "is relative",
    ),
}


def main():
    failures = []
    for kit in kitlib.kit_dirs():
        problems = check.Problems()
        check.check_kit(kit, problems)
        if problems:
            failures.append(f"kits/{kit.name} should pass: {problems}")
    with tempfile.TemporaryDirectory(dir=kitlib.ROOT, prefix=".test-") as tmp:
        for name, (break_it, expected) in CASES.items():
            folder = pathlib.Path(tmp) / name.replace(" ", "-")
            shutil.copytree(SCOUT, folder, ignore=shutil.ignore_patterns("published.json", "__pycache__"))
            break_it(folder)
            problems = check.Problems()
            check.check_kit(folder, problems)
            if not any(expected in p for p in problems):
                failures.append(f"{name}: expected a problem with {expected!r}, got {list(problems)}")
            else:
                print(f"refused: {name}")
    for failure in failures:
        print(failure, file=sys.stderr)
    if failures:
        sys.exit(1)
    print("ok")


if __name__ == "__main__":
    main()
