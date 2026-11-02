---
name: sweep-landing
description: Sweep every landing zone for reports, receipts and handoffs from other tools and lanes; bank their quoted operator words; put their NEEDS THE OPERATOR lines in the roadmap.
---
# sweep-landing

## Purpose
Anything settled in another tool lands back in the record or it is lost; the operator is never the message bus.

## When to use this
Every desk open; when the operator says sweep; when a lane lands.

## Inputs
- `record/landing/**` and every `<project>/.canon-return/**`.
- A cutoff: files newer than the last sweep (the previous day's journal file is a safe cutoff).

## Steps
1. List files newer than the cutoff, by zone. A time-out is a result: split the search by zone rather than one `find` over everything.
2. For each report or handoff: read it in full; bank its quoted operator words into the journal with the source path named; its NEEDS THE OPERATOR lines go to the roadmap; its DONE claims are claims until the desk opens the result.
3. For each lane receipt: last line STATUS; process alive or gone; a RUNNING receipt with a dead process is DEAD.
4. Note the sweep in the day note: zones, cutoff, counts, what was banked.

## Decisions
- If a landing file asks for a fire, then it goes to COULD BE RUNNING, never fired from the file.
- If a report contradicts the record, then the record wins until the operator rules; the contradiction goes to NEEDS THE OPERATOR.

## Definition of done
Every new file is named in the day note with what was done with it.

## Edge cases
- Evidence folders hold gigabytes (test caches, screenshots); never `git add` them; never `find` into a test temp folder (permission denied is noise).
