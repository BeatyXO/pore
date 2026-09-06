# PORE Appeal — Repair Verification and Warranty Enforcement

PORE is not intended to be a second generic evidence-gated escrow. It uses escrow custody as shared financial infrastructure, while its application protocol is a repair-specific workflow:

1. A sponsor creates a repair case.
2. A repair party submits an inspection record identified by an inspection hash.
3. The sponsor authorizes a quoted repair identified by a quote hash.
4. The repairer submits paired `BEFORE_PHOTO` and `AFTER_PHOTO` evidence.
5. Validators assess repair-specific milestones and weighted deliverables.
6. A successful settlement retains a warranty reserve rather than releasing the full repairer payout immediately.
7. The reserve can be released after the warranty period or returned to the sponsor through a warranty challenge when the repaired condition fails.

These requirements change the authorization model, lifecycle states, evidence semantics, settlement timing, and post-settlement behavior. The generic escrow accounting is deliberately reused for safety and composability; the repair protocol layered on top is distinct.

## New deployment

- Network: GenLayer StudioNet
- Chain ID: `61999`
- Contract: `0x9aFF0D370feeE662c3a4f1fc115D1c9Bc60F7c70`
- Deployment transaction: `0x66248b3e3eec7b8d35fccb82a97c4d9ed2c4bc9379dfe9270eadb4b3d6df6125`
- Explorer: https://explorer-studio.genlayer.com/address/0x9aFF0D370feeE662c3a4f1fc115D1c9Bc60F7c70

The earlier deployment should not be used as evidence for this redesigned source. The source of record is `contracts/pore.py` in this repository.
