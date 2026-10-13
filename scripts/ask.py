"""Tries a kit's agent from its folder, before it is published: creates the
agent in the test organization, asks each of the kit's questions in live.py in
its own session, prints the searches and the answer, and deletes everything.

    ORCA_PROD_TEST_API_KEY=... python scripts/ask.py <slug> [<question>...]

Use it while changing a kit's instructions, and check every answer against
the docs.
"""

import os
import sys

import kitlib
import live


def main(argv):
    from openai import OpenAI

    if not argv:
        sys.exit(__doc__)
    folder = kitlib.KITS / argv[0]
    questions = argv[1:] or live.QUESTIONS.get(folder.name) or sys.exit(f"no questions for kits/{folder.name}")
    key = os.environ.get("ORCA_PROD_TEST_API_KEY") or sys.exit("set ORCA_PROD_TEST_API_KEY")
    client = OpenAI(api_key=key, base_url=f"{live.ORIGIN}/v1")
    agents = client.beta.agents
    agent = kitlib._load(folder / "agent.py").define(agents)
    try:
        for question in questions:
            session = agents.sessions.create(agent_id=agent.id, environment={"type": "none"})
            try:
                with agents.sessions.stream(session.id, input=question) as stream:
                    for _ in stream:
                        pass
                items = list(reversed(agents.sessions.items.list(session.id, limit=50).data))
                searches = [getattr(getattr(i, "action", None), "query", None) for i in items if i.type == "web_search_call"]
                answer = "\n".join(
                    part.text
                    for i in items
                    if i.type == "message" and i.role == "assistant"
                    for part in (i.content or [])
                    if getattr(part, "text", None)
                )
                print(f"\n### {question}\nsearches: {searches}\n{answer}", flush=True)
            finally:
                agents.sessions.delete(session.id)
    finally:
        agents.delete(agent.id)


if __name__ == "__main__":
    main(sys.argv[1:])
