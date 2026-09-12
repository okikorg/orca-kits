# outreach-helper: design

Date: 2026-09-12
Status: approved in design, not yet built

## The problem

`marketing-helper` treats outreach as one engine among several. Its planning method writes the
outreach offer and puts an afternoon outreach slot on the founder's day, then stops. It never
opens a list, never researches a company, never drafts a message. The founder gets a 20 minute
task that says "do outreach", which is the task they were already failing to do.

This kit is that engine, done properly: find the people who have just shown the problem you
solve, work out why each one is worth a message, write the message, and keep the sequence honest
after you send it.

The category is in demand and thinly served. Lead generation and SDR work is about 6.5% of the
most viewed n8n AI templates, and the best open source AI SDR repository has under 200 stars,
while AI integration work grew 178% year over year in client spend on Upwork. What exists is
mostly mail merge with a data vendor attached.

## Decisions taken

Five, all settled before design:

1. **Draft only. The operator sends.** The pod writes messages into the pool; a person pastes and
   sends them. This keeps the repo's rule that nothing ships that publishes, sends or spends, and
   it keeps domain reputation in human hands. The cost is that the operator's daily minutes are
   the throughput ceiling, which is accepted.
2. **Signal driven discovery.** Prospects come from public places the operator names, swept on a
   schedule, each carrying the artifact that triggered it. Not from an uploaded list, because a
   list gives a draft no reason to exist.
3. **Standalone pod.** Its own pod, pool and counting. It must be useful to someone who has never
   installed `marketing-helper`.
4. **The operator reports outcomes conversationally.** No mail connection, read or otherwise.
   `sent P-014`, `P-014 replied, wants a demo`. Zero privacy surface.
5. **No trigger, no prospect.** If the scout cannot name a dated public thing the person or
   company did, the row does not enter the pipeline. This is the defence against the kit
   degenerating into mail merge, and it is mechanically checkable.

## Non-goals

- Sending, scheduling sends, or connecting to a mailbox.
- Buying, guessing or verifying email addresses.
- CRM. The pipeline file tracks a message sequence, not a deal.
- Multi-channel. Email and the public thread the trigger came from. No LinkedIn automation.
- Replacing `marketing-helper`. The two are independent and may both be installed.

## Architecture

Four agents, one skill, one pod. The campaign prompt carries the strategy, so no agent owns it.

| Agent | Owns | Model |
|---|---|---|
| `outreach-lead` | The pipeline and the day. Runs `daily` and `weekly`, delegates, computes capacity, merges proposals, applies what the operator reports, writes `today.md`, emails. Pod lead. | cheap |
| `outreach-scout` | The signals. Sweeps named public sources against watermarks, qualifies, proposes prospects with dated evidence. | strong |
| `outreach-writer` | The message. Time boxed research on one prospect, then the opener and both bumps. | strong |
| `outreach-reviewer` | The Friday. Reply rate per signal source and per angle, verdicts, the deltas the lead may apply. | strong |

The lead is on the cheap model deliberately, inverting `marketing-helper`. This lead does no
thinking: it merges rows, counts minutes, writes a list, sends an email. The judgement is in the
scout (is this a real trigger) and the writer (is this a message a person would answer), which
are the two places where being cheap costs a reply.

**No Memory Bank on any agent.** `marketing-helper` needed one because its lead had to speak
about strategy a month later, which dragged in product tagging and recall filtering. Here the
pipeline file is the memory, and it is better memory: dated, sourced, and readable by a person.
This removes one reference file and a class of cross campaign contamination bug.

## Data model

### States

```
proposed ──> drafted ──> sent ──> bumped ──> cold
   │            │          │         │
   │            │          └────┬────┘
   │            │               ↓
   │            │            replied ──> closed(meeting | no | not-now <date>)
   │            │
   └────────────┴──> dropped(<reason>)
```

**One approval gate, and it is the operator hitting send.** A second gate at `proposed` would be
two gates for one decision, since nothing leaves without a person pasting it. If the operator
dislikes who a draft is addressed to, they discard it and the row goes `dropped`.

**Drafting is demand driven.** A sweep may surface forty prospects; the operator will send five.
The lead commissions exactly as many drafts as today's capacity supports, newest trigger first.
The rest wait at `proposed`, and are dropped as stale after ten weekdays because the trigger has
gone cold by then.

### The pool

Namespaced by campaign slug so one pod can run several campaigns without them touching.

```
/pools/outreach-pod/
  campaign/<slug>/     lead      icp.md, offer.md, signals.md, suppression.md
  signals/<slug>/      scout     sweeps.md, watermarks.md, proposed.md
  prospects/<slug>/    lead      pipeline.md
  drafts/<slug>/       writer    P-014.md
  today/<slug>/        lead      today.md
  reviews/<slug>/      reviewer  2026-w38.md
  inbox/<slug>/        operator  notes/, lists/
  log/<slug>.md        everyone  one line per run
```

Single writer discipline as in the sibling kits: the scout writes `proposed.md` in its own area
and the lead merges rows into `pipeline.md`. No agent edits another's files. Hand offs go through
the pool, never through chat.

### The row

```
| id | who | company | status | trigger | source | fetched | route | draft | sent | next |
```

Ids are assigned once and never reused or renumbered, so `sent P-014` still means something in a
month. `trigger`, `source` and `fetched` are written once and never edited. Everything else is
mutable.

## Jobs

Vocabulary matches `marketing-helper` so one kit teaches the other.

### daily (weekday morning, scheduled on the pod, prompt attached)

1. Lead fixes the campaign slug from the prompt or the single campaign folder, reads the log,
   sweeps the inbox.
2. Delegate `outreach-scout` `Job: sweep`. Cheap daily because each source carries a watermark;
   a sweep reads only what is new.
3. Lead merges new proposals into `pipeline.md`; drops `proposed` rows older than ten weekdays
   as stale.
4. Lead computes capacity: minutes per weekday divided by minutes per send, both from the prompt.
5. Delegate `outreach-writer` `Job: draft. Prospects: <ids>` for exactly that many.
6. Write `today.md`, append the log line, `email_me`.

The email carries three blocks: to send, bumps due, revisits due. Each send line carries the id,
the company, the trigger in a clause, and the draft path.

### weekly (Friday)

1. Delegate `outreach-reviewer` `Job: review`.
2. Lead applies what the review may apply: retiring a dead source in `campaign/<slug>/signals.md`,
   recording angle verdicts. Anything touching the ICP or the offer goes to the operator as a
   question instead of being applied.
3. Log line, `email_me` with the verdict tables and the deltas.

### attended, on the lead

| Operator says | Effect |
|---|---|
| `sent P-014 P-021` | status `sent`, bump clock starts |
| `P-014 replied, wants a demo` | status `replied`, sequence stops, closed `meeting` |
| `P-014 no` | `closed(no)`, company suppressed |
| `P-014 not now, after Q1` | `closed(not-now)` with a revisit date surfaced in a morning email |
| `drop P-015 wrong company` | `dropped`, reason kept |
| `redraft P-014 too long` | re-commission the writer with the note |
| `never acme.dev` | permanent suppression |
| `more` | commission more drafts today |
| `next` | today's list again |

### Guardrails

1. **Two bumps, then cold.** Default plus 5 and plus 8 weekdays, configurable, and the pod cannot
   propose a third.
2. **A reply stops everything** for that prospect and for anyone else at the same company.
3. **The suppression list only grows.** Every `no`, every `never`, every bounce the operator
   reports. The scout checks it before proposing and will not resurface a suppressed company on a
   fresh signal.

## Methods

### signal-method.md

Source types, all reachable with `@default` web search and extract, none requiring a login: a
subreddit or forum searched for phrases; GitHub repositories depending on a library, or issues
matching a phrase; hiring posts naming a tool or role; Hacker News items; a company's own
changelog or blog; public event or community lists.

A proposal needs all five:

1. A dated public artifact, with URL and date fetched.
2. The artifact shows a problem the offer addresses. "Uses Kubernetes" is not a trigger. "Asked
   how to run agents on a schedule" is.
3. The company passes the ICP filter in the prompt.
4. Not suppressed, and not already in the pipeline. Deduped on domain, not on person.
5. A named route to reach them.

**The pod never guesses an email address.** No pattern matching from a name, no verifier
services. A route is a published address, a contact form, a profile carrying contact details, or
the thread itself. With no route the row is proposed as `no-route` and the operator decides
whether to find one by hand.

This produces fewer prospects than a tool with a data vendor behind it. That is the accepted
trade for a kit that has to be safe in a stranger's hands: guessed addresses bounce, bounces burn
the sending domain, and the operator is the sender.

### draft-method.md

A time boxed research pass: the trigger artifact in full, the company's front page, and at most
two further pages named in the prompt.

The draft file carries the evidence above the message, so the operator can sanity check in five
seconds: id, company, person, the trigger quoted with its source and date, the route and where it
came from, and one line on why this person.

Then an opener and two bumps. The opener stays under the word cap from the prompt, opens on the
prospect's own artifact and cites it specifically, gives one line on the offer in the prospect's
terms, and makes one small ask. Bump 1 adds one new useful thing and never says "just bumping
this". Bump 2 is one line that makes it easy to say no and closes the loop.

Every draft records the **angle** it used, chosen from a small closed set named in this
reference (for example: their stated problem, their stack, their hiring signal, their shipped
change). The set is closed because the reviewer counts reply rate per angle, and free text
cannot be counted.

Hard rules: every factual claim about the prospect traceable to a source in the file; no merge
field tells; the voice and banned words from the prompt; no em dashes.

### review-method.md

Two tables, per signal source and per angle, each with proposed, drafted, sent, replied, a reply
rate and a verdict of `scale`, `hold`, `kill` or `unread`. A source with no number gets `unread`,
never a flattering guess.

Default kill rule, configurable: 15 sends from one source with zero replies retires that source.
Deltas are one line each in a fixed form the lead can apply mechanically. Concede first: when the
week was bad, the first sentence says so.

## The campaign prompt

The control surface, and the reason one pod can run several campaigns.

```
Run the outreach method. Job: <daily|weekly|sweep|draft|review>. Campaign: <slug>.  *

## The offer          what is offered, in one paragraph, and the one small ask
## Who qualifies      the ICP, and explicitly who does not qualify
## Signals            each source, and the phrases that make a post a trigger
## Routes             where contact details may come from. No guessing.
## Voice              register, banned words, word cap, sign off
## Capacity           minutes per weekday, minutes per send
## Sequence           bump offsets, maximum bumps
## Never contact      customers, competitors, partners, anyone already burned
## Kill rule          sends with no reply that retire a source
## The pod must never publish, post, send, spend, log in, guess an address
## Notification       email at the end of every scheduled job
```

## What ships

```
kits/outreach-helper/
  agents/     outreach-lead.yaml  outreach-scout.yaml
              outreach-writer.yaml  outreach-reviewer.yaml
  skills/outreach-method/
              SKILL.md
              references/run-protocol.md      jobs, prompt gate, log line
                         pipeline-layout.md   pool, row, states
                         signal-method.md     sources, watermarks, the five part bar
                         draft-method.md      research pass, anatomy, bumps, voice
                         review-method.md     tables, verdicts, delta form
  prompts/campaign-prompt.template.md
  README.md  LICENSE
```

Template only, no filled in example, consistent with where `marketing-helper` ended up.

## Risks and open questions

**The marlin runtime and skill references. Blocking, verify first.** Every kit in the repo ships
`runtime: marlin`, but the repo README's conventions section says a marlin agent's skill must be
complete in its `SKILL.md` because `references/` are not fetched on that runtime, while both
existing kits instruct their agents to read references with `read_skill_resource`. This design
leans on five reference files. Verify against the runtime before writing any YAML. If the
convention note is accurate, either the references collapse into `SKILL.md` or the agents move to
a runtime that fetches them.

**Throughput.** Draft only caps output at the operator's daily minutes. Roughly five sends a day
at four minutes each. A campaign needing fifty sends a day is not served by this kit, and the
README should say so rather than let someone discover it in week two.

**Prospect supply.** The no guessed addresses rule plus the five part bar may starve the pipeline
for ICPs whose buyers are not publicly visible. Worth measuring in the first real campaign: if
the scout proposes fewer than a day's capacity for a week, the signals in the prompt are wrong or
the ICP is not reachable this way.

**The closed angle set.** Reply rate per angle only works if the set stays small and closed, and
the right set is not knowable before a real campaign runs. Expect to revise it in
`draft-method.md` after the first few weeks, and treat a sixth angle appearing as a signal that
the ICP is broader than the prompt says.

## Success criteria

- Someone copies the kit, writes a campaign prompt, and gets a usable draft the same day.
- Every draft in the pool carries a dated source URL for its trigger. No draft exists without one.
- A reply reported on Monday stops every pending bump for that company immediately.
- After four weeks, the Friday review can name which signal source produced replies and which
  did not, from its own records.
- No agent in the kit can send, post, spend or log in to anything.
