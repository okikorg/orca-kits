# SEO helper: a scheduled agent that drafts blog posts as pull requests

A two-agent Orca pod that researches a keyword, writes one piece of content,
draws its own figures, and opens **two pull requests** on your repo: a pick PR
holding why it chose that keyword, and a draft PR holding the post. It never
merges. Merging is publishing, and that stays with you.

It is built to run unattended on a schedule, but it works just as well as a
one-off: open a session, tell it what to write about, review the PRs it opens.

## What you get

| Agent | Role |
|---|---|
| `seo-writer` (lead) | Picks the keyword through five gates, reads the current top 3 results, writes the piece against a blocking style checklist, briefs the media agent, and opens the pick PR and the draft PR. |
| `seo-media` (member) | Authors the figures as standalone SVGs: typographic hero cards and diagrams of the literal subject. No stock images, no AI-photo look. |

The method lives in the `seo-engine` skill, so the agents stay short and the
rules stay editable in one place.

## What it needs

- **GitHub connected app** (required). Connect it on the account that owns your
  content repo. Without it the run stops at pre-flight, because there is nowhere
  to deliver.
- **DataForSEO connected app** (optional). Connected gives verified search volume
  and difficulty. Not connected drops to heuristic mode, judged from the live
  results page and labelled as such in every PR body. The workflow is fully
  usable without it.
- **A repo prompt and a site prompt** describing your repo and your site. See below.

## Setup

**1. Import the skill.** Skills > Import package > `skills/seo-engine/`.

**2. Create the agents.** Agents > Import YAML, once each for
`agents/seo-writer.yaml` and `agents/seo-media.yaml`.

**3. Connect GitHub** from the writer's banner, and DataForSEO if you want
verified keyword data.

**4. Create the pool.** Pools > New pool: name `seo-pod`, lead `seo-writer`,
member `seo-media`. The two agents share files through the pool: the writer
leaves a brief in `sot/`, the media agent writes SVGs to `board/public/assets/`.

**5. Write your prompts.** Two, both saved under **Prompts** in Orca and
attached to the session or scheduled run:

- The **repo prompt** (`prompts/repo-prompt.template.md`): the repo, where pick
  records live, and what the two pull requests are called. If you also run the
  seo-ledger kit, attach the same repo prompt to its schedule, so the two
  agents can never disagree about a folder or a branch name.
- The **site prompt** (`prompts/site-prompt.template.md`): what a post looks
  like in your repo, your topic lanes, voice, visuals, and the steps a human
  does before merging a draft.

You can also paste them into the chat box as your message; that is the same
thing to the agent. See `prompts/site-prompt.example.md` for a filled-in site
prompt from a real site if you want the level of detail that pays off.

Internally, Orca may present a saved Prompt to the agent in a block labelled
`Context` and describe it as configuration rather than chat instructions. The
shipped agent and skill explicitly recognize that block as the attached Prompt,
read it before the prompt gate, and use its body as authoritative site facts.
You do not need to repeat those facts in the scheduled run's short trigger.

You do not have to fill in everything, but three targeting facts must be present:
**your domain, the explicit repo `owner/name`, and your topic lanes.** The agent
never chooses a target by enumerating connected repositories or GitHub App
installations. Once you name the repo, it can discover optional implementation
details inside that exact repo: the default branch, content conventions,
registries, asset paths, and build checks.

For a one-off run you can skip the template and just say what you want: "write
about connection pooling for example.com, PR into acme/website" carries a domain,
a repo and a lane in one sentence. That text applies only to that run; attach a
saved site prompt to every scheduled run so later sessions receive the same
facts.

**6. Run it.** Open a session on the pool and ask for a post, or point a
scheduled run at it. A trigger with no topic is the normal scheduled case:
the agent picks a keyword from your lanes.

## What it does not remember

**Nothing carries over between sessions.** The agent has no memory of earlier
runs, and that is deliberate rather than a gap to fill.

Orca's Memory Bank is scoped per agent profile, not per session and not per
repo. If these agents drove two sites, both sets of facts would land in the same
bank and both would be fed into every later run, with nothing to tell the agent
which one the current run is for. It would open each run holding two domains and
two sets of lanes. Keeping the facts in the prompt is what lets one pod serve
several sites without them bleeding into each other.

The practical consequence: **whatever the run needs must be in operator input
in front of it.** Save your filled-in site prompt under Prompts and attach it to
the session or scheduled run, and every run starts complete even when the
visible scheduled trigger is only `Begin your scheduled run.` If you interview
the agent by hand in a session instead, those answers die with that session. It
will say so when it happens, and it hands you back a ready-to-save prompt so the
next session does not repeat the exercise.

## What a healthy run leaves behind

- A **pick PR** on `seo-pick/<slug>` holding one file, the pick record: the
  keyword, the candidates it weighed, the ones it rejected and why, and why the
  winner won. Its body is the review checklist.
- A **draft PR** on `seo-draft/<slug>` holding the post, its figures and its
  metadata, all as new files. Its body points back to the pick PR.
- One email with both links.
- One line appended to `/agents/seo-writer/status.md`.

If a run fails after the pick PR, the PRs say so: `STOPPED` in the draft PR's
Self-review, or, when the draft never opened, a pick PR whose steps say so. A
blocked run that never got that far leaves a `SKIPPED (<reason>)` line naming
exactly what was missing and opens nothing. That is deliberate: an unattended
agent that guesses its own target writes the wrong article to the wrong repo.

## Reviewing a post

Start at the pick PR the email links. Its body lists three steps, and they only
go one way:

1. Review the draft PR. Do its "Before merge" steps, then merge it to publish or
   close it to reject.
2. Back on the pick PR, fill the record's `review` block: the decision
   (`published`, `rejected` or `not-written`), the reason, whether the keyword
   pick itself was sound, and one entry per thing you had to fix.
3. Merge the pick PR. Always, whatever happened to the draft.

That is the end of your part. Every pick then sits in one folder on your default
branch, published or not, which is what the writer checks before picking again,
and what the seo-ledger kit reads to track rankings and propose better keyword
rules.

### Only new files

The writer never edits a file that already exists in your repo. A post is a set
of new files, so two drafts can't collide and a draft can't overwrite anything
already published. If your site lists posts in a shared file by hand, make the
build discover them instead, or name that file as append-only in the site
prompt, and the writer adds its line and proves it deleted nothing.

## Making it yours

**The prompts are the control surface.** When a draft disappoints, the fix
usually belongs there rather than in the draft: voice, topic lanes, the file
conventions a post must follow, your punctuation and length rules. Edit the
prompt and the next run picks it up, with no redeploy.

**The skill is the method.** `SKILL.md` holds it all, one section per step: the
Writing rules section has the anti-slop machinery (banned words and phrases, the
humanizer pass, the self-review checklist), the keyword method the five gates and
the competitor pass, the media method the figure rules. Edit these when the *method* is wrong, not when one site's
preferences differ. Anything site-specific belongs in the prompt.

**Cost.** The shipped models are the cheap end: roughly $0.20 per million input
tokens for the writer. Swap either agent's `model` field for a stronger one if
drafts need more editing than they save. That trade is usually worth making on
the writer, since editing time costs more than tokens.

## Credit

Built on the [SEO Agent Pack](https://github.com/DigiHold/seo-agent-pack) by
Nicolas Lecocq, MIT licensed. See `LICENSE`.
