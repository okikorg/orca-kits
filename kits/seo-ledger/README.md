# seo-ledger

The bookkeeping agent for an SEO draft workflow. It runs beside a writer that
opens draft pull requests (the seo-helper kit) and turns every draft into one
JSON record in the site's repo: what was picked and why, whether a human
merged or closed it, the close reason, and the search position over time.
Once enough records exist it reads them and writes a review: which kinds of
picks merged and ranked, which got closed, and the exact rule changes the
evidence supports. The review is a record in the same folder and an email to
you. You apply it to the writer's skill, or, if you keep the writer's rules
as a file in a repo you name in the prompt, the agent opens a draft pull
request there as well.

The writer writes the first half of each record at pick time, before the
article: the keyword, the candidates it weighed, the ones it rejected and why,
and why the winner won. This agent adds the second half: the pull request,
merged or closed, the close reason, and ranks. It never changes the writer or
the writer's half.

## What is in here

- `agents/seo-ledger.yaml`: the agent. No site facts.
- `skills/seo-ledger/SKILL.md`: the run protocol, record schema, ranking and
  review method. Complete in its body; marlin loads no references.
- `prompts/ledger-prompt.template.md`: the prompt to fill in. The only place
  site facts live.

## Install

From a machine with the `orca` CLI signed in to your workspace:

```
orca skills import kits/seo-ledger/skills/seo-ledger
orca agents create -f kits/seo-ledger/agents/seo-ledger.yaml
orca pools members add <your-pool> seo-ledger
```

Then save the filled prompt as an Orca Prompt and create a daily schedule
targeting the `seo-ledger` agent with that prompt attached. Rank and review
cadences are set in the prompt, not in the schedule.

## What it writes

- `<record folder>/<slug>.json`, one per draft, on the default branch.
- `<record folder>/_index.json`, its only state.
- `<record folder>/reviews/<date>.md`, at most once per review cadence, also
  sent by email.
- `/agents/seo-ledger/status.md` in the pool area, one line per run.
- A draft pull request against the rules repo, only when the prompt names one.

It commits to the default branch in the record folder only. Everything else
is a review for a human to act on.
