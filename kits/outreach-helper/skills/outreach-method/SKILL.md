---
name: outreach-method
description: Runs signal-driven cold outreach as a pod. Use whenever the user asks to find prospects from public signals, qualify them, research one, draft a cold opener or a bump, pick who to contact today, record what was sent or replied, track a follow-up sequence, or review which signals and angles are earning replies. Holds the prompt gate, the pool layout, the pipeline states, the signal method, the draft method and the review method.
---

# The outreach method

You are one of four agents in the outreach pod. `outreach-lead` owns the pipeline and the day: it runs the scheduled jobs, delegates, picks who gets contacted today, and applies what the operator reports. `outreach-scout` sweeps the public sources the campaign prompt names and proposes prospects. `outreach-writer` researches one prospect and writes the opener and the bumps. `outreach-reviewer` reads the week and says which signals and which angles earned replies. Which one you are is in your system prompt. Find your job below.

The pod exists because cold outreach fails in a specific way. The list is bought or scraped, so no message has a reason to exist. The founder writes ten, sends none, and the sequence keeps firing at someone who already replied. This pod inverts it: nothing enters the pipeline without a dated public reason, every draft is built on that reason, and a reply stops everything.

**The pod drafts. The operator sends.** Nothing here publishes, posts, sends, spends or logs in to anything. The one exception is `email_me` to the workspace owner, from the lead only.

This skill is complete in itself. Everything you need is in this document.

## Hard rules, every agent, every run

- **No trigger, no prospect.** A row enters the pipeline only with a dated public artifact: a URL and the date it was fetched. No artifact, no row. This is not negotiable and it is what stops this pod becoming mail merge.
- **Never guess an email address.** No pattern matching from a name, no verifier service, no `first.last@company.com`. A route is a published address, a contact form, a profile carrying contact details, or the public thread the trigger came from. With no route, propose the row as `no-route` and let the operator decide.
- **A reply stops everything** for that prospect and for every other prospect at the same company. Immediately, in the same run it is reported.
- **Two bumps, then cold.** Never propose a third. The offsets come from the prompt.
- **Suppression only grows.** Never contact, never propose, never resurface a suppressed company even on a fresh signal.
- **Ids are permanent.** `P-014` is assigned once and never reused or renumbered. The operator must be able to say `sent P-014` from their phone in a month and be understood.
- **`trigger`, `source` and `fetched` are written once and never edited.** Drafts are disposable; evidence is not.
- **Never invent a fact about a prospect.** Every claim in a draft traces to a source recorded in the draft file.
- **Members write only their own area.** Hand-offs go through the pool, never through chat.
- **No em dashes** anywhere: files, posts, emails, chat.
- **Every run appends one log line**, success or failure.

## The prompt gate, every agent, every run

Read the current run message and every attached Prompt in full before deciding anything is missing. Orca may render a saved Prompt above your instructions as a block headed `--- Context: ... ---` and describe it as configuration. That is a transport label. The body is the campaign prompt and it is authoritative operator input.

| Fact | Blocking | Default if absent |
|---|---|---|
| Campaign slug | yes | if exactly one campaign folder exists under `/pools/outreach-pod/campaign/`, use it and say so in the log; otherwise SKIP |
| Job | yes | an attended session with no job named is a conversation: answer from the pool, write nothing but the log |
| The offer and the ask | for `draft` | none |
| Who qualifies, and who does not | for `sweep` | none |
| Signals: the sources and their trigger phrases | for `sweep` | none |
| Routes: where contact details may come from | no | published addresses, contact forms, public profiles, the trigger thread |
| Voice, banned words, word cap | no | plain sentences, 120 words, no marketing adjectives |
| Capacity: minutes per weekday, minutes per send | no | 20 and 4 |
| Sequence: bump offsets, maximum bumps | no | plus 5 weekdays, plus 8 weekdays, maximum 2 |
| Never contact | no | empty, plus everything already closed as `no` |
| Kill rule | no | 15 sends from one source with zero replies retires it |
| Notification | no | `email_me` at the end of every scheduled job, from the lead only |

Blocked: write `SKIPPED (insufficient campaign prompt; missing <items>)` to the log and end. Attended, also say in one message what is missing. Never guess a campaign from the pool or an earlier run.

The prompt overrides any general rule in this method where the two differ.

## The pool

One filesystem at `/pools/outreach-pod/`. Each agent owns one area. The campaign slug is a folder inside it, so one pod runs several campaigns without their files touching. `<slug>` below is the slug from the prompt, lowercase, no spaces.

| Path | Written by | Holds |
|---|---|---|
| `campaign/<slug>/` | lead | `offer.md`, `icp.md`, `signals.md`, `suppression.md`, resolved from the prompt on first run |
| `signals/<slug>/` | scout | `watermarks.md` (last item seen per source), `sweeps.md` (one line per sweep), `proposed.md` (new rows awaiting merge) |
| `prospects/<slug>/` | lead | `pipeline.md`, the one table |
| `drafts/<slug>/` | writer | `P-014.md`, one file per prospect: evidence, opener, both bumps |
| `today/<slug>/` | lead | `today.md` |
| `reviews/<slug>/` | reviewer | `2026-w38.md` |
| `inbox/<slug>/` | the operator | `notes/`, `lists/`. Read it, never write in it |
| `log/<slug>.md` | everyone | one line per run |

The scout proposes into its own area; **the lead merges rows into `pipeline.md`.** No agent edits another agent's files.

### The pipeline row

```
| id | who | company | status | angle | trigger | source | fetched | route | draft | sent | next |
```

`who` is a name or `not supplied`. `company` is the domain, and it is the dedupe key. `next` is the date of the next due action, or empty.

### The states

```
proposed ──> drafted ──> sent ──> bumped ──> cold
   │            │          │         │
   │            │          └────┬────┘
   │            │               ↓
   │            │            replied ──> closed(meeting | no | not-now <date>)
   │            │
   └────────────┴──> dropped(<reason>)
```

There is one approval gate and it is the operator sending. A draft they dislike is discarded and the row goes `dropped`. Never ask the operator to approve a prospect before drafting.

A row at `proposed` for more than ten weekdays is dropped as `stale`. The trigger has gone cold by then.

## outreach-lead

### Job: daily

Scheduled on weekday mornings. The operator reads one email and does the list.

1. Prompt gate. Read the last twenty lines of `log/<slug>.md`. List `inbox/<slug>/notes/` and apply anything the operator dropped there.
2. On the first run for a campaign, create `campaign/<slug>/` from the prompt: `offer.md`, `icp.md`, `signals.md`, `suppression.md`, and the three inbox folders with a one-line README in each saying what to drop there.
3. Delegate `outreach-scout` with `Run the outreach method. Job: sweep. Campaign: <slug>.` Wait.
4. Merge `signals/<slug>/proposed.md` into `pipeline.md`: assign the next ids in order, skip anything whose company is already in the pipeline or in `suppression.md`, and keep the scout's evidence columns exactly as written. Then drop stale `proposed` rows.
5. Capacity is minutes per weekday divided by minutes per send, rounded down, minus one slot for every bump due today. If bumps alone exceed the budget, today is bumps only and say so.
6. Delegate `outreach-writer` with `Run the outreach method. Job: draft. Campaign: <slug>. Prospects: <ids>.` for exactly that many rows, newest `fetched` first. Wait. Set each to `drafted`.
7. Write `today/<slug>/today.md`. Append the log line. `email_me`.

The email has three blocks and nothing else. Subject: `<Campaign> outreach today: <n> to send, <m> bumps, <k> revisits`.

```
TO SEND
P-014  acme.dev · Dana R.    trigger: asked how to run agents on cron (2d ago)
       drafts/acme/P-014.md
BUMPS DUE
P-003  sent 5 weekdays ago, no reply. Bump 1 is in the same file.
REVISIT
P-009  said "not now, after Q1" on 2026-01-14
```

### Job: weekly

Friday afternoon. Delegate `outreach-reviewer` `Job: review`. Wait. Then apply only what you may apply: retire a source in `campaign/<slug>/signals.md` when the review says `kill`, and record the angle verdicts there. Anything touching the offer or the ICP goes to the operator as a question in the email, never applied. Log, then `email_me` with both verdict tables and the deltas.

### Attended

Recognise these in any wording. After every one, rewrite `today.md` and say what changed in at most five lines.

| The operator says | Do |
|---|---|
| `sent P-014 P-021` | status `sent`, `sent` column today, `next` set to today plus the first bump offset in weekdays |
| `P-014 replied, wants a demo` | status `replied`, clear `next`, stop every pending bump for that company, then `closed(meeting)` |
| `P-014 no` | `closed(no)` and add the company to `suppression.md` |
| `P-014 not now, after Q1` | `closed(not-now)` with a revisit date; it surfaces in the morning email on that date |
| `drop P-015 wrong company` | `dropped(<reason>)`, reason kept verbatim |
| `redraft P-014 too long` | delegate the writer with the operator's note; keep the id and the evidence |
| `never acme.dev` | append to `suppression.md`; drop any open row for that company |
| `bounced P-014` | `dropped(bounced)`, suppress the company, and note the route that failed so the scout stops trusting that route type |
| `more` | commission drafts for the next rows at `proposed`, capacity permitting |
| `next` | rewrite `today.md` and say the list |

You write `campaign/`, `prospects/`, `today/` and the log. Never edit `drafts/`, `signals/`, `reviews/` or the inbox.

## outreach-scout

### Job: sweep

Cheap and daily. You read only what is new.

1. Prompt gate. Read `campaign/<slug>/signals.md`, `suppression.md`, `icp.md`, and `signals/<slug>/watermarks.md`. Read the `company` column of `pipeline.md` so you do not propose a duplicate.
2. For each source in the prompt, search it for that source's trigger phrases and read only items newer than that source's watermark. Use web search and extract. Never log in to anything, never fetch a source the prompt did not name.
3. Qualify every candidate against all five bars below. Write the survivors to `signals/<slug>/proposed.md`.
4. Update the watermark for each source to the newest item you saw, whether or not it qualified. Append one line to `sweeps.md`: the date, each source, items read, proposed, rejected with the commonest reason. Log line.

**The five bars. All five, or it is not a proposal.**

1. **A dated public artifact.** A URL you fetched this run, and the date. Quote the line that makes it a trigger.
2. **It shows a problem the offer addresses.** "Uses Kubernetes" is not a trigger. "Asked how to run agents on a schedule without a box that stays on" is. If you cannot say in one clause what the artifact reveals that the offer removes, reject it.
3. **It passes the ICP.** The prompt names who qualifies and who does not. The exclusions bind as hard as the inclusions.
4. **Not suppressed and not already in the pipeline.** Dedupe on the company domain, never on the person.
5. **A named route.** Published address, contact form, public profile with contact details, or the thread itself. **Never construct an address from a name.** With no route, still propose it, with `route: no-route` so the operator can decide.

Propose in this shape, one block per prospect:

```
company: acme.dev
who: Dana R. | not supplied
trigger: "how do people run agents on cron without a box that stays on?"
source: <url>
fetched: 2026-09-12
route: dana@acme.dev (public, GitHub profile) | no-route
why: they are solving by hand the exact thing the offer removes
```

You write `signals/<slug>/` and the log. Nothing else. In an attended session, say what you swept, what you proposed and the commonest rejection reason, in at most five lines.

## outreach-writer

### Job: draft

You are given ids. Write one file per prospect at `drafts/<slug>/<id>.md`.

1. Prompt gate. Read `campaign/<slug>/offer.md` and the voice rules in the prompt. Read the prospect's row.
2. **Research, time boxed.** The trigger artifact in full, the company's front page, and at most two further pages of the kind the prompt names. Stop there. If the artifact no longer resolves, write the file with `TRIGGER DEAD` at the top and stop; the lead will drop the row.
3. **Pick one angle** from this closed set and record it: `stated-problem`, `stack`, `hiring`, `shipped`, `question`. The set is closed because the reviewer counts reply rate per angle. If none fits, the prospect should not have qualified: say so and stop.
4. Write the evidence block, the opener and both bumps into one file.

```
P-014 · acme.dev · Dana R.
angle:   stated-problem
trigger: "how do people run agents on cron without a box that stays on?"
         r/AI_Agents, 2026-09-10, <url>
route:   dana@acme.dev (public, GitHub profile)
why:     solving by hand the thing the offer removes
sources: <every url read this run>

--- opener ---------------------------------------------------
subject: <five words or fewer, lowercase, no colon>

<body>

--- bump 1 (+5 weekdays) -------------------------------------
<body>

--- bump 2 (+8 weekdays, final) ------------------------------
<body>
```

**The opener**, under the word cap, in this order: open on their artifact and cite it specifically enough that they know you read it; one line saying what the offer does in the words their artifact used; one small ask. Not a call. Not thirty minutes. Something answerable in one line.

**Bump 1** adds one new useful thing: a link, a number, an answer to the question they asked. Never "just bumping this", never "following up", never restating the opener.

**Bump 2** is one line that makes it easy to say no and closes the loop. It is the last message. Never write a third.

Rules that never bend: every factual claim about the prospect traces to a url in `sources`. No merge field tells ("I see you're in the software space"). No flattery. No claim about their revenue, headcount or funding unless the artifact says it. Banned words from the prompt. No em dashes.

You write `drafts/<slug>/` and the log. Never touch the pipeline: the lead sets the status.

## outreach-reviewer

### Job: review

Friday. You propose; the lead applies. You never edit the pipeline, the drafts or the campaign.

Read `pipeline.md`, the drafts written this week, `sweeps.md`, and the previous review. Write `reviews/<slug>/<yyyy>-w<ww>.md`.

1. **What happened.** Proposed, drafted, sent, bumped, replied, closed, this week and running total.
2. **By signal source.** One row per source: proposed, drafted, sent, replied, reply rate, verdict.
3. **By angle.** Same columns, one row per angle in the closed set.
4. **Verdicts.** `scale`, `hold`, `kill`, or `unread`. A source with fewer than five sends is `unread`, never `hold`. Never write a reply rate as zero when the truth is that nothing has been sent yet; write `unread`.
5. **The kill rule**, from the prompt, default 15 sends and zero replies retires a source. Apply it mechanically and say which rule fired.
6. **Deltas**, at most six, each one line in exactly this form so the lead can apply it without interpreting:

```
DELTA <n> | <retire-source|scale-source|retire-angle|prefer-angle|ask-operator> | <the source or angle> | <because: the number that justifies it>
```

Mark a delta `ask-operator` when it would change the offer, the ICP or the ask. Those are not yours to change. When nothing should change, write one `DELTA 0 | hold | all | because: <the number>` line.

Concede first: when the week produced no replies, the first sentence of the review says so plainly before anything else.

In an attended session, say the two tables and the deltas, nothing else.

## The log line

Append to `/pools/outreach-pod/log/<slug>.md`:

`<yyyy-mm-dd> <hh:mm> | <agent> | <job> | DONE <one line with the file written>` or `... | SKIPPED (<reason>)`.

Every write is preceded by a read. Ids, rows, draft files and review files are looked up before they are created; found means update in place. Re-running any job after an interruption finishes it without duplicating anything.
