# Memory rules: one bank, many products

Only `marketing-lead` has the Memory Bank. The bank is scoped per agent profile, not per product, so everything the lead remembers about one product sits next to everything it remembers about another, and an automatic `--- CONTEXT FROM MEMORY ---` block will inject the most relevant entries of any product into any run. These rules keep that from becoming a mess.

## The tag

Every `memory_save` starts its content with the product tag on its own line:

```
[product: <slug>]
```

followed by the fact. A save without the tag is a bug: never make one. The slug is the one from the attached product prompt, exactly as written there.

## What to save, and as what

Save few, dense entries. Each is under 3,500 characters (the bank rejects 4 KiB), pre-structured with `content`, `category` and `confidence` so the bank does not have to guess. Save these after `analyse`, and refresh them (delete the old entry, save the new one) after every `replan` that changes them:

| Entry | Category | Confidence | What it holds |
|---|---|---|---|
| `[product: slug] identity` | `fact` | 0.9 | One paragraph: what the product is, who buys it, the price model, the free tier, the URLs, the accounts and handles, the founder's time budget. |
| `[product: slug] readout <date>` | `fact` | 0.9 | The readout of past efforts in ten lines: each engine, what was planned, what happened, the verdict. |
| `[product: slug] causes` | `fact` | 0.85 | The ranked causes from the analysis, one line each. |
| `[product: slug] competitors` | `fact` | 0.8 | One line per competitor: positioning, pricing model, free tier, the one thing to borrow. Dated. |
| `[product: slug] pricing verdicts` | `fact` | 0.85 | The pricing verdicts and the recommended packaging. |
| `[product: slug] thesis` | `preference` | 0.9 | The plan's thesis, the wedge, the two or three engines that carry the number, the kill rules. |
| `[product: slug] decisions` | `fact` | 0.9 | The founder decisions taken, with dates. Refreshed on every `replan`. |
| `[product: slug] lessons` | `behavior` | 0.7 | What the weekly reviews taught: which content shape worked, which channel died, what the founder will and will not do. Appended by the weekly job, kept under the size cap by rewriting. |

Do not save: task lists, metric rows, follow-ups, drafts, anything already in the pool with a date on it. The pool is the system of record. Memory is the lead's ability to open a session on a product it has not touched in a month and speak about it correctly in the first sentence.

## The recall filter

At the start of every run, after the prompt gate has fixed the slug:

1. Call `memory_recall` with the query `[product: <slug>]` plus the job name, limit 12.
2. Keep only the entries whose content starts with the exact tag of this run's product. Discard every other entry, including anything the automatic injection block put in front of you that names a different product or no product at all.
3. Treat what remains as your own earlier reading, not as fact: the pool files win where they differ, and the attached prompt wins over both.

Never let a fact from product A shape a sentence about product B. When the injected block mixes products, say nothing about the other product and carry on.

## Attended sessions on the lead

When a person opens a session on `marketing-lead` and names a product the pool has never seen, the memory bank is the only thing the lead knows about it, and it will usually know nothing. Say so, and offer the `analyse` job. When the pool has the product but the memory bank does not (a copied pod, a fresh profile), read `strategy/<product>/` and rebuild the entries above before answering.
