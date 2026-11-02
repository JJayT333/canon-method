---
name: abort-and-pause
description: ABORT in capitals stops everything the desk started; pause stops nothing and brings the running list current.
---
# abort-and-pause

## Purpose
The operator's two stop words, mechanical.

## When to use this
ABORT in capitals in any window; or the word pause.

## Inputs
- The running list (every lane the desk started, each with its stop path).
- The live process list.

## Steps
1. ABORT: for each RUNNING line, run its stop path (the lane's stop script, or end the named process after checking its start identity). Touch nothing the operator or another chat started.
2. ABORT: report STOPPED, COULD NOT STOP, UNTOUCHED, one line each per process. No new work until the operator's next word.
3. pause: stop nothing; finish the write in hand; bring the running list current; report in one screen; wait.

## Decisions
- If a process's start time does not match its recorded identity, then it is not stopped and goes under COULD NOT STOP with the reason.
- If a tool session reads ABORT, then it writes the same three lists to its landing file.

## Definition of done
Every RUNNING line is in one of the three lists; the running list says so.

## Edge cases
- Lower-case "abort" or "stop" in a sentence is not the word; only ABORT in capitals stops things.
