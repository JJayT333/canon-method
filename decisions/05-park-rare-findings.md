# Decision 05: rare findings are parked; the work moves on

Status: method v1. Binds every checker finding that normal use cannot reach.

## The problem it answers
A checker found that a hand-crafted input could exhaust memory in a document reader. No real input in a set of hundreds hit it. The fix would have been a structural change to a product that was otherwise finished, for a case the operator's own use would never produce.

## The rule
1. A finding that only a crafted or one-in-a-million input can reach, and that cannot corrupt saved data in normal use, goes on the parked list. No fix round, no new card, no boxes to the operator.
2. The parked list is one file, `record/PARKED.md`: one line per finding with what it is, where the preflight that contains it stands, and what the structural answer would be if it is ever needed.
3. A parked finding comes back only when a real input the operator uses trips it. Then it is a new card with the real input as its fixture.
4. Rechecks still run the known crafted set as a regression; they do not hunt for new crafted inputs (decision 04).

## The test
Ask: in normal use, can this lose or corrupt data the operator has saved? If yes, it is a finding and gets a round. If no, and no real input reaches it, park it.
