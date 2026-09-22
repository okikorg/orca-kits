# engineering-helper: works your issue backlog into reviewed draft PRs

A three-agent Orca pod that picks up issues from your repository the way you describe them, writes the change, reviews it properly, and emails you what happened to every one. You get draft pull requests with a review already on them. You merge, or you do not.

**Read this first, because it decides whether the kit is for you.** The pod never clones your repository. It reads and writes through the GitHub connected app, which means **nothing it produces has been executed**: no tests, no build, no linter, no type check. Every pull request says so in its body and lists what you should run. That makes this pod good at small, readable changes and honest about refusing the rest. It is not a replacement for a coding agent that runs on your machine with your test suite.

Merging is always yours. The pod opens drafts and comments on them; a person merges.

## What you get

| Agent | Role |
|---|---|
| `engineering-lead` (lead) | The batch. Turns "everything assigned to me" or "issues from the last week" into a list, hands each issue to the coder and then the reviewer, records every outcome, emails you the summary. Reads no code. |
| `engineering-coder` | The change. Reads the issue and the surrounding code, then either opens a draft pull request or skips the issue with a reason. Applies review feedback once. |
| `engineering-reviewer` | The check. Reads the diff and the changed files, leaves findings as review comments on the pull request, and verdicts `approve`, `changes` or `reject`. |

The method lives in the `engineering-method` skill, so the agents stay short and the rules are editable in one place.

## The loop, per issue

```
issue ─> coder reads the code
           ├─ skip, with a reason ──────────────> reported in your email
           └─ draft PR ─> reviewer comments ─> coder applies once ─> yours to merge
```

**One review round, one fix pass.** Then it stops and the pull request comes to you whatever state it is in, with the review thread visible. Two agents arguing a third time costs money and tells you less than the disagreement itself does.

## Why skipping is the feature

Because nothing is executed, the coder skips rather than guessing when an issue needs a test run to get right, needs a product decision nobody made, is too large to hold, is a question rather than a change, or touches something you listed as off limits.

A skip with a reason in your morning email is worth more than a plausible-looking pull request that nobody can trust. A batch where everything was skipped is reported as exactly that.

## What it needs

- **A repository prompt.** The repo, your issue query in your own words, what to never touch, your house rules. See `prompts/repo-prompt.template.md`.
- **The GitHub connected app**, required rather than optional. Without it there are no issues to read and no pull requests to open.
- **An email address on the workspace** so `email_me` reaches you.

## Start here

**1. Import the skill.** Skills > Import package > `skills/engineering-method/`. With the CLI: `orca skills import ./skills/engineering-method`.

**2. Create the agents.** Agents > Import YAML, once each for the three files in `agents/`. With the CLI: `orca agents create -f agents/<agent>.yaml`, once per file.

**3. Create the pod.** Pods > New pod: name `engineering-pod`, lead `engineering-lead`, members `engineering-coder`, `engineering-reviewer`. With the CLI: `orca pools create engineering-pod --member engineering-lead:lead --member engineering-coder --member engineering-reviewer`.

**4. Connect GitHub** from the lead's banner, and check the connection's scope covers the repository you want.

**5. Write your repository prompt.** Copy `prompts/repo-prompt.template.md`, fill it in, save it under **Prompts**, attach it to every session and scheduled run for that repo.

The sections that earn their keep are **Never touch** and **Always skip**. They are how you keep the pod away from the parts of your codebase where a blind change is expensive.

**6. Run one issue first.** Open a session on `engineering-pod` with the prompt attached:

> Run the engineering method. Job: issue. Issue: 214.

Read the pull request and the review before you automate anything. One issue tells you whether the pod understands your codebase; a batch of five just multiplies whatever it got wrong.

**7. Then a batch, on a schedule if you want one.** `Run the engineering method. Job: batch.` Start with a cap of 3 and raise it when the pull requests are consistently worth reading.

## What it will not do

- **It does not merge.** Ever. It also never pushes to your default branch, never force-pushes, never closes an issue, and never dismisses a review.
- **It does not run anything.** No tests, no build, no linter. Every pull request body carries the line saying so and the commands you should run.
- **It does not claim to have tested.** If you ever see the word "tested" in one of its pull requests, that is a bug worth reporting.
- **It does not silently ignore review feedback.** Where the coder disagrees, it replies on the comment saying why and leaves the code alone, so you can see the argument.
- **It does not open a second pull request for the same issue**, or review twice.

## What it is not good at

**Anything needing execution.** Races, flaky tests, performance work, anything where the proof is running it. Those get skipped, correctly.

**Large changes.** A refactor across fourteen files is exactly the thing a pod that cannot run tests should not attempt, and the coder is instructed to skip it.

**Repositories it cannot read fully.** If your connected app's scope does not cover the repo, issues come back as `unreachable` with the error, rather than a retry loop.

## Making it yours

**The repository prompt is the control surface.** When the pull requests disappoint, the fix is usually there: the issue query is too broad, the house rules are thin, the never-touch list is missing something, the cap is too high. Edit the prompt; nothing in the files needs touching.

**The skill is the method.** `SKILL.md` holds the prompt gate, the pool layout, the issue query, the per-issue protocol, the skip rules, the pull request body format and the review method. Edit it when the *method* is wrong, not when one repository differs.

**Cost.** All three agents ship on a strong model. The coder writes code a human will merge and the reviewer is the only verification that exists. The lead only resolves a query, delegates and writes an email, and it shipped on a cheap model first, but in testing that model kept answering a blocked run with a question instead of the `SKIPPED` line and the log entry, so it moved up. Swap the `model` field on any agent; check Dev pricing first, an unpriced id quarantines the run.

**Runtime.** Tested on `runtime: marlin`. The skill is deliberately complete in its own `SKILL.md` with no `references/` directory: on marlin the skill body is composed into the system prompt and there is no tool that fetches supporting files, so a method split across `references/` never reaches the model. On `pi`, `claude`, `codex` and `vercel` the agent has `activate_skill` and `read_skill_resource`, and splitting the method back out is safe there.

## One pod, several repositories

Everything is namespaced by slug: `run/<slug>/`, `work/<slug>/`, `reviews/<slug>/`. To work a second repository, write a second prompt with a different slug and attach it to its own sessions and schedules. No agent in this pod keeps memory; the outcomes file is the record.

## License

MIT, see the repository `LICENSE`.
