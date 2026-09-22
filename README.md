# Orca kits

Working agents you can copy into your own [Orca](https://orcapods.ai) workspace: the agent
documents, the skills they run on, and the prompts that point them at your product instead of
ours.

A **kit** is a snapshot of something already built and tested: one or more agents, the skills
they depend on, and optionally a pod and a schedule. Copying one installs editable assets in
your workspace, and from that moment they are ordinary agents you own, edit and delete like any
others. See [Shared kits](https://docs.orcapods.ai/concepts/kits).

## The kits

| Kit | What it does | Shape | Needs |
| --- | --- | --- | --- |
| [seo-helper](kits/seo-helper/) | Researches a keyword, writes one post, draws its own figures, opens a draft pull request on your repo | 2 agents, 1 skill, 1 pod | GitHub connected app |
| [marketing-helper](kits/marketing-helper/) | Analyses why a product is not signing anyone up, writes the plan to your next signup goal, then runs it: today's tasks every morning, the number every Friday, a review that changes the plan | 6 agents, 1 skill, 1 pod | Workspace email; GitHub connected app optional |
| [outreach-helper](kits/outreach-helper/) | Watches the public places your buyers show a problem, proposes the ones worth writing to with the evidence, drafts an opener and two bumps, tracks the sequence. You send | 4 agents, 1 skill, 1 pod | Workspace email |
| [engineering-helper](kits/engineering-helper/) | Picks up issues the way you describe them, writes the change, reviews it, and emails what happened to each. Draft PRs with a review already on them. You merge | 3 agents, 1 skill, 1 pod | GitHub connected app; workspace email |

## Published kits on Orca

Published kits can be copied into your workspace from the link.

| Kit | Copy it |
| --- | --- |
| [seo-helper](kits/seo-helper/) | https://app.orcapods.ai/kits/kit-utRCllawsrI2cqKdT |

Three ways to use one:

1. **Open the link.** It copies the kit in as editable agents you own. Nothing to install.
2. **Add it with the CLI.** `orca kit add <link>`
3. **Hand it to your coding agent** to adapt these files to your product, the way
   [Build it with your coding agent](https://docs.orcapods.ai/build-with-your-coding-agent)
   walks through.

If you do not have the CLI yet:

```bash
curl -fsSL https://orcapods.ai/install.sh | sh
orca login
```

## Install from the files

Copying gives you the kit as published. Install from the files instead when you want to change
it first: edit the YAML and the skill here, then install what you edited. Every kit has the same
shape, so the same commands install any of them.

```bash
git clone https://github.com/okikorg/orca-kits
cd orca-kits/kits/<kit>
orca skills import ./skills/<skill-name>
orca agents create -f agents/<agent>.yaml
orca pools create <pod> --member <lead>:lead --member <member>
```

Order matters: the agent document names its skill and the server checks that the skill exists.
Repeat the `agents create` line once per file in `agents/`. A kit with more than one agent also
needs a pod; the kit's own README gives the exact `pools create` line with its name, lead and
members. Schedules have no CLI command yet and are created in the dashboard.

Or do the whole thing in the dashboard: **Skills > Import package**, then **Agents > Import
YAML** once per file, then **Pods > New pod**.

## The prompt is the control surface

Every kit ships a prompt template you fill in, and some ship a filled-in example to calibrate
against. That prompt is where your facts live: your domain, your repo, your topic lanes, your
voice, the things the agents must never do.

Save it in Orca under **Prompts** and attach it to the session or the scheduled run. Orca may
present it to the agent in a block labelled `Context`; the kits here recognise that block and
read it as authoritative operator input.

This is deliberate, and it is why the same kit can serve two sites. Orca's Memory Bank is scoped
per agent profile rather than per project, so a kit that wrote your facts into memory would feed
both sites' facts into every later run with no way to tell which run they belong to. Keeping the
facts in the prompt is what makes one kit reusable. Each kit's README says exactly what it does
and does not remember.

## Conventions every kit here follows

Useful if you fork one, and the bar for anything added to this repo.

- **The method lives in a skill, the agent stays short.** An agent's system prompt says who it
  is and which section of the skill to read first. The rules live in `skills/<name>/SKILL.md`,
  so they are editable in one place and shared between agents.
- **A `marlin` agent's skill is complete in its `SKILL.md`.** On `runtime: marlin` the skill body
  is composed into the system prompt and there is no tool that fetches supporting files, so a
  method split across `references/` never reaches the model. On `pi`, `claude`, `codex` and
  `vercel` the agent has `activate_skill` and `read_skill_resource` and may split its method
  into `references/`. seo-helper still carries `references/` and was tested on `pi`; every
  other kit here ships on `marlin`, and each kit's README names the runtime it was tested on.
- **Nothing ships that publishes, sends or spends.** Kits write drafts, files and pull requests,
  and email the workspace owner. A person presses the button.
- **A blocked run stops cleanly.** Missing facts produce one `SKIPPED (<reason>)` line naming
  exactly what was missing, not a guess. An unattended agent that guesses its own target does
  the wrong work confidently.
- **Every run leaves a record**, because nobody watches the chat: a status line in the pod or the
  agent's own file, and one email.
- **No em dashes**, anywhere, in any copy an agent writes.

## Write your own

The fastest way is to ask the coding agent you already have open:
[Build it with your coding agent](https://docs.orcapods.ai/build-with-your-coding-agent) walks
through the prompt that produces good files, creating them with the CLI, testing on input with
traps in it, and the loop that fixes what is wrong. The by-hand version is
[Start here](https://docs.orcapods.ai/start-here).

To publish what you build as a link anyone can copy, see
[Shared kits](https://docs.orcapods.ai/concepts/kits). A kit link works for people who have never
heard of Orca.

## Contributing

Issues and pull requests welcome. A kit that lands here should run somewhere real, follow the
conventions above, carry its own README and its prompt files, and name the runtime it was tested
on.

## License

MIT, see [LICENSE](LICENSE). seo-helper is derived from the
[SEO Agent Pack](https://github.com/DigiHold/seo-agent-pack) by Nicolas Lecocq and carries its
own [LICENSE](kits/seo-helper/LICENSE) preserving that notice.
