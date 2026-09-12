# Analysis method: the lead's map for `analyse`

The analysis answers one question: why is this product not getting the signups its effort deserves, and what would? It is honest about the past, specific about the market, and ends in verdicts a founder can act on. It is written once per product and refreshed when the lead is asked to, never on a schedule.

The output is `strategy/<product>/analysis.md` in exactly this section order. A section with nothing to say says so in one line rather than disappearing.

## 0. Gather, in this order

1. **The prompt.** What the product is, who it is for, the price, the goal, the accounts, where past marketing lives, which competitors to compare.
2. **Past marketing.** Every file under `inbox/<product>/docs/` and every repo path the prompt names, read whole. Look for: a tracker with goals and checkboxes; channel plans; published posts and their engagement; ad flights and their numbers; an outreach list with statuses; a metrics table. Note the date of the last edit of each. An empty metrics table is a finding, not a gap.
3. **The live product surface.** Home page, pricing page if any, docs start page, the machine-readable page for agents if any, the signup page as far as it can be seen signed out. Record verbatim: the hero headline and subheadline, every CTA label, the section order, any proof shown (numbers, logos, quotes), any price shown, and whether a video, a demo, a template gallery or real screenshots appear.
4. **Public distribution.** The GitHub org: which repos are public, stars, last push. The founder's and the brand's X handles if given: follower counts if visible. The blog: how many posts, last date.
5. **Competitors.** For each named competitor, fetch home and pricing today. Record: hero headline verbatim, one-line pitch, the persona, the section order, the primary CTA and where it leads, whether there is a live demo or a no-signup try, whether it is open source and the stars, every plan with its price and limits, the free tier, any markup or fee on model usage stated, the self-host option, notable growth tactics visible (launch posts, compare pages, community, credits programs).
6. **The category.** The closest six to ten platforms the product would be compared with by a buyer, with their pricing model, free tier, entry paid price, usage fee, self-host. Fetch pricing pages; mark anything from a secondary source `unverified`.

Every fact carries its source and, for anything fetched, the date. If a fact cannot be verified, say so; never fill the gap with a plausible number.

## 1. Where we are

A scoreboard of four to six numbers that say it all (signups vs goal, the biggest planned event and whether it ran, sends vs plan, posts vs cadence, free credit vs the market, commits or releases in the same window if the contrast is the point), then a table: one row per engine the product ran, with the plan, what happened, and a verdict in three words. Then one paragraph on the ratio that explains most of it.

## 2. Why it stalled

The causes, ranked by weight, each with a heading, a paragraph and the evidence from the gather. Typical causes to test, not assume:

- The largest planned source of reach was gated on a slow engine and never fired.
- Positioning sells the layer the buyer evaluates last (infrastructure, features) rather than the job the buyer wants done.
- Distribution is closed where the category is open (no public repo, no stars, nothing to watch).
- The offer is small or the price is hidden relative to the market.
- The named ICP is the right payer and the wrong first hundred.
- Process outran output: docs written, numbers never logged, drafts never published, reads never taken.
- The founder is not in front; a brand handle posts rarely.

Quote the product's own evidence back to it: which post did best, which ad theme won, what the tracker's own numbers say.

## 3. What the winners do

One card per named competitor: positioning, the proof they show, the CTA design, onboarding, pricing in one line, distribution and growth tactics, and the two or three things worth borrowing. Then a table, pattern by pattern (hero shows the product doing a job; one named primitive the page hangs on; try without signing up; onboard through the visitor's coding agent; open source core; generous free tier; plain pricing page; proof strip; compare pages; founder in front; vocabulary repeated everywhere), with who does it, what the product does today, and a gap verdict: missing, built but hidden, have it, opposite.

## 4. Pricing

The product's pricing in one paragraph. Then the comparison table: product, model, free tier, entry paid, fee on model usage, self-host. Then a verdict block per topic, each opening with a bold one-sentence verdict: the free tier against the market; the fee or markup against what competitors say out loud; the pricing page and the nav; the packaging ladder (Free / Pro / Enterprise or whatever the category settled on) and the missing rung. Each verdict ends in the concrete change and a rough cost or exposure number where money is involved.

## 5. Decisions only the founder can take

The numbered list of calls the plan will depend on: open-sourcing, credit amounts, price disclosure, the founder's own account, dropping a gate, dates, what stays off until when. Each in one sentence with the recommendation first. These become `decisions.md` when `plan` runs.

## 6. Sources

Every URL fetched, with the date, and every repo path or inbox file read. The analysis is only as good as this list.

## Voice

Plain sentences, real numbers, no adjectives that could sit on a landing page. Concede first where the product is weak; a founder reading it should recognise their own evidence, not feel sold to. No em dashes.
