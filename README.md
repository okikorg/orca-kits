# Orca kits

Ready-made agents for [Orca](https://orcapods.ai), with their code. Each folder under [`kits/`](kits/) is one kit: an agent (and, where it needs them, skills and a template) that you copy into your organization with one link, and the programs that run it where your own code has to take part.

New to Orca? Start at [docs.orcapods.ai/start-here](https://docs.orcapods.ai/start-here), or have your coding agent set you up with [the prompt on that page](https://docs.orcapods.ai/start-here#have-your-coding-agent-do-it).

## The kits

| Kit | What it does | Code on your side |
| --- | --- | --- |
| [Scout](kits/scout/) | Researches a question on the web and answers with its sources | None |
| [Cram Coach](kits/cram-coach/) | Turns one textbook chapter (a text PDF) and an exam date into a cram plan, Anki flashcards, a practice test and cited answers | None; you attach the PDF with `orca chat --file` |

Each folder's README says what the kit does, what it uses, and how to add and use it.

## Add a kit

Copy it into your organization with its link:

```bash
orca kits copy https://app.orcapods.ai/kits/kit-tdCEUXGA3NbuIWJJ6 --yes   # Scout
```

Or open the link and choose **Copy**. A copy becomes ordinary agents, skills and templates in your organization, with no tie back to the kit. See [kits](https://docs.orcapods.ai/kits).

Or create the same agent from code: every kit defines its agent in `agent.py` and `agent.ts` as the `agents.create` call of the `openai` package, and running either file creates it in your organization.

```bash
python -m pip install -r requirements.txt          # openai==3.13.0
ORCA_API_KEY=... python kits/scout/agent.py

npm install                                        # openai@7.15.0
ORCA_API_KEY=... node --experimental-strip-types kits/scout/agent.ts
```

## What a kit folder holds

| File | What it is |
| --- | --- |
| `kit.json` | The kit's name, description and author |
| `README.md` | This folder's page, and the README on the kit's page (below) |
| `agent.py`, `agent.ts` | The agent, as an `agents.create` call; the two must send the same body |
| `template.py`, `template.ts` | An environment template, where the kit has skills |
| `skills/<name>/SKILL.md` | A skill, with any files it refers to |
| `run.py`, `run.ts` | Only where your code takes part: function tools, git, or files from your machine |
| `example.json` | Optional: one real run of the kit's Use it question, written by `scripts/example.py` (below) |
| `published.json` | The kit's ids in the Orca kits organization, written by `scripts/publish.py` |

### The README

A kit's README is both its folder's page here and the README published with the kit, so its links are absolute and it holds these sections, in this order, and nothing else:

1. `# <name>`, the kit's name as in `kit.json`.
2. One short paragraph on what the agent does and how it answers.
3. `## Example`, only when the kit has an `example.json`: that file as `scripts/example.py` writes it (below).
4. `## What it uses`: the model, what else it calls, whether it needs a sandbox, and a link to [pricing](https://orcapods.ai/pricing), never an amount.
5. `## Add it`: `orca kits copy <the kit's link> --yes`, then "Or click **Copy** on [the kit's page](<the kit's link>).", and a line on credentials if it needs any.
6. `## Use it`: the one example command.

At most 1,500 bytes without the Example section, and `kit.json`'s description is one sentence of at most 140 characters. `scripts/check.py` enforces all of this. The kit's page shows a GitHub icon linking to the kit's folder here; `scripts/publish.py` sets that link on every publish, so the README carries no line about where it was published from.

### The example

An example is optional (since 2026-10-15) and the kit's page no longer shows one. Scout keeps its run because Orca's landing page shows it. When a kit has one, it is never written by hand. `scripts/example.py` records it from one live run in the test organization (copy the published kit, ask the question, read the answer and the run's cost, delete the session and the copy), into `example.json` and the README's Example section:

```bash
ORCA_PROD_TEST_API_KEY=... python scripts/example.py scout
```

`scripts/check.py` fails if the two differ, so an answer or a cost edited by hand never reaches the README. Record it again when the answer goes stale.

## Checks

Every pull request runs:

```bash
npm ci && npx tsc --noEmit                        # TypeScript against the pinned openai
python -m pip install -r requirements.txt
python scripts/check.py                           # the kit contract, Python and TypeScript bodies equal, the words
python scripts/test_check.py                      # the check fails on each shape the server refuses
python scripts/check_docs_code.py ../orca-docs    # the docs pages' agent code equals their kits'
```

## Publishing

Kits are published from the Orca kits organization on production by the **publish** workflow, which a maintainer starts with the kit's folder name and approves. Each kit is run live before a release with `scripts/live.py`.

## The 1.x kits

The Orca 1.x kits (seo-helper, seo-ledger, marketing-helper, outreach-helper, engineering-helper) are at the tag [`1.x-final`](https://github.com/okikorg/orca-kits/tree/1.x-final). They ran on pods, schedules and connected apps, which Orca 2.0 does not have.

## License

[MIT](LICENSE).
