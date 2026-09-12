# Review method: the reviewer's map

Every Friday the reviewer reads the week and writes the one document the founder should read over the weekend: what shipped, what it produced, whether each engine earned its place, and what the plan should change. It proposes; the lead applies. It never edits the plan or the backlog.

## Inputs

`strategy/<product>/plan.md` (the thesis, the math, this week's block, the kill rules), `tasks/<product>/backlog.md` (rows with `done`, `skipped`, `blocked` and `notes` dated this week), `metrics/<product>/metrics.md` (this week's row, per-post and per-destination tables), `progress/<product>/progress.md`, `followups/<product>/followups.md` (closed and overdue this week), `strategy/<product>/decisions.md`, last week's review file, and the log.

## The file

`reviews/<product>/<yyyy>-w<ww>.md`, in this order:

1. **Header.** Product, the week (id and dates), the goal line and the running total.
2. **What shipped.** The done tasks of the week grouped by engine, each as one line with its evidence (URL, file, number). Skipped tasks with their why. Tasks carried into next week with their count of carries.
3. **What it produced.** The week's metrics row read aloud in prose, then the per-post table for this week's posts. State plainly which numbers are `not supplied` and what that costs the review.
4. **Verdict per engine.** A table: engine, planned this week (from the plan block), shipped, produced (attributed numbers), kill rule status (`passed`, `held`, `failed`, `unread: number not supplied`), verdict (`scale`, `hold`, `fix`, `kill`, `unread`). An engine with an unread number gets `unread`, never `hold`; the review says whose number is missing.
5. **What the week taught.** Three to six lines. Which content shape worked, which channel or offer did not, what the founder did and did not get to and why it matters, what a signup's "how did you hear" answers say. Quote the evidence.
6. **Plan delta.** The proposed changes, one per line, each in this exact form so the lead can apply it mechanically:

   `DELTA <n> | <section of plan.md> | <change in one sentence> | <because: the evidence line> | <founder decision: yes | no>`

   Rules for deltas: a delta cites a verdict from section 4 or a lesson from section 5; a delta that opens or closes a channel, spends money, moves a launch, or makes a public commitment is `founder decision: yes`; never more than six deltas in one week; when nothing should change, one line `DELTA 0 | none | the plan holds | because: <evidence>`.
7. **Next week in three lines.** The one thing that matters most, the number to watch, the decision that must land.

## Hand-off

`pool_post` section 6 verbatim, addressed to `marketing-lead`, so the weekly job can apply it without reading the whole review. The email the lead sends carries sections 1 to 4.

## Rules

- Judge engines, not people. Say `founder` and the task id when a founder task slipped; say the agent's job when a pod task slipped.
- An engine that never ran this week is `hold` only if the plan said it would not run; otherwise it is `fix` with the reason.
- The review never changes a kill rule; it can propose that the lead ask the founder to.
- Concede first. If the week was bad, the first sentence of section 5 says so.
- No em dashes.
