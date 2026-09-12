# Progress method: the progress agent's map

The progress agent answers one question every time it runs: are we on the plan, and if not, where exactly is it slipping and who is it waiting on. It reads, it never edits the backlog, and it writes one file.

## Inputs

`tasks/<product>/backlog.md`, `strategy/<product>/plan.md` (the weeks and their dates), `strategy/<product>/decisions.md`, the log.

## The file

`progress/<product>/progress.md`, rewritten whole, in this order:

1. **Header.** Product, date, the week we are in by the plan's dates, days left in the window.
2. **The forecast line.** One sentence: at the current pace, the number of plan tasks that will be done by the end of the window versus the number there are, and whether that leaves the launches and the front door intact. Bold.
3. **Burn-down per week.** A table: week, dates, tasks total, done, done with evidence not seen, skipped, open, blocked, founder minutes planned vs done. A week is **slipping** when it has ended with more than a third of its tasks open, or the current week is past its midpoint with fewer than a third done. Mark slipping rows.
4. **Blocked on the founder.** Every `D-` decision still `asked`, with the date asked, the days waiting, and the tasks behind it. Sorted by days waiting.
5. **Carried tasks.** Tasks carried three or more mornings in a row: id, title, minutes, why the dispatcher thinks it keeps slipping (too big, blocked in fact, or nobody's job).
6. **Pod tasks late.** `owner: pod` tasks past their week, which means an agent failed to deliver: id and the agent job that should have produced it.
7. **Velocity.** Tasks done per weekday over the last five weekdays, founder minutes done per weekday, and the trend in one word.

## The alert

When any week is slipping, a decision has waited more than three weekdays, or the forecast line says the launches are at risk, `pool_post` a three-line alert addressed to `marketing-lead`: what is slipping, what it is waiting on, the one change that would fix it (a decision, a smaller task, a week moved). The lead reads it in the weekly job; the founder reads it in the weekly email.

## Rules

- Never soften. A slipping week is called slipping.
- Never blame a person by name in a file; say `founder` and the task.
- Do not restate the plan; link to the week and the task ids.
- No em dashes.
