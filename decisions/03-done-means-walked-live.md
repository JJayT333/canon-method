# Decision 03: done means walked live

Status: method v1. Binds every lane that claims a fix or a feature in a running product.

## The problem it answers
An audit of four days found seventeen claims of done, accepted or working that were not. In every one, tests passed and a checker read the diff and nobody ran the product the way the operator runs it.

## The rule
- Done means walked live: a lane that claims a fix drives the running app the way the operator uses it, puts the screenshot in its record folder, and the checker checks that run. No screenshot, no done.

## In practice
- A lane's card names the live proof it must bring: the running app (a separate instance on its own ports when the operator's is up), the exact clicks or typed inputs, the screenshot and timing files under its record folder's `evidence/`.
- The checker's card names the same proof and the checker runs it itself where its sandbox allows. Where it cannot (a sandbox with no browser), the checker says so once and the desk gets the live run from a checker on the other harness. A diff read alone is never acceptance.
- A test suite green, a typecheck green or a size cap green is evidence, not done.
- The operator's own walk is still the last word; the rule only stops the desk from saying done before anyone has seen it run.
