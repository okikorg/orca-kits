# Cram Coach

Give Cram Coach one textbook chapter as a PDF and your exam date, and it saves four files: `cram-plan.md`, a day-by-day plan worked back from the exam, hardest topics first, with a review day before it; `flashcards.csv`, cards that import into Anki; `practice-test.md`, 10 to 15 questions in the chapter's style; and `answers.md`, each answer cited to its section and page. It uses only what the chapter says. Limits: text PDFs only (on a scan it says so and stops; no OCR), one chapter per run, and no reminders.

## What it uses

Model calls on `orca/openrouter/openai/gpt-5.6-luna`, paid from your Orca credit, and a sandbox where it reads the PDF with Python, so it uses machine time. See [pricing](https://orcapods.ai/pricing).

## Add it

Click **Get started** on the kit's page. Or create the same agent from code with [agent.py](https://github.com/okikorg/orca-kits/blob/main/kits/cram-coach/agent.py) or [agent.ts](https://github.com/okikorg/orca-kits/blob/main/kits/cram-coach/agent.ts).

## Use it

From the CLI (the dashboard cannot attach a PDF to a chat yet):

```bash
orca chat cram-coach "My exam is on 2026-10-23." --file chapter.pdf
```

The last line names the session: get the files with `orca sessions artifacts download session_... --all`, then `orca sessions delete session_... --yes`. To make it yours, change its instructions with `orca agents update`, for example the number of cards or the length of a session.
