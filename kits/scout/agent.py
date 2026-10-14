"""Scout: a research assistant that searches the web and cites its sources.

Copy the kit, or run this file to create the agent in your organization:

    ORCA_API_KEY=... python agent.py
"""

import os

from openai import OpenAI


def define(agents):
    return agents.create(
        name="scout",
        model="orca/openrouter/openai/gpt-5.6-luna",
        instructions=(
            "You are Scout, a research assistant. Answer in a few short paragraphs or a short list.\n"
            "Search the web when the answer depends on facts that change, such as releases, versions, "
            "prices or news, and cite each source with its link.\n"
            "Newer releases may exist than you remember: for anything \"latest\", search without naming a version, "
            "and trust what you find over what you remember.\n"
            "If the sources disagree, or you cannot find an answer, say so instead of guessing."
        ),
        tools=[{"type": "web_search"}],
    )


if __name__ == "__main__":
    client = OpenAI(
        api_key=os.environ["ORCA_API_KEY"],
        base_url=os.environ.get("ORCA_BASE_URL", "https://api.orcapods.ai/v1"),
    )
    print(define(client.beta.agents).id)
