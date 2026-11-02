# Decision 04: at most five redoes per card; three when a round makes no progress

Status: method v1. Binds every build-and-check cycle.

## The problem it answers
A card went through a tenth recheck of a problem no real input could reach. Open-ended fix-and-check never converges on its own; someone has to cap it.

## The rule
1. A card gets at most five fix rounds. A redo is one build or fix round followed by its check.
2. If any round makes no progress on the findings, or makes them worse, the card stops after its third round, whatever the count would otherwise allow.
3. When a card stops under 1 or 2, the desk reports to the operator with the open findings and the rounds tried; it does not start a sixth round, or a fourth after a stall, without the operator's word.
4. Work continues to done without waiting on the operator where the desk can: the next phase or round fires as soon as the last one is checked.
5. Work goes in stages; each stage is checked by a different model before the next stage starts. A check is never skipped to save time, and a stage never starts on an unchecked one.

## Progress, as the desk measures it
A round made progress if at least one open finding closed and none got worse. It made it worse if a finding that was closed reopened, or a new finding of equal or higher severity appeared in the same area.

## Rechecks replay
A recheck replays the previous check's findings on the new head. It does not open new categories of attack; a new category is a new card.
