---
name: fire-codex-checker
description: Fire the independent acceptance checker from the other harness on a landed lane. The desk never accepts its own work.
---
# fire-codex-checker

## Purpose
An independent reader writes ACCEPTED or NOT ACCEPTED to its own file; the desk's DONE line quotes it.

## When to use this
Before a merge, a ship or a changed tool. When the work is Claude's, the checker is a Codex job; when the work is Codex's, the checker is a Claude lane on the same card shape. Not after every run.

## Inputs
- The operator's words for the job, verbatim.
- The lane's card, output file, worktree and branch, frozen at a named head, and the files it changed.
- The template `cards/TEMPLATE-acceptance-card.md`.
- A dedicated acceptance folder under `record/landing/`, outside every product source tree, holding the verdict file and an `evidence/` subtree for all generated logs, profiles, screenshots, test temp and caches.
- The launcher `launchers/fire-codex-job.ps1` (a Codex checker) or the Agent tool (a Claude checker).

## Steps
1. Write the checker card from the template: the operator's words; what the lane was told; the checks in order (ran where told; started for real; the result against each requirement with file and line; the live walk rerun; the gate rerun with last lines quoted; scope); one verdict file plus the evidence subtree; save as you go (the verdict file in the first minute, each check appended the moment it is done). Product source is read-only for the checker; no fix of any kind.
2. Run `python tools/card_check.py <CARD.md>`; fix every FAIL.
3. Fire: `pwsh -NoProfile -File launchers/fire-codex-job.ps1 -Card <CARD.md> -Cwd <the lane's worktree> -Model <model>` for Codex; the Agent tool for Claude. Read the clock.
4. First-minute check: `launchers/check-lane.ps1 -Receipt <verdict file> -Repo <repo> -Worktree <worktree> -Branch <branch>`. A missing receipt, a read-only sandbox that blocks the evidence write, or a card the worker cannot read means BLOCKED, not RUNNING.
5. Write RUNNING only after that check, with the process identity and the exact stop action.
6. When the worker finishes: open its verdict file; the last line is the verdict. Review field: passed for ACCEPTED, failed for NOT ACCEPTED; a checker that cannot run is reported once and leaves review pending. A missing verdict means no acceptance, whatever the exit code. One plain line per finding reaches the operator, worst first; tallies stay in the file.
7. NOT ACCEPTED: a fix round on the lane's branch, then a recheck on the new frozen head; the old verdict file is kept. At most five rounds, three when a round makes no progress (decisions/04-the-redo-cap.md).

## Decisions
- If the checker's file never gets its verdict line and the process is gone, then the check is DEAD; say so; refire only on the operator's word.
- If the checker finds something outside its card, then it still counts; scope cuts only what it may change, not what it may see.
- If the branch moved during the check, then the verdict is NOT ACCEPTED and the recheck runs on the new frozen head.
- Do not relaunch the same blocked runtime with unchanged conditions; a retry needs a specific, evidenced correction.

## Definition of done
The verdict line exists, the job's review field carries it, it is quoted to the operator, and the follow-ups are on the running list.

## Edge cases
- A checker's own generated evidence (fresh runtime, screenshots, test fixtures) is allowed under its evidence subtree; source edits are never allowed.
- A slow checker is RUNNING until its process is gone; one once wrote its verdict three days after its fire.
- Merge only on the operator's word; after a merge the full suite runs on the merged tip and its count goes in the day note.
- The log stream can be hundreds of kilobytes; never open it whole; tail it.
