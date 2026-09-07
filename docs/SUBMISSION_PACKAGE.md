# PORE Submission Package

## Category

Standalone GenLayer Intelligent Contract.

## Canonical source

`contracts/pore.py`, class `EvidenceGatedIntentEscrow`.

The contract is branded PORE (Proof-of-Repair Escrow). The stable class name is retained for compatibility with the currently used GenLayer loader conventions.

## Verification status

The corrected-source StudioNet deployment completed on 2026-09-07:

- Contract: `0x655C404805dD3Ab6A52f609Da78a8046653532D1`
- Deployment transaction: `0x712f09e24487ffed2af4aefc336e7b1accf917cdf61235f9afadc495b5eb7eaf`
- Status: `ACCEPTED`
- Result: `MAJORITY_AGREE`
- Validators: 5 votes revealed; quorum reached in round 0.
- Schema retrieval: successful; all public methods and payable flags loaded.
- Read-only `stats()`: successful; initial escrow balance was `0`.
- Negative-path live write: unfunded `create_repair_case` correctly rolled back with `EXPECTED: escrow amount required`, while the transaction itself reached `ACCEPTED / MAJORITY_AGREE`.

The corrected source independently verifies warranty-failure claims through validator consensus and exposes held warranty reserves separately from amounts actually paid. The new deployment is the authoritative source for the redesigned appeal.
