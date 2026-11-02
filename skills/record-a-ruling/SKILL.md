---
name: record-a-ruling
description: Write one of the operator's rulings into the record: the decision file when it binds future work, the settled entry, the day note, a corrections entry when the desk was wrong. Run after bank-words, the same turn.
---
# record-a-ruling

## Purpose
The ruling reaches the files the next session reads, in the operator's words, with plain names first.

## When to use this
The operator rules, orders or corrects, and the ruling binds work beyond this turn.

## Inputs
- The journal entry (entry number, clock, verbatim quote).
- The next decision number (`ls decisions | tail -1`).
- The registers: `record/registers/settled.md` (the map of rulings), `corrections.md` (the desk's failures), `craft.md` (method lessons).

## Steps
1. Bank the words first (skill bank-words).
2. If it binds future work: `decisions/NN-<plain-slug>.md` with: title, date and status, the operator's words verbatim, the ruling as numbered points, what it replaces (a dated supersession banner on the file it replaces), the desk's own additions labeled as the desk's, why, and the receipt (day note entry).
3. settled.md: one entry, `[<date> N#] (the operator, clock): **Plain name (decision NN).** Words: "..." What changes, one line.`
4. corrections.md when the desk was wrong: the quote, what the desk did, the fix, the lesson. craft.md when a method lesson came out of it.
5. The day note: one entry saying what was written and where.
6. Surfaces that state it (the product note, the running list) get their line; commit with a plain summary.

## Decisions
- If the ruling restates an earlier ruling, then it is banked as RULED and the earlier decision gets a dated amendment, not a new file.

## Definition of done
The words are in the journal and in the decision; the settled entry exists; the day note names both; the commit exists.

## Edge cases
- Times come from the clock, never estimated.
- A desk-added number (a term, a cap, a threshold) is labeled as the desk's in the decision, every time.
