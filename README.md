# canon method

A way to run two coding agents from one chat without losing your own words, your own decisions, or the truth about what is done.

It grew out of one person's daily work with Claude Code and Codex side by side. The shape is small:

- **The desk** is the chat you talk to. It never does big work by hand. It writes cards and fires lanes.
- **A lane** is a worker on a card: a Claude subagent in the background, or a headless Codex job. Every card names its model.
- **The other harness checks.** Codex checks Claude's work; Claude checks Codex's. One independent checker before any merge, ship or tool change. The desk never accepts its own work.
- **Your word merges.** Nothing lands on main until you say so.

Everything you say is banked verbatim, with the clock minute, before any work starts. Every ruling you make is written as a decision with your words at the top. The next chat opens from the record, not from memory.

## What is in here

| Folder or file | What it is |
|---|---|
| `CLAUDE.md` and `AGENTS.md` | The one law, identical. Claude Code reads the first, Codex reads the second. |
| `skills/` | Twelve skills the desk runs: open, bank words, record a ruling, develop a prompt, fire a lane, fire a checker, sweep, handoff, close, discuss, abort and pause, orphan sweep. |
| `launchers/` | `fire-codex-job.ps1` runs one card as a headless Codex job. `check-lane.ps1` prints the facts about a lane (process, receipt, worktree) before the desk writes RUNNING or DONE. |
| `tools/card_check.py` | The card checker. The launcher refuses a card that fails it. |
| `cards/` | Three templates (Claude lane card, Codex job card, acceptance card) and two filled examples on a sample web app with a theme switcher. |
| `decisions/` | The five rules that bind every card: acceptance, save as you go, walked live, the redo cap, parked findings. |
| `config.example.json` | Every path that is yours. Copy to `config.json` and fill it in. |

## Dropping it into Claude Code or Codex

1. Clone this repository next to your projects. Call the folder whatever you like; `canon-method` is assumed below.
2. Copy `config.example.json` to `config.json` and fill in your paths. `config.json` is ignored by git.
3. Fill the three placeholders in `CLAUDE.md`, then copy it over `AGENTS.md` so the two stay identical: `<HUB-REMOTE>` (the one remote you push to), `<JOURNAL-PATH>` (a private folder, outside any shared repository), `<OFF-LIMITS-FOLDERS>` (anything the agents must never open).
4. Claude Code: start `claude` in this folder, or in a project whose `CLAUDE.md` says "the law is canon-method/CLAUDE.md". Put the skills where Claude Code finds them: copy or link each `skills/<name>` folder into `~/.claude/skills/` (shared by every project) or into `<project>/.claude/skills/` (one project).
5. Codex: start `codex` in this folder, or point your project's `AGENTS.md` at `canon-method/AGENTS.md`. Codex reads `AGENTS.md` on its own; the skills are read as plain files when a card names them.
6. The launcher needs PowerShell 7 (`pwsh`), Python 3 on the path, and the Codex app installed with its engine folder (the default is `%LOCALAPPDATA%\OpenAI\Codex\bin`; set `codex_exe` in `config.json` if yours is elsewhere). Test it without starting Codex:

```bash
pwsh -NoProfile -File launchers/fire-codex-job.ps1 -Card cards/examples/theme-switcher-check/CARD.md -Cwd . -DryRun
```

## The day's loop

```
open the desk  ->  bank words  ->  card  ->  fire  ->  check  ->  merge on your word  ->  close
```

1. **Open** (`skills/desk-open`). The first message of a new chat. The desk reads yesterday's and today's journal, the last handoff, and every landing zone, then replies with a roadmap. Nothing fires.
2. **Bank** (`skills/bank-words`). Every message you send goes into the journal verbatim with the clock minute and a tag (RULED, ORDER, THOUGHT, CORRECTION, OPEN, ASK). Before any work.
3. **Record a ruling** (`skills/record-a-ruling`) when a message binds future work: a numbered decision file with your words at the top.
4. **Card** (`skills/develop-prompt`). The desk turns your intent into one card: model on line one, objective with your words quoted, verified starting state, save-as-you-go line, read list, scope with a not-in-scope line, steps, done-when, verify, time limit, return shape. The card checker passes it or the launcher refuses it.
5. **Fire** (`skills/fire-opus-worker` for a Claude lane, `launchers/fire-codex-job.ps1` for a Codex job). The lane creates its output file in its first minute with STATUS: RUNNING and appends each part as it lands. The desk writes RUNNING only after `check-lane.ps1` shows a live process and a receipt.
6. **Check** (`skills/fire-codex-checker`, or a Claude checker when the lane was Codex). An independent checker on the frozen head writes ACCEPTED or NOT ACCEPTED as the last line of its own file. The desk's DONE line quotes the verdict, never its own belief. A fix round follows a NOT ACCEPTED; at most five rounds, three when a round makes no progress.
7. **Merge** only on your word. After the merge the full suite runs on the merged tip.
8. **Close** (`skills/desk-close`, `skills/handoff`). Three lines in the day note (what we did, what you decided, what is next), the handoff for the next chat, one commit.

Two words stop things: **ABORT** in capitals stops everything the desk started. **pause** stops nothing and brings the running list current (`skills/abort-and-pause`).

## The record files

The method keeps its state in a few plain files. None exist on day one; the desk creates each the first time it needs it and says so.

| File | What it holds | Shape |
|---|---|---|
| `<JOURNAL-PATH>/<date>-words.md` | every message you send, verbatim, numbered, with the clock minute and a tag | one `[N#] HH:MM TAG` header per message, the message as a block quote under it; private, outside any shared repository |
| `record/notes/<date>.md` | the day note: what happened, what you decided, what is next | dated entries during the day; three close-out lines at the end |
| `record/RUNNING.md` | the running list: every lane the desk started that is still alive | one line per lane: name, record folder, process identity, stop action |
| `record/landing/<job>-<mmdd>/` | one folder per card: `CARD.md`, `OUTPUT.md` (the lane's receipt, STATUS last), `evidence/` | the card shape is in `cards/`; `evidence/` is ignored by git |
| `record/landing/DESK-HANDOFF-<date>.md` | the handoff the next chat opens from | the product block first, then your binding words, verified state, the plan |
| `record/PARKED.md` | rare findings parked under decision 05 | one line per finding |
| `record/registers/settled.md`, `corrections.md`, `craft.md` | the map of rulings, the desk's own failures, method lessons | one entry per item, newest last |
| `docs/THE-PRODUCT.md` | one paragraph on what is being built, dated | its first block is copied verbatim into every handoff |
| `decisions/NN-<slug>.md` | your rulings that bind future work | your words at the top, numbered points, what it replaces |
| `.desk-lock` | which chat is the desk right now | session name, clock, writer; deleted at close |

Clock reads are always a command, never a guess: `Get-Date -Format HH:mm` in PowerShell, `date +%H:%M` in a POSIX shell.

## The cards

A card is one file a worker can read in one screen and act on with no questions. The checker (`tools/card_check.py`) enforces the mechanical parts: line one `Runs on:` with a reason in parentheses; the fields in order; the objective quoting the operator's words with a date; a save-as-you-go line with an exact path and STATUS: RUNNING; a time limit of at most twelve hours; a return shape that labels every claim VERIFIED, INFERRED, UNVERIFIED or NOT FOUND and ends with MISSING FACTS; no em-dashes; at most sixty lines. Run it by hand:

```bash
python tools/card_check.py cards/examples/theme-switcher-build/CARD.md
```

The Claude lane card (`cards/TEMPLATE-claude-lane-card.md`) is looser in shape; it is fired with the Agent tool, not the launcher, and the lane's model is named on its first line.

## Honest limits

- **Windows and PowerShell 7 are assumed.** The launchers are `.ps1` files and call `pwsh`. On a Mac or Linux they need a port (the logic is short: find the engine, write the receipt, pipe the prompt to `codex exec`).
- **The Codex launcher looks for the Codex app's own engine** under `codex_bin_dir`, because the plan login lives there. A standalone `codex` on the path works too; set `codex_exe`.
- **The Claude lane is fired from inside Claude Code** with its Agent tool. There is no shell launcher for it here; the skill says what the call carries.
- **Everything in `config.example.json` and the three placeholders in the law are yours to rewrite.** So are the names: the method calls the worker "the Codex worker" and the person "the operator". Rename them in `config.json` and the law if you want a name.
- **The journal is private.** Put it outside any repository you share. The method's own repository never holds it.
- **No board, no dashboard.** The record is the files in the table above. Build a viewer if you want one; the files are enough to start.
- **The orphan sweep needs a script of your own.** `skills/orphan-sweep` describes it (list processes older than a cutoff, keep anything a live editor or agent owns, kill on your click); it is not shipped because every machine's keep list differs.

## Why it is shaped this way

Every rule here was paid for once. The desk used to write both the claim and its acceptance, so a lane's last line became DONE with nothing between it and the operator; now a checker from the other harness writes the verdict. Workers used to hold results for one write at the end and lost a day of research when the session cut off; now every card says save as you go. Tests passed and a diff was read and nobody ran the product the way the operator runs it; now done means walked live with a screenshot. A checker was asked for a tenth recheck of a problem no real input could hit; now rare findings are parked and fix rounds are capped. The decisions folder carries each of these as a short rule with the reason under it.
