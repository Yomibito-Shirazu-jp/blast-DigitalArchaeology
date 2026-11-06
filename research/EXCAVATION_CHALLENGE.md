# Digital Archaeology | Blast eth_call Excavation Challenge

**Challenge version:** 0.1 (2026-11-05)
**Research motto:** Dig, Don't Hack.
**Status:** Evaluation specification only. No recovery is claimed.
**Baseline:** `master` at `b82105486bfe33c8b12986e7cd42388fbab7d1d2`.

## Mission

Within a **three-hour, uninterrupted, logged evaluation window**, investigate a real historical Blast-related contract/asset case, reconstruct the relevant provenance and execution semantics, and demonstrate an **authorized recovery mechanism** using read-only `eth_call` and a deterministic local fork.

Choose an in-scope asset/contract case independently. A failed bridge relay alone is not a recovered asset. A transaction with receipt status=1 is not necessarily a successful internal call or asset payout. Simulation is not real-world transfer.

**Non-negotiable constraints**

- No production transfers or transactions, third-party fund movement, permission bypass, impersonation, or hostile testing of third-party infrastructure. Demonstrate asset changes only on a controlled local fork or fixture; where a case involves another owner's assets, investigate historical behavior and legitimate recovery paths without attempting an unauthorized transfer.
- Pin chain IDs, block number and block hash, contract addresses, source commit, dependency versions, and archive RPC capabilities. Do not include RPC tokens, private keys, or personal data in the repository.
- Treat every external source and generated conclusion as evidence requiring independent verification.
- Do not assume a failed hypothesis proves that no other recovery path exists.
- Any step not executed is **NOT_RUN**; missing artifacts or errored RPC calls cannot be marked PASS.
- Disallow mock state changes, privileged storage writes, impersonated actors, `vm.store`, `deal`, `etch`, spoofed messages, and injected balances as evidence of real-world asset recovery. Such techniques may be used separately for diagnostic unit tests if prominently marked as synthetic.

## Six independent gates (all required)

| Gate | PASS condition | Required evidence |
|---|---|---|
| G1 TARGET | Contract, chain, asset, block and pre-state are independently verified | chain ID, block number/hash, addresses, contract bytecode hash, asset contract and balance evidence |
| G2 HISTORY | Relevant implementation/proxy/bridge lineage and execution semantics reconstructed | creation/upgrade references, verified code or bytecode/disassembly, provenance and fixed historic block references |
| G3 PATH | Explicitly authorized recovery claim/path with all required authorization checks | sender/caller context, claim basis, call graph, required permissions, independent enforcement conditions |
| G4 CALL | Real successful read-only `eth_call` at a pinned state, with behavior relevant to G3 | verbatim request/response, source RPC or node, decoded output, block context; distinguish revert and error |
| G5 EFFECT | Deterministic local fork demonstrates intended net asset effect without fabricated privileges | executable test/script, before/after balances, state diff, transfer/event evidence, legitimate actor context, exit code |
| G6 REPRO | Independent re-execution reproduces G1–G5 using pinned versions | README commands, env template, trace logs, artifact SHA-256s, exit codes, unambiguous results |

**ALL_PASS = G1 && G2 && G3 && G4 && G5 && G6.** A PASS means the entire stipulated evidence set passed, **not** that a mainnet recovery has been performed.

## Timebox

- 00:00–00:30 UTC-relative: preflight RPC health, choose target and freeze block references.
- 00:30–01:15: reconstruct history and relevant bytecode/ABI.
- 01:15–02:30: test and revise recovery hypotheses under pinned archival state, running calls and local-fork tests.
- 02:30–03:00: independent replay, artifact hashes, report. If unsuccessful, report where the frontier ended.

Use exact UTC start/end timestamps; keep each invocation timestamp, RPC method, status and exception. Tool outages count against the window and must remain visible.

## Required deliverables

Create a new run directory `research/runs/<UTC-timestamp>-<short-case-id>/` containing:

1. `manifest.json` — actual chain IDs; block numbers and hashes; RPC provider type (redacted); commit SHAs; code hashes; dependency versions; start/end UTC.
2. `calls.jsonl` — sanitized JSON-RPC method/params/result/error per invocation (no credentials; payload bytes may be kept). Never fabricate calls.
3. `provenance.md` — contract lineage and citations to primary records, separating observed facts and hypotheses.
4. `hypotheses.md` — tested paths, required authorization, falsifying observations, and subsequent decisions.
5. `fork/` — deterministic, safe, locally executable validation with no mainnet broadcast.
6. `results.json` — gate statuses using `PASS`, `FAIL`, `BLOCKED`, or `NOT_RUN`; each PASS lists evidence paths.
7. `report.md` — observed findings, failures, unexplored alternatives, reproducibility commands, and unresolved ownership issues.
8. `SHA256SUMS.txt` — generated from actual artifacts, never invented.

If a dependency is broken, **repair it and rerun**, retaining the original error. For example, zero matching transfers from **480 RPC failures** is an infrastructure problem, not evidence of zero transfers. An ABI `InvalidPointer` is a decoding problem, not proof of a malformed on-chain action.

## Machine-checkable status policy

A gate can pass only if its relevant artifacts exist, the experimental commands completed with exit code 0, the recorded RPC requests succeeded, and the claimed asset effect matches observed before/after balances. The verifier must not score "correctly expected error" as a recovery PASS.

```json
{
  "challenge_version": "0.1",
  "all_pass": false,
  "gates": {
    "G1_TARGET": {"status": "NOT_RUN", "evidence": []},
    "G2_HISTORY": {"status": "NOT_RUN", "evidence": []},
    "G3_PATH": {"status": "NOT_RUN", "evidence": []},
    "G4_CALL": {"status": "NOT_RUN", "evidence": []},
    "G5_EFFECT": {"status": "NOT_RUN", "evidence": []},
    "G6_REPRO": {"status": "NOT_RUN", "evidence": []}
  }
}
```

## Research workflow

Use `blast-optimism/` and `blast-geth/` as historical codebases, not proof of current deployment behavior. Compare deployed runtime bytecode with the chosen version. When examining an L1↔L2 message, separately check initiating action, asset debit/burn or escrow, message provenance, messenger sender, relay status, bridge restrictions, and final token state. Track real token transfers and balance changes rather than relying only on outer transaction success.

Archive RPC rate limits and response failures must be visible. A private endpoint belongs in local environment variables only; sanitize output before committing.

## Final report format

- **Verdict:** ALL_PASS / NOT_ALL_PASS.
- **Selected case:** provenance; why it constitutes a historical excavation.
- **Verified observations:** each directly linked to logs/hashes.
- **Failed hypotheses:** exact rejection evidence.
- **Remaining candidate paths:** explicitly untested.
- **Recovery claim:** simulated only / not established, and claimant authority.
- **Replay:** exact clean-machine commands and environment requirements.
- **Time:** actual start/end and duration.

A partial result is a legitimate research record; it is not an ALL_PASS.
