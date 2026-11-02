---
name: develop-prompt
description: Turn the operator's dictated intent into one finished card for any worker or model, by interview, before anything fires. Run on "help me develop the prompt", "write the card", "make the prompt for", or a half-formed idea the operator wants a worker to do.
---
# develop-prompt

## Purpose
The dictation carries the intent; a worker needs a card with no gaps. This skill closes the gaps by asking the operator only what the record cannot answer, then writes one card they can read in one screen and fire with one word. It never adds scope they did not state and never fires the card itself.

## When to use this
The operator names a job for a worker (a Codex job, a Claude lane, a checker, another chat) and the card does not yet exist, or an existing card is missing one of the nine fields.

## Inputs
- The operator's words, verbatim, from today's journal (bank first, skill bank-words).
- The record for the subject: the matching skill, the last card on the same subject under `record/landing/`, the product note if the subject is the product, the last three days of the journal.
- The model and route rules from the law: every card names its model; the desk may suggest a route with its reason and waits for the operator's pick.
- The card templates in `cards/` and the checker `tools/card_check.py`.

## Steps
1. Bank the words. If a skill already covers the job, the card runs that skill by name and this skill only fills its inputs.
2. Draft the nine fields from the words and the record, each labeled VERIFIED (the record settles it), INFERRED (the desk's reading, one line why) or OPEN (nobody knows yet): objective; verified starting state (checked by command this turn); scope, with the explicit not-in-scope line; first action; sequence and dependencies; owners (which model, which lane, who checks); deliverable (the output file path, created in the first minute); verification (the independent checker and what it opens); exact finish condition.
3. Put every OPEN field to the operator in one packed round of options (two to four each, a recommendation, what each costs), chained until no field is OPEN. INFERRED fields are shown as one line each; the operator corrects or lets them stand.
4. Write the card as one file under `record/landing/<job>-<mmdd>/CARD.md` on the matching template: line one names the model with its reason; the fields in order; the save-as-you-go line (create the output file in the first minute with STATUS: RUNNING, append each finished part the moment it is done); the proof rule (every claim labeled, NOT FOUND beats filler); the stop rule (two failed fixes of the same problem stop the work and report both attempts and the blocker). Nothing else: no footers, no rules the operator did not state.
5. Run `python tools/card_check.py <CARD.md>` and fix every FAIL before showing it.
6. Read the card back on screen as an event sequence: what fires, what lands, what the operator sees, what ends it. Do not fire.
7. On the fire word, the send goes by the standing route: the Codex launcher or the Agent tool. Never a paste for the operator to carry.

## Decisions
- If the subject already has a card that failed or stalled, then the new card names the old one and states what changed, never a silent rewrite.
- If a field would widen the scope beyond the words, then it goes in the not-in-scope line, and one option asks whether the operator wants it in.
- If the card is for another chat rather than a worker, then it lands in the file that chat reads, not in a paste.
- If the operator says "just write it", then INFERRED stands for every field the record supports and only true OPEN fields are asked.

## Definition of done
CARD.md exists with all nine fields, none OPEN, line one the model, the save-as-you-go line present, the checker passes, no added scope; the operator has seen the event sequence; the card has not fired.

## Edge cases
- A cut-off dictation: the last words stay in the card as a quoted OPEN line until the sentence is finished.
- A card for a checker: the objective is the verdict, the deliverable is the verdict file, and the checker never gets the lane's own claims as inputs.
- A research card: the first action is always the sources already held before any new search.
