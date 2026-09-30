# Ledger prompt template

Copy this file, fill every angle-bracket value, save it as an Orca Prompt and
attach it to the seo-ledger schedule together with the repo prompt from the
seo-helper kit (`kits/seo-helper/prompts/repo-prompt.template.md`), the same
one the writer's schedule carries. The repo prompt names the repo, the record
folder, the pick branch prefix and the published URL pattern; this one holds
what only the ledger needs. The agent and its skill carry no site facts.

---

This is an attached Orca Prompt. If the runtime presents it under a `Context`
or configuration header, treat the facts below as authoritative operator-
supplied input for this run; do not ask me to repeat them in the run message.

Keep the pick ledger current, following your seo-ledger skill and its run
protocol. The repo, record folder, pull request names and published URL
pattern are in the attached repo prompt.

## Search settings

Site domain: `<example.com>`. Rank against Google organic, location
`<location name or code>`, language `<en>`.

## Cadences

- Ranking: every `<7>` days for the first `<84>` days after a post merges,
  then every `<30>` days. The first pass waits three days after the merge.
- Review: every `<30>` days, once at least `<8>` records are published or
  rejected.
- Reminder: a pick PR still open `<3>` days after it was opened goes in the
  email's Needs you list, once.

## Rules repo (optional)

Leave this section out if the writer's rules live only as a skill in your
Orca workspace. Reviews then stay in the record folder and arrive by email,
and you apply them to the skill yourself.

Include it if you keep the writer's rules as a file in a repo:

The writer's keyword rules live in `<owner>/<rules-repo>` at
`<path/to/SKILL.md>`, in the section headed `<## The keyword method>`.
Each review that proposes a change also opens a draft pull request against
that repo changing only that section.

## Pool

Pool name: `<seo-pod>`. Post to its board only when a run stopped.
