"""Records a kit's example from one real run, as a new user would make it, in
the test organization, then deletes everything the run created.

    ORCA_PROD_TEST_API_KEY=... python scripts/example.py <slug>

It copies the published kit with `orca kits copy <link> --yes`, asks the
kit's agent the question in its README's Use it line with `orca chat`, reads
the answer from the session's items and the run's cost from
`GET /api/usage?session=<id>`, then deletes the session and the copy. It
writes kits/<slug>/example.json and the README's Example section from that
record. Nothing in the answer is edited, whatever its length: the kit's page
shows its first lines with Read the full answer (orca-design kits-teams
D5.2, amended 2026-10-14). The wallet is read before and after.

Set ORCA_CLI to the orca binary to use (default: orca on PATH), and
ORCA_EXAMPLE_RAW to a file outside the repo to keep the run's raw items and usage.
"""

import datetime
import json
import os
import pathlib
import re
import sys
import tempfile
import time
import urllib.error

import kitlib
from live import Run

USE_IT = re.compile(r'^orca chat (\S+) "([^"\n]+)"$', re.MULTILINE)


def question_of(folder):
    """(agent, question) from the README's Use it line."""
    match = USE_IT.search((folder / "README.md").read_text())
    if not match:
        sys.exit(f"kits/{folder.name}/README.md has no `orca chat <agent> \"...\"` line in Use it")
    return match.group(1), match.group(2)


def answer_of(items):
    """The last assistant message's text, exactly as the agent wrote it."""
    for item in items:  # newest first
        if item.get("type") == "message" and item.get("role") == "assistant":
            parts = [part.get("text", "") for part in item.get("content") or [] if part.get("type") == "output_text"]
            if any(parts):
                return "".join(parts)
    return None


def cost_of(usage):
    """The session's charge across every meter (model calls, web searches, machine time)."""
    return int(usage.get("cost_micro_usd") or 0)


def wallet(run, when):
    body = run.api("GET", "/api/billing/wallet")
    print(f"wallet {when}: {body.get('balance_micro_usd')} micro-USD", flush=True)


def main(argv):
    names = [a for a in argv if not a.startswith("--")]
    if len(names) != 1:
        sys.exit(__doc__)
    folder = kitlib.KITS / names[0]
    public_id = kitlib.published(folder).get("public_id") or sys.exit(f"kits/{folder.name} is not published yet")
    key = os.environ.get("ORCA_PROD_TEST_API_KEY") or sys.exit("set ORCA_PROD_TEST_API_KEY")
    link = f"https://app.orcapods.ai/kits/{public_id}"
    agent_name, question = question_of(folder)
    model = (kitlib.python_bodies(folder).get("agent") or {}).get("model")

    with tempfile.TemporaryDirectory(prefix="orca-example-") as tmp:
        run = Run(key, pathlib.Path(tmp))
        wallet(run, "before")
        before = {s["id"] for s in run.api("GET", "/v1/agents/sessions?limit=100")["data"]}
        started = int(time.time()) - 60
        copied = run.orca("--json", "kits", "copy", link, "--yes", show=False)
        created = json.loads(copied.stdout).get("created", []) if copied.returncode == 0 else []
        record = None
        try:
            agent = next((c for c in created if c["kind"] == "agent" and c["name"] == agent_name), None)
            if not agent:
                sys.exit(f"the copy made no agent named {agent_name}")
            chat = run.orca("chat", agent["name"], question)
            if chat.returncode:
                sys.exit("the chat failed; nothing is recorded")
            sessions = [s for s in run.api("GET", "/v1/agents/sessions?limit=100")["data"] if s["id"] not in before]
            if len(sessions) != 1:
                sys.exit(f"expected one new session, found {len(sessions)}")
            session = sessions[0]["id"]
            items = run.api("GET", f"/v1/agents/sessions/{session}/items?limit=100&order=desc")["data"]
            raw = os.environ.get("ORCA_EXAMPLE_RAW")
            if raw:  # what the run returned, kept outside the repo in case recording fails
                pathlib.Path(raw).write_text(json.dumps({"session": session, "items": items}, indent=2))
            answer = answer_of(items)
            if not answer:
                sys.exit(f"session {session} has no answer from the agent")
            # Charges land as the run's rows are written; wait for them.
            cost = 0
            for _ in range(12):
                usage = run.api("GET", f"/api/usage?session={session}&start={started}&end={int(time.time()) + 60}")
                cost = cost_of(usage)
                if raw:
                    pathlib.Path(raw).write_text(json.dumps({"session": session, "items": items, "usage": usage}, indent=2))
                if cost > 0:
                    break
                time.sleep(5)
            if cost <= 0:
                print(json.dumps(usage, indent=2), file=sys.stderr)
                sys.exit(f"session {session} shows no cost yet; nothing is recorded")
            record = {
                "question": question,
                "answer": answer,
                "cost_micro_usd": cost,
                "model": model,
                "session": session,
                "asked_on": datetime.date.today().isoformat(),
            }
        finally:
            for session in run.api("GET", "/v1/agents/sessions?limit=100")["data"]:
                if session["id"] not in before:
                    run.api("DELETE", f"/v1/agents/sessions/{session['id']}")
                    print(f"deleted session {session['id']}")
            paths = {"agent": "/v1/agents/", "skill": "/v1/skills/", "template": "/v1/agents/environments/templates/"}
            for item in reversed(created):
                try:
                    run.api("DELETE", paths[item["kind"]] + item["id"])
                    print(f"deleted {item['kind']} {item['id']}")
                except urllib.error.HTTPError as error:
                    print(f"LEFT BEHIND: {item['kind']} {item['id']}: HTTP {error.code}", file=sys.stderr)
            wallet(run, "after")

    (folder / "example.json").write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n")
    readme = folder / "README.md"
    readme.write_text(kitlib.with_example(readme.read_text(), record))
    print(f"\nkits/{folder.name}: example recorded from session {record['session']}, cost {kitlib.money(record['cost_micro_usd'])}")


if __name__ == "__main__":
    main(sys.argv[1:])
