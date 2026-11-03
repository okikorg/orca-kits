# Demo Prep Agent

Give it your company's website and a cold lead, and it researches both with web search and Apollo: what you sell, and what the lead does, its size, funding, technologies, hiring and senior people. It maps where your products fit, with evidence and a confidence for each, and plans a demo set in the lead's own world: who to invite, a timed agenda, scenes with talk tracks, discovery questions, objections and a next step. Every claim cites its source.

## What it uses

Model calls on `orca/openrouter/openai/gpt-5.6-luna` and web search, paid from your Orca credit, and no sandbox. **Apollo, required:** its MCP server at `https://mcp.apollo.io/mcp` with your own Apollo account; enriching the lead and reading its job postings spend your Apollo credits, and it asks first. See [pricing](https://orcapods.ai/pricing).

## Add it

Click **Copy** on the kit's page. Or create the same agent from code with [agent.py](https://github.com/okikorg/orca-kits/blob/main/kits/demo-prep-agent/agent.py) or [agent.ts](https://github.com/okikorg/orca-kits/blob/main/kits/demo-prep-agent/agent.ts).

Then connect Apollo once with [connect_apollo.py](https://github.com/okikorg/orca-kits/blob/main/kits/apollo-gtm-agent/connect_apollo.py), the same `apollo` vault the Apollo GTM Agent uses.

## Use it

```
orca chat demo-prep-agent --vault apollo "Seller: orcapods.ai. Lead: Acme Inc. (acme.com)"
```
