# CARD: the theme switcher cut to three themes (2026-01-15, fired 09:2x by the desk)

Model: Claude Opus (claude-opus-5-5). This card names its model; the lane never inherits the desk's.

Operator's words, verbatim: N4 09:12 "three themes, that is all, and remember which one I picked when I come back"; N6 09:18 "go".

## What this is
A build lane on the sample web app: cut the theme list to three, persist the pick, remove dead CSS, on one branch off hub/main. Decision 02: create the output file in your first minute and append each part the moment it is done. Decision 03: no screenshot, no done.

## Read first
README.md; src/theme/themes.ts; src/theme/ThemeSwitcher.tsx; src/theme/useTheme.ts; the tests under src/theme/__tests__/.

## Where
- Repo at the folder config.json names as repo_root (remote hub is the only remote you push to). Do not touch the operator's live checkout.
- Your worktree: `git -C <repo_root> worktree add <repo_root>-theme-switcher-0115 -b claude/theme-switcher-0115 hub/main` (write the base commit in OUTPUT.md).
- Output file (first minute, STATUS: RUNNING): record/landing/theme-switcher-build-0115/OUTPUT.md. Screenshots in record/landing/theme-switcher-build-0115/evidence/.
- Ports: Vite on 5614. Never 5173. Headless browser only; nothing opens on the operator's screen.

## The work, one commit each
1. themes.ts: exactly light, dark, high-contrast; default light; a stored value outside the three falls back to light.
2. useTheme.ts: the pick written to one localStorage slot and read on first render.
3. Dead CSS: grep src for the removed data-theme values; remove the rules that nothing selects.

Do not touch: the colors of the three themes; other components; the build pipeline. No new dependencies.

## Checks (worktree root)
`npm run typecheck`, `npm run build`, `npm test`. Report each result line verbatim and the test counts.

## Walk
Headless Playwright on port 5614: fresh context opens in light; click dark, reload, still dark; click high-contrast, reload, still high-contrast; screenshots light.png, dark.png, high-contrast.png; console errors per screen (baseline 0).

## Commit and push
Three commits, plain messages. `git push hub claude/theme-switcher-0115`. Never main, never another remote, never merge. Freeze the branch when OUTPUT.md says COMPLETE; a Codex checker runs on the frozen head (cards/examples/theme-switcher-check/CARD.md).

## Boundaries
Nothing outside the worktree and the record folder. No web. No other agents. If a check or the walk cannot run, say why and end STATUS: FAILED, never COMPLETE.

## OUTPUT.md shape
Five plain lines first (STATUS, branch and head, the three pieces of work in one line each, checks in one line). Then READ, WORK 1 to 3, CHECKS (verbatim), WALK (screenshots named with console counts), FINDINGS worst first, a verdict line, `Cost:`. Under 200 lines. No em-dashes. Reply at the end with only the OUTPUT.md path and its last line.
