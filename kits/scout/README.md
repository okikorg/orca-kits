# Scout

Scout answers a question in a few short paragraphs. When the answer depends on facts that change, such as releases, prices or news, it searches the web first and cites each source with its link; if it finds nothing reliable, it says so. It is the sample agent of Orca's [start page](https://docs.orcapods.ai/start-here).

## Example

> What's new in the latest Python release? Cite your sources.

The latest stable Python release is **Python 3.15.0**, released **October 9, 2026**. Its major additions include:

- **Explicit lazy imports** with `lazy import`, allowing imports to be deferred until needed.
- New built-in **`frozendict`** and **`sentinel`** types.
- **UTF-8 as the default encoding**.
- **Unpacking in comprehensions**, such as `[*items for items in lists]`.
- New profiling tools, including a `profiling` package and Tachyon statistical profiler.
- Improvements to the experimental **JIT compiler** and stable-ABI support for free-threaded builds.
- Better error-message suggestions and new `.start` package startup configuration files.

See the official [Python 3.15.0 release page](https://www.python.org/downloads/release/python-3150/) and the full [“What’s New in Python 3.15” documentation](https://docs.python.org/3.15/whatsnew/3.15.html).

A real run on 2026-10-14. It cost $0.11 of Orca credit.

## What it uses

Model calls on `orca/openrouter/openai/gpt-5.6-luna`, paid from your Orca credit, and a web search when it looks something up. It needs no sandbox, so it uses no machine time. See [pricing](https://orcapods.ai/pricing).

## Add it

```bash
orca kits copy https://app.orcapods.ai/kits/kit-tdCEUXGA3NbuIWJJ6
```

Or click **Copy** on [the kit's page](https://app.orcapods.ai/kits/kit-tdCEUXGA3NbuIWJJ6).

## Use it

```bash
orca chat scout "What's new in the latest Python release? Cite your sources."
```
