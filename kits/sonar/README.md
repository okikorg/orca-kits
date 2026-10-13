# Sonar

Sonar answers questions about Orca from its documentation. It searches and reads docs.orcapods.ai through the docs' own MCP server, answers only from what the docs return, and cites the page each part of the answer comes from. When the docs do not cover a question, it says so plainly instead of guessing. It never quotes prices or amounts; for anything about cost it links the [pricing page](https://orcapods.ai/pricing).

This is Sonar for Orca 2.0. The Orca 1.x Sonar was built into the old platform; this one is an ordinary agent you copy into your organization and change as you like.

## When to use it

- You have a question about Orca and want the answer with the page it comes from.
- You want a small, working example of an agent that answers from one docs site, to point at your own.

## What it uses

Model calls on `orca/openrouter/openai/gpt-5.6-luna`, paid from your Orca credit, and the docs' MCP server at `https://docs.orcapods.ai/mcp`, which needs no key. Its two tools are `search_orca`, which searches the live docs, and `query_docs_filesystem_orca`, which reads a page in full. It needs no sandbox, so it uses no machine time. See [pricing](https://orcapods.ai/pricing) for what model calls cost.

## Add it

Copy the kit into your organization from the terminal:

```bash
orca kits copy https://app.orcapods.ai/kits/kit-0AOaC9ybJiz0Fmx5Q --yes
```

Or open [the kit's page](https://app.orcapods.ai/kits/kit-0AOaC9ybJiz0Fmx5Q) and choose **Get started**.

Or create the same agent from code with [agent.py](https://github.com/okikorg/orca-kits/blob/main/kits/sonar/agent.py) or [agent.ts](https://github.com/okikorg/orca-kits/blob/main/kits/sonar/agent.ts), which hold Sonar's whole definition.

No credentials to add. The kit's page lists the docs server as a credential, because Orca lists every MCP server a kit uses; it needs none, so skip it.

## Use it

```bash
orca chat sonar "How do I connect Orca's MCP server to Claude Code?"
```

Run `orca chat sonar` with no question for a back-and-forth conversation.

## Make it yours

- **Point it at your own docs.** Hosted Orca reaches only the MCP servers it enables, so for your own docs site swap the MCP tool for `{"type": "web_search", "allowed_domains": ["docs.example.com"]}` and name your product in the instructions. Search then reaches only the pages its provider has indexed.
- **Change how it answers.** Its instructions set the length, the citations and what it never says; rewrite them with `orca agents update`.
