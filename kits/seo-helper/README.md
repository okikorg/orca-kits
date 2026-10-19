# SEO Helper

It researches what your blog should rank for next with DataForSEO: five topics that pass its gates, with their numbers and the gap you can win, then an SEO brief for the one you pick. Your coding agent writes the post from the brief, under your repo's own rules, and commits it.

## What it uses

Model calls on `orca/openrouter/openai/gpt-5.6-luna`, paid from your Orca credit, and no sandbox. **DataForSEO, required:** its MCP server at `https://mcp.dataforseo.com/mcp`, called with your own DataForSEO API login, so each search is charged to your DataForSEO account at [their prices](https://dataforseo.com/pricing). See [Orca's pricing](https://orcapods.ai/pricing).

## Add it

```bash
orca kits copy https://app.orcapods.ai/kits/kit-utRCllawsrI2cqKdT
```

Or click **Copy** on [the kit's page](https://app.orcapods.ai/kits/kit-utRCllawsrI2cqKdT).

Then add your DataForSEO API login once, in your own terminal; the password goes in a hidden prompt (from app.dataforseo.com, API access):

```
orca vaults create dataforseo
orca vaults credentials add dataforseo --name dataforseo --server https://mcp.dataforseo.com/mcp --basic --login you@example.com
```

## Use it

```
orca chat seo-helper --vault dataforseo "Give me the top 5 topics for my blog's next post."
```

From a coding agent: "Let's do SEO with seo-helper: top 5 topics for my next post." It sends your post list with the question, then asks `Brief: <keyword>` for the one you pick, never a number.
