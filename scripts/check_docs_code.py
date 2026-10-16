"""Docs pages show a kit's agents.create call in Python and TypeScript:
the start page and the Kits tab's page for Scout show kits/scout's, and the
Kits tab's pages for Cram Coach and Margin Check show kits/cram-coach's and
kits/margin-check's. This fails unless each equals the call in its kit,
character for character, so a page and its kit can never drift.

    python scripts/check_docs_code.py <orca-docs dir> [<orca-kits dir>]

orca-kits CI runs it against orca-docs main; orca-docs CI runs it, from
orca-kits main, against its own tree.
"""

import pathlib
import re
import sys

# Each page, and the kit whose code it shows.
PAGES = {
    "start-here.mdx": "scout",
    "kits/scout.mdx": "scout",
    "kits/cram-coach.mdx": "cram-coach",
    "kits/margin-check.mdx": "margin-check",
}
BLOCK = re.compile(r"^```(\w+)[^\n]*\n(.*?)^```", re.DOTALL | re.MULTILINE)


def create_call(text):
    """The text from `agents.create(` to its closing parenthesis, with the
    indentation of its first line taken off every line, or None."""
    start = text.find("agents.create(")
    if start < 0:
        return None
    depth, quote, escaped, end = 0, None, False, None
    for i in range(start + len("agents.create"), len(text)):
        c = text[i]
        if quote:
            if escaped:
                escaped = False
            elif c == "\\":
                escaped = True
            elif c == quote:
                quote = None
        elif c in "'\"`":
            quote = c
        elif c in "([{":
            depth += 1
        elif c in ")]}":
            depth -= 1
            if depth == 0:
                end = i + 1
                break
    if end is None:
        return None
    line_start = text.rfind("\n", 0, start) + 1
    indent = len(text[line_start:start]) - len(text[line_start:start].lstrip())
    lines = text[start:end].split("\n")
    return "\n".join([lines[0]] + [line[indent:] if line[:indent].strip() == "" else line for line in lines[1:]])


def agent_name(call):
    """The name a create call gives its agent, or None."""
    found = re.search(r"\bname\s*[:=]\s*['\"]([^'\"]+)['\"]", call)
    return found and found[1]


def page_calls(page, name):
    """The create call in each language on a page: the code blocks that
    create an agent with this name."""
    calls = {}
    for lang, body in BLOCK.findall(page):
        call = create_call(body)
        if call and agent_name(call) == name:
            key = {"python": "py", "typescript": "ts", "ts": "ts", "py": "py"}.get(lang)
            if key and key not in calls:
                calls[key] = call
    return calls


def check_page(docs, kits, path, kit):
    """The errors for one page: none if each language's call equals the
    kit's. A page not in this tree yet has nothing to compare."""
    if not (docs / path).is_file():
        print(f"{path} is not in the docs yet; nothing to compare")
        return []
    code = {key: create_call((kits / "kits" / kit / f"agent.{key}").read_text()) for key in ("py", "ts")}
    calls = page_calls((docs / path).read_text(), agent_name(code["py"]))
    errors = []
    for key in ("py", "ts"):
        if key not in calls:
            errors.append(f"{path}: no {key} code block creating {kit}")
        elif calls[key] != code[key]:
            errors.append(f"{path}: the {key} code differs from kits/{kit}/agent.{key}\n--- page\n{calls[key]}\n--- kit\n{code[key]}")
    if not errors:
        print(f"{path}: the Python and TypeScript code equal kits/{kit}")
    return errors


def main(argv):
    if not argv:
        sys.exit(__doc__)
    docs = pathlib.Path(argv[0])
    kits = pathlib.Path(argv[1]) if len(argv) > 1 else pathlib.Path(__file__).resolve().parent.parent
    errors = [error for path, kit in PAGES.items() for error in check_page(docs, kits, path, kit)]
    if errors:
        sys.exit("\n".join(errors))


if __name__ == "__main__":
    main(sys.argv[1:])
