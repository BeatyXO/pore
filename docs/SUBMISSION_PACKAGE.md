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

## Funded lifecycle evidence

Against `0x655C404805dD3Ab6A52f609Da78a8046653532D1`, the funded integration lifecycle passed: create `0x35e84e239b6ab7e80c7c602e8b22fdf0a201bcf9b5e79ee2c0f0efda4f49d926`; inspection `0xed6f26f7f074a1a1418c5db668e817d4ba435929a6254075d917f1a1a4bd8c6a`; authorization `0x0eff07e7b1fe6c906deb3b69ef2c2296e6b91ba96c94b027d7d31ebabb2886a7`; BEFORE photo `0x60621636c799f8d50bcc7c3f9372484d654103055cfe18f3de56a0f6289e632d`; AFTER photo `0xf37471a38e4fdf191b1723f973d2cfd8fcc7192915bffe154eb253f2b2fcd9f1`; resolve `0xf1962a3aa6237ae0b1b0d144bf0406df9bf73b397ac111912f2d72eda496d141`.

Final accounting: verdict `PARTIAL`; `paid_to_requester=4000000000000000`; `paid_to_fulfiller=4800000000000000`; `held_warranty_reserve=1200000000000000`; gross fulfiller entitlement `6000000000000000`.

Parity record: source commit `1206942`; local normalized SHA-256 `60E631F7B4BA0A613910612E77B7E614737741A76205E0BA70EEB4F661D70378`; `gen_getContractCode(0x655C...)` returned `ADE42871D5F15C0FB57804DBD559C1C0FC2AC29046057EB84E9DAADD22A48D51`, so the deployed source does not exactly match that commit.

The corrected source independently verifies warranty-failure claims through validator consensus and exposes held warranty reserves separately from amounts actually paid. The new deployment is the authoritative source for the redesigned appeal.
