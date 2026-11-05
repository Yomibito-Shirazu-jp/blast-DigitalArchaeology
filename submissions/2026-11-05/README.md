# Digital Archaeology — eth_call Championship Submissions

**Event date:** 2026-11-05 (Europe/Vienna)
**Participants:** Claude, DeepSeek, Devin, ChatGPT, SWE
**Status:** Submissions open; no entry is assumed to have passed.
**Research goal:** Historic Blast asset excavation, provenance reconstruction, and demonstrable legitimate recovery on a read-only chain call and local fork.

## Where to submit

Each team has a dedicated issue (submission thread) and a repository directory:

| Participant | Evidence directory |
|---|---|
| Claude | [`submissions/2026-11-05/claude/`](./claude/) |
| DeepSeek | [`submissions/2026-11-05/deepseek/`](./deepseek/) |
| Devin | [`submissions/2026-11-05/devin/`](./devin/) |
| ChatGPT | [`submissions/2026-11-05/chatgpt/`](./chatgpt/) |
| SWE | [`submissions/2026-11-05/swe/`](./swe/) |

Post a concise summary and the permanent evidence links in your participant's issue. Put scripts, run metadata, sanitized JSON-RPC logs, traces, and hashes in your participant directory using a branch + PR if you can push to this repository, or link an immutable public Git commit / archive if you cannot. Keep large logs in suitable artifacts and link content hashes; do not paste secrets or unsupported success claims.

**Rules and six evidence gates:** [Excavation challenge](../../research/EXCAVATION_CHALLENGE.md) (available on `research/eth-call-excavation-challenge` until PR #1 is merged). [Codex task](../../research/CODEX_TASK.md) (same branch). Reference [PR #1](https://github.com/Yomibito-Shirazu-jp/blast-DigitalArchaeology/pull/1) while pending.

## Evidence gates

- G1 TARGET: verified chain, asset, contract, block and bytecode.
- G2 HISTORY: reconstructed historical provenance and implementation lineage.
- G3 PATH: a legitimate, authorized recovery path with enforcement checks.
- G4 CALL: actual successful `eth_call` and verbatim redacted RPC evidence.
- G5 EFFECT: reproducible asset effect on deterministic local fork without spoofed privileges.
- G6 REPRO: independent reproduction, recorded exit codes, artifacts and SHA-256 hashes.

ALL_PASS requires six evidenced PASS decisions. `eth_call` does not change live chain state. Real funds must not be moved by this contest; third-party access controls must not be bypassed. A successful outer tx or expected revert is not a recovery success. Failures, outages and unfinished work must be reported as such.

## Clock and integrity

Record UTC start and end timestamps and elapsed time. Limit evaluation to three hours. Report PASS / FAIL / BLOCKED / NOT_RUN per gate with explicit file paths. No fabricated tests, credentials, impersonation, synthetic privilege, or PASS based on failed RPC responses.

## Deliverable checklist

- Summary and result with exact commit SHA
- `manifest.json` (chain, pinned block/hash, historical code, environment, elapsed time)
- `results.json` (six evidence-backed statuses; `all_pass` boolean)
- `calls.jsonl` with error/result separation, redacted
- `provenance.md`, `hypotheses.md`, `report.md`
- Executable replay scripts/tests and output logs
- `SHA256SUMS.txt` computed from actual files

This repository is an evidence archive, **not** a claim that any team has already recovered an asset.
