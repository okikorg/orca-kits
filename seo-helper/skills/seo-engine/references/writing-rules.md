# Writing Rules: the blocking standard for every piece

This is a **blocking checklist**. No article or page is delivered unless it passes every UNIVERSAL rule plus the site prompt's VOICE rules.

## UNIVERSAL: every article and page

### The bar test (TOP rule)
- Write as if **you were explaining it to a friend at a bar**: direct, human, in plain words, as if a real person wrote it and not an AI. Address the reader directly.
- **Translate or drop jargon** unless the site prompt's jargon calibration says the reader is technical. Even then, anything product-specific gets a one-clause plain explanation on first use.
- Have real, concrete opinions. Use everyday examples. If it reads like a corporate brochure, rewrite it.

### Anti-AI-slop (hard fails)
- **Two-layer anti-slop: a constraint pass DURING writing, a humanizer pass AFTER.** Keep this file's rules and banned lists active while you draft, so the first draft comes out clean. Then audit the finished draft against the known signs of AI writing (Wikipedia's "Signs of AI writing" guide is the reference set: em/en dashes, staccato sentences, rule-of-three, AI vocabulary, negative parallelisms, filler, vague attributions) and rewrite every hit.
- **Punctuation and sentence-length rules are house style, and the site prompt
  owns them.** This engine ships no absolute of its own: read the prompt's Voice
  section and apply exactly what it states. Two common house choices, quoted here
  so the prompt can simply name them:
  - *No em dashes or en dashes*: use a spaced dash ` - `, a comma, or a period.
  - *No sentence under N words*: after the humanizer pass, flag anything shorter
    and merge it into its neighbour.
  If the prompt is silent on both, use ordinary editorial judgement rather than
  inventing a rule: vary sentence length, and do not lean on dashes as a tic.
- **No banned words:** delve, tapestry, landscape, robust, seamless, cutting-edge, groundbreaking, transformative, unprecedented, pivotal, leverage, harness, unlock, unleash, navigate, foster, elevate, embark, furthermore, moreover, additionally, consequently, notably, compelling, innovative, dynamic, utilize, comprehensive, paramount, meticulous, game-changer, streamline, scalable, crucial, remarkable, profound, multifaceted, nuanced, facilitate, endeavor, resonate, bolster, underscore, illuminate, empower, supercharge, skyrocket, shed light on, cultivate. (Ban the equivalents in the site's language if it is not English.)
- **No banned phrases:** "here's the thing", "let's dive in", "it's worth noting", "in conclusion", "at the end of the day", "in today's world", "when it comes to", "that being said", "a testament to", "move the needle", "hits different/home/hard", "the answer? …", "the result? …", "my take:", "hot take:", "the hard part", "the hard part isn't …", "the part that catches … off guard", "here's the part".
- **No throat-clearing filler before the point.** If you can delete the opening clause and the paragraph still makes sense, delete it. Test every sentence: would a real person say this out loud?
- **No "Not X. It's Y." pivots. No "No X. No Y. Just Z." triplets. No three-adjective triads** ("fast, reliable, secure").
- **No rhetorical-question transitions. No transition-word abuse** (furthermore/moreover): use "but", "and", "also".
- **The "what other posts don't tell you" framing at most ONCE per article**; on the second use it reads as a tic.
- **Contractions mandatory** (it's, don't, can't, won't, doesn't; never the formal form).
- **Vary sentence length.** Avoid the staccato-fragment tic; honour any minimum the site prompt sets.
- **No run-on sentences.** A sentence chaining three or more clauses with ", which", ", so", ", and", ", but" gets split at the strongest seam. Rough ceiling: ~30 words or two joined clauses.
- **Quotation punctuation = logical/British**: commas and periods go OUTSIDE the quotes.

### Fact-check discipline (part of the self-review gate)
- **One version number per behavior, exactly as the source attributes it.** When two changes shipped in different versions, never collapse them under one version, even in the same sentence. Re-open the source and match each number to its behavior.
- **Every code block label must describe what its code actually shows.**
- **Every displayed command must be valid, runnable shell**, including inside figures: check quoting, flags that exist, and grammatical prompt strings.
- **During self-review, re-verify every number, version string, flag name and quoted claim against the fetched source page**, not against memory of it. A claim that cannot be traced to a source line gets softened to an experiential statement or cut.

### Lists and tables (STRICT: prose is the default)
- **Write in flowing paragraphs by default.** A list is allowed ONLY for a genuine parallel enumeration: ordered steps, a true short checklist, a few discrete options. A "list" item that is a full explanatory sentence must be a paragraph.
- **Hard caps per article:** at most 2 or 3 lists total, never more than one list per 2-3 H2 sections, each list 3-6 items, short items. No two lists back-to-back, no nested lists.
- **Never let the article degrade into bullets, especially the second half.** The closing sections must be as fully written as the intro.
- **Tables** only for a true 2-D comparison, and not in every article. Plain markdown tables only, never hand-rolled HTML. Never a dumping ground to avoid prose.
- Self-review check: if removing every bullet and table would gut the article, they were load-bearing (fine). If it would simply read as cleaner prose, convert them back to paragraphs.

### Where the checks run
- The jargon, em-dash, banned-word and bar-test checks run on **every rendered surface**: title, meta description, FAQ questions and answers, image alt text, and front matter fields. A clean body with jargon in the FAQ still fails.

### Accuracy (hard fail if violated)
- Every price, stat, date and product claim must be **verified via live fetch during the run**. Never from memory. Doubly true for AI model names, versions and pricing: training data is stale and WILL be wrong; fetch each vendor's current lineup live and use only verified names. If you cannot verify it live, do not say it.
- Exact figures, never rounded or embellished. Distinguish self-reported from independently verified. If unverifiable, omit.

### Article structure
- **Quick answer at the very top**: the opening directly answers the title in 2-4 sentences, self-contained.
- **H2 headings phrased as questions** when possible. **First sentence after each H2 directly answers that heading.**
- **Visuals per `references/media-method.md`**: one SVG hero plus in-body SVG figures where a section has something genuinely diagrammable (2 or 3 is a good default; no per-H2 quota, no filler graphics). Every figure shows the literal subject, never a metaphor. Every image reference in the body must match a produced asset filename.
- **No "Conclusion" / "Introduction" / "In summary" headings.** Use a substantive synthesis or action heading.
- **FAQ: 4-8 natural-language questions**, primary keyword in at least 2, plus FAQPage JSON-LD when the site's format supports structured data.
- **Word count: 2,500-3,000.** 2,500 is the floor to rank; ~3,000 is a hard cap. Completeness over length, every section earning its place.

### SEO / metadata
- **Title ≤ ~60 characters rendered**, primary keyword first. Check the site's title template: if the layout appends the brand, do not include the brand again.
- **Meta description ≤ ~150-155 chars**, primary keyword in the first 20 words.
- **Titles varied across the blog.** Scan the existing titles from pre-flight: if a filler word ("guide") already appears often, do not use it. Each title gets a distinct angle.
- Exactly one H1 with the primary keyword. Canonical where the site's format carries it.

### Internal linking
- **3-5 internal links** per article to existing pages from the pre-flight content list, descriptive keyword anchors, never "click here". Relevance-gated: link only when topically additive. Never invent URLs; every internal link target must exist in the sitemap or repo.
- **Hub rule**: when the new piece belongs to a listing or hub page the prompt names (a registry, an index, a category hub), add it there in the same shape as the existing entries, in the same PR.

## SITE VOICE

The site prompt's Voice section defines persona, rhythm, jargon calibration, brand-mention policy, CTAs, currency and forbidden claims. It overrides the universal rules where they differ. Never make a claim the prompt forbids; never state pricing or product facts from memory.

## SELF-REVIEW GATE (MANDATORY: run on the finished draft BEFORE delivery)

One editor pass against this checklist. Bounded, **not a loop**:

- **First, confirm the humanizer pass ran and the scans are clean**: 0 sentences under 6 words, 0 em/en dashes, no banned word or phrase hits. If any failed, fix that now, before anything else.
- Read the draft once and note only the specific items that fail. Make targeted fixes to those items. Do not rewrite the whole article; do not regenerate assets unless one is genuinely missing or broken.
- Re-check only what you changed. **Cap: one corrective pass.** If something still fails and would need a full rewrite, deliver as a draft anyway and state the issue in the PR body for human review.

**Value and keyword:**
- [ ] Keyword passed all five gates in the declared mode; no invented numbers anywhere.
- [ ] Step 5 delivered: the draft covers the top-3 baseline AND fills their gaps, and the differentiation sentence still holds against the finished draft.
- [ ] Every fact is fetched, not remembered; one consistent currency.

**Writing quality:**
- [ ] 2,500-3,000 words. Quick answer up top. H2s as questions.
- [ ] Punctuation and sentence-length rules from the site prompt all pass; no slop patterns, no banned words, contractions throughout, no run-ons, no sub-6-word fragments.
- [ ] FAQ present. First sentence after each H2 answers it.
- [ ] Site voice respected: persona, rhythm, brand-mention policy, no forbidden claims.
- [ ] Title varied and ≤ ~60 chars rendered; meta ≤ ~155 chars with the keyword early.

**Assets and technical:**
- [ ] Every SVG asset exists in `/pools/seo-pod/board/public/assets/`, is referenced in the body with keyword alt text, and follows media-method.md.
- [ ] 3-5 internal links, all targets real.
- [ ] Front matter matches the repo's existing posts exactly; the file lands at the prompt's content path; any registry or hub file is updated in the same branch.

If anything is borderline, fix it rather than ship it. Quality is constant only because this gate runs every time.
