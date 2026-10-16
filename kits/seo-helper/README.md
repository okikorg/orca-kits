# SEO Helper

It reads your blog and your repo through your coding agent, gives you five topics with their search numbers and who ranks for them today, writes the one you pick on its method plus anything you ask for that post only, revises it with you, and hands the files back for your coding agent to put in your repo.

## What it uses

Model calls on `orca/openrouter/openai/gpt-5.6-luna`, paid from your Orca credit; a sandbox for each conversation (machine time); and **DataForSEO, required**: its MCP server at `https://mcp.dataforseo.com/mcp`, called with your own DataForSEO API login, so each search is charged to your DataForSEO account at [their prices](https://dataforseo.com/pricing). See [Orca's pricing](https://orcapods.ai/pricing).

## Add it

```
orca vaults create dataforseo
orca vaults credentials add dataforseo --name dataforseo --server https://mcp.dataforseo.com/mcp --basic --login you@example.com
```

Use the API login and password from app.dataforseo.com, API access, not your dashboard password.

## Use it

```
orca chat seo-helper --template seo-helper --vault dataforseo --file site-digest.md "Give me the top 5 topics for my blog's next post."
```

Or tell your coding agent: "Let's write a blog today with seo-helper. Look at my current blogs at https://example.com/blog and my repo, and give me the top 5 topics for the next post."
