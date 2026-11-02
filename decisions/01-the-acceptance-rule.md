# Decision 01: the acceptance rule (the desk never accepts its own work)

Status: method v1. Binds every lane that produces work for a merge, a ship or the operator's eye.

## The problem it answers
The desk wrote both the claim and its acceptance. A lane's last line, or the desk's own belief, became DONE with nothing between it and the operator. Eleven failures in two days, every one covered by an existing rule, every one caught by the operator and none by the desk.

## The rule
1. **A DONE line is earned by a check the desk did not write.** Before any work is reported finished, an independent checker opens the actual result (the file, the page, the suite output, the diff) and compares it to the operator's words for that job. A lane's STATUS: COMPLETE is a claim, never a result. The DONE line quotes the checker's verdict and names what was opened and what was compared.
2. **A RUNNING line is earned in the lane's first minute.** The process is alive, the receipt exists, and the receipt names the intended folder and branch. A worktree exists only when `git worktree list` shows the intended path and a source file sits in it. A launcher that has not produced a live process and a receipt is not running and is not reported as running.
3. **What reaches the operator is only what the desk can show.** One plain line per finding: the thing, and what to do. Tallies and judge vocabulary stay in the landing files.

## The checker
Every lane gets an independent acceptance check before its DONE line: a checker from the other harness (Codex for Claude's work, Claude for Codex's) receives the operator's original words for the job and the lane's card, inspects the real worktree, the real startup, the real result and the live walk, and writes ACCEPTED or NOT ACCEPTED with the reason as the last line of its own file, beside the lane's receipt. The producing lane cannot write that file. The desk does not substitute its own verdict. The card shape is `cards/TEMPLATE-acceptance-card.md`.

## The mechanical check
`launchers/check-lane.ps1` prints, for a receipt and a worktree: live process, receipt present with its last STATUS line and age, worktree registered at the intended path with a source file present, branch as expected. The desk runs it before every RUNNING and DONE line.
