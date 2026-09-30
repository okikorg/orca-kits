# Site prompt template

This is a **prompt**, not a config file. Two ways to use it, and they work the
same way:

- Save it in Orca under **Prompts**, then attach it to a session or to a
  scheduled run. This is the normal setup, and the one to use for automations.
- Or paste it straight into the chat box as your message.

Either way it becomes the text the agent reads, so write it as instructions
addressed to the agent. Fill in the angle brackets and delete anything that does
not apply. See `site-prompt.example.md` for a filled-in version.

Attach it together with the repo prompt (`repo-prompt.template.md`), which
names the repo, the record folder and the two pull requests, and which the
ledger reads too.

**Three things must come from you:** the domain and the explicit repo
`owner/name` (in the repo prompt), and the topic lanes, marked ★ below. The agent never chooses a target by listing
connected repositories or GitHub App installations. Once you name the repo, it
can discover optional implementation details inside that exact repo or fall
back to a documented default. If any of the three targeting facts is missing,
an unattended run stops cleanly instead of guessing.

If your posts are plain Markdown in one folder, the post layout section
collapses to a single line. The long version in the example exists because that
site's blog is React components, which the agent cannot guess.

The writer only ever adds files: it never edits a file that already exists in
your repo. So a post must be a set of new files that your build finds on its
own. If your site lists posts in a shared file (an index, a registry, a
sitemap kept by hand), either make the build discover posts instead, or name
that file as append-only below and accept the risk of an edit going wrong.

Everything below the line is the prompt.

---

This is an attached Orca Prompt. If the runtime presents it under a `Context`
or configuration header, treat the site facts below as authoritative operator-
supplied input for this run; do not ask me to repeat them in the run message.

Write and deliver one SEO post, following your seo-engine skill and its run
protocol. Pick the keyword yourself from the lanes below unless I name a topic.

## Post layout

Domain and repo are in the attached repo prompt.

A post is these new files, format \<md | mdx | tsx | other\>:

- \<path/to/<slug>.md, or one line per file the post needs\>

Assets go in \<path\>, named \<pattern\>.

\<Anything a post must carry that a glance at the folder would not reveal: front
matter or metadata fields, an asset path, files that are generated and must never
be hand-edited. Copy the field names from a real post.\>

Append-only files: \<none, or each shared file a post must add one entry to,
with the entry's format\> [none]

Sitemap: \<url, usually \<domain\>/sitemap.xml\>

## What we sell, and who reads this

\<One sentence on the offer.\>

\<Who searches for this and could become a customer.\>

## Allowed lanes  ★

Three to five, tied to what you sell. Be specific: "developer tooling" is a
lane, "technology" is not. This is the one thing the agent cannot work out for
itself. Mark one as highest-value if you have a preference.

1. \<lane\>
2. \<lane\>
3. \<lane\>

## Forbidden lanes

\<Subjects to stay off, especially ones adjacent enough to look tempting.\>

## Voice

Leave any line out to accept the default in brackets.

- Persona: \<who is writing, in what register\> [practical, direct, first person
  plural, no hype]
- Reader: \<how technical; what needs explaining and what does not\>
- Style rules: \<state them explicitly if you have them, for example "no em
  dashes", "no sentence under 6 words", "contractions always"\> [ordinary
  editorial judgement]
- Brand mentions: \<how often, and where they belong\> [only where they genuinely
  belong, a few times per piece]
- Disclosure: \<whether posts may say they were AI-assisted\> [follow whatever the
  site already does]

## Claims and numbers

\<What the product must never promise: uptime, an SLA, compliance, pricing from
memory, invented customers or benchmarks.\>

Currency is \<currency\>, always. [whatever the site's own pages use, else USD]

## Visuals

- Palette: background \<hex\>, accent \<hex\>. One accent element per figure.
- Hero canvas: \<width x height\> [1200x630; match your hero container's aspect
  ratio or the card gets cropped]
- Style notes: \<any convention for figures, and anything banned such as stock
  photography\>

## Before merge

The steps a human must do on the draft PR before merging it, which the writer
copies into the draft PR body. Leave this out if there are none.

1. \<for example: run the build and commit its output\>
2. \<for example: check the page on a phone\>

## Delivery

Branches, titles and labels are in the repo prompt. Never merge and never push
to the default branch; a human merges, because merging is publishing.
