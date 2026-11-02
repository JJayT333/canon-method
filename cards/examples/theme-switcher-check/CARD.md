Runs on: the Codex engine's default model (the one checker from the other harness before a merge, decision 01; the build was a Claude lane, so Codex checks it)
Family: B, Check

OBJECTIVE: The verdict on the Claude theme-switcher lane for the sample web app, on its frozen head, before the desk merges it. Operator's words (2026-01-15 09:12): "three themes, that is all, and remember which one I picked when I come back". Why: the old switcher listed seven themes and forgot the pick on reload.

STARTING STATE: Worktree <repo_root>-theme-switcher-0115, branch claude/theme-switcher-0115, clean at the head the desk writes here, three commits above hub/main, pushed to hub, FROZEN: nothing will be committed to it while you run. The lane's card and record: record/landing/theme-switcher-build-0115/ (CARD.md; OUTPUT.md with CUT, PERSIST, CSS, CHECKS and WALK sections; screenshots under evidence/).

SAVE AS YOU GO: Create record/landing/theme-switcher-check-0115/ACCEPTANCE-theme-switcher-0115.md in your first minute with Execution: running, Review: pending and STATUS: RUNNING as its last line. Append each finished check the moment it is done. At the end, replace the last line with the verdict line. Generated evidence only under record/landing/theme-switcher-check-0115/evidence/; build output, caches, browser profiles and test temp under evidence/generated/.

READ FIRST: the lane's OUTPUT.md whole; `git log --oneline hub/main..HEAD`; `git diff --stat hub/main..HEAD`; the three diffs in full.
READ AND SKIP: the colors inside each theme file (ruled out of scope by the desk); the build pipeline.

SCOPE: in: 1. The head matches the lane's OUTPUT.md and git status is clean; confirm at start and again at the end (a moved branch is NOT ACCEPTED). 2. The list: src/theme/themes.ts is exactly light, dark, high-contrast, default light; a stored value outside the three falls back to light. 3. The pick persists: useTheme.ts reads and writes one localStorage slot; your own walk proves it (below). 4. No dead CSS: grep src for the removed data-theme values; each hit is gone or named in the lane's FINDINGS. 5. Your own headless walk from the worktree (Playwright, chromium), Vite only on port 5615, never the operator's ports: fresh context opens in light; the switcher shows exactly three; click dark, reload, still dark; click high-contrast, reload, still high-contrast; screenshot each state into evidence/; console errors per screen against the lane's baseline (0). 6. The gate, your own isolated run from the worktree root with output under evidence/generated: `npm run typecheck`, `npm run build`, `npm test`; quote each result line verbatim. 7. Scope: the three commits touch only src/theme/** and its tests; anything else is a finding. Out: style opinions on the three themes. Do not touch: the branch (read-only except evidence); the operator's live checkout; no commit, no push, no network, no install beyond what npm ci already placed; no fix of any kind; kill only processes you start.

STEPS: 1 to 7, then the verdict.
WHAT GOOD LOOKS LIKE: every claim checked by your own run with the command and the number; ACCEPTED, ACCEPTED WITH FINDINGS (lows logged) or NOT ACCEPTED with the first unmet requirement and its file and line.
WHAT BAD LOOKS LIKE: reusing the lane's screenshots as your walk (instead: your own run at the frozen head); failing the lane for the colors of a theme (instead: log it as out of scope). BAD EXAMPLE: "NOT ACCEPTED: the dark theme should be bluer".

DONE WHEN: the acceptance file holds the seven results, each claim labeled, and the last line is exactly one of ACCEPTED: ..., ACCEPTED WITH FINDINGS: ... or NOT ACCEPTED: ..., then Execution: complete, Review: passed or failed.
VERIFY: this is the verification of the theme-switcher lane on its frozen head (checker 1 of 1).
TIME LIMIT: 2 hours.
RETURN: every claim labeled VERIFIED, INFERRED, UNVERIFIED or NOT FOUND; end with a MISSING FACTS list. No em-dashes. PowerShell 7 (pwsh) for shell. If rg is not installed, search with Select-String, git grep or Python.
