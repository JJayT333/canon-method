# CARD: <plain title> (<date>, fired <clock> by the desk)

Model: <the model, e.g. claude-opus-5-5>. This card names its model; the lane never inherits the desk's.

Operator's words, verbatim: <entry number> <clock> "<the words>"; <entry number> <clock> "<the words>".

## What this is
<One paragraph: a build lane, a research lane or a review lane, on what, off which branch. Decision 02: create the output file in your first minute and append each part the moment it is done. Decision 03: no screenshot, no done.>

## Read first
<The files, in order, with paths. The last card on this subject if there was one.>

## Where
- Repo <path> (remote `<HUB-REMOTE>` is the only remote you push to; never add another). Do not touch the operator's live checkout at <path>.
- Your worktree: `git -C <repo> worktree add <worktree path> -b <branch> <base>` (confirm the base commit and write it in OUTPUT.md).
- Output file (first minute, STATUS: RUNNING): <record folder>/OUTPUT.md. Screenshots and small metrics in the same folder; large traces to <archive path>, never into the record.
- Ports: use <port>. Never <the operator's ports>. Headless browser only; nothing opens on the operator's screen.

## The work, one commit each
1. <Fix or feature 1: what, where (file and line), how to prove it (before and after numbers, the screenshot name).>
2. <Fix or feature 2.>
3. <Fix or feature 3.>

Do not touch: <the areas that stay as they are>. No new dependencies. No other refactors.

## Checks (worktree root)
<The exact commands: typecheck, build, unit. Report each result line verbatim and the test counts. Fix shared modules, not tests.>

## Walk
Headless, the app on its own port, no paid calls: <the exact screens, clicks and screenshot names>; console error counts before and after per screen against the baseline <numbers>.

## Commit and push
<N> commits, plain messages. `git push <HUB-REMOTE> <branch>`. Never main, never another remote, never merge. Freeze the branch when OUTPUT.md says COMPLETE; a checker from the other harness runs on the frozen head.

## Boundaries
Never <OFF-LIMITS-FOLDERS>. No web unless named above. No other agents. No operator data into the repo. If a check, a proof or the walk cannot run, say why and end STATUS: FAILED, never COMPLETE.

## OUTPUT.md shape
Five plain lines first (STATUS, branch and head, each piece of work in one line with before and after, checks in one line). Then READ, WORK 1, WORK 2, WORK 3 (each: files and lines changed, the before and after table, screenshots named), CHECKS (verbatim), FINDINGS worst first (anything you would not touch without the operator's word), a verdict line, `Cost:`. Under 200 lines. No em-dashes. Reply at the end with only the OUTPUT.md path and its last line.
