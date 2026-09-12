# SEO helper: a scheduled agent that drafts blog posts as pull requests

A two-agent Orca pod that researches a keyword, writes one piece of content,
draws its own figures, and opens a **draft pull request** on your repo. It never
merges. Merging is publishing, and that stays with you.

It is built to run unattended on a schedule, but it works just as well as a
one-off: open a session, tell it what to write about, read the PR it opens.

## What you get

| Agent | Role |
|---|---|
| `seo-writer` (lead) | Picks the keyword through five gates, reads the current top 3 results, writes the piece against a blocking style checklist, briefs the media agent, and delivers the PR. |
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
- **A site prompt** describing your site. See below.

## Setup

**1. Import the skill.** Skills > Import package > `skills/seo-engine/`.

**2. Create the agents.** Agents > Import YAML, once each for
`agents/seo-writer.yaml` and `agents/seo-media.yaml`.

**3. Connect GitHub** from the writer's banner, and DataForSEO if you want
verified keyword data.

**4. Create the pool.** Pools > New pool: name `seo-pod`, lead `seo-writer`,
member `seo-media`. The two agents share files through the pool: the writer
leaves a brief in `sot/`, the media agent writes SVGs to `board/public/assets/`.

**5. Write your site prompt.** Copy `prompts/site-prompt.template.md`, fill it
in, and use it either way:

- Save it under **Prompts** in Orca and attach it to the session or the scheduled
  run. This is the setup to use for automations.
- Or paste it into the chat box as your message.

They are the same thing to the agent, so pick whichever suits. See
`prompts/site-prompt.example.md` for a filled-in version from a real site if you
want the level of detail that pays off.

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

- One draft PR labelled `seo-draft` on branch `seo/<slug>`, carrying the post,
  its SVG assets, and any registry or sitemap updates in the same branch.
- One email with the PR link.
- One line appended to `/agents/seo-writer/status.md`.

A blocked run leaves a `SKIPPED (<reason>)` line naming exactly what was missing
and opens no PR. That is deliberate: an unattended agent that guesses its own
target writes the wrong article to the wrong repo.

## Making it yours

**The site prompt is the control surface.** When a draft disappoints, the fix
usually belongs there rather than in the draft: voice, topic lanes, the file
conventions a post must follow, your punctuation and length rules. Edit the
prompt and the next run picks it up, with no redeploy.

**The skill is the method.** `writing-rules.md` holds the anti-slop machinery
(banned words and phrases, the humanizer pass, the self-review checklist),
`keyword-method.md` the five gates and the competitor pass, `media-method.md` the
figure rules. Edit these when the *method* is wrong, not when one site's
preferences differ. Anything site-specific belongs in the prompt.

**Cost.** The shipped models are the cheap end: roughly $0.20 per million input
tokens for the writer. Swap either agent's `model` field for a stronger one if
drafts need more editing than they save. That trade is usually worth making on
the writer, since editing time costs more than tokens.

## Credit

Built on the [SEO Agent Pack](https://github.com/DigiHold/seo-agent-pack) by
Nicolas Lecocq, MIT licensed. See `LICENSE`.
