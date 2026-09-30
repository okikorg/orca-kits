# Example site prompt: orcapods.ai

A filled-in example of `site-prompt.template.md`, from a site this workflow runs
against in production. It is attached next to that site's repo prompt, which
names `okikorg/orca`, the record folder `landing/seo/picks/` and the
`seo-pick/` and `seo-draft/` branches. Use it to see the level of detail that pays off, then
write your own. Do not attach this one: it will send your run at someone else's
repo.

Everything below the line is the prompt itself.

---

This is an attached Orca Prompt. If the runtime presents it under a `Context`
or configuration header, treat the site facts below as authoritative operator-
supplied input for this run; do not ask me to repeat them in the run message.

Write and deliver one SEO post, following your seo-engine skill and its run
protocol. Pick the keyword yourself from the lanes below unless I name a topic.

## Post layout

Domain orcapods.ai, repo okikorg/orca (see the repo prompt).

Posts are **not Markdown or MDX**. The blog is a Vite React multi-page app and
each post is a TSX component. **A post is one new folder,
`landing/src/blog/posts/<slug>/`**, which the build finds on its own. Never
edit an existing file; there are no append-only files on this site.

1. `meta.ts`, committed first, relative imports only: `export const post:
   BlogPostMeta` with `slug` and `href` matching the folder (SEO posts set
   `featured: false`, `category: 'Technical'`, `heroVersion: 1`, and both
   `heroBarLabel` and `heroBarTag`), and `export const heroCard:
   BlogHeroCard` for the hero PNG.
2. `article.tsx`: `import { post } from './meta'`, a default-exported
   component built with `BlogArticleTemplate`, including TOC, FAQ JSON-LD and
   `sourceNote`. Use `BlogFigureLive` and `BlogCodeBlock` for figures.

Figures go in `landing/public/blog/<slug>-fig-<name>.svg`.

Read `landing/src/blog/README.md` before you start and follow it. **Never
hand-edit generated HTML, the sitemap, or og and title tags.** The build
writes them from each post's `meta.ts`.

Sitemap: https://orcapods.ai/sitemap.xml

## What we sell, and who reads this

Orca runs AI agents in isolated cloud sandboxes on a schedule, metered to the
micro-dollar, so teams do not need a machine that stays on or hand-rolled safety
rails.

Readers are developers, founders and platform engineers who build agents with
Claude Code, the Agent SDK, Codex, LangGraph or MCP, and need to run them
headless, scheduled and safely.

## Allowed lanes

1. Running AI agents in production: cost, reliability, failure modes, spend caps.
2. Headless and scheduled coding agents: `claude -p`, cron and launchd, overnight
   runs. **This is the highest-value lane.**
3. Agent sandboxing and isolation.
4. Agent cost control and metering: token costs, MCP schema overhead, per-run
   billing.
5. Comparisons and alternatives for agent runtimes.

## Forbidden lanes

Generic what-is-AI explainers, prompt-engineering listicles, AI news, model
training or GPU content, consumer chatbot and creator-tool content, crypto or
trading bots, growth-hacking, SEO about SEO. Never name outreach prospects or
customers without written permission.

## Voice

An engineer who runs the platform. First person plural, building in public,
direct and concrete, honest about failures and costs.

The reader is a developer: sandbox, cron, token and API need no explanation.
Orca-specific terms get one plain clause on first use.

Hard style rules:

- No hype, no marketing adjectives, no exclamation marks.
- Contractions always.
- **Zero em dashes and en dashes anywhere.**
- No sentence under 6 words.
- No run-ons. Split anything chaining three or more clauses. Roughly 30 words is
  the ceiling.
- Mention Orca only where it belongs, 2 to 5 times per piece. No bespoke CTA
  block; the template renders the CTA.

## Claims and numbers

Never invent customers, case studies, usage numbers or benchmarks. Use verified
numbers only, with honest qualifiers. Never promise uptime, an SLA or SOC 2.
Never state pricing from memory. Currency is USD, always.

**Never say or imply a post was drafted by AI or by an agent.**

## Visuals

Background near-black `#121212` (hsl 0 0% 7%). Accent coral vermilion `#F45434`
(hsl 10 90% 58%). One accent element per figure.

No photoreal or AI stock-style images, ever. Figures are live animated React
components, real code, or diagram GIFs. Heroes are typographic stat cards at
**1200x750**, in the style of `landing/public/blog/hero-217kb-5kb.png`.

## Before merge

1. From `landing/`, run `bun run build`. It must pass.
2. Render the hero from `landing/scripts/blog-hero-cards.html?card=<slug>`
   at 1200x750 into `landing/public/blog/<slug>-hero.png`, and commit it with
   the build output.
3. Check the page at 1440 and 390 wide, no console errors.

## Delivery

Branches, titles and labels are in the repo prompt. Before writing, check for
cannibalization against the post folders, the live sitemap and every pick
record. Another agent also drafts for this repo.

A human merges, because merging is publishing. Never run `gh pr merge` and
never push to `main`.
