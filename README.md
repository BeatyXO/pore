# PORE — Proof-of-Repair Escrow

PORE is a standalone GenLayer Intelligent Contract primitive for staged repair work. A sponsor funds a case; the parties submit an inspection record, the sponsor authorizes a quoted repair, and the repairer submits bounded before/after evidence. Validators assess the repair record against the inspection and work specification; deterministic code settles the escrow.

PORE is intentionally contract-only and composable. It is suitable for property maintenance, vehicle damage, warranty claims, logistics damage, construction punch lists, and equipment repair.

## Live deployment

- **Network:** GenLayer StudioNet
- **Chain ID:** `61999`
- **Contract:** `0x655C404805dD3Ab6A52f609Da78a8046653532D1`
- **Studio Explorer:** [open PORE on GenLayer Explorer](https://explorer-studio.genlayer.com/address/0x655C404805dD3Ab6A52f609Da78a8046653532D1)
- **Deployment transaction:** `0x712f09e24487ffed2af4aefc336e7b1accf917cdf61235f9afadc495b5eb7eaf`

The redesigned source adds inspection and quote authorization gates before repair evidence is accepted, paired before/after evidence enforcement, a recorded warranty duration, a held warranty reserve, and requester warranty challenges.

## Consensus design

The contract never stores an LLM answer as authority. `resolve` constructs a bounded evidence bundle and runs a leader/validator judgment through `gl.vm.run_nondet_unsafe`. The leader returns a small verdict envelope: `SATISFIED`, `NOT_SATISFIED`, `PARTIAL`, `INCONCLUSIVE`, or `EXTERNAL_FAILURE`, plus a basis. Validators re-run the source-grounded judgment and compare only stable verdict fields and, for `PARTIAL`, stable deliverable IDs—not arbitrary explanatory prose.

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
