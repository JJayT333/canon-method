# Decision 02: every worker saves its work as it goes

Status: method v1. Binds every card and prompt the desk sends to any worker.

## The problem it answers
A wave of nineteen research lanes was told to write its findings once at the end. A usage limit stopped the wave mid-run. Ten lanes lost everything they had found and five kept partial drafts. The desk refired fifteen of them on the same card the next morning before anyone noticed the card was the defect.

## The rule
1. Every card or prompt the desk sends to any worker (a Claude lane, a Codex job, a checker, a repair worker, any model) tells it to save as it goes:
   - create the output file in the first minute, with STATUS: RUNNING as its last line;
   - append each finished part the moment it is done;
   - never hold results for one write at the end, so a worker cut off leaves everything it found on disk;
   - at the end, replace the last line with the verdict and STATUS: COMPLETE (or FAILED, never COMPLETE when a check could not run).
2. A card that tells a worker to write once at the end is a defect; the desk fixes the card before it fires.
3. A worker already running without the line gets it by message the moment the gap is found.

## Where the rule sits
On every surface a worker can be sent from: the law (`CLAUDE.md` and `AGENTS.md`), the three card templates in `cards/`, the two fire skills, and the launcher's prompt. The card checker enforces the path and STATUS: RUNNING in the SAVE AS YOU GO field.
