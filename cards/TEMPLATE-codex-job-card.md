Runs on: <model, e.g. the Codex engine's default> (<why this model and route: the one checker from the other harness, or the build worker the desk picked>)
Family: <A make or fix, B check, C files and records, D find out, E build with proof, F write, G repair a tool>

OBJECTIVE: <One sentence: what exists when this is done.> Operator's words (<YYYY-MM-DD HH:MM>): "<the words, verbatim>". Why: <one line on the reason behind the words>.

STARTING STATE: <Worktree path, branch, head commit, clean or not, how many commits above the base, pushed or not, FROZEN or live. The record folder for this card. The previous card on the subject if any.>

SAVE AS YOU GO: Create <record folder>/OUTPUT.md in your first minute with Execution: running, Review: pending and STATUS: RUNNING as its last line. Append each finished part the moment it is done. At the end, replace the last line with the verdict. Generated evidence only under <record folder>/evidence/; build output, caches, browser profiles and test temp under evidence/generated/.

READ FIRST: <the files, in order>.
READ AND SKIP: <what to open only to confirm it is out of scope>.

SCOPE: in: 1. <numbered requirement>. 2. <numbered requirement>. 3. <...>. Out: <what is not this card's>. Do not touch: <the operator's live checkout; other branches; no commit to main, no push to any remote but <HUB-REMOTE>, no network beyond what the card names, no install beyond what is already placed; kill only processes you start>.

STEPS: <1 to N, in order, each one checkable>.
WHAT GOOD LOOKS LIKE: <every claim backed by your own run with the command and the number; the exact shape of a good last line>.
WHAT BAD LOOKS LIKE: <a named failure mode and what to do instead, in the same clause>. BAD EXAMPLE: "<a one-line example of a bad result>".

DONE WHEN: <the exact condition: the file holds the N results, each claim labeled, and the last line is exactly one of ACCEPTED: ..., ACCEPTED WITH FINDINGS: ... or NOT ACCEPTED: ..., then Execution: complete, Review: passed or failed>.
VERIFY: <who checks this card's result and on what; for a checker card, "this is the verification of <lane> on its frozen head">.
TIME LIMIT: <N> hours.
RETURN: every claim labeled VERIFIED, INFERRED, UNVERIFIED or NOT FOUND; end with a MISSING FACTS list. No em-dashes. PowerShell 7 (pwsh) for shell. If rg is not installed, search with Select-String, git grep or Python.
