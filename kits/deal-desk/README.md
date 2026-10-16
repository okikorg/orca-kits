# Deal Desk

Ask Deal Desk about a deal, and it answers what the deal does to gross margin and who has to approve it: the verdict first, then a table of the figures with their working, the discount rules that decided it by number, and a counter-offer the rep or a sales manager could approve alone. It also answers questions about current contracts, such as which end soon. Limits: the price list, costs, discount policy and contracts are sample data for Larkspur Analytics, a made-up company, held in the agent's instructions; replace them with yours by editing the instructions. It needs no sandbox, but with `--sandbox` it computes every figure with Python.

## What it uses

Model calls on `orca/openrouter/openai/gpt-5.6-luna`, paid from your Orca credit. No tools and no sandbox, so no machine time unless you add `--sandbox`. See [pricing](https://orcapods.ai/pricing).

## Add it

Click **Copy** on the kit's page. Or create the same agent from code with [agent.py](https://github.com/okikorg/orca-kits/blob/main/kits/deal-desk/agent.py) or [agent.ts](https://github.com/okikorg/orca-kits/blob/main/kits/deal-desk/agent.ts).

## Use it

```bash
orca chat deal-desk "Brightline wants to renew at 100 Team seats for 24 months at 25 percent off. What does that do to margin, and who approves it?"
```

From a coding agent, ask it the same through Orca's MCP `chat` tool. For questions about dates, give today's date, such as "Which contracts end in the next 60 days? Today is 2026-10-16."
