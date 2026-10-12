"""The start page shows Scout's agents.create call in Python and TypeScript.
This fails unless each equals the call in kits/scout, character for
character, so the page and the kit can never drift.

    python scripts/check_docs_code.py <orca-docs dir> [<orca-kits dir>]

orca-kits CI runs it against orca-docs main; orca-docs CI runs it, from
orca-kits main, against its own tree.
"""

import pathlib
import re
import sys

PAGE = "start-here.mdx"
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


def page_calls(page):
    """Scout's create call in each language on the page: the code blocks
    that create an agent named scout."""
    calls = {}
    for lang, body in BLOCK.findall(page):
        call = create_call(body)
        if call and re.search(r"name\s*[:=]\s*['\"]scout['\"]", call):
            key = {"python": "py", "typescript": "ts", "ts": "ts", "py": "py"}.get(lang)
            if key and key not in calls:
                calls[key] = call
    return calls


def main(argv):
    if not argv:
        sys.exit(__doc__)
    docs = pathlib.Path(argv[0])
    kits = pathlib.Path(argv[1]) if len(argv) > 1 else pathlib.Path(__file__).resolve().parent.parent
    page = (docs / PAGE).read_text()
    calls = page_calls(page)
    if not calls:
        # The page with Scout's code is orca-docs #18; until it is on main,
        # there is nothing to compare.
        print(f"{PAGE} shows no Scout code yet; nothing to compare")
        return
    failed = False
    for key in ("py", "ts"):
        kit = create_call((kits / "kits" / "scout" / f"agent.{key}").read_text())
        if key not in calls:
            print(f"{PAGE}: no {key} code block creating scout", file=sys.stderr)
            failed = True
        elif calls[key] != kit:
            print(f"{PAGE}: Scout's {key} code differs from kits/scout/agent.{key}", file=sys.stderr)
            print(f"--- page\n{calls[key]}\n--- kit\n{kit}", file=sys.stderr)
            failed = True
    if failed:
        sys.exit(1)
    print(f"{PAGE}: Scout's Python and TypeScript code equal kits/scout")


if __name__ == "__main__":
    main(sys.argv[1:])
