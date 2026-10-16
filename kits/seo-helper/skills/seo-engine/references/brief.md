# The site brief

The site brief holds what is particular to one site. The coding agent saves it in the owner's repo at `.orca/seo-helper/site-brief.md` and stages it as `/workspace/site-brief.md` in every later session. The owner edits it like any file.

## Drafting it

On the first topics turn there is no brief. Draft one from:

- `/workspace/site-digest.md`, which the coding agent wrote from the repo: every post (title, slug, date, description, headings, tags), the post layout (folder, file names, front matter with a real example, asset path and naming, files never to hand-edit), maybe one short sample post for voice, and old pick records (title and keyword);
- the blog index, read with `on_page_content_parsing` on the URL the owner gave.

Mark every line you inferred with `(inferred)`, so the owner knows what to check. Never invent a fact about the business; write "unknown" instead.

## Fields

```markdown
# Site brief: <domain>

Updated: YYYY-MM-DD

## Offer and readers
- Domain: <domain>
- Blog: <blog URL>
- What the site sells or does: <one line>
- Readers: <who reads the blog, and who buys>
- Location and language for search data: <for example United States, English>

## Lanes
- Allowed: 3 to 5 numbered topic lanes, one line each
- Forbidden: topics never to write about

## Voice
- Persona and rhythm: <one or two lines>
- Jargon: <plain, or technical readers>
- Brand mentions and calls to action: <how the product is named, where a CTA goes>
- Claims never to make: <for example no prices, no customer names>
- Allowed terms: <banned-list words the site uses as names, for example harness as a noun; passed to check_post.py --allow>
- Currency: <USD>

## Post layout
- Path: <for example content/blog/<slug>.mdx, or a folder of files such as meta.ts and article.tsx>
- Front matter: <the fields, with one real example>
- Title template: <whether the layout appends the brand>
- Assets: <path and naming, for example public/blog/<slug>-fig-<name>.svg>
- Never hand-edit: <generated files>
- Before merge: <the site's build or check command, if the digest shows one>

## Figures
- Palette: background <hex>, text <hex>, accent <hex>
- Hero canvas: <width>x<height> (default 1200x630)
- Style: <one line>

## Defaults for posts
- Length: 2,500 to 3,000 words
- Audience: <from Readers>
- Code samples: <yes, where they help, or no>
```

## Changing it

Only "remember that" changes the brief. Write a new `outputs/site-brief.md` with the change, update the `Updated` date, and say in your reply which line changed. A one-off instruction for one post never changes it.
