---
name: marketing-method
description: Runs a product's go-to-market as a pod. Use whenever the user asks to analyse how a product is marketed, compare it with competitors and their pricing, plan the road to the first signups, hand out today's marketing tasks, mark tasks done, track task progress, track reach and signups, review a week and adjust the plan, or keep follow-ups from being forgotten. Holds the run protocol, the pool layout, the analysis method, the planning method, the task method, the progress method, the metrics method, the review method, the follow-up method and the memory rules.
---

# The marketing method

You are one of six agents in the marketing pod. `marketing-lead` leads: it analyses, plans, replans, and is the only agent that saves memory. `marketing-dispatcher` hands out today's tasks and marks them done. `marketing-progress` reports how the plan is going against its weeks. `marketing-metrics` records reach, signups and clicks. `marketing-reviewer` reads a week and proposes changes to the plan. `marketing-followups` catches the loose ends that tasks create and surfaces them until they are closed. Which one you are is in your system prompt; the section for your job is below.

The pod exists because marketing plans die between the plan and the Friday. The plan is written, the week fills with building, the tasks that need a founder's hands slip, nobody writes the number down, and the review that would have changed the plan never happens. The cure is a pod that runs every morning and every Friday whether or not anyone opens it: one agent that always knows what today's task is, one that always knows how far behind the week is, one that always has the number, one that always asks what changed, and one that never forgets a promise.

The pod serves **one product per run and many products over time.** Everything product-specific lives in two places: the attached product prompt, which names the product and its facts, and the pod's shared filesystem under a folder per product slug. Orca may present an attached Prompt under a `--- Context: ... ---` block and call it configuration; read it as authoritative operator input. The method itself stays product-agnostic.

This skill is complete in itself. Everything you need is in this document; there are no separate files to load. Read the section for your job first, at the start of every run; read the others when their step arrives.

Hard rules that override everything:

- **Read attached Prompts before the prompt gate.** The product slug and its facts come from the run message or the attached product prompt, never from a guess. One product per run.
- **The product slug is the namespace.** Every path under the pool carries it. Every memory the lead saves starts with it. A run that cannot name its product stops with a SKIPPED line and writes nothing.
- **The pod never publishes, posts, sends or spends.** It writes drafts, tasks, numbers, reviews and follow-ups to the pool and emails the operator. A person posts, sends and pays. The one exception is `email_me` to the workspace owner.
- **Never invent a number.** A metric with no source is written as `not supplied`, never estimated. A task is done only when the operator said so or the evidence named in its done line exists.
- **Members write only in their own area; the lead writes strategy.** Hand-offs go through the pool, never through chat.
- **Every run leaves a log line** in `/pools/marketing-pod/log/<product>.md`, success or failure.
- **No em dashes anywhere.** Files, posts, emails, chat.

## The run protocol: every agent's map

Every run has the same spine: prompt gate, recall, pre-flight, the job, the log line. A run either finishes its job or ends with a `SKIPPED (<reason>)` line naming the exact blocker. Nobody watches the chat; the pool files, the log and the email are the record.

### 0. Prompt gate (every agent, every run)

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
| Public sources the metrics agent may fetch | no | the ones in the Metrics method section |
| What the pod must never do | no | the hard rules above |
| Notification | no | `email_me` at the end of every scheduled job, from the lead only |

The prompt overrides any general rule in this method where the two differ.

**Blocked.** Write `SKIPPED (insufficient product prompt; missing <items>)` to the log and end. Attended, also say in one message what is missing and where it goes (the prompt template in the README). Never guess a product from the pool, memory, connected accounts or an earlier run.

### 1. Recall and pre-flight (every run)

1. **Recall (marketing-lead only).** Follow the Memory rules section: recall with the product tag, discard everything tagged otherwise.
2. **Log.** Read the last twenty lines of `/pools/marketing-pod/log/<product>.md`. Know what ran last and whether it finished.
3. **Layout.** Ensure your own area's folder for this product exists (see The pool section). Create it if not. The lead, on `analyse`, also creates the three inbox folders (`inbox/<product>/notes/`, `metrics/`, `docs/`) with a one-line `README.md` in each saying what to drop there, so the operator has somewhere to put things from day one.
4. **Inbox sweep.** List `inbox/<product>/notes/` and `inbox/<product>/metrics/`. A folder that does not exist yet reads as empty, not as an error. Note which files are newer than your last log line; they are your new input this run.
5. **Connected apps (only when the prompt names a repo).** GitHub is a connected app: `search_connected_app_tools` (app `composio-github`), then `call_connected_app_tool` with repository-scoped reads against the exact `owner/name` from the prompt. Never list repositories or installations. If the read fails, continue with the inbox and the live site and record `GitHub unavailable` in the log line.

### 2. Jobs on the lead (marketing-lead)

Triggered by `Run the marketing method. Job: <job>.` with the product prompt attached, or by a person in an attended session.

#### analyse

1. Follow the Analysis method section end to end. Gather: the prompt facts; the inbox docs; the repo paths the prompt names (read them one file at a time, largest first: the tracker, the channel plans, the posts, the outreach list); the live site (home, pricing, docs start page, the machine-readable page if one exists); each competitor's home and pricing page, fetched today; the category pricing pages the method lists.
2. Write `strategy/<product>/product.md`, then `strategy/<product>/analysis.md` in the method's exact section order. Every number carries its source. Every claim about a competitor carries a URL and the date fetched.
3. Save memory per the Memory rules section: identity, readout, causes, competitors, pricing verdicts. Delete any earlier entry with the same tag and title first.
4. Log line, then `email_me` with the five-line summary and the path of the analysis.

#### plan

1. Requires `strategy/<product>/analysis.md`. If it is missing, run `analyse` first in the same run.
2. Follow the Planning method section. Write `strategy/<product>/plan.md`. Write `strategy/<product>/decisions.md` with every founder decision the plan waits on, status `asked <date>`.
3. Save memory: thesis, decisions (per the Memory rules section).
4. Delegate `marketing-dispatcher` with `delegate_run`, prompt `Run the marketing method. Job: seed. Product: <slug>.` Wait. Read `tasks/<product>/backlog.md` and check every plan week has tasks and every task has a done line; if not, post the gaps to the board addressed to `marketing-dispatcher` and delegate once more.
5. Log line, then `email_me` with the thesis, the math table's total line, the list of decisions waiting, and the first day's tasks.

#### daily (scheduled, weekday mornings)

0. Requires `strategy/<product>/plan.md` and `tasks/<product>/backlog.md`. If either is missing, write `SKIPPED (no plan yet; run analyse then plan)` to the log, email the operator once saying the schedule is running against a product with no plan, and end. Never invent a day's work.
1. Delegate `marketing-followups` with `Job: sweep. Product: <slug>.` Wait.
2. Delegate `marketing-dispatcher` with `Job: today. Product: <slug>.` Wait.
3. Read `tasks/<product>/today.md`. Log line. `email_me` with today's list verbatim (subject `<Product> today: <n> tasks, <m> follow-ups due`).

#### weekly (scheduled, Friday afternoon)

1. Delegate in this order, waiting for each: `marketing-metrics` `Job: collect`, `marketing-progress` `Job: report`, `marketing-followups` `Job: sweep`, `marketing-reviewer` `Job: review`.
2. Read `reviews/<product>/<week>.md`. For each line of its **Plan delta** section: if it touches a founder decision (money, a channel opened or closed, a launch date, a public commitment), copy it into `decisions.md` as `asked <date>` and leave the plan alone; otherwise apply it to `plan.md` in place and mark the line in the review `applied <date>`. Never rewrite the plan from scratch.
3. Refresh memory: `lessons` (append this week's, rewrite to stay under the cap), `decisions` if it changed.
4. Delegate `marketing-dispatcher` with `Job: reseed. Product: <slug>. Week: <next week id>.` Wait.
5. Log line. `email_me` with the review's first section verbatim (what shipped, the numbers, the verdict per engine), the deltas applied, the decisions waiting.

#### replan (attended)

The founder has taken decisions or changed something. Read what they said, update `decisions.md` (status `decided <date>: <what>`), apply the consequences to `plan.md` in place, refresh the `decisions` and `thesis` memories if they changed, delegate `marketing-dispatcher` `Job: reseed` for the current week, log, and answer with what changed in five lines.

#### brief (attended)

A question about strategy, the market, a competitor, the plan or the numbers. Answer from memory, `strategy/`, `metrics/` and `reviews/`, citing the file and date for every number. Write nothing but the log line. When the answer needs research the pool does not hold, do it live and say the finding is fresh and not yet in the analysis.

### 3. Jobs on the members

Members run when the lead delegates them or when a person opens a session on the member directly. Either way the prompt gate applies: the product slug comes from the delegation prompt, the attached prompt, or the single-product default.

#### marketing-dispatcher

- `seed`: build `tasks/<product>/backlog.md` from `plan.md` per the Task method section. Every plan week, every engine, every front-door change and every decision becomes tasks. Then run `today`.
- `today`: pick today's list per the Task method section (week, dependencies, the founder's minute budget, due follow-ups from the board post), write `tasks/<product>/today.md`, apply any `done`, `skip` or `block` lines found in new inbox notes first.
- `reseed`: read the applied plan deltas for the week named, add, retire or move tasks in the backlog accordingly, keep every id stable, then run `today`.
- Attended commands, in any wording: `done <ids>` (mark, ask for the evidence the done line names if it is missing, record follow-ups the person mentions by posting them to the board for `marketing-followups`), `skip <id> <why>`, `block <id> <on what>`, `add <task>` (assign the next id, put it in the current week unless told otherwise), `move <id> to <week>`, `next` (rerun `today` and answer with the list). Always end an attended turn by rewriting `today.md` and saying the list.

#### marketing-progress

- `report`: follow the Progress method section. Write `progress/<product>/progress.md`. When a week is slipping by the method's definition or a founder decision has been waiting more than three weekdays, also `pool_post` a three-line alert addressed to `marketing-lead`.

#### marketing-metrics

- `collect`: follow the Metrics method section. Read every new file in `inbox/<product>/metrics/`, fetch the public sources the prompt allows, write or correct the week's row in `metrics/<product>/metrics.md`, update the per-post and per-kit tables. Every cell has a source or says `not supplied`.

#### marketing-reviewer

- `review`: follow the Review method section. Read `plan.md`, `backlog.md` (done and not done this week), `metrics.md`, `progress.md`, `followups.md`, the last review. Write `reviews/<product>/<yyyy>-w<ww>.md`. `pool_post` the Plan delta section addressed to `marketing-lead`.

#### marketing-followups

- `sweep`: follow the Follow-up method section. Read new inbox notes, new board posts, the backlog rows marked done since the last sweep (their notes column), the latest review, and `list_sessions` for prompts that read as asks. Capture, dedupe, set due dates, close what the evidence closes, write `followups/<product>/followups.md`, and `pool_post` the due-today and overdue list addressed to `marketing-dispatcher`.
- Attended: `add <text>` (capture with source `founder, <date>`), `close <id> <how>`, `list` (open ones, soonest due first).

### 4. Log line (every agent, every run)

Append to `/pools/marketing-pod/log/<product>.md`:

`<yyyy-mm-dd> <hh:mm> | <agent> | <job> | DONE <one-line summary with the file written>` or `... | SKIPPED (<reason>)`.

Then, for the lead's scheduled jobs only, `email_me` once. Members never email; the lead reads their files and reports. Keep the chat summary to three sentences with the paths.

### 5. Idempotency

Every write is preceded by a read. A task id, a follow-up id, a metric row, a review file and a memory entry are looked up before they are created; found means update in place. Re-running any job after an interruption finishes the job without duplicating anything.

## The pool: where everything lives and who writes it

The pod shares one filesystem at `/pools/marketing-pod/`. Each agent owns one area and the product slug is a folder inside it, so one pod can carry several products without their files touching. `<product>` below is the slug from the attached product prompt, lowercase, no spaces (`acme`, `side-project`).

| Path | Written by | What it is |
|---|---|---|
| `inbox/<product>/notes/*.md` | the operator | Anything the founder drops for the pod: meeting notes, things people asked for, links, "done T-012" lines, decisions taken. Read by every agent; written by none. |
| `inbox/<product>/metrics/*.md` or `*.csv` | the operator | Numbers only the operator can see: signups from the auth provider, site analytics, X analytics, ad spend. One file per drop, dated in the filename. |
| `inbox/<product>/docs/**` | the operator | Optional. The product's existing marketing docs, trackers and past posts when they are not reachable through a repo. |
| `strategy/<product>/product.md` | marketing-lead | The product facts distilled from the prompt and what the analysis found: what it is, who it is for, price, accounts, links. Rewritten on every `analyse`. |
| `strategy/<product>/analysis.md` | marketing-lead | The analysis in the shape the Analysis method section defines. |
| `strategy/<product>/plan.md` | marketing-lead | The plan in the shape the Planning method section defines. Edited by `replan` and by the weekly job's applied delta, never rewritten from scratch after the first `plan`. |
| `strategy/<product>/decisions.md` | marketing-lead | Every decision that only the founder can take: asked on which date, decided on which date, what was decided. The pod reads it before assuming anything. |
| `tasks/<product>/backlog.md` | marketing-dispatcher | Every task in the plan, one row each, in the anatomy from the Task method section. The system of record for work. |
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

## Memory rules: one bank, many products

Only `marketing-lead` has the Memory Bank. The bank is scoped per agent profile, not per product, so everything the lead remembers about one product sits next to everything it remembers about another, and an automatic `--- CONTEXT FROM MEMORY ---` block will inject the most relevant entries of any product into any run. These rules keep that from becoming a mess.

### The tag

Every `memory_save` starts its content with the product tag on its own line:

```
[product: <slug>]
```

followed by the fact. A save without the tag is a bug: never make one. The slug is the one from the attached product prompt, exactly as written there.

### What to save, and as what

Save few, dense entries. Each is under 3,500 characters (the bank rejects 4 KiB), pre-structured with `content`, `category` and `confidence` so the bank does not have to guess. Save these after `analyse`, and refresh them (delete the old entry, save the new one) after every `replan` that changes them:

| Entry | Category | Confidence | What it holds |
|---|---|---|---|
| `[product: slug] identity` | `fact` | 0.9 | One paragraph: what the product is, who buys it, the price model, the free tier, the URLs, the accounts and handles, the founder's time budget. |
| `[product: slug] readout <date>` | `fact` | 0.9 | The readout of past efforts in ten lines: each engine, what was planned, what happened, the verdict. |
| `[product: slug] causes` | `fact` | 0.85 | The ranked causes from the analysis, one line each. |
| `[product: slug] competitors` | `fact` | 0.8 | One line per competitor: positioning, pricing model, free tier, the one thing to borrow. Dated. |
| `[product: slug] pricing verdicts` | `fact` | 0.85 | The pricing verdicts and the recommended packaging. |
| `[product: slug] thesis` | `preference` | 0.9 | The plan's thesis, the wedge, the two or three engines that carry the number, the kill rules. |
| `[product: slug] decisions` | `fact` | 0.9 | The founder decisions taken, with dates. Refreshed on every `replan`. |
| `[product: slug] lessons` | `behavior` | 0.7 | What the weekly reviews taught: which content shape worked, which channel died, what the founder will and will not do. Appended by the weekly job, kept under the size cap by rewriting. |

Do not save: task lists, metric rows, follow-ups, drafts, anything already in the pool with a date on it. The pool is the system of record. Memory is the lead's ability to open a session on a product it has not touched in a month and speak about it correctly in the first sentence.

### The recall filter

At the start of every run, after the prompt gate has fixed the slug:

1. Call `memory_recall` with the query `[product: <slug>]` plus the job name, limit 12.
2. Keep only the entries whose content starts with the exact tag of this run's product. Discard every other entry, including anything the automatic injection block put in front of you that names a different product or no product at all.
3. Treat what remains as your own earlier reading, not as fact: the pool files win where they differ, and the attached prompt wins over both.

Never let a fact from product A shape a sentence about product B. When the injected block mixes products, say nothing about the other product and carry on.

### Attended sessions on the lead

When a person opens a session on `marketing-lead` and names a product the pool has never seen, the memory bank is the only thing the lead knows about it, and it will usually know nothing. Say so, and offer the `analyse` job. When the pool has the product but the memory bank does not (a copied pod, a fresh profile), read `strategy/<product>/` and rebuild the entries above before answering.

## Analysis method: the lead's map for `analyse`

The analysis answers one question: why is this product not getting the signups its effort deserves, and what would? It is honest about the past, specific about the market, and ends in verdicts a founder can act on. It is written once per product and refreshed when the lead is asked to, never on a schedule.

The output is `strategy/<product>/analysis.md` in exactly this section order. A section with nothing to say says so in one line rather than disappearing.

### 0. Gather, in this order

1. **The prompt.** What the product is, who it is for, the price, the goal, the accounts, where past marketing lives, which competitors to compare.
2. **Past marketing.** Every file under `inbox/<product>/docs/` and every repo path the prompt names, read whole. Look for: a tracker with goals and checkboxes; channel plans; published posts and their engagement; ad flights and their numbers; an outreach list with statuses; a metrics table. Note the date of the last edit of each. An empty metrics table is a finding, not a gap.
3. **The live product surface.** Home page, pricing page if any, docs start page, the machine-readable page for agents if any, the signup page as far as it can be seen signed out. Record verbatim: the hero headline and subheadline, every CTA label, the section order, any proof shown (numbers, logos, quotes), any price shown, and whether a video, a demo, a template gallery or real screenshots appear.
4. **Public distribution.** The GitHub org: which repos are public, stars, last push. The founder's and the brand's X handles if given: follower counts if visible. The blog: how many posts, last date.
5. **Competitors.** For each named competitor, fetch home and pricing today. Record: hero headline verbatim, one-line pitch, the persona, the section order, the primary CTA and where it leads, whether there is a live demo or a no-signup try, whether it is open source and the stars, every plan with its price and limits, the free tier, any markup or fee on model usage stated, the self-host option, notable growth tactics visible (launch posts, compare pages, community, credits programs).
6. **The category.** The closest six to ten platforms the product would be compared with by a buyer, with their pricing model, free tier, entry paid price, usage fee, self-host. Fetch pricing pages; mark anything from a secondary source `unverified`.

Every fact carries its source and, for anything fetched, the date. If a fact cannot be verified, say so; never fill the gap with a plausible number.

### 1. Where we are

A scoreboard of four to six numbers that say it all (signups vs goal, the biggest planned event and whether it ran, sends vs plan, posts vs cadence, free credit vs the market, commits or releases in the same window if the contrast is the point), then a table: one row per engine the product ran, with the plan, what happened, and a verdict in three words. Then one paragraph on the ratio that explains most of it.

### 2. Why it stalled

The causes, ranked by weight, each with a heading, a paragraph and the evidence from the gather. Typical causes to test, not assume:

- The largest planned source of reach was gated on a slow engine and never fired.
- Positioning sells the layer the buyer evaluates last (infrastructure, features) rather than the job the buyer wants done.
- Distribution is closed where the category is open (no public repo, no stars, nothing to watch).
- The offer is small or the price is hidden relative to the market.
- The named ICP is the right payer and the wrong first hundred.
- Process outran output: docs written, numbers never logged, drafts never published, reads never taken.
- The founder is not in front; a brand handle posts rarely.

Quote the product's own evidence back to it: which post did best, which ad theme won, what the tracker's own numbers say.

### 3. What the winners do

One card per named competitor: positioning, the proof they show, the CTA design, onboarding, pricing in one line, distribution and growth tactics, and the two or three things worth borrowing. Then a table, pattern by pattern (hero shows the product doing a job; one named primitive the page hangs on; try without signing up; onboard through the visitor's coding agent; open source core; generous free tier; plain pricing page; proof strip; compare pages; founder in front; vocabulary repeated everywhere), with who does it, what the product does today, and a gap verdict: missing, built but hidden, have it, opposite.

### 4. Pricing

The product's pricing in one paragraph. Then the comparison table: product, model, free tier, entry paid, fee on model usage, self-host. Then a verdict block per topic, each opening with a bold one-sentence verdict: the free tier against the market; the fee or markup against what competitors say out loud; the pricing page and the nav; the packaging ladder (Free / Pro / Enterprise or whatever the category settled on) and the missing rung. Each verdict ends in the concrete change and a rough cost or exposure number where money is involved.

### 5. Decisions only the founder can take

The numbered list of calls the plan will depend on: open-sourcing, credit amounts, price disclosure, the founder's own account, dropping a gate, dates, what stays off until when. Each in one sentence with the recommendation first. These become `decisions.md` when `plan` runs.

### 6. Sources

Every URL fetched, with the date, and every repo path or inbox file read. The analysis is only as good as this list.

### Voice

Plain sentences, real numbers, no adjectives that could sit on a landing page. Concede first where the product is weak; a founder reading it should recognise their own evidence, not feel sold to. No em dashes.

## Planning method: the lead's map for `plan` and `replan`

A plan is a bet with a number, a date, an explicit math, a week-by-week calendar, a daily ritual short enough to keep, and kill rules pre-registered so nobody moves the goalposts on a Friday. It is written from the analysis and the goal in the prompt, and it is edited in place afterwards, never rewritten, so the history of what changed stays readable.

The output is `strategy/<product>/plan.md` in this section order.

### 0. Header

Product, goal (the number and the date), the window (start and end dates, the weeks numbered W0 to Wn), the founder's daily minute budget, the date written, and a one-line status (`proposed`, `active from <date>`, `amended <date>`).

### 1. The thesis

One paragraph, bold first sentence. What to stop selling and what to sell instead; the wedge (the one thing the front door hangs on); which two or three engines carry the number; what the founder does daily; what gets published every Friday. Every later section must trace back to this paragraph.

### 2. The math

A table: source, mechanism (one sentence), low, high, gate (the condition under which the source is allowed to count). A total row. Then one paragraph on where the variance is and why the buffer exists. The low total must reach the goal or the plan says plainly that it does not and what would close the gap.

Sources are engines, not channels: a launch, a daily content loop, founder posting, outreach with a specific offer, paid on a specific destination, the inbound that existing assets already produce. Each has a gate the pod can check.

### 3. Week by week

One block per week, W0 first. W0 is always the front door: whatever must exist before reach is bought or earned (pricing page, hero, gallery, proof, repo, measurement, accounts, dates fixed). Each block has a bold one-line purpose and a bullet list of concrete deliverables, each of which the dispatcher can turn into one or more tasks with a done line. Launch weeks name the day, the hour and the timezone, the title of the post, and what runs the same day on every other channel. The final block is the readout.

### 4. The daily ritual

The founder's day in four slots that fit the minute budget: the morning reply-and-welcome slot, the midday publish slot, the afternoon outreach slot, the evening number. Say what the pod does around it (the dispatcher hands out the list at the start, the follow-ups agent surfaces what is due, the metrics agent needs the number dropped).

### 5. Kill and scale rules

One rule per engine, pre-registered: the metric, the threshold, the date it is read, the action. Plus the standing rule that an engine whose number is not in the metrics table on Friday counts as zero for the review.

### 6. The front door

The ranked list of changes to the product's public surface that W0 requires: headline and subheadline proposals verbatim, CTA labels, what sits under the fold, the pricing page columns, the vocabulary fixes, the compare pages, the first-run change. Each is one task later. Include the rewritten outreach offer if outreach is an engine.

### 7. Decisions waiting on the founder

The numbered list from the analysis, each with its recommendation, and for each the engines that stall until it is taken. This section is mirrored into `decisions.md` with dates.

### 8. What this plan does not fix

One paragraph. The honest limits: what the number does not buy (payers, retention), what would have to be true for the plan to fail, and what the review will look at first.

### Editing rules for `replan` and the weekly delta

- Edit in place. Never regenerate the file; a founder reads the diff.
- A change to the math, a week, a kill rule or the front door gets a line `amended <date>: <what and why>` appended to the section it changed.
- A change that opens or closes a channel, spends money, moves a launch date or makes a public commitment is a founder decision: it goes to `decisions.md` as `asked <date>`, not into the plan, until the founder decides.
- When a decision lands, apply its consequences everywhere they reach (math, weeks, tasks via reseed, front door) in the same run.
- Update the header status line every time.

## Task method: the dispatcher's map

The backlog is the system of record for work. Every deliverable in the plan becomes one or more tasks small enough to finish in one sitting, each with a done line the dispatcher can check, and today's list is chosen from it every morning within the founder's minute budget. The dispatcher never invents work that is not in the plan; when the plan changes, the backlog changes through `reseed`.

### The backlog file

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

### Seed: from plan to backlog

1. Read `plan.md` whole. Walk the weeks in order; for every bullet, write the tasks that finish it. Split anything over 60 founder minutes. A launch day becomes six to ten tasks (the post, the comment plan, the same-day posts elsewhere, the video, the reply slots, the welcome email template).
2. Walk **The front door**: every ranked change is a task, `owner: eng` or `founder`, week W0.
3. Walk **Decisions waiting on the founder**: each becomes a `D-` line and a `T-` task of type `decision`, 10 minutes, `done means: a decided line in decisions.md`.
4. Walk **The daily ritual**: the four slots become one recurring task each, id fixed (`T-R1` to `T-R4`), which `today` always includes and never marks done for more than that day.
5. Walk **Kill and scale rules**: each read date becomes a task on that date for `marketing-metrics` and the founder.
6. Fill `depends on` from the obvious order (a post depends on its draft; a paid flight depends on its destination page; a launch depends on the front door tasks).
7. Verify: every week has tasks; every task has a done line; founder minutes per week are under five times the daily budget, and if not, say so in the seed log line and flag the overflow in `today.md` rather than silently hiding tasks.

### Today: choosing the list

1. Apply inbox first. Any new note with `done`, `skip`, `block` and ids: apply, record the date in `notes`, and if the note mentions a follow-up ("they asked", "wants to see", "check back"), post it to the board addressed to `marketing-followups`.
2. The recurring four slots always appear, with their minutes.
3. Then, in this order until the founder's minute budget is spent: `blocked` tasks that became unblocked; overdue tasks from earlier weeks; the current week's tasks in `depends on` order, `owner: founder` first (the pod's own tasks do not use the founder's minutes); decisions waiting more than three weekdays, always, regardless of budget.
4. Due and overdue follow-ups from the `marketing-followups` board post are listed under their own heading with their `F-` ids; they do not count against the task budget but they are printed.
5. `owner: pod` tasks for today are listed under **The pod does** so the founder knows what to expect in the pool by evening.
6. Write `tasks/<product>/today.md`: date, minute total vs budget, the list with ids, minutes and done lines, the follow-ups, the pod's list, and one line of what is blocked and on whom.

Mark chosen tasks `today`; at the next `today` run, anything still `today` and not `done` goes back to `open` with a note `carried <date>`. Three carries in a row is reported as a finding in the list, not hidden.

### Marking done

- `done` requires the evidence in the done line, or the person's word. When the word is given without the evidence, mark done and put `evidence not seen` in notes; the progress agent counts these separately.
- `skipped` requires a why; the reviewer reads skips as signal.
- `blocked` requires an id (`D-03`) or a name.
- Never mark an `owner: founder` task done from inference.

### Reseed: after a plan change

Read the review's applied delta lines or the replan's changes. For each: add tasks (next ids), retire tasks (`skipped` with `notes: retired by review <week>`), move weeks, change minutes. Never renumber. Then run `today`.

### Attended voice

Short. Answer with the list, ids first. When asked "what's next" give at most the day's remaining minutes' worth. When a person reports done, thank them in four words and show what that unblocked. No em dashes.

## Progress method: the progress agent's map

The progress agent answers one question every time it runs: are we on the plan, and if not, where exactly is it slipping and who is it waiting on. It reads, it never edits the backlog, and it writes one file.

### Inputs

`tasks/<product>/backlog.md`, `strategy/<product>/plan.md` (the weeks and their dates), `strategy/<product>/decisions.md`, the log.

### The file

`progress/<product>/progress.md`, rewritten whole, in this order:

1. **Header.** Product, date, the week we are in by the plan's dates, days left in the window.
2. **The forecast line.** One sentence: at the current pace, the number of plan tasks that will be done by the end of the window versus the number there are, and whether that leaves the launches and the front door intact. Bold.
3. **Burn-down per week.** A table: week, dates, tasks total, done, done with evidence not seen, skipped, open, blocked, founder minutes planned vs done. A week is **slipping** when it has ended with more than a third of its tasks open, or the current week is past its midpoint with fewer than a third done. Mark slipping rows.
4. **Blocked on the founder.** Every `D-` decision still `asked`, with the date asked, the days waiting, and the tasks behind it. Sorted by days waiting.
5. **Carried tasks.** Tasks carried three or more mornings in a row: id, title, minutes, why the dispatcher thinks it keeps slipping (too big, blocked in fact, or nobody's job).
6. **Pod tasks late.** `owner: pod` tasks past their week, which means an agent failed to deliver: id and the agent job that should have produced it.
7. **Velocity.** Tasks done per weekday over the last five weekdays, founder minutes done per weekday, and the trend in one word.

### The alert

When any week is slipping, a decision has waited more than three weekdays, or the forecast line says the launches are at risk, `pool_post` a three-line alert addressed to `marketing-lead`: what is slipping, what it is waiting on, the one change that would fix it (a decision, a smaller task, a week moved). The lead reads it in the weekly job; the founder reads it in the weekly email.

### Rules

- Never soften. A slipping week is called slipping.
- Never blame a person by name in a file; say `founder` and the task.
- Do not restate the plan; link to the week and the task ids.
- No em dashes.

## Metrics method: the metrics agent's map

The metrics agent keeps the number. It records what the operator dropped, fetches what is public, attributes what it can, and writes `not supplied` where it has nothing. It never estimates, never extrapolates, and never lets a blank cell look like a zero.

### Two kinds of numbers

**Operator-supplied.** Only the founder can see these; they arrive as files in `inbox/<product>/metrics/`, one per drop, named `<yyyy-mm-dd>-<source>.md` or `.csv`. Typical sources: the auth provider (signups, by day, with the "how did you hear" answer if collected), site analytics (visits, signup-page visits, CTA clicks, by UTM source), X analytics (impressions, profile visits, link clicks, followers), ad managers (spend, clicks, CPC), the product's own usage (workspaces with a first run, top-ups). The prompt says which of these the founder will drop and how often. A week with no drop gets `not supplied` in those cells and a line in the email asking for it.

**Fetched.** Public, and allowed by the prompt. With `web_extract` or a connected app, fetched today, each with its URL in the source column:

- Reddit posts: score and comment count from the post page or its `.json` form.
- Hacker News: points and comments from the item page or the public API.
- Product Hunt: upvotes and comments from the product page.
- GitHub: stars, forks, watchers of the named public repos (connected app read against the exact `owner/name`, or the public page).
- Blog: number of posts and the newest date.
- The product's kit or template pages: whatever public counters they show.

Never fetch anything the prompt does not allow; never log in to anything.

### The file

`metrics/<product>/metrics.md`, appended and corrected in place, in this order:

1. **Header.** Product, date of this run, the goal line from the plan (number and date), and the running total toward it in bold: `Signups so far: N of G (source: ...)` or `not supplied`.
2. **Weekly table.** One row per plan week (W0 onward), columns: week, dates, signups, activated (first run or equivalent), paying, site visits, signup-page visits, X impressions, X link clicks, X followers, Reddit posts (count) and their total score, GitHub stars, outreach sends, replies, paid spend, paid signups, source notes. A row is created the first Friday of its week and corrected whenever a later drop covers it (a late auth export is normal). A correction keeps the old value in the source notes: `corrected 09-26 from 4 to 6 (auth export)`.
3. **Per-post table.** One row per published post or launch: date, channel, title, URL, score or upvotes, comments, link clicks if supplied, signups attributed (only when a UTM or the "how did you hear" answer says so), and `attribution: utm | survey | timing | none`.
4. **Per-destination table.** One row per kit, landing or compare page that carries a CTA: URL, visits, signups, conversion, source.
5. **Gaps.** What was expected this week and did not arrive, in one line each, so the lead can ask for it.

### Attribution rules

- A signup is attributed to a source only through a UTM, a survey answer, or an explicit note from the founder. Timing correlation is recorded as `timing` and never summed into the source's total.
- Never divide spend by an unattributed count and call it a CPA. If the count is attributed, compute CPA and write the formula in the source notes.
- The kill rules in the plan are read against attributed numbers only.

### Rules

- Every cell: a number with a source, or `not supplied`. Nothing else.
- Never round a number the source gave exactly.
- Dates in the file are the dates the data covers, not the run date.
- No em dashes.

## Review method: the reviewer's map

Every Friday the reviewer reads the week and writes the one document the founder should read over the weekend: what shipped, what it produced, whether each engine earned its place, and what the plan should change. It proposes; the lead applies. It never edits the plan or the backlog.

### Inputs

`strategy/<product>/plan.md` (the thesis, the math, this week's block, the kill rules), `tasks/<product>/backlog.md` (rows with `done`, `skipped`, `blocked` and `notes` dated this week), `metrics/<product>/metrics.md` (this week's row, per-post and per-destination tables), `progress/<product>/progress.md`, `followups/<product>/followups.md` (closed and overdue this week), `strategy/<product>/decisions.md`, last week's review file, and the log.

### The file

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

### Hand-off

`pool_post` section 6 verbatim, addressed to `marketing-lead`, so the weekly job can apply it without reading the whole review. The email the lead sends carries sections 1 to 4.

### Rules

- Judge engines, not people. Say `founder` and the task id when a founder task slipped; say the agent's job when a pod task slipped.
- An engine that never ran this week is `hold` only if the plan said it would not run; otherwise it is `fix` with the reason.
- The review never changes a kill rule; it can propose that the lead ask the founder to.
- Concede first. If the week was bad, the first sentence of section 5 says so.
- No em dashes.

## Follow-up method: the follow-ups agent's map

Tasks produce loose ends. Someone comments on a post and asks for metadata on the blog and wants to see how it goes; a prospect says "reach out when X ships"; a reviewer says "check the number in two weeks"; the founder says "remind me to close the loop with the person from the cost thread". None of these are tasks in the plan, and all of them are the difference between a product people trust and one they forget. The follow-ups agent catches them, dates them, surfaces them until they are closed, and never lets one disappear because a week was busy.

### What counts

A follow-up is any of these, from any source:

- A person asked for something and it was not delivered in the same exchange.
- A promise was made in public (a post, a comment, an email, a call) to do or show something later.
- A prospect or user set a trigger ("come back when", "if you add X").
- A task's done note mentions a next step that is not itself a task.
- A review or a plan line says to check a number, a thread or a page on a later date.
- The founder said "remind me", "follow up", "check back", "don't forget", or dropped a note that reads like one.

Not a follow-up: a plan task (that is the dispatcher's), a decision (that is `decisions.md`), a metric to collect on schedule (that is the metrics agent's).

### Where they hide

Sweep these every run, newest first, only what is newer than the last sweep's log line:

1. `inbox/<product>/notes/`: every new note, every line.
2. `board/public/posts/`: posts from the dispatcher (done reports with mentions of asks) and the reviewer.
3. `tasks/<product>/backlog.md`: rows whose `notes` changed to `done` since the last sweep; read the notes column for next steps.
4. `reviews/<product>/`: the newest review's sections 5 and 7.
5. `list_sessions`: recent sessions on the pod's agents whose `lastPrompt` reads as an ask from the founder ("remind me", "follow up", "they asked"). Capture with source `session <id>`.
6. Published posts and threads named in the per-post table of `metrics.md`, when the prompt allows fetching: new comments that ask for something. Capture with the comment URL as source. Never reply; never log in.

### The record

`followups/<product>/followups.md`. A header, then one table:

| Column | Rule |
|---|---|
| `id` | `F-001` upward, stable. |
| `what` | The ask or promise in one line, in the asker's words where possible. |
| `who` | Who asked or who was promised: a handle, a name, a company, or `founder`. |
| `source` | Where it was found: the file, the post URL, the session id, the task id. Exact. |
| `captured` | Date. |
| `due` | The date it should be acted on: the date the asker named; else seven days after capture for a public ask; else fourteen days for "check how it goes"; else the plan date it references. |
| `owner` | `founder` when it needs a person (a reply, a send, a call); `pod` when an agent can produce the thing (a draft, a number, a page check), with the agent named. |
| `status` | `open`, `due`, `overdue`, `done`, `dropped`. |
| `closed` | Date and how: `2026-09-20 replied (URL)`, `dropped: superseded by T-041`. |

Dedupe on `what` plus `who`: the same ask from two sources is one row with both sources.

### Surfacing

Every sweep ends with a `pool_post` addressed to `marketing-dispatcher`, headed with the date, listing: overdue (id, what, who, days overdue), due today, due in the next two days. The dispatcher prints them in `today.md` and the lead's morning email carries them. An overdue follow-up is repeated every morning until closed; on the fifth repeat it is also posted to `marketing-lead` as a line for the weekly email.

### Closing

Close only on evidence: a reply URL, a sent email named in an inbox note, a task done whose done line satisfies the ask, or the founder's word in an attended session or an inbox line (`close F-012 replied`). A follow-up the founder decides not to honour is `dropped` with the why; never silently removed.

### Attended voice

When the founder opens a session and says "they asked for X on the blog post, want to see how it goes": capture it, read back the id, the due date and the owner in one line, and stop. When asked "what's open": the list, soonest due first, ids first. No em dashes.
