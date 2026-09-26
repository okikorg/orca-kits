# Ledger prompt template

Copy this file, fill every angle-bracket value, save it as an Orca Prompt and
attach it to the seo-ledger schedule. The agent and its skill carry no site
facts; this prompt is the only place they live.

---

This is an attached Orca Prompt. If the runtime presents it under a `Context`
or configuration header, treat the facts below as authoritative operator-
supplied input for this run; do not ask me to repeat them in the run message.

Keep the pick ledger current, following your seo-ledger skill and its run
protocol.

## Repo

Repo: `<owner>/<name>`, default branch `<main>`. Draft pull requests carry the
label `<seo-draft>` and come from branches named `<seo/><slug>`.

## Record folder

The writer writes its pick record to `<path/to/picks/><slug>.json` on each
branch, before the article. Read that folder on the default branch first and
complete what is there. It is the only place you commit to. The index lives
at `<path/to/picks/>_index.json`. Use the same path in the writer's site
prompt; when neither prompt names one, both agents use `.orca/seo/picks/`.

## PR body spec (optional)

Only needed for drafts opened before the writer kept pick records. Leave it
out when every draft has one. The writer's pull request body used these
headings and fields, in this order:

```
## SEO draft
**Primary keyword:** <keyword>
**Lane:** <number>
**Mode:** verified | heuristic
**Intent:** informational | commercial
**Volume:** <number or n/a>
**Difficulty:** <number or n/a>
**Differentiation:** <one sentence>

## Competitor pass
<one line per page: URL, what it covers>

## Rejected keywords
<one line per keyword: keyword, the gate it failed>

## Self-review
<one line per item>

## Files changed
<one path per line>
```

Anything after those sections is ignored.

## Search settings

Site domain: `<example.com>`. Rank against Google organic, location
`<location name or code>`, language `<en>`.

## Rules repo (optional)

Leave this section out if the writer's rules live only as a skill in your
Orca workspace. Reviews then stay in the record folder and arrive by email,
and you apply them to the skill yourself.

Include it if you keep the writer's rules as a file in a repo:

The writer's keyword rules live in `<owner>/<rules-repo>` at
`<path/to/SKILL.md>`, in the section headed `<## The keyword method>`.
Each review also opens a draft pull request against that repo changing only
that section.

## Cadences

Ranks every `<7>` days, for merged records at least three days old. Review
every `<30>` days, once at least `<8>` records have an outcome of merged or
closed.

## Pool

Pool name: `<seo-pod>`. Post to its board only when a human has to act.
