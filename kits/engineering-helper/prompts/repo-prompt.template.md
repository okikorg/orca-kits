# Repository prompt template

This is a **prompt**, not a config file. Save it in Orca under **Prompts** and attach it to every session and every scheduled run of the engineering pod, or paste it into the chat as your message. It is the text the agents read, so write it as instructions addressed to them. Fill in the angle brackets and delete what does not apply.

**Two facts must come from you**, marked with a star: the repository and the job. For `batch` the issue query is needed too. The pod never guesses a repository; a run without one stops and says so.

One prompt per repository. The pod serves several repositories by swapping the attached prompt; every file it writes carries the slug, so two repositories never touch.

Everything below the line is the prompt.

---

This is an attached Orca Prompt. If the runtime presents it under a `Context` or configuration header, treat the facts below as authoritative operator-supplied input for this run; do not ask me to repeat them in the run message.

Run the engineering method. Job: \<batch | issue\>. Repo: \<owner/name\>. ★

## The repository  ★

Repo: \<owner/name\>. Slug: \<short name, lowercase, no spaces; the folder every file lives under\>.
Base branch: \<main\>. Branch prefix for your work: \<eng/\>.
My GitHub login: \<handle, needed for "assigned to me"\>.
What it is, in one paragraph: \<what the codebase does, so an issue title makes sense\>.
Language and stack: \<...\>.
Where the code lives: \<the directories that matter, and what is in each\>.

## Which issues  ★ for batch

\<Say it in your own words. For example: all issues created in the last 7 days. Or: everything assigned to me. Or: open issues on the "Sprint 12" project board in the Ready column. Or: anything labelled bug or good-first-issue. Combine them if you want.\>

Issues per run: \<5\>.
Oldest first, so nothing starves.

## Never touch

\<Generated files, migrations, lockfiles, anything under infra/, the public API surface, the release workflow. One per line. The coder skips an issue rather than touching these.\>

## Always skip, beyond the standard rules

\<Issues labelled discussion or needs-design. Anything from an outside contributor. Anything touching auth or billing. Anything that needs a decision from me.\>

## House rules for the change

Match the conventions already in the file you are editing; they beat any general style rule.
\<Tabs or spaces, import style, error handling pattern, how tests are named if you add one, whether comments are wanted.\>
Keep the diff minimal. No unrelated tidy-ups in the same pull request.
\<Anything the linter will reject that you should know in advance.\>

## Pull requests

Draft pull requests only, against the base branch. Label: \<agent-draft\>.
Title format: \<#<issue> <what changed>\>.
Always include the block saying nothing was executed, and the commands I should run to verify.
Never merge, never push to \<main\>, never close an issue. I merge.

## Review

One review round and one fix pass, then the pull request comes to me whatever state it is in.
Focus the review on: \<correctness, breaking existing callers, error paths\>.
Do not raise: \<formatting, naming preferences, anything the linter already catches\>.

## Notification

Email me at the end of every batch: what got a pull request, what was skipped and why, what was unreachable, and what was above the cap.
