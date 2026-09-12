# Release notes: the smallest useful kit

One agent and one skill. Hand it a list of merged pull request titles and it returns three
sections, Added, Fixed and Changed, then a final line naming the pull requests it deliberately
left out.

It exists to be read rather than to be impressive. It is the worked example in
[Build it with your coding agent](https://docs.orcapods.ai/build-with-your-coding-agent), and it
is the smallest thing that shows the split every other kit in this repo is built on:

- **The agent** (`agents/release-notes.yaml`) owns the shape of one answer: three sections in
  that order, then the Dropped line. Change this when the output's form is wrong.
- **The skill** (`skills/release-notes-style/SKILL.md`) owns the house rules every writing agent
  should share: what counts as user-visible, how an entry reads, what never appears. Change this
  when the judgement is wrong.

Get that split right and the next writing agent you build inherits the rules for free. Get it
wrong and you paste the same paragraph into every agent until the copies disagree.

## Install

```bash
orca skills import ./skills/release-notes-style
orca agents create -f agents/release-notes.yaml
```

The skill goes first: the agent document names it, and the server checks that it exists.

## Run it

`prs.txt` is a test input with traps in it. Three entries are real, one is a performance change
that lands in the wrong section if the agent is careless, and three must not appear at all.

```bash
orca run release-notes "Turn these merged pull requests into release notes.

$(cat prs.txt)"
```

What you should get back:

```text
## Added
Added library rows to the navigation, and a session list on the Sessions page.
Granted new organizations a signup credit, with a receipt by email.

## Fixed
Deleted the sandboxes of idle sessions, and reclaimed orphans left behind by a runner.

## Changed
Dispatches 100 tool calls in 0.3 ms, was 1.1 ms.

Dropped: #940, #936, #930
```

The wording varies between runs. Three things should not: the three headings in that order, the
performance entry under Changed rather than Added, and the Dropped line naming exactly the
dependency bump, the test and the refactor. That is the whole test and it reads in two seconds.

## Make it yours

Swap the sections for your own (`Shipped`, `Fixed`, `Known issues`), or the input for commit
subjects, a changelog, or closed issues. The two files are the artefact; the copy in your
workspace is a deployment of them.

When the output disappoints, the fix belongs in exactly one of four places. The
[guide](https://docs.orcapods.ai/build-with-your-coding-agent#which-file-does-this-belong-in) has
the table.
