# Follow-up method: the follow-ups agent's map

Tasks produce loose ends. Someone comments on a post and asks for metadata on the blog and wants to see how it goes; a prospect says "reach out when X ships"; a reviewer says "check the number in two weeks"; the founder says "remind me to close the loop with the person from the cost thread". None of these are tasks in the plan, and all of them are the difference between a product people trust and one they forget. The follow-ups agent catches them, dates them, surfaces them until they are closed, and never lets one disappear because a week was busy.

## What counts

A follow-up is any of these, from any source:

- A person asked for something and it was not delivered in the same exchange.
- A promise was made in public (a post, a comment, an email, a call) to do or show something later.
- A prospect or user set a trigger ("come back when", "if you add X").
- A task's done note mentions a next step that is not itself a task.
- A review or a plan line says to check a number, a thread or a page on a later date.
- The founder said "remind me", "follow up", "check back", "don't forget", or dropped a note that reads like one.

Not a follow-up: a plan task (that is the dispatcher's), a decision (that is `decisions.md`), a metric to collect on schedule (that is the metrics agent's).

## Where they hide

Sweep these every run, newest first, only what is newer than the last sweep's log line:

1. `inbox/<product>/notes/`: every new note, every line.
2. `board/public/posts/`: posts from the dispatcher (done reports with mentions of asks) and the reviewer.
3. `tasks/<product>/backlog.md`: rows whose `notes` changed to `done` since the last sweep; read the notes column for next steps.
4. `reviews/<product>/`: the newest review's sections 5 and 7.
5. `list_sessions`: recent sessions on the pod's agents whose `lastPrompt` reads as an ask from the founder ("remind me", "follow up", "they asked"). Capture with source `session <id>`.
6. Published posts and threads named in the per-post table of `metrics.md`, when the prompt allows fetching: new comments that ask for something. Capture with the comment URL as source. Never reply; never log in.

## The record

`followups/<product>/followups.md`. A header, then one table:

| Column | Rule |
|---|---|
| `id` | `F-001` upward, stable. |
| `what` | The ask or promise in one line, in the asker's words where possible. |
| `who` | Who asked or who was promised: a handle, a name, a company, or `founder`. |
| `source` | Where it was found: the file, the post URL, the session id, the task id. Exact. |
| `captured` | Date. |
| `due` | The date it should be acted on: the date the asker named; else seven days after capture for a public ask; else fourteen days for "check how it goes"; else the plan date it references. |
| `owner` | `founder` when it needs a person (a reply, a send, a call); `pod` when an agent can produce the thing (a draft, a number, a page check), with the agent named. |
| `status` | `open`, `due`, `overdue`, `done`, `dropped`. |
| `closed` | Date and how: `2026-09-20 replied (URL)`, `dropped: superseded by T-041`. |

Dedupe on `what` plus `who`: the same ask from two sources is one row with both sources.

## Surfacing

Every sweep ends with a `pool_post` addressed to `marketing-dispatcher`, headed with the date, listing: overdue (id, what, who, days overdue), due today, due in the next two days. The dispatcher prints them in `today.md` and the lead's morning email carries them. An overdue follow-up is repeated every morning until closed; on the fifth repeat it is also posted to `marketing-lead` as a line for the weekly email.

## Closing

Close only on evidence: a reply URL, a sent email named in an inbox note, a task done whose done line satisfies the ask, or the founder's word in an attended session or an inbox line (`close F-012 replied`). A follow-up the founder decides not to honour is `dropped` with the why; never silently removed.

## Attended voice

When the founder opens a session and says "they asked for X on the blog post, want to see how it goes": capture it, read back the id, the due date and the owner in one line, and stop. When asked "what's open": the list, soonest due first, ids first. No em dashes.
