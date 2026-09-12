# Task method: the dispatcher's map

The backlog is the system of record for work. Every deliverable in the plan becomes one or more tasks small enough to finish in one sitting, each with a done line the dispatcher can check, and today's list is chosen from it every morning within the founder's minute budget. The dispatcher never invents work that is not in the plan; when the plan changes, the backlog changes through `reseed`.

## The backlog file

`tasks/<product>/backlog.md`. A header line, then one table with these columns, in this order:

| Column | Rule |
|---|---|
| `id` | `T-001` upward, assigned once, never reused or renumbered. Stable ids are what let a person say "done T-014" from their phone. |
| `week` | `W0` to `Wn` from the plan. A task moves weeks; its id does not change. |
| `engine` | The plan's source or section it serves: `front door`, `launch 1`, `kits loop`, `founder x`, `outreach`, `paid`, `measurement`, `decision`. |
| `title` | Imperative, one line, specific enough to start without reading anything else: "Write the /pricing page copy: four columns, fee stated, free credit $20". |
| `owner` | `founder` (needs the person's hands, account or money), `pod` (an agent can produce it as a draft in the pool), `eng` (a code change the founder or an engineer ships). The pod never marks an `owner: founder` task done on its own. |
| `minutes` | The honest estimate. Founder tasks add up against the daily budget. |
| `depends on` | Task ids that must be done first, or blank. |
| `status` | `open`, `today`, `done`, `skipped`, `blocked`. |
| `done means` | The evidence: a URL live, a file in the pool, a number in the metrics table, a decision line in `decisions.md`, an email sent. A task without a checkable done line is not seeded; write the evidence or split the task. |
| `notes` | Dates and one-liners: `done 2026-09-16 (URL)`, `blocked 2026-09-15 on D-03`, `follow-up: F-012`. |

Below the table: a **Decisions** list mirrored from `decisions.md` with ids `D-01` upward, each with the tasks blocked on it, so the founder sees the cost of not deciding.

## Seed: from plan to backlog

1. Read `plan.md` whole. Walk the weeks in order; for every bullet, write the tasks that finish it. Split anything over 60 founder minutes. A launch day becomes six to ten tasks (the post, the comment plan, the same-day posts elsewhere, the video, the reply slots, the welcome email template).
2. Walk **The front door**: every ranked change is a task, `owner: eng` or `founder`, week W0.
3. Walk **Decisions waiting on the founder**: each becomes a `D-` line and a `T-` task of type `decision`, 10 minutes, `done means: a decided line in decisions.md`.
4. Walk **The daily ritual**: the four slots become one recurring task each, id fixed (`T-R1` to `T-R4`), which `today` always includes and never marks done for more than that day.
5. Walk **Kill and scale rules**: each read date becomes a task on that date for `marketing-metrics` and the founder.
6. Fill `depends on` from the obvious order (a post depends on its draft; a paid flight depends on its destination page; a launch depends on the front door tasks).
7. Verify: every week has tasks; every task has a done line; founder minutes per week are under five times the daily budget, and if not, say so in the seed log line and flag the overflow in `today.md` rather than silently hiding tasks.

## Today: choosing the list

1. Apply inbox first. Any new note with `done`, `skip`, `block` and ids: apply, record the date in `notes`, and if the note mentions a follow-up ("they asked", "wants to see", "check back"), post it to the board addressed to `marketing-followups`.
2. The recurring four slots always appear, with their minutes.
3. Then, in this order until the founder's minute budget is spent: `blocked` tasks that became unblocked; overdue tasks from earlier weeks; the current week's tasks in `depends on` order, `owner: founder` first (the pod's own tasks do not use the founder's minutes); decisions waiting more than three weekdays, always, regardless of budget.
4. Due and overdue follow-ups from the `marketing-followups` board post are listed under their own heading with their `F-` ids; they do not count against the task budget but they are printed.
5. `owner: pod` tasks for today are listed under **The pod does** so the founder knows what to expect in the pool by evening.
6. Write `tasks/<product>/today.md`: date, minute total vs budget, the list with ids, minutes and done lines, the follow-ups, the pod's list, and one line of what is blocked and on whom.

Mark chosen tasks `today`; at the next `today` run, anything still `today` and not `done` goes back to `open` with a note `carried <date>`. Three carries in a row is reported as a finding in the list, not hidden.

## Marking done

- `done` requires the evidence in the done line, or the person's word. When the word is given without the evidence, mark done and put `evidence not seen` in notes; the progress agent counts these separately.
- `skipped` requires a why; the reviewer reads skips as signal.
- `blocked` requires an id (`D-03`) or a name.
- Never mark an `owner: founder` task done from inference.

## Reseed: after a plan change

Read the review's applied delta lines or the replan's changes. For each: add tasks (next ids), retire tasks (`skipped` with `notes: retired by review <week>`), move weeks, change minutes. Never renumber. Then run `today`.

## Attended voice

Short. Answer with the list, ids first. When asked "what's next" give at most the day's remaining minutes' worth. When a person reports done, thank them in four words and show what that unblocked. No em dashes.
