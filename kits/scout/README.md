# Scout

Scout is a research assistant. Ask it a question and it answers in a few short paragraphs or a short list. When the answer depends on facts that change, such as releases, versions, prices or news, it searches the web first and cites each source with its link. If the sources disagree, or it finds nothing reliable, it says so instead of guessing.

It is the sample agent of Orca's [start page](https://docs.orcapods.ai/start-here).

## When to use it

- You want a quick, sourced answer to a question about something current.
- You want a small, working agent to copy and change into your own.

## What it uses

Model calls on `orca/openrouter/openai/gpt-5.6-luna`, paid from your Orca credit, and a web search whenever it decides to look something up. It needs no sandbox, so it uses no machine time. See [pricing](https://orcapods.ai/pricing) for what each costs.

## Add it

Choose **Get started** on the kit's page. Or create the same agent from code with [agent.py](https://github.com/okikorg/orca-kits/blob/main/kits/scout/agent.py) or [agent.ts](https://github.com/okikorg/orca-kits/blob/main/kits/scout/agent.ts), which hold Scout's whole definition.

No credentials to add.

## Use it

```bash
orca chat scout "What's new in the latest Python release? Cite your sources."
```

Run `orca chat scout` with no question for a back-and-forth conversation. From your own code, open a session of `scout` and stream the answer, as the [start page](https://docs.orcapods.ai/start-here) shows.

## Make it yours

- **Limit the sources.** Give `web_search` an `allowed_domains` list, for example your own docs site.
- **Change the job.** Copy it under another name and rewrite its instructions with `orca agents update`.
- **Quote pages exactly.** Orca does not fetch the pages behind the results; add a [function tool](https://docs.orcapods.ai/guides/function-tools) that does, if Scout must quote a page word for word.
