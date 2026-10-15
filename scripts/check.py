"""Checks every kit folder against what the server accepts, and the repo's
words.

    python scripts/check.py              every kit, and every file's words
    python scripts/check.py scout        one kit

The kit rules mirror orca-agent-server main@46db784: src/kits/mod.rs
(selection, manifest, templates), src/api/validation.rs (agent fields, tools)
and src/api/templates.rs (template fields). The bodies themselves are typed
by the pinned openai packages (tsc), and the Python and TypeScript bodies
must be equal.

A kit's README is published with the kit (orca-design kits-teams D5.2,
amended 2026-10-13 and 2026-10-15), so it holds five sections and no more:
the title, a short description, What it uses, Add it and Use it, in at most
1,500 bytes. Kits have no recorded example since 2026-10-15: the kit's page
no longer shows one.
"""

import json
import re
import sys

import kitlib

AGENT_FIELDS = {"model", "instructions", "name", "metadata", "multi_agent", "reasoning", "service_tier", "text", "tools"}
TOOL_TYPES = {"function", "tool_search", "programmatic_tool_calling", "web_search", "mcp"}
TEMPLATE_FIELDS = {"name", "capability_directories", "env", "files", "network", "packages", "plugins", "setup_commands", "skills"}
WORD_FIELDS = {"name": 100, "description": 1000, "author": 100}
README_MAX = 1_500
SECTIONS = ["## What it uses", "## Add it", "## Use it"]
DESCRIPTION_MAX = 140
KIT_LINK = "https://app.orcapods.ai/kits/"
MAX_PER_KIND = 50
MODEL = "orca/openrouter/openai/gpt-5.6-luna"
SKILL_NAME = re.compile(r"^[A-Za-z0-9_-]+$")
# A currency sign before a digit, a percentage, or a number before a unit of
# money or time: amounts belong on the pricing page, not in a README.
AMOUNT = re.compile(r"[$€£]\s?\d|\d\s?%|\b\d[\d,.]*\s*(?:hours?|hrs?|credits?|cents?|USD|per\b)", re.IGNORECASE)
LINK = re.compile(r"\]\(([^)\s]+)")
# Phrases that only the coding-agent prompt uses. The prompt lives on
# docs.orcapods.ai/start-here; everything else links to it.
PROMPT_PHRASES = ("Set me up on Orca", "Onboard me to Orca")


class Problems(list):
    def add(self, where, message):
        self.append(f"{where}: {message}")


def check_words(folder, problems):
    where = f"kits/{folder.name}/kit.json"
    try:
        words = kitlib.words(folder)
    except (OSError, json.JSONDecodeError) as error:
        problems.add(where, f"cannot read: {error}")
        return
    if set(words) != set(WORD_FIELDS):
        problems.add(where, f"holds exactly {sorted(WORD_FIELDS)}, not {sorted(words)}")
    for field, limit in WORD_FIELDS.items():
        value = words.get(field)
        if not isinstance(value, str) or not value.strip() or len(value.encode()) > limit:
            problems.add(where, f"{field} is text of 1 to {limit} bytes")
    description = words.get("description")
    if isinstance(description, str) and (len(description) > DESCRIPTION_MAX or not description.endswith(".") or re.search(r"[.!?]\s", description)):
        problems.add(where, f"description is one sentence of at most {DESCRIPTION_MAX} characters, what the kit does for the visitor")


def check_agent(where, body, problems):
    if not isinstance(body, dict):
        problems.add(where, "define() returns no body")
        return
    unknown = set(body) - AGENT_FIELDS
    if unknown:
        problems.add(where, f"fields the server refuses: {sorted(unknown)}")
    if body.get("model") != MODEL:
        problems.add(where, f"model is {MODEL}, an Orca credit model anyone can copy")
    if not isinstance(body.get("name"), str) or not body["name"].strip():
        problems.add(where, "name is required, so programs can find the copy")
    for i, tool in enumerate(body.get("tools") or []):
        if not isinstance(tool, dict) or tool.get("type") not in TOOL_TYPES:
            problems.add(where, f"tools[{i}] type is one of {sorted(TOOL_TYPES)}")
        elif tool["type"] == "function" and not tool.get("name"):
            problems.add(where, f"tools[{i}] function needs a name")
        elif tool["type"] == "mcp":
            problems.add(where, f"tools[{i}]: remote MCP is blocked on hosted Orca")


def check_template(where, body, skill_names, problems):
    if not isinstance(body, dict):
        problems.add(where, "define() returns no body")
        return
    unknown = set(body) - TEMPLATE_FIELDS
    if unknown:
        problems.add(where, f"fields the server refuses: {sorted(unknown)}")
    if not isinstance(body.get("name"), str) or not body["name"].strip():
        problems.add(where, "name is required")
    for i, file in enumerate(body.get("files") or []):
        if isinstance(file, dict) and file.get("type") == "file_id":
            problems.add(where, f"files[{i}] mounts an uploaded file, which a kit does not carry; use inline files")
    for i, skill in enumerate(body.get("skills") or []):
        ref = skill.get("skill_id", "") if isinstance(skill, dict) else ""
        if not (isinstance(skill, dict) and skill.get("type") == "skill_reference" and ref.startswith("kit_skill:")):
            problems.add(where, f"skills[{i}] names a skill by its folder: skills[\"<folder>\"]")
        elif ref.removeprefix("kit_skill:") not in skill_names:
            problems.add(where, f"skills[{i}] names {ref.removeprefix('kit_skill:')}, which is not in skills/")
    if body.get("env"):
        problems.add(where, "sets environment values, which never travel in a kit; the copier sets them")


def check_skills(folder, problems):
    names = set()
    for skill in kitlib.skill_dirs(folder):
        where = f"kits/{folder.name}/skills/{skill.name}"
        names.add(skill.name)
        if not SKILL_NAME.match(skill.name):
            problems.add(where, "a skill name is letters, digits, _ and -")
        text = (skill / "SKILL.md").read_text() if (skill / "SKILL.md").exists() else ""
        front = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
        if not front:
            problems.add(where, "SKILL.md starts with frontmatter holding name and description")
            continue
        fields = dict(line.split(":", 1) for line in front.group(1).splitlines() if ":" in line)
        if fields.get("name", "").strip() != skill.name:
            problems.add(where, "SKILL.md's name matches its folder")
        if not fields.get("description", "").strip():
            problems.add(where, "SKILL.md has a description")
    return names


def headings(text):
    """(line number, heading) for each markdown heading outside fenced code."""
    found, fenced = [], False
    for number, line in enumerate(text.splitlines(), 1):
        if line.startswith("```"):
            fenced = not fenced
        elif not fenced and re.match(r"^#{1,6}\s", line):
            found.append((number, line.strip()))
    return found


def check_sections(where, text, name, public_id, problems):
    """The title, one short paragraph, then What it uses, Add it and Use it."""
    found = headings(text)
    if not found or found[0] != (1, f"# {name}"):
        problems.add(where, f"starts with the title line \"# {name}\", the kit's name in kit.json")
    rest = [heading for _, heading in found[1:]]
    sections = SECTIONS
    if rest != sections:
        problems.add(where, f"has exactly the sections {sections}, in that order, and no other heading; found {rest}")
        return
    lines = text.splitlines()
    starts = {heading: number for number, heading in found}
    intro = "\n".join(lines[1 : starts[sections[0]] - 1]).strip()
    if not intro or "\n\n" in intro or intro.startswith(("-", "*", ">", "```", "|")):
        problems.add(where, "has one short paragraph between the title and What it uses")
    add_it = "\n".join(lines[starts["## Add it"] : starts["## Use it"] - 1])
    if public_id and f"orca kits copy {KIT_LINK}{public_id} --yes" not in add_it:
        problems.add(where, f"Add it holds `orca kits copy {KIT_LINK}{public_id} --yes`, the kit's own link")
    if public_id and f"Or click **Copy** on [the kit's page]({KIT_LINK}{public_id})." not in add_it:
        problems.add(where, f"Add it ends with \"Or click **Copy** on [the kit's page]({KIT_LINK}{public_id}).\"")


def check_readme(folder, problems):
    where = f"kits/{folder.name}/README.md"
    path = folder / "README.md"
    if not path.exists():
        problems.add(where, "missing")
        return
    text = path.read_text()
    if len(text.encode()) > README_MAX:
        problems.add(where, f"at most {README_MAX} bytes; it has {len(text.encode())}")
    for match in AMOUNT.finditer(text):
        problems.add(where, f"names an amount ({match.group(0)!r}); link to https://orcapods.ai/pricing instead")
    for target in LINK.findall(text):
        if not target.startswith(("https://", "http://", "mailto:", "#")):
            problems.add(where, f"link {target} is relative; the kit's page shows this README too")
    try:
        name = kitlib.words(folder).get("name", "")
    except (OSError, json.JSONDecodeError):
        name = ""  # check_words reports it
    check_sections(where, text, name, kitlib.published(folder).get("public_id"), problems)


def check_kit(folder, problems):
    check_words(folder, problems)
    check_readme(folder, problems)
    skill_names = check_skills(folder, problems)
    has = {name: (folder / name).exists() for name in ("agent.py", "agent.ts", "template.py", "template.ts", "run.py", "run.ts")}
    for stem in ("agent", "template", "run"):
        if has[f"{stem}.py"] != has[f"{stem}.ts"]:
            problems.add(f"kits/{folder.name}", f"{stem}.py and {stem}.ts come together, or not at all")
    if not has["agent.py"]:
        problems.add(f"kits/{folder.name}", "agent.py and agent.ts define the kit's agent")
        return
    if skill_names and not has["template.py"]:
        problems.add(f"kits/{folder.name}", "skills reach a session only through a template: add template.py and template.ts")
    if len(skill_names) > MAX_PER_KIND:
        problems.add(f"kits/{folder.name}", f"at most {MAX_PER_KIND} skills")
    try:
        python = kitlib.python_bodies(folder)
        typescript = kitlib.typescript_bodies(folder)
    except Exception as error:  # a definition that does not load is the finding
        problems.add(f"kits/{folder.name}", f"definitions do not load: {error}")
        return
    check_agent(f"kits/{folder.name}/agent.py", python.get("agent"), problems)
    if "template" in python:
        check_template(f"kits/{folder.name}/template.py", python["template"], skill_names, problems)
    for kind in sorted(set(python) | set(typescript)):
        if python.get(kind) != typescript.get(kind):
            problems.add(
                f"kits/{folder.name}/{kind}",
                "the Python and TypeScript definitions differ:\n"
                f"  py: {json.dumps(python.get(kind), sort_keys=True)}\n"
                f"  ts: {json.dumps(typescript.get(kind), sort_keys=True)}",
            )


def check_repo_words(problems):
    files = kitlib.git("ls-files", "--cached", "--others", "--exclude-standard").splitlines()
    for name in files:
        path = kitlib.ROOT / name
        if not path.is_file() or name.endswith("package-lock.json"):
            continue
        try:
            text = path.read_text()
        except UnicodeDecodeError:
            continue
        if chr(0x2014) in text:
            problems.add(name, "has an em dash")
        if name != "scripts/check.py" and any(phrase in text for phrase in PROMPT_PHRASES):
            problems.add(name, "copies the coding-agent prompt; link docs.orcapods.ai/start-here#have-your-coding-agent-do-it")


def main(argv):
    problems = Problems()
    names = [a for a in argv if not a.startswith("--")]
    folders = [kitlib.KITS / n for n in names] if names else kitlib.kit_dirs()
    for folder in folders:
        check_kit(folder, problems)
    if not names:
        check_repo_words(problems)
    for problem in problems:
        print(problem, file=sys.stderr)
    if problems:
        sys.exit(1)
    print("ok")


if __name__ == "__main__":
    main(sys.argv[1:])
