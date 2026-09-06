# PORE Submission Package

## Category

Standalone GenLayer Intelligent Contract.

## Canonical source

`contracts/pore.py`, class `EvidenceGatedIntentEscrow`.

The contract is branded PORE (Proof-of-Repair Escrow). The stable class name is retained for compatibility with the currently used GenLayer loader conventions.

## Verification status

The hardened-source StudioNet deployment completed on 2026-09-03:

- Contract: `0x9aFF0D370feeE662c3a4f1fc115D1c9Bc60F7c70`
- Deployment transaction: `0x66248b3e3eec7b8d35fccb82a97c4d9ed2c4bc9379dfe9270eadb4b3d6df6125`
- Status: `ACCEPTED`
- Result: `MAJORITY_AGREE`
- Validators: 5 votes revealed; quorum reached in round 0.
- Schema retrieval: successful; all public methods and payable flags loaded.
- Read-only `stats()`: successful; initial escrow balance was `0`.
- Negative-path live write: unfunded `create_repair_case` correctly rolled back with `EXPECTED: escrow amount required`, while the transaction itself reached `ACCEPTED / MAJORITY_AGREE`.

The redesigned repository includes Direct Mode and live integration coverage for inspection → authorization → paired before/after evidence. Direct Mode remains useful for local regression testing; the installed Windows runner has an allocation/cache compatibility issue. The new deployment is the authoritative source for the redesigned appeal.
