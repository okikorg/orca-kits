# Sonar

Sonar answers questions about Orca from its documentation. It searches docs.orcapods.ai, answers only from the pages it finds, and cites the page each part of the answer comes from. When the pages it can find do not cover a question, it says so plainly instead of guessing. It never quotes prices or amounts; for anything about cost it links the [pricing page](https://orcapods.ai/pricing).

This is Sonar for Orca 2.0. The Orca 1.x Sonar was built into the old platform; this one is an ordinary agent you copy into your organization and change as you like.

## When to use it

- You have a question about Orca and want the answer with the page it comes from.
- You want a small, working example of a search agent limited to one site, to point at your own docs.

## What it uses

Model calls on `orca/openrouter/openai/gpt-5.6-luna`, paid from your Orca credit, and a web search, limited to docs.orcapods.ai, for each question. It needs no sandbox, so it uses no machine time. See [pricing](https://orcapods.ai/pricing) for what each costs.

Its search reaches only the docs pages the search provider has indexed, so it sometimes finds no page for a question the docs do cover. It then says the docs it could reach do not cover it, and you can read [docs.orcapods.ai](https://docs.orcapods.ai) directly.

## Add it

Copy the kit into your organization from the terminal:

```bash
orca kits copy https://app.orcapods.ai/kits/kit-0AOaC9ybJiz0Fmx5Q --yes
```

Or open [the kit's page](https://app.orcapods.ai/kits/kit-0AOaC9ybJiz0Fmx5Q) and choose **Get started**.

Or create the same agent from code with [agent.py](https://github.com/okikorg/orca-kits/blob/main/kits/sonar/agent.py) or [agent.ts](https://github.com/okikorg/orca-kits/blob/main/kits/sonar/agent.ts), which hold Sonar's whole definition.

No credentials to add.

## Use it

```bash
orca chat sonar "How do I connect Orca's MCP server to Claude Code?"
```

Run `orca chat sonar` with no question for a back-and-forth conversation.

## Make it yours

- **Point it at your own docs.** Change `allowed_domains` in its `web_search` tool to your docs site, and the instructions to name your product.
- **Change how it answers.** Its instructions set the length, the citations and what it never says; rewrite them with `orca agents update`.
