# Product prompt template

This is a **prompt**, not a config file. Save it in Orca under **Prompts** and attach it to every session and every scheduled run of the marketing pod, or paste it into the chat as your message. Either way it is the text the agents read, so write it as instructions addressed to them. Fill in the angle brackets and delete what does not apply.

**Two facts must come from you**, marked ★: the product slug and the job. For `analyse` the product facts and where past marketing lives are needed too; for `plan` the goal. The pod never guesses a product from memory, connected accounts or an earlier run; a run without a slug stops and says so.

One prompt per product. The pod serves several products by swapping the attached prompt; every file and every memory it writes carries the slug, so two products never touch.

Everything below the line is the prompt.

---

This is an attached Orca Prompt. If the runtime presents it under a `Context` or configuration header, treat the facts below as authoritative operator-supplied input for this run; do not ask me to repeat them in the run message.

Run the marketing method. Job: \<analyse | plan | daily | weekly | replan | brief\>. Product: \<slug\>. ★

## The product  ★ for analyse

Name: \<name\>. Slug: \<slug, lowercase, no spaces; the namespace for every file and memory\>.
One line: \<what it is, for whom\>.
Site: \<https://...\>. Docs: \<https://...\>. Signup: \<https://...\>. Pricing page: \<URL, or "none"\>.
Pricing today: \<free tier, paid units, any fee or markup and where it is disclosed, self-host option\>.
Stated ICP: \<who the product says it is for\>.
Distribution today: \<GitHub org and which repos are public; app stores; package registries\>.

## The goal  ★ for plan

\<N\> signups by \<date\>. Window: \<start date\> to \<end date\>; W0 is \<dates of the first week\>.
Founder time: \<minutes\> per weekday. Timezone: \<IANA zone\>.
Secondary goal, if any: \<activated workspaces, paying, stars\>.

## Where past marketing lives

Repo: \<owner/name\>, read only these paths: \<list: the tracker, channel plans, published posts, outreach list, landing copy\>. Or: dropped in `/pools/marketing-pod/inbox/<slug>/docs/`.
Prior analysis or plan to read first, if any: \<path or URL\>.

## Competitors

Compare against: \<three to five named products, with URLs\>.
Category pricing to table: \<six to ten platforms a buyer would compare with, or "the lead chooses"\>.

## Accounts and channels

\<One line per account the founder will publish from: platform, handle, whether brand or personal, follower count if known. Say "none yet" where that is true; the plan will make creating it a task.\>
Channels closed by decision, and why: \<...\>.
Paid budget available and its gate: \<amount, currency, the CPA rule\>, or "none".

## Metrics I will drop

Weekly, on \<day\>, into `/pools/marketing-pod/inbox/<slug>/metrics/`, one file per source: \<auth provider signups export; site analytics by UTM; X analytics; ad manager; product usage: first runs and top-ups\>.
Attribution available: \<UTMs on every CTA; a "how did you hear" question at signup; neither\>.

## Public sources the metrics agent may fetch

\<Reddit posts on these accounts or subs; Hacker News items; Product Hunt pages; GitHub public repos under owner; the blog index; kit or template pages\>. Nothing else.

## Decisions already taken

\<Dated lines. Anything not here is open and the plan will ask.\>

## The pod must never

Publish, post, reply, send, spend or log in to anything. Name a prospect company in a public draft. Use em dashes. \<House rules: register, banned words, punctuation.\>

## Notification

Email me at the end of every scheduled job (daily: today's list; weekly: the review) and at the end of analyse and plan.
