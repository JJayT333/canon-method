---
name: orphan-sweep
description: The morning orphan process sweep: a dry-run count by the desk, the kill by the operator's own hand.
---
# orphan-sweep

## Purpose
Dead lane and session processes from earlier days are counted every morning and killed by the operator's hand, never the desk's.

## When to use this
Every desk open; and when the operator asks for the count.

## Inputs
- A kill script of the operator's own (not shipped here) that lists processes older than a cutoff and keeps anything owned by a live editor, terminal, Claude or Codex session. A one-line PowerShell `Get-Process | Where-Object StartTime -lt <cutoff>` with a keep list is enough to start.
- A double-click wrapper for it (a `.cmd` file) so the kill is one click.

## Steps
1. Run the script with the cutoff at the previous day and `-WhatIf`.
2. Put the count in line one of the roadmap: candidates, kept, to kill, memory.
3. Say the kill is the operator's double-click of the wrapper.
4. After the click, if asked: run `-WhatIf` again and report what remains.

## Decisions
- If the permission layer blocks the kill from the desk, then say so once and hand the operator the double-click; never a command block to paste.
- If the candidates include a process a live lane owns (check the running list), then name it as kept before the click.

## Definition of done
The count is in the roadmap's first line with the cutoff date.

## Edge cases
- Leftover tool servers from closed sessions (database servers, browser automation) are the usual orphans; nothing under a live app is ever selected.
