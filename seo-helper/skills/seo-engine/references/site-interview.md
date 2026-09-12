# Site interview: the last resort

**This file exists to be unused.** Reach it only when the prompt gate in
`run-protocol.md` has already established that the prompt is missing the domain,
the target repo owner/name, or the topic lanes. Those are targeting facts: they
come from the operator, never from connected-account enumeration. The whole
method below is about asking once and leaving an unattended run stopped cleanly.

## Order of resort, strictly

Work down this list. Only what survives every step is a question.

**1. Take it from what you already have.** Re-read the current run message and
every attached Prompt/context block in full. Orca may label an attached Prompt
as `Context` and describe it as configuration rather than conversation
instructions; its site facts are still authoritative operator input. Never ask
for a fact already present in that block. The available input often carries
more than first appears: a request like "write about
connection pooling for example.com, PR into acme/website" supplies the domain,
the repo and a topic lane in one sentence. Never ask for something already
stated.

**2. Discover optional details inside the named repo.** Only when the prompt
already supplies an explicit `owner/name`, use the GitHub connected app to read
that exact repo. Most non-targeting site details are sitting there, and reading
them is faster and more accurate than asking a human to describe them:

| Fact | How to discover it rather than ask |
|---|---|
| Content path and format | List the repo root, find the content directory, open one or two recent posts. Their extension and front matter *are* the format. |
| Registry or index files | The same posts will import from or register in one. Follow the reference. |
| Asset path | Where existing posts' images live. |
| Sitemap URL | Try `<domain>/sitemap.xml` and confirm it resolves. |
| Existing content | The sitemap, the content directory, and open pull requests. |
| Default branch | Query the named `owner/name` directly. |

Confirm what you discovered in your summary rather than asking permission for it
first. Being wrong about a discovered fact is cheap and visible; a question costs
a round trip every time.

Do not list repositories, accounts, or GitHub App installations to find a target.
Never call `GITHUB_LIST_APP_INSTALLATIONS` or
`GITHUB_LIST_ACCESSIBLE_REPOSITORIES`. If `owner/name` is missing, it remains a
question; an accessible repo is not proof that it is the intended repo.

**3. Fall back to a documented default.** These are never worth a question. Use
the default, state that you used it, and let the operator correct it later in the
prompt:

- **Voice**: practical and direct, first person plural, no hype, contractions.
- **Punctuation and sentence-length house rules**: none beyond ordinary editorial
  judgement (see `writing-rules.md`).
- **Currency**: whatever the site's own pages already use, else USD.
- **Publish policy**: draft pull request, always, never merged by you.
- **Visuals**: the site's own background and accent colours if you can read them
  from its CSS or an existing asset, else a neutral dark palette with one accent.
  Hero canvas 1200x630 unless the site's hero container implies otherwise.

## What is actually worth asking

After the steps above, at most three things can still be blocking. Ask for
exactly those, and only the ones still missing:

1. **The domain.** Which site is this for?
2. **The repo.** The explicit `owner/name` for the repo that holds the content.
3. **The topic lanes.** Three to five subject areas tied to what the business
   sells, and anything to avoid. This is editorial intent and cannot be
   discovered: it is the one genuinely irreducible question.

Ask them in **one message**, as a short numbered list, with your discovered
defaults shown so the operator only has to correct what is wrong. Do not
interview conversationally, do not ask follow-ups one at a time, and do not ask
about anything on the defaults list above.

## Send the question and the stop line together

You cannot reliably tell whether a human is reading. Handle both cases in one
move: ask the question **and** write the status line
`SKIPPED (insufficient site prompt; asked for <the missing items>)`.

An attended run gets answered and continues. An unattended run leaves a status
line naming exactly what was missing, which is the same clean stop the prompt
gate would have produced, rather than hanging on a question nobody will read.

## Close the loop so it never happens twice

An interview that does not outlive its own run has solved today and nothing
else. You cannot fix that yourself, so hand the operator what they need to fix
it permanently.

### Hand back a reusable prompt

End the run by handing back a **complete site prompt**, formatted ready to save
under Prompts and attach to future runs (see the shipped
`prompts/site-prompt.template.md` for the shape), combining what you were told,
what you discovered, and the defaults you applied.

### Say plainly that it does not persist

Then tell them, in as many words, that **nothing from this session carries over**:

> These answers live in this session only. I do not remember them. If you start a
> new session, or a scheduled run fires, I will ask for all of this again unless
> the full site prompt is in front of me. Save the prompt above under Prompts and
> attach it to the session or scheduled run, or paste it in at the start of every
> new session.

Do not soften this and do not skip it because the answers arrived smoothly. An
operator who assumes you remembered is an operator whose next scheduled run stops
with the same three questions.

**Never write the prompt to a file, and never save it to memory.** It is the
operator's input. An agent that persists one site's facts has quietly welded
itself to that site, and the next run for a different repo inherits the wrong
domain, the wrong lanes and the wrong palette with no way to tell which is
current.
