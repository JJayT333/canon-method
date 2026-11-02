Runs on: the Codex engine's default model (the desk's pick for a small, well-bounded front-end build; a Claude checker follows, decision 01)
Family: A, Make or fix

OBJECTIVE: The sample web app has a theme switcher with exactly three themes (light, dark, high-contrast), the choice persists across reloads, and the page renders with no console errors in each theme. Operator's words (2026-01-15 09:12): "three themes, that is all, and remember which one I picked when I come back". Why: the current switcher lists seven themes and forgets the pick on reload.

STARTING STATE: Repo at the folder the desk names in config.json under repo_root (a Vite and React app, `npm ci` already run). Worktree <repo_root>-theme-switcher-0115 on branch codex/theme-switcher-0115 from hub/main at the head the desk writes here before firing. Live checkout of the operator: never touched. Record folder: record/landing/theme-switcher-build-0115/.

SAVE AS YOU GO: Create record/landing/theme-switcher-build-0115/OUTPUT.md in your first minute with Execution: running, Review: pending and STATUS: RUNNING as its last line. Append each finished part the moment it is done. At the end, replace the last line with the verdict. Screenshots under record/landing/theme-switcher-build-0115/evidence/; build output and browser profiles under evidence/generated/.

READ FIRST: README.md; src/theme/themes.ts (the theme list); src/theme/ThemeSwitcher.tsx; src/theme/useTheme.ts; the tests under src/theme/__tests__/.

SCOPE: in: 1. themes.ts lists exactly light, dark, high-contrast; default light; a stored value that is not one of the three falls back to light. 2. useTheme.ts writes the pick to localStorage under one named slot and reads it on first render. 3. ThemeSwitcher.tsx shows exactly three buttons with the current one marked. 4. The removed themes leave no live CSS: grep src for their data-theme values and remove dead rules. 5. Tests updated for the three-theme list and the fallback. Out: colors of the three themes; any other component; the build pipeline. Do not touch: the operator's live checkout; main; no push to any remote but hub; no new dependencies; no network.

STEPS: 1. Confirm the worktree, branch and head; write them in OUTPUT.md. 2. Cut the list and the fallback (one commit). 3. Persist the pick (one commit). 4. Remove dead CSS (one commit). 5. Run `npm run typecheck`, `npm run build`, `npm test`; quote each result line verbatim. 6. Walk: Vite on port 5614 headless (Playwright, chromium), fresh context opens in light; click dark, reload, still dark; click high-contrast, reload, still high-contrast; screenshot each state into evidence/; console errors per screen (baseline 0). 7. Push the branch to hub; freeze it; write the verdict.

DONE WHEN: OUTPUT.md holds the head, the three commits, the three check lines verbatim, the walk's three screenshots named with console counts, and ends with one of DONE: ... or FAILED: ..., then Execution: complete or failed, Review: pending.
TIME LIMIT: 2 hours.
RETURN: every claim labeled VERIFIED, INFERRED, UNVERIFIED or NOT FOUND; end with a MISSING FACTS list. No em-dashes. PowerShell 7 (pwsh) for shell. If rg is not installed, search with Select-String, git grep or Python.
