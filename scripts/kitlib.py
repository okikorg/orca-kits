"""Reading a kit folder: its words, README, skills, and the bodies its Python
and TypeScript definitions send. Shared by check.py, publish.py and live.py.

A definition is called with a stand-in whose create() returns its arguments,
so the body is what the API would get, read without calling it.
"""

import importlib.util
import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
KITS = ROOT / "kits"


class _Record:
    def create(self, **body):
        return body


class _SkillIds(dict):
    """Skill ids by folder name. Missing names read as a stand-in that says
    which kit skill was meant, so a definition can be read before publishing."""

    def __missing__(self, name):
        return f"kit_skill:{name}"


def kit_dirs():
    return sorted(p for p in KITS.iterdir() if p.is_dir()) if KITS.is_dir() else []


def words(folder):
    return json.loads((folder / "kit.json").read_text())


def skill_dirs(folder):
    skills = folder / "skills"
    return sorted(p for p in skills.iterdir() if p.is_dir()) if skills.is_dir() else []


def _load(path):
    name = f"kit_{path.parent.name.replace('-', '_')}_{path.stem}"
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(path.parent))
    try:
        spec.loader.exec_module(module)
    finally:
        sys.path.remove(str(path.parent))
    return module


def python_bodies(folder, skill_ids=None):
    """{"agent": body, "template": body} from agent.py and template.py."""
    bodies = {}
    if (folder / "agent.py").exists():
        bodies["agent"] = _load(folder / "agent.py").define(_Record())
    if (folder / "template.py").exists():
        ids = _SkillIds(skill_ids or {})
        bodies["template"] = _load(folder / "template.py").define(_Record(), ids)
    return bodies


def typescript_bodies(folder):
    """The same, from agent.ts and template.ts, through scripts/define.ts."""
    result = subprocess.run(
        ["node", "--experimental-strip-types", "--no-warnings", str(ROOT / "scripts" / "define.ts"), str(folder)],
        capture_output=True,
        text=True,
        cwd=ROOT,
    )
    if result.returncode != 0:
        raise RuntimeError(f"define.ts failed for {folder.name}:\n{result.stderr.strip()}")
    return json.loads(result.stdout)


def published(folder):
    path = folder / "published.json"
    return json.loads(path.read_text()) if path.exists() else {}


def git(*args, check=True):
    result = subprocess.run(["git", *args], capture_output=True, text=True, cwd=ROOT)
    if check and result.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)}: {result.stderr.strip()}")
    return result.stdout.strip()


# A kit's example: one real run, recorded by scripts/example.py in
# example.json and shown as the README's Example section, which the kit's
# page lifts out and draws above the README (orca-design kits-teams D5.2,
# amended 2026-10-14). The section ends at its run line, so an answer may
# hold any markdown, headings included.
EXAMPLE_HEADING = "## Example"
EXAMPLE_FIELDS = ("question", "answer", "cost_micro_usd", "model", "session", "asked_on")
RUN_LINE = re.compile(r"^A real run on (\d{4}-\d{2}-\d{2})\. It cost \$(\d+(?:\.\d+)?) of Orca credit\.$")


def example(folder):
    path = folder / "example.json"
    return json.loads(path.read_text()) if path.exists() else None


def money(micro):
    """Micro-USD as dollars: to the cent from a cent up, else to four places."""
    dollars = micro / 1_000_000
    return f"${dollars:.2f}" if dollars >= 0.01 else f"${dollars:.4f}"


def render_example(record):
    """The README's Example section for a record, ending at its run line."""
    question = " ".join(record["question"].split())
    return "\n\n".join(
        [
            EXAMPLE_HEADING,
            f"> {question}",
            record["answer"].strip(),
            f"A real run on {record['asked_on']}. It cost {money(record['cost_micro_usd'])} of Orca credit.",
        ]
    )


def example_span(text):
    """(start, end) of the Example section in a README: from its heading to
    the end of its run line, or None when there is none."""
    lines = text.splitlines(keepends=True)
    offset, start = 0, None
    for line in lines:
        bare = line.rstrip("\n")
        if start is None and bare == EXAMPLE_HEADING:
            start = offset
        elif start is not None and RUN_LINE.match(bare):
            return start, offset + len(bare)
        offset += len(line)
    return None


def without_example(text):
    """The README with its Example section (and the blank line after it) left out."""
    span = example_span(text)
    if not span:
        return text
    start, end = span
    return text[:start] + text[end:].lstrip("\n")


def with_example(text, record):
    """The README with its Example section replaced, or added before What it uses."""
    section = render_example(record)
    span = example_span(text)
    if span:
        return text[: span[0]] + section + text[span[1] :]
    marker = "\n## What it uses"
    index = text.index(marker)
    return text[:index] + "\n" + section + "\n" + text[index:]
