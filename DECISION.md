# PORE Design Decision

PORE was selected because repair completion is a repeated trust boundary: a payer needs a settlement decision about evidence that combines semantic interpretation, live web observation, and visual inspection. A backend, single operator, or single LLM can produce a decision, but cannot provide independent validator agreement bound to the escrow transition.

The primitive is distinct from the workspace's generic intent escrow because its domain contract is an immutable repair specification with before/after evidence, visual evidence, and repair-specific evidence categories. It is also distinct from dispute resolvers because the primary lifecycle is funded repair completion, not open-ended claim adjudication.

Three consumers can reuse it without changing the core contract: a property-maintenance marketplace, a vehicle/warranty claims contract, and a construction milestone contract.
