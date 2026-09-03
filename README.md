# PORE — Proof-of-Repair Escrow

PORE is a standalone GenLayer Intelligent Contract primitive for escrowed repair work. A sponsor funds a repair case; a repairer submits bounded text, web, rendered-page, or image-URL evidence; validators independently inspect the evidence against an immutable repair specification; and deterministic code settles the escrow.

PORE is intentionally contract-only and composable. It is suitable for property maintenance, vehicle damage, warranty claims, logistics damage, construction punch lists, and equipment repair.

## Consensus design

The contract never stores an LLM answer as authority. `resolve` constructs a bounded evidence bundle and runs a leader/validator judgment through `gl.vm.run_nondet_unsafe`. The leader returns a small verdict envelope: `SATISFIED`, `NOT_SATISFIED`, `PARTIAL`, `INCONCLUSIVE`, or `EXTERNAL_FAILURE`, plus a basis and score. Validators re-run the source-grounded judgment and accept only substantively compatible verdicts. Scores are compared with tolerance, while prose is not compared.

Evidence kinds include `TEXT`, `WEB_TEXT`, `WEB_SCREENSHOT`, and `IMAGE_URL`. Image evidence is supplied through a public URL so validators can independently fetch it; PORE does not pretend that an uploaded private binary is independently observable.

## Escrow safety

All money enters through payable methods and is recorded as deposited ledger fields. Every settlement path reads those fields, zeros them, persists the record, and only then emits GEN through `_send_gen`. A second settlement therefore finds an empty ledger. If consensus remains inconclusive, the parties may agree to a bounded split, or the sponsor may recover after the resolution deadline.

## Interface

- `create_repair_case(...)` — create and fund a repair case.
- `add_repairer_bond(...)` — optional repairer bond.
- `submit_repair_evidence(...)` — add bounded evidence before the deadline.
- `resolve(...)` — consensus-backed assessment and deterministic settlement.
- `timeout_refund(...)` — recovery when resolution is not completed.
- `cancel_before_evidence(...)` — sponsor cancellation before evidence exists.
- `accept_mutual_repair_settlement(...)` — consensual split after inconclusive review.
- `get_intent`, `get_evidence`, `resolution_of`, `stats` — machine-readable views.

## Documentation basis

Implementation follows GenLayer's current guidance on nondeterministic blocks, web access, structured outputs, tolerant equivalence, and deterministic state mutation:

- https://docs.genlayer.com/developers/intelligent-contracts/equivalence-principle
- https://docs.genlayer.com/developers/intelligent-contracts/features/web-access
- https://docs.genlayer.com/developers/intelligent-contracts/features/non-determinism
- https://skills.genlayer.com/

## Local verification

From this directory, install the current GenLayer test tooling and run:

```text
genvm-lint check contracts/pore.py --json
pytest -q tests/direct
```
