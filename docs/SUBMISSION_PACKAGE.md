# PORE Submission Package

## Category

Standalone GenLayer Intelligent Contract.

## Canonical source

`contracts/pore.py`, class `EvidenceGatedIntentEscrow`.

The contract is branded PORE (Proof-of-Repair Escrow). The stable class name is retained for compatibility with the currently used GenLayer loader conventions.

## Verification status

The hardened-source StudioNet deployment completed on 2026-09-03:

- Contract: `0x9232E691658D6B3Bb04c36857dDBe86fcC7341B6`
- Deployment transaction: `0x1016be0464c353651c063e5c253a85e4de26952ba2b3cd1ed44636883a4c4d61`
- Status: `ACCEPTED`
- Result: `MAJORITY_AGREE`
- Validators: 5 votes revealed; quorum reached in round 0.
- Schema retrieval: successful; all public methods and payable flags loaded.
- Read-only `stats()`: successful; initial escrow balance was `0`.
- Negative-path live write: unfunded `create_repair_case` correctly rolled back with `EXPECTED: escrow amount required`, while the transaction itself reached `ACCEPTED / MAJORITY_AGREE`.

The repository includes Direct Mode tests. On 2026-09-03, the installed `gltest` runner failed while allocating both PORE and the pre-existing evidence escrow with `AttributeError: ... has no attribute __type_desc__`. This is a shared local SDK/runtime issue and must be rerun after the GenLayer runner installation is repaired.

The linter command was invoked, but its validator phase could not load the SDK because Windows denied access to the cached extracted runner. The source lint phase passed.
