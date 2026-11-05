# Devin → Claude: adversarial cross-review

**Target:** user-supplied `claude_submission_v2.zip` (nine files; transfer to a branch or separate attachment before independent review). The contents are **not yet accessible from this repository**.
**Intake:** [CLAUDE_V2_INTAKE.md](./CLAUDE_V2_INTAKE.md).

Review G1–G6 using actual submitted `blast_poc.py`, `calls.jsonl`, `calls_alchemy.jsonl`, `manifest.json`, `results.json`, `report.md`, `provenance.md`, `hypotheses.md`, `SHA256SUMS.txt`.

Especially check:
1. historical L1/L2 pinned block hashes (no `latest` substitution);
2. live proxy implementation and UUPS upgrade authorization vs. independent Safe authorization;
3. authentic stETH shares/balance accounting, plus DAI/USDC and Maker DSR balances versus liabilities;
4. exact `stateOverride` requests and `debug_traceCall` traces, not merely a statement that traces occurred;
5. distinction between zeroing shares and transferring shares to an authorized recipient;
6. no assumption that an imagined new `rescueToken` implementation is deployed or executable;
7. original submitted `results.json` says `all_pass:false` with `G3_PATH:PARTIAL`, `G5_EFFECT:NOT_PASS`; preserve this honesty correction rather than reverting to an earlier claim of ALL_PASS;
8. G6 requires actually rerunning complete relevant experiments. A script executing only public `latest` calls does not prove archived stateOverride reproduction.

Return an evidence-by-gate independent verdict (REPRODUCED / CONDITIONAL / DISPUTED / INSUFFICIENT_EVIDENCE / NOT_RUN), code line citations, and exact replay logs. Keep production fully read-only.
