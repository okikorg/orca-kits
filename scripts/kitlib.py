"""Reading a kit folder: its words, README, skills, and the bodies its Python
and TypeScript definitions send. Shared by check.py, publish.py and live.py.

A definition is called with a stand-in whose create() returns its arguments,
so the body is what the API would get, read without calling it.
"""

import importlib.util
import json
import pathlib
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
