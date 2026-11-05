# Recovery Map policy — Every excavation must include a map

**Effective:** 2026-11-05

All future digital-archaeology case reports, submissions and cross-reviews must reference a Recovery Map in the shared format at [RECOVERY_MAP_TEMPLATE.md](./RECOVERY_MAP_TEMPLATE.md).

## Mandatory outputs for every case

1. Human-readable `recovery-map.md`, copied from the template and completed with exact status; never fill unknowns with guesses.
2. Structured `recovery-map.json` following [the machine-readable example](./recovery-map.example.json); keep stable field names for future comparative papers.
3. A pointer to evidence (pinned block number/hash, chain ID, contract code hash, immutable source commit, sanitized logs, timestamps, actual executable outcomes).
4. A review verdict separate from the original agent's own verdict. Include counterexamples, limitations and remaining dependencies.
5. A public-safety decision: `PUBLIC_MAP`, `REDACTED_MAP`, or `PRIVATE_REVIEW`. Publication requires clearance; writing a map does not authorize public release.

## Research classifications

`A`: claimant-controlled; `B`: administrator-dependent; `C`: technically plausible but authority unresolved; `D`: blocked at the investigated snapshot, not necessarily forever; `U`: insufficient evidence.

**Do not treat held assets as unencumbered surplus.** Disclose escrow liabilities, overlapping claims, price timestamps, rebasing accounting, and exact address-count definitions. Never conflate hypothetical authorized simulation with on-chain disbursement.

## Publication / paper use

Use stable `case_id`, `snapshot`, `assets`, `rights`, `recovery`, `verification` and `publication` fields to build a longitudinal corpus. Record case inclusion and exclusion rules, independent replay status, denominator and false-positive rates where measurable. A case that fails some gates still belongs in the dataset with honest status; never discard negative results to improve apparent success rate.

For the already existing cases, add a map **retrospectively after review**, without changing or rewriting original agent evidence. A template file is not a completed archaeological case.
