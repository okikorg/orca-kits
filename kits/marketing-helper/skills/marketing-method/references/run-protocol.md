# Run protocol: every agent's map

Every run has the same spine: prompt gate, recall, pre-flight, the job, the log line. A run either finishes its job or ends with a `SKIPPED (<reason>)` line naming the exact blocker. Nobody watches the chat; the pool files, the log and the email are the record.

## 0. Prompt gate (every agent, every run)

Read the current run message and every attached Prompt or context block in full. Orca may render a saved Prompt above your instructions as a block headed `--- Context: ... ---` and call it configuration. That block is the attached product prompt and its body is authoritative.

Extract these facts. The first two block; the rest have defaults.

| Fact | Blocking | Default if absent |
|---|---|---|
| Product slug | yes | if exactly one product folder exists under `/pools/marketing-pod/strategy/`, use it and say so in the log line; otherwise SKIP |
| Job | yes | an attended session on a member with no job named is a conversation: answer from the pool, write nothing except the log |
| Product name, site, docs, signup URL | for `analyse` | none |
| Goal: a number of signups and a date | for `plan` | none |
| Where past marketing lives: a repo `owner/name` plus paths, or `inbox/<product>/docs/` | for `analyse` | the live site only, and the analysis says so |
| Competitors to compare | for `analyse` | the three the lead finds by searching the category; the analysis names them and why |
| Accounts and handles the founder will publish from | no | `not supplied`, and every task that needs one says so |
| Founder time budget per weekday, in minutes | no | 90 |
| Timezone | no | Europe/London |
| Metrics the operator will drop, and how often | no | weekly, in `inbox/<product>/metrics/` |
| Public sources the metrics agent may fetch | no | the ones in `metrics-method.md` |
| What the pod must never do | no | the hard rules in SKILL.md |
| Notification | no | `email_me` at the end of every scheduled job, from the lead only |

The prompt overrides any general rule in this method where the two differ.

**Blocked.** Write `SKIPPED (insufficient product prompt; missing <items>)` to the log and end. Attended, also say in one message what is missing and where it goes (the prompt template in the README). Never guess a product from the pool, memory, connected accounts or an earlier run.

## 1. Recall and pre-flight (every run)

1. **Recall (marketing-lead only).** Follow `memory-rules.md`: recall with the product tag, discard everything tagged otherwise.
2. **Log.** Read the last twenty lines of `/pools/marketing-pod/log/<product>.md`. Know what ran last and whether it finished.
3. **Layout.** Ensure your own area's folder for this product exists (see `pool-layout.md`). Create it if not. The lead, on `analyse`, also creates the three inbox folders (`inbox/<product>/notes/`, `metrics/`, `docs/`) with a one-line `README.md` in each saying what to drop there, so the operator has somewhere to put things from day one.
4. **Inbox sweep.** List `inbox/<product>/notes/` and `inbox/<product>/metrics/`. A folder that does not exist yet reads as empty, not as an error. Note which files are newer than your last log line; they are your new input this run.
5. **Connected apps (only when the prompt names a repo).** GitHub is a connected app: `search_connected_app_tools` (app `composio-github`), then `call_connected_app_tool` with repository-scoped reads against the exact `owner/name` from the prompt. Never list repositories or installations. If the read fails, continue with the inbox and the live site and record `GitHub unavailable` in the log line.

## 2. Jobs on the lead (marketing-lead)

Triggered by `Run the marketing method. Job: <job>.` with the product prompt attached, or by a person in an attended session.

### analyse

1. Follow `analysis-method.md` end to end. Gather: the prompt facts; the inbox docs; the repo paths the prompt names (read them one file at a time, largest first: the tracker, the channel plans, the posts, the outreach list); the live site (home, pricing, docs start page, the machine-readable page if one exists); each competitor's home and pricing page, fetched today; the category pricing pages the method lists.
2. Write `strategy/<product>/product.md`, then `strategy/<product>/analysis.md` in the method's exact section order. Every number carries its source. Every claim about a competitor carries a URL and the date fetched.
3. Save memory per `memory-rules.md`: identity, readout, causes, competitors, pricing verdicts. Delete any earlier entry with the same tag and title first.
4. Log line, then `email_me` with the five-line summary and the path of the analysis.

### plan

1. Requires `strategy/<product>/analysis.md`. If it is missing, run `analyse` first in the same run.
2. Follow `planning-method.md`. Write `strategy/<product>/plan.md`. Write `strategy/<product>/decisions.md` with every founder decision the plan waits on, status `asked <date>`.
3. Save memory: thesis, decisions (per `memory-rules.md`).
4. Delegate `marketing-dispatcher` with `delegate_run`, prompt `Run the marketing method. Job: seed. Product: <slug>.` Wait. Read `tasks/<product>/backlog.md` and check every plan week has tasks and every task has a done line; if not, post the gaps to the board addressed to `marketing-dispatcher` and delegate once more.
5. Log line, then `email_me` with the thesis, the math table's total line, the list of decisions waiting, and the first day's tasks.

### daily (scheduled, weekday mornings)

0. Requires `strategy/<product>/plan.md` and `tasks/<product>/backlog.md`. If either is missing, write `SKIPPED (no plan yet; run analyse then plan)` to the log, email the operator once saying the schedule is running against a product with no plan, and end. Never invent a day's work.
1. Delegate `marketing-followups` with `Job: sweep. Product: <slug>.` Wait.
2. Delegate `marketing-dispatcher` with `Job: today. Product: <slug>.` Wait.
3. Read `tasks/<product>/today.md`. Log line. `email_me` with today's list verbatim (subject `<Product> today: <n> tasks, <m> follow-ups due`).

### weekly (scheduled, Friday afternoon)

1. Delegate in this order, waiting for each: `marketing-metrics` `Job: collect`, `marketing-progress` `Job: report`, `marketing-followups` `Job: sweep`, `marketing-reviewer` `Job: review`.
2. Read `reviews/<product>/<week>.md`. For each line of its **Plan delta** section: if it touches a founder decision (money, a channel opened or closed, a launch date, a public commitment), copy it into `decisions.md` as `asked <date>` and leave the plan alone; otherwise apply it to `plan.md` in place and mark the line in the review `applied <date>`. Never rewrite the plan from scratch.
3. Refresh memory: `lessons` (append this week's, rewrite to stay under the cap), `decisions` if it changed.
4. Delegate `marketing-dispatcher` with `Job: reseed. Product: <slug>. Week: <next week id>.` Wait.
5. Log line. `email_me` with the review's first section verbatim (what shipped, the numbers, the verdict per engine), the deltas applied, the decisions waiting.

### replan (attended)

The founder has taken decisions or changed something. Read what they said, update `decisions.md` (status `decided <date>: <what>`), apply the consequences to `plan.md` in place, refresh the `decisions` and `thesis` memories if they changed, delegate `marketing-dispatcher` `Job: reseed` for the current week, log, and answer with what changed in five lines.

### brief (attended)

A question about strategy, the market, a competitor, the plan or the numbers. Answer from memory, `strategy/`, `metrics/` and `reviews/`, citing the file and date for every number. Write nothing but the log line. When the answer needs research the pool does not hold, do it live and say the finding is fresh and not yet in the analysis.

## 3. Jobs on the members

Members run when the lead delegates them or when a person opens a session on the member directly. Either way the prompt gate applies: the product slug comes from the delegation prompt, the attached prompt, or the single-product default.

### marketing-dispatcher

- `seed`: build `tasks/<product>/backlog.md` from `plan.md` per `task-method.md`. Every plan week, every engine, every front-door change and every decision becomes tasks. Then run `today`.
- `today`: pick today's list per `task-method.md` (week, dependencies, the founder's minute budget, due follow-ups from the board post), write `tasks/<product>/today.md`, apply any `done`, `skip` or `block` lines found in new inbox notes first.
- `reseed`: read the applied plan deltas for the week named, add, retire or move tasks in the backlog accordingly, keep every id stable, then run `today`.
- Attended commands, in any wording: `done <ids>` (mark, ask for the evidence the done line names if it is missing, record follow-ups the person mentions by posting them to the board for `marketing-followups`), `skip <id> <why>`, `block <id> <on what>`, `add <task>` (assign the next id, put it in the current week unless told otherwise), `move <id> to <week>`, `next` (rerun `today` and answer with the list). Always end an attended turn by rewriting `today.md` and saying the list.

### marketing-progress

- `report`: follow `progress-method.md`. Write `progress/<product>/progress.md`. When a week is slipping by the method's definition or a founder decision has been waiting more than three weekdays, also `pool_post` a three-line alert addressed to `marketing-lead`.

### marketing-metrics

- `collect`: follow `metrics-method.md`. Read every new file in `inbox/<product>/metrics/`, fetch the public sources the prompt allows, write or correct the week's row in `metrics/<product>/metrics.md`, update the per-post and per-kit tables. Every cell has a source or says `not supplied`.

### marketing-reviewer

- `review`: follow `review-method.md`. Read `plan.md`, `backlog.md` (done and not done this week), `metrics.md`, `progress.md`, `followups.md`, the last review. Write `reviews/<product>/<yyyy>-w<ww>.md`. `pool_post` the Plan delta section addressed to `marketing-lead`.

### marketing-followups

- `sweep`: follow `followup-method.md`. Read new inbox notes, new board posts, the backlog rows marked done since the last sweep (their notes column), the latest review, and `list_sessions` for prompts that read as asks. Capture, dedupe, set due dates, close what the evidence closes, write `followups/<product>/followups.md`, and `pool_post` the due-today and overdue list addressed to `marketing-dispatcher`.
- Attended: `add <text>` (capture with source `founder, <date>`), `close <id> <how>`, `list` (open ones, soonest due first).

## 4. Log line (every agent, every run)

Append to `/pools/marketing-pod/log/<product>.md`:

`<yyyy-mm-dd> <hh:mm> | <agent> | <job> | DONE <one-line summary with the file written>` or `... | SKIPPED (<reason>)`.

Then, for the lead's scheduled jobs only, `email_me` once. Members never email; the lead reads their files and reports. Keep the chat summary to three sentences with the paths.

## 5. Idempotency

Every write is preceded by a read. A task id, a follow-up id, a metric row, a review file and a memory entry are looked up before they are created; found means update in place. Re-running any job after an interruption finishes the job without duplicating anything.
