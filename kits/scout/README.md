# Scout

Scout answers a question in a few short paragraphs. When the answer depends on facts that change, such as releases, prices or news, it searches the web first and cites each source with its link; if it finds nothing reliable, it says so. It is the sample agent of Orca's [start page](https://docs.orcapods.ai/start-here).

## Example

> What's new in the latest Python release? Cite your sources.

The latest **feature release is Python 3.14**, released on **October 7, 2025**. Its biggest changes include:

- **Deferred evaluation of annotations**, plus the new `annotationlib` module.
- **Template string literals** (`t"..."`), enabling libraries to safely process interpolated strings.
- **Multiple interpreters** in the standard library via `concurrent.interpreters`.
- Official support for **free-threaded (“no-GIL”) builds**, alongside improvements to parallel execution.
- New **Zstandard compression** support through `compression.zstd`.
- **External debugging** of running Python processes with `sys.remote_exec()`.
- Better error messages, syntax highlighting in the REPL, new UUID versions, and improved asyncio process inspection.

For upgrade planning, check compatibility with code that reads `__annotations__` directly, multiprocessing defaults, and third-party C extensions—especially when using free-threaded Python.

Sources: [Python 3.14 release page](https://www.python.org/downloads/release/python-3140/) · [What’s New in Python 3.14](https://docs.python.org/3.14/whatsnew/3.14.html)

A real run on 2026-10-14. It cost $0.09 of Orca credit.

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
