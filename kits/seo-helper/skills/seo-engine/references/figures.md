# Figures

Every visual is an authored SVG: text that commits cleanly, renders anywhere and shows the literal subject. No photos, no image models, no screenshots of things that do not exist.

## How many

A hero always. In-body figures where a section has something to diagram: 1 or 2 for a short post, 2 or 3 for a long one. A section with nothing concrete to show gets prose, never a filler graphic.

## The hero: a typographic card

- The canvas the brief gives (default 1200x630, `viewBox="0 0 1200 630"`). A mismatched canvas gets cropped by the site's hero container.
- The brief's background, one accent, the post's core statement set large, a short kicker label, the domain small in a corner.
- Text is the design: size contrast, letter spacing on labels, generous margins.

## In-body figures: the literal subject

A flow of the actual process the section describes, a labelled comparison grid, a timeline, an annotated command block, a bar strip with real numbers fetched in this session. Never a metaphor: a stranger glancing at it sees the section's real subject.

## Rules for every SVG

- Standalone and valid: well-formed XML, a `viewBox`, no `<script>`, no event attributes, no `<image>`, no external references or font imports.
- System font stacks only: `ui-sans-serif, system-ui, sans-serif` or `ui-monospace, SFMono-Regular, Menlo, monospace`.
- One accent colour per figure, highlighting exactly one thing (the current step, the winning column, the key number). Background and text from the brief's palette.
- Text at least 14px at the natural size, with real contrast, never over busy shapes. Every `<text>` fits its box; when in doubt, make the canvas bigger.
- No em or en dashes in any text.
- Filenames: `<slug>-hero.svg`, `<slug>-fig-<name>.svg`, never `image1.svg`.

## Alt text

The section's keyword phrased as a description of what the figure literally shows. The hero's alt text is the primary keyword.

Check each file with `python3 <skill folder>/scripts/check_post.py --svg <file>`.
