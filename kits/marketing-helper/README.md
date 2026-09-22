# marketing-helper: a pod that runs your go-to-market, one day at a time

A six-agent Orca pod for the moment a product is good and nobody is signing up. Point it at your product and the marketing you have already done, and it analyses why it stalled against the competitors that are winning, writes the plan to your next signup goal, and then runs that plan: today's tasks every weekday morning, the number every Friday, a review that changes the plan when the evidence says it should, and a record of every loose end so nothing quietly disappears.

It never publishes, posts, sends or spends. It writes, it counts, it reminds, and it emails you. You do the parts that need a person.

It is built to run unattended (two schedules and an email you read on your phone) and to be talked to (say `done T-014` to the dispatcher, ask the lead why a channel is worth keeping).

## What you get

| Agent | Role |
|---|---|
| `marketing-lead` (lead) | The strategist. Analyses the product, the past efforts, the competitors and their pricing; writes the plan and the founder decisions it waits on; applies the weekly review's changes; sends the morning and Friday emails. The only agent with memory, and the only one that writes strategy. |
| `marketing-dispatcher` | The day. Turns the plan into a backlog of tasks with checkable done lines, picks today's list inside your minute budget, marks things done when you say so, and answers "what is next". |
| `marketing-progress` | The plan's health. Burn-down per week, what is slipping, what is blocked on a decision you have not taken, and a forecast line that says whether the launches survive. |
| `marketing-metrics` | The number. Reach, clicks, signups, activations, spend, per week and per post, from the exports you drop plus public counters it can read. Writes `not supplied` rather than guessing. |
| `marketing-reviewer` | The Friday. What shipped, what it produced, a verdict per engine against the plan's own kill rules, and up to six proposed changes in a form the lead can apply mechanically. |
| `marketing-followups` | The loose ends. Every ask and promise a task leaves behind, with a due date, surfaced every morning until it is closed on evidence. |

The method lives in the `marketing-method` skill, so the agents stay short and the rules stay editable in one place.

## What it needs

- **A product prompt.** The one input that matters. It names the product, the slug, the goal, where your past marketing lives, which competitors to compare, what you will drop as metrics, and what the pod must never do. See `prompts/product-prompt.template.md`.
- **Web tools** (in `@default`, already in every shipped agent): how the lead reads competitor pricing pages and how the metrics agent reads public counters.
- **GitHub connected app** (optional). Lets the lead read your marketing docs and the metrics agent read star counts straight from your repo. Without it, drop the docs in the pod inbox instead; nothing else changes.
- **An email address on the workspace** so `email_me` reaches you. That is where the morning list and the Friday review arrive.

## Start here

**1. Import the skill.** Skills > Import package > `skills/marketing-method/`. With the CLI: `orca skills import ./skills/marketing-method`.

**2. Create the agents.** Agents > Import YAML, once each for the six files in `agents/`. With the CLI: `orca agents create -f agents/<agent>.yaml`, once per file.

**3. Create the pod.** Pods > New pod: name `marketing-pod`, lead `marketing-lead`, members `marketing-dispatcher`, `marketing-progress`, `marketing-metrics`, `marketing-reviewer`, `marketing-followups`. With the CLI: `orca pools create marketing-pod --member marketing-lead:lead --member marketing-dispatcher --member marketing-progress --member marketing-metrics --member marketing-reviewer --member marketing-followups`. The agents hand work to each other through the pod's shared files; the layout is in `skills/marketing-method/references/pool-layout.md`.

**4. Connect GitHub** from the lead's banner, if your marketing docs live in a repo.

**5. Write your product prompt.** Copy `prompts/product-prompt.template.md`, fill it in, save it under **Prompts**. Attach it to every session and every scheduled run for that product.

Internally, Orca may present a saved Prompt to the agent in a block labelled `Context` and describe it as configuration rather than chat instructions. The shipped agents and skill recognise that block as the attached Prompt, read it before the prompt gate, and use its body as authoritative product facts. You do not need to repeat those facts in a scheduled run's short trigger.

**6. Analyse.** Open a session on `marketing-pod` with the prompt attached and say `Run the marketing method. Job: analyse.` It reads your marketing history, your live site, your competitors and the category's pricing, and leaves `strategy/<slug>/analysis.md` plus an email with the five lines that matter. Read it before you plan; it is where the argument for the plan lives.

**7. Plan.** Same session or a new one: `Run the marketing method. Job: plan.` It writes the plan, the decisions it needs from you, and seeds the backlog through the dispatcher. The email carries the thesis, the math, the decisions waiting and the first day's tasks.

**8. Take the decisions.** Open `strategy/<slug>/decisions.md` (or read them in the email). Answer them in an attended session on `marketing-lead`: `Run the marketing method. Job: replan. Product: <slug>.` then say what you decided. Every engine that was waiting unblocks in the same run.

**9. Turn on the two schedules.** Point one at the pod each weekday morning with `Run the marketing method. Job: daily.` and one at Friday afternoon with `Run the marketing method. Job: weekly.`, both with the product prompt attached. Create them under Schedules in the dashboard (there is no CLI command for schedules yet). When this kit is copied from a published link they arrive **stopped**, which is deliberate: nothing spends on a schedule its new owner has not seen. Start them when the plan is the one you want to run.

**10. Work the day.** The morning email is the day. Do the tasks, then tell the dispatcher: open a session on `marketing-dispatcher` and say `done T-003 T-004`, or `block T-007 on D-02`, or just `next`. Drop anything else the pod should know into `/pools/marketing-pod/inbox/<slug>/notes/` as a note; every agent reads it.

## Working a plan you already have

If you arrive with a plan (a document, an artifact, a tracker) rather than a blank page, put it where the lead will read it: drop the file in `/pools/marketing-pod/inbox/<slug>/docs/`, or name its repo path in the product prompt under "Prior analysis or plan to read first". Then run `analyse` anyway. The lead verifies the plan's claims against the live product and the competitors rather than trusting them, and `plan` turns what survives into weeks, tasks and kill rules. A plan nobody turned into Monday morning is the failure mode this pod exists to fix.

## One pod, several products

Everything the pod writes is namespaced by the product slug: `strategy/<slug>/`, `tasks/<slug>/`, `metrics/<slug>/`, and every memory the lead saves starts with `[product: <slug>]`. To run a second product, write a second product prompt with a different slug and attach it to its own sessions and schedules. Nothing else changes, and the two never mix: the lead recalls with the tag and discards everything tagged otherwise.

This is also why the lead is the only agent with memory. Orca's Memory Bank is scoped per agent profile, so an untagged bank serving two products would feed both sets of facts into every run. The tag plus the recall filter is what makes one bank safe; the rules are in `skills/marketing-method/references/memory-rules.md`.

## What it will not do

- **It does not publish, post, reply, send or spend.** It writes drafts and tasks; you press the button. The only thing it sends is `email_me` to the workspace owner.
- **It does not invent numbers.** A metric with no source is written `not supplied`. An engine whose number is missing gets the verdict `unread`, never a flattering guess.
- **It does not mark your work done for you.** A task owned by the founder is done when you say so or when the evidence its done line names exists.
- **It does not quietly change the plan.** Anything that opens or closes a channel, spends money, moves a launch date or makes a public commitment goes to `decisions.md` and waits for you.

## What a healthy week leaves behind

- Five morning emails, each a list short enough to do in your time budget, with the follow-ups due that day.
- A backlog whose ids never move, so `done T-014` still means something in a month.
- One row in the metrics table with a source in every cell, or an honest `not supplied`.
- One review file: what shipped, what it produced, a verdict per engine, up to six proposed changes.
- A plan amended in place, with a dated line saying what changed and why.
- A follow-ups table where nothing has gone quiet.

## Making it yours

**The product prompt is the control surface.** When the plan or the tasks disappoint, the fix usually belongs there: the goal, the time budget, the competitors, the channels you have ruled out, the metrics you can actually supply, the register the drafts must be written in. Edit the prompt and run `replan`.

**The skill is the method.** `analysis-method.md` holds what an analysis must contain, `planning-method.md` the shape of a plan, `task-method.md` the task anatomy and how today is chosen, `metrics-method.md` the attribution rules, `review-method.md` the delta form, `followup-method.md` what counts as a loose end, `memory-rules.md` the multi-product rules. Edit these when the *method* is wrong, not when one product differs.

**Cost.** The lead, the metrics agent and the reviewer ship on a strong model because a wrong number or a wrong verdict costs more than tokens. The dispatcher, the progress agent and the follow-ups agent ship on a cheap one; their work is counting and copying, and the lead reads it. Swap the `model` field on any agent; check Dev pricing first, an unpriced id quarantines the run.

## Credit

Built from a real go-to-market review and the plan it produced. MIT licensed, see the repository `LICENSE`.

**Runtime.** Tested on `runtime: marlin`. The method is long, so it is split into `references/` and each agent loads only the section its job needs with `read_skill_resource`; that works on marlin as on the other runtimes, the same way seo-helper loads its references.
