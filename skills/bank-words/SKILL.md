---
name: bank-words
description: Bank one message of the operator's verbatim into today's journal with the clock minute and a tag. Run the moment they say anything, before any work.
---
# bank-words

## Purpose
The operator's words are the asset; paraphrase destroys them. Every message lands verbatim, timestamped, tagged, before work starts.

## When to use this
Every message from the operator, every time, including greetings, dismissals and cut-off sentences.

## Inputs
- The message, exactly as typed or dictated, typos kept.
- The clock minute (`date +%H:%M`), read now, never estimated.
- Today's `<JOURNAL-PATH>/<date>-words.md` (create with the day's header if absent).
- The next entry number (count the existing `[N` entries).

## Steps
1. Read the clock.
2. Read `.desk-lock`. If it is not yours: write the entry to `record/landing/<engine>-AFTER-CLOSE-<date>.md` for the desk to sweep, and stop here; no journal write, no commit.
3. Append `[N#] HH:MM TAG (typed or dictated, which window):` then a blank line, then the message as a `>` quote, line breaks kept.
4. Tags: RULED, ORDER, THOUGHT, CORRECTION, OPEN, ASK; more than one joined with a slash.
5. Under it, one "Desk reading" line only when the reading is not obvious: which repo an "it" names, what a garble is taken as, what is OPEN.
6. A cut-off sentence gets its last words kept and OPEN; ask only if the ending changes what you would do.
7. Commit after the bank, or with the work it triggers, whichever is sooner.
8. Show the banked entry in the reply in one line: entry number, the saved line, file, commit.

## Decisions
- If a number or a name was dictated and could be misheard, then check it back in the reply; never put it on a card unchecked.
- If the message is an answer to a box of options, then bank the box's question and the pick together.

## Definition of done
The entry exists with a real clock minute, the words verbatim, a tag, and it is committed or landed.

## Edge cases
- Two messages in one turn: two entries, in order.
- A message that restates a ruling is banked as RULED, not THOUGHT.
- Never label time by feel: a desk that estimated the clock once drifted five hours in a day.
