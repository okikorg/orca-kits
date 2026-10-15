# Cram Coach

Give Cram Coach one textbook chapter as a PDF and your exam date, and it saves four files: `cram-plan.md`, a day-by-day plan worked back from the exam, hardest topics first, with a review day before it; `flashcards.csv`, cards that import into Anki; `practice-test.md`, 10 to 15 questions in the chapter's style; and `answers.md`, each answer cited to its section and page. It uses only what the chapter says. Limits: text PDFs only (on a scan it says so and stops; no OCR), one chapter per run, no reminders, and for now PDFs under 48 KB.

## Example

> My exam is on 2026-10-22.

Chapter 3, Demand and Supply. You have 7 days to the exam. Created 28 flashcards and 12 practice questions.

Files: `cram-plan.md`, `flashcards.csv`, `practice-test.md`, `answers.md`

A real run on 2026-10-15. It cost $0.02 of Orca credit.

## What it uses

Model calls on `orca/openrouter/openai/gpt-5.6-luna`, paid from your Orca credit, and a sandbox where it reads the PDF with Python, so it uses machine time. See [pricing](https://orcapods.ai/pricing).

## Add it

```bash
orca kits copy https://app.orcapods.ai/kits/kit-KDdGOG9YTLrtpQs64 --yes
```

Or click **Copy** on [the kit's page](https://app.orcapods.ai/kits/kit-KDdGOG9YTLrtpQs64).

## Use it

From the CLI (the dashboard cannot attach a PDF to a chat yet), with your own chapter or [this sample](https://github.com/okikorg/orca-kits/raw/main/kits/cram-coach/chapter.pdf):

```bash
orca chat cram-coach --sandbox --file chapter.pdf "My exam is on 2026-10-22."
```

Then `orca sessions artifacts download session_... --all` saves the files and `orca sessions delete session_... --yes` stops the sandbox. In Anki, File, then Import, opens `flashcards.csv` with its fronts and backs.
