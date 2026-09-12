# Metrics method: the metrics agent's map

The metrics agent keeps the number. It records what the operator dropped, fetches what is public, attributes what it can, and writes `not supplied` where it has nothing. It never estimates, never extrapolates, and never lets a blank cell look like a zero.

## Two kinds of numbers

**Operator-supplied.** Only the founder can see these; they arrive as files in `inbox/<product>/metrics/`, one per drop, named `<yyyy-mm-dd>-<source>.md` or `.csv`. Typical sources: the auth provider (signups, by day, with the "how did you hear" answer if collected), site analytics (visits, signup-page visits, CTA clicks, by UTM source), X analytics (impressions, profile visits, link clicks, followers), ad managers (spend, clicks, CPC), the product's own usage (workspaces with a first run, top-ups). The prompt says which of these the founder will drop and how often. A week with no drop gets `not supplied` in those cells and a line in the email asking for it.

**Fetched.** Public, and allowed by the prompt. With `web_extract` or a connected app, fetched today, each with its URL in the source column:

- Reddit posts: score and comment count from the post page or its `.json` form.
- Hacker News: points and comments from the item page or the public API.
- Product Hunt: upvotes and comments from the product page.
- GitHub: stars, forks, watchers of the named public repos (connected app read against the exact `owner/name`, or the public page).
- Blog: number of posts and the newest date.
- The product's kit or template pages: whatever public counters they show.

Never fetch anything the prompt does not allow; never log in to anything.

## The file

`metrics/<product>/metrics.md`, appended and corrected in place, in this order:

1. **Header.** Product, date of this run, the goal line from the plan (number and date), and the running total toward it in bold: `Signups so far: N of G (source: ...)` or `not supplied`.
2. **Weekly table.** One row per plan week (W0 onward), columns: week, dates, signups, activated (first run or equivalent), paying, site visits, signup-page visits, X impressions, X link clicks, X followers, Reddit posts (count) and their total score, GitHub stars, outreach sends, replies, paid spend, paid signups, source notes. A row is created the first Friday of its week and corrected whenever a later drop covers it (a late auth export is normal). A correction keeps the old value in the source notes: `corrected 09-26 from 4 to 6 (auth export)`.
3. **Per-post table.** One row per published post or launch: date, channel, title, URL, score or upvotes, comments, link clicks if supplied, signups attributed (only when a UTM or the "how did you hear" answer says so), and `attribution: utm | survey | timing | none`.
4. **Per-destination table.** One row per kit, landing or compare page that carries a CTA: URL, visits, signups, conversion, source.
5. **Gaps.** What was expected this week and did not arrive, in one line each, so the lead can ask for it.

## Attribution rules

- A signup is attributed to a source only through a UTM, a survey answer, or an explicit note from the founder. Timing correlation is recorded as `timing` and never summed into the source's total.
- Never divide spend by an unattributed count and call it a CPA. If the count is attributed, compute CPA and write the formula in the source notes.
- The kill rules in the plan are read against attributed numbers only.

## Rules

- Every cell: a number with a source, or `not supplied`. Nothing else.
- Never round a number the source gave exactly.
- Dates in the file are the dates the data covers, not the run date.
- No em dashes.
