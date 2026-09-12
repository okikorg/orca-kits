# Planning method: the lead's map for `plan` and `replan`

A plan is a bet with a number, a date, an explicit math, a week-by-week calendar, a daily ritual short enough to keep, and kill rules pre-registered so nobody moves the goalposts on a Friday. It is written from the analysis and the goal in the prompt, and it is edited in place afterwards, never rewritten, so the history of what changed stays readable.

The output is `strategy/<product>/plan.md` in this section order.

## 0. Header

Product, goal (the number and the date), the window (start and end dates, the weeks numbered W0 to Wn), the founder's daily minute budget, the date written, and a one-line status (`proposed`, `active from <date>`, `amended <date>`).

## 1. The thesis

One paragraph, bold first sentence. What to stop selling and what to sell instead; the wedge (the one thing the front door hangs on); which two or three engines carry the number; what the founder does daily; what gets published every Friday. Every later section must trace back to this paragraph.

## 2. The math

A table: source, mechanism (one sentence), low, high, gate (the condition under which the source is allowed to count). A total row. Then one paragraph on where the variance is and why the buffer exists. The low total must reach the goal or the plan says plainly that it does not and what would close the gap.

Sources are engines, not channels: a launch, a daily content loop, founder posting, outreach with a specific offer, paid on a specific destination, the inbound that existing assets already produce. Each has a gate the pod can check.

## 3. Week by week

One block per week, W0 first. W0 is always the front door: whatever must exist before reach is bought or earned (pricing page, hero, gallery, proof, repo, measurement, accounts, dates fixed). Each block has a bold one-line purpose and a bullet list of concrete deliverables, each of which the dispatcher can turn into one or more tasks with a done line. Launch weeks name the day, the hour and the timezone, the title of the post, and what runs the same day on every other channel. The final block is the readout.

## 4. The daily ritual

The founder's day in four slots that fit the minute budget: the morning reply-and-welcome slot, the midday publish slot, the afternoon outreach slot, the evening number. Say what the pod does around it (the dispatcher hands out the list at the start, the follow-ups agent surfaces what is due, the metrics agent needs the number dropped).

## 5. Kill and scale rules

One rule per engine, pre-registered: the metric, the threshold, the date it is read, the action. Plus the standing rule that an engine whose number is not in the metrics table on Friday counts as zero for the review.

## 6. The front door

The ranked list of changes to the product's public surface that W0 requires: headline and subheadline proposals verbatim, CTA labels, what sits under the fold, the pricing page columns, the vocabulary fixes, the compare pages, the first-run change. Each is one task later. Include the rewritten outreach offer if outreach is an engine.

## 7. Decisions waiting on the founder

The numbered list from the analysis, each with its recommendation, and for each the engines that stall until it is taken. This section is mirrored into `decisions.md` with dates.

## 8. What this plan does not fix

One paragraph. The honest limits: what the number does not buy (payers, retention), what would have to be true for the plan to fail, and what the review will look at first.

## Editing rules for `replan` and the weekly delta

- Edit in place. Never regenerate the file; a founder reads the diff.
- A change to the math, a week, a kill rule or the front door gets a line `amended <date>: <what and why>` appended to the section it changed.
- A change that opens or closes a channel, spends money, moves a launch date or makes a public commitment is a founder decision: it goes to `decisions.md` as `asked <date>`, not into the plan, until the founder decides.
- When a decision lands, apply its consequences everywhere they reach (math, weeks, tasks via reseed, front door) in the same run.
- Update the header status line every time.
