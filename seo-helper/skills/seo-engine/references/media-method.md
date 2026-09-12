# Media method: SVG visuals from seo-media

Every visual on a post is an authored SVG, produced by the `seo-media` agent. No photoreal images, no AI-stock look, no image-generation models, no screenshots of things that do not exist. SVG is text: it commits cleanly, renders on GitHub and in any blog, and always shows the literal subject.

## The contract between the agents

1. `seo-writer` writes the brief to `/pools/seo-pod/sot/media-brief.md`:
   - The article's title, primary keyword and slug.
   - The palette from the site prompt (background hex, accent hex) and any style notes.
   - The asset list: one hero plus each in-body figure, with one line per asset stating exactly what it must show, literally.
2. `seo-writer` spawns `seo-media` and waits.
3. `seo-media` reads the brief, authors each SVG into `/pools/seo-pod/board/public/assets/`, using the exact filenames the brief specifies, and finishes.
4. `seo-writer` verifies every file exists, references them in the article body, and commits them with the post. Verification includes the hero's canvas: check its `viewBox` matches the aspect ratio the prompt asks for, because a card that renders fine standalone can still be cropped by the site's own hero container.

## Asset rules (seo-media follows these)

- **Hero: a typographic stat card.** Use the exact canvas the site prompt's Visuals section gives for heroes, and only fall back to 1200x630 when the prompt is silent. Getting this wrong is not cosmetic: a blog whose hero container has a fixed aspect ratio will crop a mismatched card, and the crop eats the edges of the statement and the domain line. Site background color, one accent color, the post's core statement set large, a short kicker label, the domain small in a corner. Text is the design; make the typography deliberate (size contrast, letterspacing on labels, generous margins). System font stacks only (`font-family="ui-monospace, SFMono-Regular, Menlo, monospace"` or a clean sans stack); never reference external fonts or images, an SVG must be fully self-contained.
- **In-body figures: diagrams of the literal subject.** A flow diagram of the actual process the section describes, a labeled comparison grid, a timeline, a annotated config or command block, a simple bar or metric strip with real verified numbers. Never a metaphor, never decoration: a stranger glancing at the figure must see the section's real subject.
- **One accent color per figure.** Background and text from the palette; the accent highlights exactly one thing per figure (the current step, the winning column, the key number).
- **Filenames**: keyword slugs, e.g. `<slug>-hero.svg`, `<slug>-fig-costs.svg`. Never `image1.svg`.
- **Legibility floor**: minimum ~14px equivalent text at the SVG's natural size, real contrast against the background, no text over busy shapes. Every `<text>` element must fit its container; when in doubt, make the canvas bigger.
- **Validity**: well-formed XML, a proper `viewBox`, no external references (no `<image href>`, no font imports, no scripts). Each file must render standalone.

## How many

Hero always. In-body figures where they genuinely help: a good default is 2 or 3 for a 2,500-word article, one per major section that has something diagrammable. A section with nothing concrete to show gets prose, not a filler graphic. Never one-figure-per-H2 as a quota.

## Alt text

`seo-writer` writes the alt text: the section's keyword phrased as a description of what the figure literally shows. Hero alt = the primary keyword.
