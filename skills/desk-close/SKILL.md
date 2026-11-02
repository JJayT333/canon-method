---
name: desk-close
description: Close the desk. Run on "wrap up", "close", a handoff order, or when the operator names another chat or tool as the next director.
---
# desk-close

## Purpose
Leave the record in a state the next session can open from without rebuilding anything.

## When to use this
The operator says wrap up, close, hand off, or names another director (a new chat, the other harness).

## Inputs
- Today's day note and journal.
- The running list (every lane the desk started today, with its stop path).
- The live process list, the worktree lists, every lane receipt touched today.

## Steps
1. Bank the operator's closing words verbatim with the clock minute.
2. Verify by command: nothing the desk started is running, or each running thing has a stop path in the handoff.
3. If the product changed this session, update the product note and date it.
4. If handing off, run `handoff`.
5. Write the three close-out lines in the day note: what we did, what the operator decided, what is next.
6. Bring the running list to the closing state (every lane the session touched, with its proof).
7. Commit with a plain summary. Delete `.desk-lock` (only your own).
8. Report: DONE names the commit and the lock; RUNNING lists anything alive with its stop path.

## Decisions
- Ninety seconds: the close is three lines and a commit, not a session of its own. Status surfaces update on material change only.
- If a lane is mid-flight, then it stays running and the handoff carries its stop path; never kill at close unless the operator said ABORT.
- If the lock is not yours, then delete nothing and say so.

## Definition of done
Three lines in the day note, one commit, no lock of yours, the handoff present if handing off, and the reply names all of them.

## Edge cases
- The operator keeps talking after the close: answer as landing-only unless they order a write; then take the lock with a note and release it after.
- Untracked evidence folders (gigabytes) stay untracked; say so, never `git add -A` at the root.
