# Scout

Scout answers a question in a few short paragraphs. When the answer depends on facts that change, such as releases, prices or news, it searches the web first and cites each source with its link; if it finds nothing reliable, it says so. It is the sample agent of Orca's [start page](https://docs.orcapods.ai/start-here).

## What it uses

Model calls on `orca/openrouter/openai/gpt-5.6-luna`, paid from your Orca credit, and a web search when it looks something up. It needs no sandbox, so it uses no machine time. See [pricing](https://orcapods.ai/pricing).

## Add it

```bash
orca kits copy https://app.orcapods.ai/kits/kit-tdCEUXGA3NbuIWJJ6 --yes
```

Or click **Copy** on [the kit's page](https://app.orcapods.ai/kits/kit-tdCEUXGA3NbuIWJJ6).

## Use it

```bash
orca chat scout "What's new in the latest Python release? Cite your sources."
```
