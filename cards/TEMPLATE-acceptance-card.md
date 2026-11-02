Runs on: <the checker's model> (the one checker from the other harness before a merge, decision 01; the checker did not do the work and may not fix it)
Family: B, Check

OBJECTIVE: The verdict on <the lane> on its frozen head <commit>, before the desk merges it. Operator's words (<YYYY-MM-DD HH:MM>): "<the words the lane was built from, verbatim>". Why: <one line>.

STARTING STATE: Worktree <path>, branch <branch>, clean at <commit>, <N> commits above <base>, pushed to <HUB-REMOTE>, FROZEN: nothing will be committed to it while you run. The lane's card and record: <record folder> (CARD.md; OUTPUT.md; screenshots under evidence/). <The previous verdict file if this is a recheck; its findings stand and its scripts under evidence/ may be reused where unchanged.>

SAVE AS YOU GO: Create <acceptance folder>/ACCEPTANCE-<lane>-<date>.md in your first minute with Execution: running, Review: pending and STATUS: RUNNING as its last line. Append each finished check the moment it is done. At the end, replace the last line with the verdict line. Generated evidence only under <acceptance folder>/evidence/; build output, caches, browser profiles and test temp under evidence/generated/.

READ FIRST: the lane's OUTPUT.md whole; `git log --oneline <base>..<commit>`; `git diff --stat <base>..<commit>`; the diffs in full.
READ AND SKIP: <the areas ruled out of scope by the desk>.

SCOPE: in: 1. The lane ran where it was told: `git worktree list` shows the assigned path on the assigned branch at <commit>, clean; confirm at start and again at the end (a moved branch is NOT ACCEPTED). 2. The lane started for real: OUTPUT.md was created in the first minute and appended over time, not written once at the end. 3. The result is what the operator asked for, not what the lane says it did: for each requirement in the words above, name the file and line that satisfies it, or write NOT MET with what is there instead; a requirement the lane reinterpreted is NOT MET. 4. The live walk, your own: run the app headless on port <port> from the worktree, drive <the exact screens and clicks>, screenshot each into evidence/, count console errors per screen against the lane's baseline <numbers>. 5. The gate, your own isolated run at <commit>: <the exact typecheck, build and unit commands>, output and temp under evidence/generated; quote each result line verbatim. 6. Scope: the diff touches only <the files the lane's card allowed>; anything else is a finding, and good work outside scope is still NOT ACCEPTED. Out: style opinions; anything the desk ruled. Do not touch: the branch (read-only except evidence); the operator's live checkout <path>; no commit, no push, no network, no install beyond what is already placed; no fix of any kind; kill only processes you start.

STEPS: 1 to 6, then the verdict.
WHAT GOOD LOOKS LIKE: every claim checked by your own run with the command and the number; ACCEPTED, ACCEPTED WITH FINDINGS (lows logged) or NOT ACCEPTED with the first unmet requirement and its file and line.
WHAT BAD LOOKS LIKE: reusing the lane's own numbers as your result (instead: your own run at <commit>); failing the lane for something the desk ruled out of scope (instead: log it as a finding and judge the scope as written). BAD EXAMPLE: "NOT ACCEPTED: the lane's OUTPUT.md says the tests passed, so I agree".

DONE WHEN: the acceptance file holds the six results, each claim labeled, and the last line is exactly one of ACCEPTED: ..., ACCEPTED WITH FINDINGS: ... or NOT ACCEPTED: ..., then Execution: complete, Review: passed or failed.
VERIFY: this is the verification of <the lane> on its frozen head (checker 1 of 1; a recheck names the previous verdict file).
TIME LIMIT: 2 hours.
RETURN: every claim labeled VERIFIED, INFERRED, UNVERIFIED or NOT FOUND; end with a MISSING FACTS list. No em-dashes. PowerShell 7 (pwsh) for shell. If rg is not installed, search with Select-String, git grep or Python.
