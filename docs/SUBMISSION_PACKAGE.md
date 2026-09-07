# PORE Submission Package

## Category

Standalone GenLayer Intelligent Contract.

## Canonical source

`contracts/pore.py`, class `EvidenceGatedIntentEscrow`.

The contract is branded PORE (Proof-of-Repair Escrow). The stable class name is retained for compatibility with the currently used GenLayer loader conventions.

## Verification status

The corrected-source StudioNet deployment completed on 2026-09-07:

- Contract: `0x3378Bc396b4d99F443085C3fC958875D34AAE979`
- Deployment transaction: `0x6962ef87d77c69748abfcc440e8c90c65a23163229ab999b68f97de5bf0c588f`
- Status: `ACCEPTED`
- Result: `MAJORITY_AGREE`
- Validators: 5 votes revealed; quorum reached in round 0.
- Schema retrieval: successful; all public methods and payable flags loaded.
- Read-only `stats()`: successful; initial escrow balance was `0`.
- Negative-path live write: unfunded `create_repair_case` correctly rolled back with `EXPECTED: escrow amount required`, while the transaction itself reached `ACCEPTED / MAJORITY_AGREE`.

The corrected source independently verifies warranty-failure claims through validator consensus and exposes held warranty reserves separately from amounts actually paid. The new deployment is the authoritative source for the redesigned appeal.

The funded integration lifecycle was rerun against this deployment with publicly retrievable paired image evidence (`https://httpbin.org/image/jpeg` and `https://httpbin.org/image/png`): create → inspection → authorization → paired evidence → resolve completed successfully, with deterministic PARTIAL settlement assertions passing.
