# seo-ledger

The bookkeeping agent for an SEO draft workflow. It runs beside the seo-helper
writer, which opens two pull requests per post: a pick PR holding one pick
record (why this keyword), and a draft PR holding the post. You review the
draft, merge or close it, fill the record's `review` block, and merge the pick
PR whatever happened to the draft. So every pick ever made lands as one JSON
file in one folder on your default branch.

This agent keeps that folder current. Each run it scans every record and fills
in the record's `ledger` block: whether the draft is still open, published or
rejected, the published URL, and the search position over time. Once enough
records exist it reads them and writes a review: which kinds of picks
published and ranked, which got rejected, and the exact rule changes the
evidence supports. You apply the review to the writer's skill, or, if you keep
the writer's rules as a file in a repo you name in the prompt, the agent opens
a draft pull request there as well.

## The record

One file per pick, three blocks, one owner each:

- `pick`: the writer's, written at pick time and never edited.
- `review`: yours, filled on the pick PR before you merge it.
- `ledger`: this agent's, rewritten as the draft's state and its ranks change,
  with `updatedAt` and `rankedAt` dates.

The agent replaces its own block and nothing else. There is no index file:
each record carries the dates that decide what is due for it next.

## What is in here

- `agents/seo-ledger.yaml`: the agent. No site facts.
- `skills/seo-ledger/SKILL.md`: the run protocol, record schema, ranking,
  review and email. Complete in its body; marlin loads no references.
- `prompts/ledger-prompt.template.md`: what only the ledger needs (search
  settings, cadences, an optional rules repo). The repo, record folder and
  pull request names come from the seo-helper kit's repo prompt, attached to
  both schedules.

## Install

From a machine with the `orca` CLI signed in to your workspace:

```
orca skills import kits/seo-ledger/skills/seo-ledger
orca agents create -f kits/seo-ledger/agents/seo-ledger.yaml
orca pools members add <your-pool> seo-ledger
```

Then save the filled ledger prompt as an Orca Prompt and create a daily
schedule targeting the `seo-ledger` agent with both it and the repo prompt
attached. Rank and review cadences are set in the prompt, not in the schedule.

## What it writes

- The `ledger` block of `<record folder>/<slug>.json`, for records whose
  draft changed state or whose ranking pass came due.
- `<record folder>/reviews/<date>.md`, at most once per review cadence.
- `/agents/seo-ledger/status.md` in the pool area, one line per run.
- A draft pull request against the rules repo, only when the prompt names one
  and a review proposes a change.

It never commits to the default branch. Each run's writes go to a branch of
its own, one file per commit, each read back, then land through one pull
request the agent opens and merges itself once every file is verified. That
is the only pull request it merges. If a write or the merge fails, the pull
request stays open for a human and the run reports STOPPED.

## What it emails

One email per run, only when something happened: records changed, a review
was written, something needs you, or the run stopped. It lists the merged
ledger PR, one line per changed record (`drafting to published`, `ranked 14
(was 22)`), a Needs you list (a pick PR waiting on review, a pick merged
without its review, a review that disagrees with what GitHub shows), when the
next ranking pass and review are due, and the review itself when one ran.
