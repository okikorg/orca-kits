# Repo prompt template

The facts the SEO writer and the SEO ledger must agree on: which repo, where
the pick records live, what the two pull requests are called, and where a
published post ends up. Save it once as an Orca Prompt and attach it to both
schedules, next to each agent's own prompt. Keeping these in one place means
the writer can never write records to a folder the ledger doesn't read.

If you only run the writer, you can paste this section into the site prompt
instead. Fill in the angle brackets; leave a line out to take the default in
square brackets.

Everything below the line is the prompt.

---

This is an attached Orca Prompt shared by the SEO writer and the SEO ledger.
If the runtime presents it under a `Context` or configuration header, treat
the facts below as authoritative operator-supplied input for this run; do not
ask me to repeat them in the run message.

## Repo

Repo: `<owner/name>`, default branch `<main>`. Domain: `<example.com>`.

A published post lives at `<https://example.com/blog/<slug>>`.

## Pick records

Pick records live in `<path/to/picks/>` [`.orca/seo/picks/`], one
`<slug>.json` per pick. Make sure your site's build ignores that folder.

## Pull requests

Each post is two pull requests, both from the default branch:

- The pick PR: branch `<seo-pick/><slug>`, titled `[SEO pick] <keyword>`,
  label `<seo-pick>`. It holds the pick record only, and a human merges it
  after reviewing the draft, whatever happened to the draft.
- The draft PR: branch `<seo-draft/><slug>`, titled `[SEO draft] <title>`,
  label `<seo-draft>`. It holds the post only, and a human merges it to
  publish or closes it to reject.

The ledger's own pull requests come from `seo-ledger/` branches and carry the
label `seo-ledger`.
