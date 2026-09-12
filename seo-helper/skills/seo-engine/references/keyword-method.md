# The keyword method

Pick the piece's primary keyword with the site prompt's domain, location and language. Five gates, all mandatory, then the competitor pass. The method runs in one of two modes:

- **Verified mode**: the DataForSEO connected app answered during pre-flight. Volume, difficulty and intent come from real data. Reach it with `search_connected_app_tools` (app `composio-dataforseo`) to find the tool you need, then `call_connected_app_tool` to run it; `keyword_overview` gives volume and difficulty, the SERP tools give the live results page. Say `mode: verified` in the PR body.
- **Heuristic mode**: the DataForSEO app is absent, unconnected or failing. Volume and difficulty are judged from live SERP evidence as described per gate below. Say `mode: heuristic` in the PR body. Never print a number you did not fetch; in heuristic mode you describe demand, you do not quantify it.

Pre-flight already decided which mode this run is in. Do not re-probe per keyword, and never let a DataForSEO failure mid-run stop the piece: drop to heuristic mode, relabel the run, and carry on.

## Gate 1: Relevance (HARD filter, before anything else)

A keyword is eligible ONLY if it clearly serves THIS site's offer and would bring a real potential customer.

- Candidates come only from the prompt's allowed topic lanes.
- It must pass: "would someone searching this plausibly become a customer of this business?" If no, drop it.
- It must not sit in a forbidden lane.
- Watch context, not just the word. For a web-design agency, `website for artisans` is relevant (an artisan is a client); bare `artisan recipes` is off topic.
- When unsure, drop it and pick another. Never write off-topic content.

## Gate 2: Demand (volume floor and anti-junk)

- **Verified mode**: the candidate must have a real, non-zero `search_volume` from the connected app's keyword_overview call. If suggestions return junk (off-topic global terms, fallback noise), discard and re-seed from the topic lanes. Judge value, not just volume: a low-volume, high-intent term can beat a big generic one.
- **Heuristic mode**: demand evidence comes from the live SERP. The term should appear in autocomplete or People Also Ask, the SERP should show real pages competing on it (not an empty or nonsense results page), and related long-tail variants should exist. If a search for the term returns nothing coherent, the demand is not real; re-seed.

## Gate 3: Intent (routing)

- **Informational** ("how to", "how much", "why", "what is", "X or Y") → article.
- **Commercial** ("pricing", "best", "alternatives", "vs", "buy", "tool") → page.
Confirm against the live SERP: a page of guides means informational, a page of product and vendor pages means commercial. On an article request only informational keywords are eligible; on a page request only commercial ones.

## Gate 4: Winnability (pick what this site can actually rank)

Volume is worthless if the site cannot reach page 1.

- **Verified mode, new or low-authority site**: hard-prefer KD ≤ 25, long-tail, specific angle. Never target KD > 35 head terms regardless of volume; note them in the PR body as "later, once authority grows" if they came up.
- **Heuristic mode**: run the SERP test. If page 1 is wall-to-wall household-name domains, the term is not winnable for a newer site; move on. If forums, small blogs, thin or dated pages rank, that is a gap worth taking. Prefer specific long-tail phrasings over head terms.
- Never copy a strong competitor's head keywords just because they rank; their authority earned it.

## Gate 5: Anti-cannibalization (mandatory before creating)

- Check the candidate against the FULL existing-content list from pre-flight: sitemap URLs and titles, repo content files, and open `seo-draft` PRs. Drafts cannibalize too.
- **Match by target keyword, not by URL.** A page can own a keyword without the term in its slug; scan titles and H1s, not just paths.
- Any existing page, article or draft already targeting this keyword, a near-synonym, or the same intent → pick a different keyword or angle. Never ship a second piece that competes with an existing one.
- HARD STOP: a candidate whose title would lead with the same head term as an existing title is a duplicate, whatever the page type. Pick a different long-tail instead.

## The competitor pass (Step 5, MANDATORY before writing, both modes)

Read the actual top 3 ranking pages for the keyword (fetch them; skip aggregators like Wikipedia and YouTube) and produce:

1. **Coverage map**: the subtopics each top page covers. The union is the baseline you must at least match.
2. **Gap and weakness list**: what they miss, get wrong, leave vague, or bury: unanswered questions, missing concrete numbers, outdated info, no honest recommendation, no quick answer.
3. **The differentiation sentence (write it down)**: one clear sentence answering "why would someone read mine instead of the current top 3?", naming 2 or 3 concrete value-adds you will deliver.
4. If you cannot write that sentence convincingly, do not ship this keyword. Pick another. Matching the SERP is not enough; beating it is the bar.

## Output: the brief

Primary keyword, secondary keywords, intent, mode, volume/difficulty (verified mode only), the coverage map and gaps, the differentiation sentence with its value-adds, and the verified facts (fetched live) the writing may use. The writer covers the baseline, fills the gaps, and leads with the angle.
