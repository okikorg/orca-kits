# Pool layout: where everything lives and who writes it

The pod shares one filesystem at `/pools/marketing-pod/`. Each agent owns one area and the product slug is a folder inside it, so one pod can carry several products without their files touching. `<product>` below is the slug from the attached product prompt, lowercase, no spaces (`acme`, `side-project`).

| Path | Written by | What it is |
|---|---|---|
| `inbox/<product>/notes/*.md` | the operator | Anything the founder drops for the pod: meeting notes, things people asked for, links, "done T-012" lines, decisions taken. Read by every agent; written by none. |
| `inbox/<product>/metrics/*.md` or `*.csv` | the operator | Numbers only the operator can see: signups from the auth provider, site analytics, X analytics, ad spend. One file per drop, dated in the filename. |
| `inbox/<product>/docs/**` | the operator | Optional. The product's existing marketing docs, trackers and past posts when they are not reachable through a repo. |
| `strategy/<product>/product.md` | marketing-lead | The product facts distilled from the prompt and what the analysis found: what it is, who it is for, price, accounts, links. Rewritten on every `analyse`. |
| `strategy/<product>/analysis.md` | marketing-lead | The analysis in the shape `analysis-method.md` defines. |
| `strategy/<product>/plan.md` | marketing-lead | The plan in the shape `planning-method.md` defines. Edited by `replan` and by the weekly job's applied delta, never rewritten from scratch after the first `plan`. |
| `strategy/<product>/decisions.md` | marketing-lead | Every decision that only the founder can take: asked on which date, decided on which date, what was decided. The pod reads it before assuming anything. |
| `tasks/<product>/backlog.md` | marketing-dispatcher | Every task in the plan, one row each, in the anatomy from `task-method.md`. The system of record for work. |
| `tasks/<product>/today.md` | marketing-dispatcher | Today's list, rewritten each morning and on every `next`. |
| `progress/<product>/progress.md` | marketing-progress | The burn-down per week, slippage, what is blocked on the founder, the forecast line. Rewritten each run. |
| `metrics/<product>/metrics.md` | marketing-metrics | The weekly table, one row per week, plus the per-post and per-kit tables. Rows are appended and corrected, never deleted. |
| `reviews/<product>/<yyyy>-w<ww>.md` | marketing-reviewer | One file per week: what shipped, what it produced, the verdict per engine, the proposed plan delta. |
| `followups/<product>/followups.md` | marketing-followups | Every follow-up, open or closed, with its source and due date. |
| `log/<product>.md` | every agent | One line per run: `<date> <time> | <agent> | <job> | DONE <summary>` or `SKIPPED (<reason>)`. The pod's journal; the first thing any agent reads to know what ran last. |
| `board/public/posts/` | every agent, via `pool_post` | Hand-offs between agents inside one run (the reviewer's delta for the lead, the follow-ups agent's due list for the dispatcher). Short, dated, addressed by agent name in the first line. |

Rules:

- Create a missing folder before writing into it. A run never fails because a folder did not exist.
- Files are rewritten whole except `metrics.md`, `followups.md`, `decisions.md` and the log, which are appended to and corrected in place.
- Every file starts with a one-line header naming the product, the agent and the date it was written, so a file read out of context still says whose it is.
- Nothing under `inbox/` is ever edited or deleted by an agent. When an inbox note has been processed (a done line applied, a metric row recorded, a follow-up captured), the agent records that in its own file and in the log, not by touching the note.
- A member never writes outside its area. If it needs the lead to change strategy, it writes a `pool_post` addressed to `marketing-lead` and says what and why.
