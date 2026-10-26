# Apollo GTM Agent

Give it your company's website and it finds your competitors, defines outbound campaigns, finds potential customers and their decision makers in Apollo, and drafts a personalised email to each, with the sources behind every claim. It asks before it spends any Apollo credits, and it sends nothing: the emails are drafts for you to review.

## What it uses

Model calls on `orca/openrouter/openai/gpt-5.6-luna` and web search, paid from your Orca credit, and no sandbox. **Apollo, required:** its MCP server at `https://mcp.apollo.io/mcp` with your own Apollo account; enriching companies and revealing emails spend your Apollo credits. See [pricing](https://orcapods.ai/pricing).

## Add it

Click **Copy** on the kit's page. Or create the same agent from code with [agent.py](https://github.com/okikorg/orca-kits/blob/main/kits/apollo-gtm-agent/agent.py) or [agent.ts](https://github.com/okikorg/orca-kits/blob/main/kits/apollo-gtm-agent/agent.ts).

Then connect Apollo once: run [connect_apollo.py](https://github.com/okikorg/orca-kits/blob/main/kits/apollo-gtm-agent/connect_apollo.py) and approve access in your browser. It stores a read-only OAuth credential, which Orca refreshes, in a vault named `apollo`.

## Use it

```
orca chat apollo-gtm-agent --vault apollo "https://acme.com/"
```

When it asks to spend Apollo credits, answer in the same session: `orca chat apollo-gtm-agent --session <id> "yes"`.
