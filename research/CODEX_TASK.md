# Codex assignment: Autonomous Blast Excavation (3-hour challenge)

You are a digital archaeology excavation researcher. Your job is to **produce evidence**, not to write an optimistic narrative.

Read `research/EXCAVATION_CHALLENGE.md` first. Work against existing repository structure (`blast-optimism/`, `blast-geth/`, `config/`) without changing upstream source unless essential, and document each such modification. You may independently select any historically interesting Blast asset/contract case where historical provenance and **authorized** recovery can be safely validated without touching production funds.

**Action order (autonomous, no routine approvals):**

1. Inspect repository and available tooling. Record commit SHA and tool versions.
2. Validate L1/L2 archive RPC access and chain IDs before substantive queries. Record availability, historical `eth_getCode`, `eth_getStorageAt`, `eth_getLogs`, `eth_call`, and trace support, differentiating unavailable methods from empty results.
3. Select and pin a candidate case with a specific L1 or L2 block number and hash. Prefer a scope with independently demonstrable legitimate recovery rather than inventing ownership.
4. Reconstruct historic deployed code lineage; compare implementation sources with chain bytecode.
5. State competing hypotheses and an explicit independent enforcement point for each.
6. Run read-only `eth_call` with actual responses retained; reproduce relevant effects in a fork with no production broadcast or simulated authorization.
7. Fix crashes, invalid ABI decodes, rate limits, bad assumptions and failed tests. Each failure must remain in the record.
8. Generate required artifacts and re-run the independent reproduction. Do not mark any gate PASS without its supporting proof.

**Special caution from earlier failed attempts:** outer L1 transaction success does not prove the cross-domain message succeeded; `FailedRelayedMessage` does not demonstrate asset payout; a rejected `onlyOtherBridge` action must not be silently counted as salvage. Do not infer absence from failed RPC queries.

**Return** a concise report with exact commit, run directory, six statuses, ALL_PASS boolean, verified asset effects (if any), unresolved conditions and replay command.

**Honesty requirement:** Do not invent RPC responses, code execution, recovered funds, test pass counts, or an expected time of completion. If permissions or infrastructure are missing, document the failure and continue investigating permitted alternatives. Preserve untested paths rather than asserting global impossibility.
