# Orca kits

Ready-made agents for [Orca](https://orcapods.ai), with their code. Each folder under [`kits/`](kits/) is one kit: an agent (and, where it needs them, skills and a template) that you copy into your organization with one link, and the programs that run it where your own code has to take part.

New to Orca? Start at [docs.orcapods.ai/start-here](https://docs.orcapods.ai/start-here), or have your coding agent set you up with [the prompt on that page](https://docs.orcapods.ai/start-here#have-your-coding-agent-do-it).

## The kits

| Kit | What it does | Code on your side |
| --- | --- | --- |
| [Scout](kits/scout/) | Researches a question on the web and answers with its sources | None |
| [Cram Coach](kits/cram-coach/) | Turns one textbook chapter (a text PDF) and an exam date into a cram plan, Anki flashcards, a practice test and cited answers | None; you attach the PDF with `orca chat --file` |
| [Margin Check](kits/margin-check/) | Answers what a deal does to gross margin and who has to approve it, from a sample company's price list, discount policy and contracts, held in its instructions | None |
| [SEO helper](kits/seo-helper/) | Finds blog topics with DataForSEO's numbers and briefs the post | Your coding agent sends your post list and writes the post; a DataForSEO account |

Each folder's README says what the kit does, what it uses, and how to add and use it.

## Add a kit

Copy it into your organization with its link. The CLI prints what the kit holds, then asks y/N:

```bash
orca kits copy https://app.orcapods.ai/kits/kit-tdCEUXGA3NbuIWJJ6   # Scout
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
| `kit.json` | The kit's name and description |
| `README.md` | This folder's page, and the README on the kit's page (below) |
| `agent.py`, `agent.ts` | The agent, as an `agents.create` call; the two must send the same body |
| `template.py`, `template.ts` | An environment template, where the kit has skills |
| `skills/<name>/SKILL.md` | A skill, with any files it refers to |
| `run.py`, `run.ts` | Only where your code takes part: function tools, git, or files from your machine |
| `example.json` | Optional: one real run of the kit's Use it question, written by `scripts/example.py` (below) |
| `published.json` | The kit's ids in the Orca kits organization, written by `scripts/publish.py`, and its public id once Orca first publishes it |

### The README

A kit's README is both its folder's page here and the README published with the kit, so its links are absolute and it holds these sections, in this order, and nothing else:

1. `# <name>`, the kit's name as in `kit.json`.
2. One short paragraph on what the agent does and how it answers.
3. `## Example`, only when the kit has an `example.json`: that file as `scripts/example.py` writes it (below).
4. `## What it uses`: the model, what else it calls, whether it needs a sandbox, and a link to [pricing](https://orcapods.ai/pricing), never an amount.
5. `## Add it`: `orca kits copy <the kit's link>` on its own line, never with `--yes`, so a person reads the review and answers y/N; then "Or click **Copy** on [the kit's page](<the kit's link>).", and a line on credentials if it needs any.
6. `## Use it`: the one example command.

At most 1,500 bytes without the Example section, and `kit.json`'s description is one sentence of at most 140 characters. `scripts/check.py` enforces all of this. The kit's page shows a GitHub icon linking to the kit's folder here; `scripts/publish.py` sets that link on every draft, so the README carries no line about where it was published from.

### The example

An example is optional (since 2026-10-15) and the kit's page no longer shows one. Scout keeps its run because Orca's landing page shows it. When a kit has one, it is never written by hand. `scripts/example.py` records it from one live run in the test organization (copy the published kit, ask the question, read the answer and the run's cost, delete the session and the copy), into `example.json` and the README's Example section:

```bash
ORCA_PROD_TEST_API_KEY=... python scripts/example.py scout
```

`scripts/check.py` fails if the two differ, so an answer or a cost edited by hand never reaches the README. Record it again when the answer goes stale.

## Connect an MCP server that uses OAuth

`orca vaults credentials add` takes a token or a login and password. For a remote MCP server that signs you in with OAuth instead, such as [Composio Connect](https://docs.orcapods.ai/guides/connect-apps-composio), use `scripts/connect_mcp_oauth.py`. It works with any MCP server that does OAuth with dynamic client registration and PKCE:

```bash
python3 scripts/connect_mcp_oauth.py --server https://connect.composio.dev/mcp --vault composio
```

It registers a client with the server, opens your browser to sign in, takes the reply once on `127.0.0.1`, and creates an `mcp_oauth` credential in the vault, bound to that exact URL, with what Orca needs to refresh the token itself. Run it again to sign in again: the new credential replaces the one for the same URL in that vault. The Orca key comes from `ORCA_API_KEY`, else your `orca auth login`, else a hidden prompt, and must be an admin's. It prints only ids, never a token or a key, and writes nothing to disk.

## Checks

Every pull request runs:

```bash
npm ci && npx tsc --noEmit                        # TypeScript against the pinned openai
python -m pip install -r requirements.txt
python scripts/check.py                           # the kit contract, Python and TypeScript bodies equal, the words
python scripts/test_check.py                      # the check fails on each shape the server refuses
python scripts/test_publish.py                    # publish.py updates drafts only, and prints the operator line
python scripts/test_connect_mcp_oauth.py          # the connect script signs in safely and stores the right credential
python scripts/check_docs_code.py ../orca-docs    # the docs pages' agent code equals their kits'
```

## Publishing

Only Orca publishes kits, from the Orca kits organization, and only the server's operator command publishes. Every step, the publish key and the constraints on each are in orca-agent-server's [Publishing a kit](https://github.com/okikorg/orca-agent-server/blob/main/docs/kits-publishing.md). Each kit is run live before a release with `scripts/live.py`.

1. **Update the draft.** From a clean checkout of `main`, run `python scripts/publish.py <slug>` with the publish key in `ORCA_KITS_API_KEY`: a Member key of the Orca kits organization whose id is in the server's `ORCA_KIT_PUBLISHER_KEYS`, kept in the publisher's own environment and never on GitHub. It updates the kit's agent, skills, template and draft by the ids in `published.json`, publishes nothing, and prints the operator line: `orca-agent-server kits publish --kit <kit_...> --public-id <kit-...>`, with no `--public-id` for a kit's first publish.
2. **Review the diff.** Run that line at the server container's shell. It prints the version's review and a diff against the live version.
3. **Type yes** to publish it. Anything else publishes nothing.

## The 1.x kits

The Orca 1.x kits (seo-helper, seo-ledger, marketing-helper, outreach-helper, engineering-helper) are at the tag [`1.x-final`](https://github.com/okikorg/orca-kits/tree/1.x-final). They ran on pods, schedules and connected apps, which Orca 2.0 does not have.

## License

[MIT](LICENSE).
