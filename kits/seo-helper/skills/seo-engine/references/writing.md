# Writing rules

A blocking checklist: a post is handed back only when it passes every rule here plus the site brief's Voice, or when the one corrective pass is spent and the reply names what is left. The owner's one-off instructions for this post override the defaults they name.

## The bar test (the top rule)

- Write as if you were explaining it to a friend at a bar: direct, human, plain words. Address the reader directly.
- Translate or drop jargon unless the brief says the readers are technical. Even then, anything product-specific gets a one-clause plain explanation on first use.
- Have real, concrete opinions. Use everyday examples. If it reads like a corporate brochure, rewrite it.

## Anti-slop (hard fails)

- Two layers: keep these rules active while you draft, then audit the finished draft against the known signs of AI writing (dashes, staccato sentences, rule of three, AI vocabulary, negative parallelisms, filler, vague attributions) and rewrite every hit.
- No em dashes and no en dashes, anywhere: use a comma, a period, or "to" in ranges.
- No sentence under 6 words: merge it into its neighbour.
- No banned words: delve, tapestry, landscape, robust, seamless, cutting-edge, groundbreaking, transformative, unprecedented, pivotal, leverage, harness, unlock, unleash, navigate, foster, elevate, embark, furthermore, moreover, additionally, consequently, notably, compelling, innovative, dynamic, utilize, comprehensive, paramount, meticulous, game-changer, streamline, scalable, crucial, remarkable, profound, multifaceted, nuanced, facilitate, endeavor, resonate, bolster, underscore, illuminate, empower, supercharge, skyrocket, shed light on, cultivate.
- No banned phrases: "here's the thing", "let's dive in", "it's worth noting", "in conclusion", "at the end of the day", "in today's world", "when it comes to", "that being said", "a testament to", "move the needle", "hits different", "hits home", "hits hard", "the answer?", "the result?", "my take:", "hot take:", "the hard part", "the part that catches", "here's the part".
- No throat-clearing before the point. If you can delete the opening clause and the paragraph still works, delete it.
- No "Not X. It's Y." pivots, no "No X. No Y. Just Z." triplets, no three-adjective triads.
- No rhetorical-question transitions; "but", "and", "also" instead of transition words.
- "What other posts don't tell you" framing at most once.
- Contractions throughout (it's, don't, can't).
- Vary sentence length. No run-ons: a sentence of more than about 30 words, or chaining three clauses, gets split at its strongest seam.
- Logical quotation punctuation: commas and periods outside the quotes.

## Facts

- Every price, statistic, date, version and product claim comes from a page or a DataForSEO result fetched in this session. Never from memory, doubly so for model names, versions and prices. If you cannot trace a claim to a fetched source, soften it to experience or cut it.
- Exact figures, never rounded up or embellished. Say when a figure is self-reported.
- Every command shown must be valid, runnable shell; every code label must match its code.

## Lists and tables

- Prose by default. A list only for a real parallel enumeration (steps, a short checklist, a few options). At most 3 lists in a post, 3 to 6 short items each, never two in a row, never nested.
- Tables only for a true two-way comparison, plain markdown.
- The second half is as fully written as the first.

## Structure

- A quick answer at the very top: 2 to 4 sentences that answer the title on their own.
- H2 headings phrased as questions where it reads naturally; the first sentence after each H2 answers it.
- No "Introduction", "Conclusion" or "In summary" headings.
- An FAQ of 4 to 8 natural questions, the primary keyword in at least 2, with FAQPage JSON-LD when the site's format allows it (the digest shows whether posts carry structured data).
- Default length: 2,500 to 3,000 words. A one-off length replaces it for that post.
- Figures as `references/figures.md` says; every image reference in the body matches a file you made.

## SEO and metadata

- Title at most about 60 characters rendered, primary keyword first. If the layout appends the brand, do not add it again.
- Meta description at most 155 characters, primary keyword in the first 20 words.
- Exactly one H1 (or the title in front matter, if the layout renders it as the H1; then no H1 in the body), carrying the primary keyword.
- Titles varied across the blog: if a filler word ("guide") already appears often in the digest, avoid it.
- 3 to 5 internal links to existing posts from the digest, with descriptive anchors. Never invent a URL.
- The checks run on every rendered surface: title, description, FAQ, alt text and front matter too.

## The self-review gate

Run `check_post.py`, then read the draft once against this list, and note only what fails:

- the keyword passed all five gates; no invented numbers;
- the post covers the top 3's baseline, fills their gaps, and the differentiation sentence still holds;
- length, quick answer, question H2s, FAQ;
- no dashes, no sentence under 6 words, no banned word or phrase, contractions, no run-ons;
- voice and forbidden claims as the brief says;
- title and meta lengths;
- every figure exists and is referenced with alt text;
- 3 to 5 internal links, all real;
- front matter matches the digest's example exactly.

Fix those items in one targeted pass. Do not rewrite the whole post. If something still fails and would need a rewrite, hand it back anyway and say what is left.
