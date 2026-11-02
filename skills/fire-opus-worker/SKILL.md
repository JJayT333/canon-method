---
name: fire-opus-worker
description: Fire a Claude worker (Opus by default) as a background agent with a card and one output file. The card names its model and the desk fires; the lane never inherits the desk's model.
---
# fire-opus-worker

## Purpose
A bounded build, review or research job by a Claude model, in the background, writing one output file and its evidence, never touching the record beyond its own folder.

## When to use this
Big or long work for a Claude worker; the desk sends it to a lane (the law: every card names its model; a lane never inherits the desk's model).

## Inputs
- The operator's words for the job, verbatim, with the journal entry number.
- The lane folder: `record/landing/<job>-<MMDD>/`.
- The card on `cards/TEMPLATE-claude-lane-card.md`: line one names the model; what this is; the exact files to read and in what order; where it works (its own worktree and branch, never the operator's live checkout); the work itself; the checks to run; the live walk and its screenshots; the one output file; save as you go (the file in the first minute with STATUS: RUNNING, each finished part appended the moment it is done, never one write at the end); boundaries (the off-limits folders from the law; no merge; no push to main; no web unless named); under 200 lines; no em-dashes; a `Cost:` line at the end of the file and one message to the desk when the file ends STATUS: COMPLETE, a notification only, never a verdict.

## Steps
1. Write the card text; keep a copy in the lane folder as CARD.md.
1a. Gate the card before the fire: run `pwsh -NoProfile -File launchers/check_card.ps1 -Card <CARD.md>` from the method root (the same checker the Codex launcher runs, in its Claude lane form). Exit 0 only on PASS; a FAIL means the card is fixed and rerun before any Agent call. The lane's OUTPUT.md names the check result in its first lines.
2. Fire with the Agent tool: subagent general-purpose, the model the card names, run in the background, the card as the prompt, and the instruction to reply with only the output path and its last line.
3. Within the first minute run `launchers/check-lane.ps1 -Receipt <OUTPUT.md> -Repo <repo> -Worktree <worktree> -Branch <branch>`; write RUNNING only when the receipt exists and the worktree is on the intended branch.
4. When the completion notice arrives: open the output file in full; one plain line per finding reaches the operator, worst first; fix what is the desk's; a finding that needs the operator's word goes to NEEDS THE OPERATOR.
5. Freeze the branch and fire the checker from the other harness (skill fire-codex-checker) before any merge.

## Decisions
- If the job writes outside its folder, its worktree and its evidence, then it is NOT ACCEPTED and its writes are reverted.
- If a card tells the worker to write once at the end, then the card is wrong: fix it before firing; a worker already running without the save-as-you-go line gets it by message.
- If the worker asks a question, then the desk answers from the record or marks it OPEN; the worker never asks the operator.

## Definition of done
The output file exists with a verdict line; its findings are in the reply; the day note names it; the checker is fired or its card is ready.

## Edge cases
- Two workers on one folder overwrite each other; each worker gets its own folder.
- A review by a Claude worker is a read, not a test; its VERIFIED lines are what it opened, and a claim about runtime behavior needs a run, by the worker itself or by a checker that executes it.
- A stop click in the desk chat ends every background lane of that chat; list the agents and refire each from its OUTPUT.md.
