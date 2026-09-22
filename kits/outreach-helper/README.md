# outreach-helper: cold outreach that has a reason to exist

A four-agent Orca pod for outreach you would actually send. It watches the public places where your buyers show the problem you solve, proposes the ones worth writing to with the evidence attached, researches each one, and writes an opener and two bumps. You read the draft, paste it, send it, and tell the pod what came back.

Nothing here sends. The pod drafts, counts and reminds; a person presses the button. That is deliberate: deliverability and your domain's reputation stay with the human whose name is on the message.

The rule the whole kit turns on: **no trigger, no prospect.** If the scout cannot name a dated public thing a company just did, the row never enters the pipeline. That is what separates this from mail merge, and it is mechanically checkable in every draft file.

## What you get

| Agent | Role |
|---|---|
| `outreach-lead` (lead) | The pipeline and the day. Runs the two schedules, merges proposals, picks who you contact today inside your minute budget, applies what you report, emails you. Writes no messages. |
| `outreach-scout` | The signals. Sweeps the sources you named against watermarks so a daily sweep is cheap, qualifies against five bars, proposes prospects with the artifact that triggered each one. |
| `outreach-writer` | The message. Time-boxed research on one prospect, then an opener and two bumps in your voice, built on the trigger. |
| `outreach-reviewer` | The Friday. Reply rate per signal source and per angle, verdicts, and at most six deltas in a form the lead can apply without interpreting. |

The method lives in the `outreach-method` skill, so the agents stay short and the rules are editable in one place.

## What it needs

- **A campaign prompt.** The one input that matters: the offer, who qualifies, the signal sources and their trigger phrases, your voice, your minute budget, who to never contact. See `prompts/campaign-prompt.template.md`.
- **Web tools** (in `@default`, already in every shipped agent). That is the whole toolkit for sweeping. Nothing logs in to anything.
- **An email address on the workspace** so `email_me` reaches you. The morning list and the Friday review arrive there.

No data vendor, no mailbox connection, no CRM.

## Start here

**1. Import the skill.** Skills > Import package > `skills/outreach-method/`. With the CLI: `orca skills import ./skills/outreach-method`.

**2. Create the agents.** Agents > Import YAML, once each for the four files in `agents/`. With the CLI: `orca agents create -f agents/<agent>.yaml`, once per file.

**3. Create the pod.** Pods > New pod: name `outreach-pod`, lead `outreach-lead`, members `outreach-scout`, `outreach-writer`, `outreach-reviewer`. With the CLI: `orca pools create outreach-pod --member outreach-lead:lead --member outreach-scout --member outreach-writer --member outreach-reviewer`.

**4. Write your campaign prompt.** Copy `prompts/campaign-prompt.template.md`, fill it in, save it under **Prompts**. Attach it to every session and every scheduled run for that campaign.

The signals section is the part worth the time. "r/AI_Agents" is not a signal. "r/AI_Agents, posts asking how to run an agent on a schedule" is. The difference decides whether the drafts have anything to open on.

**5. Sweep once, attended.** Open a session on `outreach-pod` with the prompt attached and say `Run the outreach method. Job: sweep.` Read `signals/<slug>/proposed.md` before you automate anything. If the proposals are wrong, the signals in your prompt are wrong, and no amount of drafting fixes that.

**6. Turn on the two schedules.** One at the pod each weekday morning with `Run the outreach method. Job: daily.` and one on Friday afternoon with `Run the outreach method. Job: weekly.`, both with the campaign prompt attached. Start them when the proposals look right.

**7. Work the day.** The morning email is the day. Open each draft, paste what you like, send it from your own client. Then tell the lead: `sent P-014 P-021`. When someone answers: `P-014 replied, wants a demo`. That one line stops every pending bump for that company.

## What you say to it

In a session on `outreach-lead`, in whatever words come naturally:

| You say | What happens |
|---|---|
| `sent P-014 P-021` | marked sent, first bump scheduled |
| `P-014 replied, wants a demo` | sequence stops for the whole company, closed as a meeting |
| `P-014 no` | closed, and the company is suppressed for good |
| `P-014 not now, after Q1` | closed with a revisit date that comes back in a morning email |
| `bounced P-014` | dropped, company suppressed, and the route type is noted so the scout stops trusting it |
| `drop P-015 wrong company` | dropped with your reason kept |
| `redraft P-014 too long` | rewritten, same id, same evidence |
| `never acme.dev` | permanent suppression |
| `more` | more drafts today, capacity permitting |
| `next` | today's list again |

## What it will not do

- **It does not send, post, reply or spend.** The only thing it sends is `email_me` to you.
- **It does not guess email addresses.** No pattern-matching a name into an address, no verifier services. A route is published, or the row is marked `no-route` and left to you. Guessed addresses bounce, bounces burn your domain, and you are the sender.
- **It does not write a third bump.** Two, then the sequence is cold. Ask for a third and it will tell you the sequence is finished and offer to find a fresh trigger instead.
- **It does not keep emailing someone who replied.** A reply stops the sequence for that person and everyone else at that company, in the same run you report it.
- **It does not invent a reason to write to someone.** If the trigger artifact has gone dead, the draft comes back marked `TRIGGER DEAD` rather than with a manufactured opener.

## What it is not good at

Worth knowing before you install it rather than in week two.

**Volume.** Draft-only means your minutes are the ceiling. At the default 20 minutes and 4 minutes a send, that is about five sends a day. A campaign that needs fifty a day is not this kit.

**Buyers who are invisible.** No trigger and no guessed addresses together mean some ICPs simply cannot be reached this way. The tell is the scout proposing fewer than a day's capacity for a week straight. That means your signals are wrong or your buyers do not post in public, and the honest answer may be that outreach is the wrong channel for them.

**Named individuals.** Many triggers name a company but not a person. Those rows carry `who: not supplied` and the draft is written to the company. That converts worse, and it is visible in the reviewer's per-source table.

## Making it yours

**The campaign prompt is the control surface.** When the drafts disappoint, the fix is almost always there: the trigger phrases are too loose, the ask is too big, the ICP does not exclude enough, the voice section is thin. Edit the prompt; nothing in the files needs touching.

**The skill is the method.** `SKILL.md` holds the prompt gate, the pool layout, the pipeline states, the five qualification bars, the draft anatomy and the review form. Edit it when the *method* is wrong, not when one campaign differs.

**Cost.** The scout, the writer and the reviewer ship on a strong model; the lead ships on a cheap one. That inverts `marketing-helper` deliberately. This lead merges rows, counts minutes and writes a list, while the judgement sits in what qualifies and what gets written, which are the two places where being cheap costs you a reply. Swap the `model` field on any agent; check Dev pricing first, an unpriced id quarantines the run.

**Runtime.** Tested on `runtime: marlin`. The skill is complete in its own `SKILL.md` with no `references/` directory because the method is short enough to carry whole and one file is easier to edit. Splitting it into `references/` is safe on every runtime, marlin included: the agent loads them on demand with `read_skill_resource`, the way seo-helper and marketing-helper do.

## One pod, several campaigns

Everything is namespaced by the campaign slug: `campaign/<slug>/`, `prospects/<slug>/`, `drafts/<slug>/`. To run a second campaign, write a second prompt with a different slug and attach it to its own sessions and schedules. No agent in this pod keeps memory; the pipeline file is the record, which means two campaigns cannot contaminate each other.

## License

MIT, see the repository `LICENSE`.
