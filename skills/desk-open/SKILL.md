---
name: desk-open
description: Open the desk for a session. Run on "good morning", "pick up the desk", or any first message of a new desk chat.
---
# desk-open

## Purpose
Open the desk so the first reply is a roadmap built from the record, not from memory.

## When to use this
The first message of a new desk chat, whatever it says, unless it is ABORT.

## Inputs
- `.desk-lock` at the method root (present or absent).
- Yesterday's and today's journal files, `<JOURNAL-PATH>/<date>-words.md` (on the first day, neither exists yet).
- The last handoff (`record/landing/DESK-HANDOFF-<date>.md`), read in full.
- The landing zones: `record/landing/**` and every `<project>/.canon-return/**`.
- The clock, read by command before every bank: `Get-Date -Format HH:mm` in PowerShell, `date +%H:%M` in a POSIX shell.

## Steps
1. Read `.desk-lock`. Absent: write it (session name, clock, writer). Present with another writer: say its name and time in one line; if the operator is talking to you, take it and note that you took it; otherwise landing-only. A worker never takes the lock.
2. Read yesterday's journal in full, then today's if it exists.
3. Read the last handoff in full, then every file it names as "start here".
4. Sweep the landing zones (skill sweep-landing). For each report from a lane or another tool: bank its quoted operator words into the journal with the source named; put its NEEDS THE OPERATOR lines in the roadmap.
5. Run `orphan-sweep` in dry-run and take the count.
6. Verify by command anything you will state as running: process list, worktrees, receipts. A file's claim is not liveness.
7. Bank the operator's first message verbatim with the clock's minute (skill bank-words).
8. Reply with the roadmap: line one names the model on the wheel and the orphan count; one line naming what was opened in step 3, so the review is evidence, not a claim; the ordered day, one line per item with its state and fire word; nothing fires.
9. Commit with a plain summary.

## Decisions
- If a handoff says a product changed, then update the product note before the roadmap.
- If two handoffs disagree, then the later one governs and the disagreement goes on the roadmap as OPEN.
- If the first message is a question about the product, then answer it after steps 1 to 7, never before step 3.

## Definition of done
The lock is yours; the journal has today's first entry with a clock minute; the roadmap reply names the model, the orphan count and what was opened; the commit exists.

## Edge cases
- First open ever: no journal, no handoff, no landing files. Create `.desk-lock`, today's journal with its header, `record/notes/<date>.md` (the day note), `record/RUNNING.md` (the running list) and `docs/THE-PRODUCT.md` (one paragraph on what is being built), say in the roadmap that this is the first open, and go on. See the README's section on the record files.
- A checker or lane from yesterday is still alive: it goes in RUNNING with its stop path, never restarted.
- The model on the wheel may differ from yesterday's; say which model it is in line one.
- A corrupted surface (mojibake, tripled blank lines) is rebuilt from HEAD's structure keeping its added lines; say so in the day note.
