---
name: handoff
description: Write the desk handoff to the next session or tool: the product block first, then the operator's binding words, verified state, the plan, the rules that bit.
---
# handoff

## Purpose
The next director carries the operator's meaning forward without rebuilding it from commits.

## When to use this
The operator names another director, or the desk closes for the day, or a tool asks for the desk.

## Inputs
- The product note (its first block is copied verbatim).
- Today's journal: the entries tagged RULED and ORDER.
- The running list, the READY and FIRED cards, the day's landed lanes.
- The clock.

## Steps
1. Open with the product block, verbatim from the product note, before any worktree, receipt or gate.
2. The operator's words today that bind, one line each with the entry number.
3. State at close, each line verified by command this hour: running (with stop paths), committed (immutable hashes only), READY and unfired, landed, open decisions, untracked material.
4. The plan, numbered, in the operator's own shape.
5. The operator's standing instructions to the next director (model routing, spend, boundaries).
6. Rules that bit today, one line each with the register pointer.
7. Save it at `record/landing/DESK-HANDOFF-<date>.md` and, where the harness has a memory the next chat loads, there too. Never a file the operator must open or paste themselves; the next chat starts on one plain sentence and the record does the rest.
8. Point the running list and the day note at it. Commit.

## Decisions
- If the product changed this session, then update the product note first and say so in the handoff.
- If a fact is mutable (branch tips, dirty trees), then write the command, not the value.

## Definition of done
The file exists, opens with the product block, and an independent reader can find no ruling of the operator's that it fails to carry.

## Edge cases
- READY means: a card with mechanical steps, a landing folder on disk, fireable in under two minutes with zero decisions. A file existing is not READY.
- A readiness claim about a path the operator will walk needs a receipted execution of that path first, from their own entry door.
- A packet crossing tools opens with five plain lines (what this is, what it asks, what it changes, what happens if ignored, current status); a long packet may still only ask a one-sentence question.
- A handoff that buries the product under mechanics costs the next morning; lead with the product.
