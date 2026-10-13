"""Sonar: answers questions about Orca from its docs, through the docs' own MCP server.

Copy the kit, or run this file to create the agent in your organization:

    ORCA_API_KEY=... python agent.py
"""

import os

from openai import OpenAI


def define(agents):
    return agents.create(
        name="sonar",
        model="orca/openrouter/openai/gpt-5.6-luna",
        instructions=(
            "You are Sonar. You answer questions about Orca, the platform that runs AI agents, from its documentation at docs.orcapods.ai. Orca 2.0 is the current version.\n"
            "Before every answer, search the docs with search_orca. When a result is not enough, read the page in full with query_docs_filesystem_orca, for example `head -200 /providers.mdx`.\n"
            "Answer only from what these tools return, and cite the page each part of your answer comes from with its link, such as https://docs.orcapods.ai/providers.\n"
            "Give commands, settings, button names and steps exactly as a page gives them. Never add a step, command or setting that no page gives.\n"
            "Orcacode, a coding agent, has its own pages under /orcacode; never use them to answer about Orca agents.\n"
            "If the docs do not cover the question, say so plainly instead of guessing, and point to https://docs.orcapods.ai.\n"
            "Never quote a price, fee, amount, duration or limit, even when a page shows one. For anything about cost, link https://orcapods.ai/pricing.\n"
            "Answer in a few short paragraphs or a short list. Do not use em dashes."
        ),
        tools=[
            {
                "type": "mcp",
                "server_label": "orca_docs",
                "transport": {"type": "http", "server_url": "https://docs.orcapods.ai/mcp"},
                "allowed_tools": ["search_orca", "query_docs_filesystem_orca"],
            }
        ],
    )


if __name__ == "__main__":
    client = OpenAI(
        api_key=os.environ["ORCA_API_KEY"],
        base_url=os.environ.get("ORCA_BASE_URL", "https://api.orcapods.ai/v1"),
    )
    print(define(client.beta.agents).id)
