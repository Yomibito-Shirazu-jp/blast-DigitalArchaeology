# Devin PoC addition: preliminary source-and-log review

**Commit:** `2e99b6a91816ae5bdad137370d455999a261b19b`.
**Files:** `submissions/2026-11-05/devin/fork/poc.py`, `poc_log.txt`.
**State:** Code and log visible on GitHub; no independent rerun claimed here.

The submitted `poc_log.txt` reports **9/9 PASS, POC_EXIT=0**. The PoC source checks fixed historical balances and an expired unlock time; a successful `eth_call` from the depositor address; a non-depositor revert; read-only `prestateTracer` showing two expected token-storage values; and a local Anvil synthetic transaction showing recipient-credit and LockManager-debit.

Crucial limitations:

1. The 9 checks are **not identical** to the original 6 independent gates: the PoC does not itself assert G2 historical lineage or G6 independent replay.
2. `eth_call`/`debug_traceCall` with `from=depositor` is caller context simulation, not an independently signed live transaction.
3. The supplemental fork transaction invokes `anvil_impersonateAccount` and `anvil_setBalance`. This can test contract logic but must **never** be counted as proof of production signer control.
4. The read-only diff check compares a set of two post-storage values; it does not itself verify corresponding storage-slot identities, pre-values and conservation rules. Its independent interpretation depends on the separate trace artifacts and verified BLAST storage layout.
5. The code pins the block **number** but does not independently compare `eth_getBlockByNumber` against the expected block **hash** within the nine checks.
6. Re-running from an external environment and recording actual exit code is still necessary for G6 independent replication.
7. The PoC's script has no actual signed transaction by the claimant; its legitimate withdrawal is *conditional on the claimant's signing authority*, as expected for a normal user withdrawal.

Assessment: **credible simulation evidence; externally reproduced ALL_PASS not yet established.** Keep the historical novelty question separate from computational correctness.


## Update: Devin commit 9b81e63 (2026-11-05)

The GitHub head of PR #2 advanced to `9b81e63d0c4bdce1146fb4b3bac2978b5508e84a`. New `fork/poc.py`, `fork/poc_log.txt`, `fork/alchemy_calltracer.json`, expanded `calls.jsonl`, and updated report/results were committed.

Inspection of the actual script and committed log shows **16/16 self-checks PASS; POC_EXIT=0 reported**. Newly covered: block hash and timestamp, bytecode equality vs saved artifact, deployment transaction block, explicit trace diff pre/post for two BLAST balance slots and locked-token quantity, conservation (100,000 BLAST debit equals credit), and synthetic-marked local fork receipt.

**Important boundary:** 16/16 is a substantive, stronger internal validation suite; it is *not* independent third-party replay, and it is not equivalent to final G1–G6 reviewer acceptance. An `eth_call` caller address does not establish possession of that account's signing key. The local `eth_sendTransaction` remains impersonated on a fork, for diagnostic purposes only.

### Remaining reviewer tasks

1. Independently execute pinned calls and `python poc.py` from a clean environment and record observed exit code.
2. Verify keccak-derived slot identities against a separate trusted EVM keccak implementation or independent storage-layout evidence; the PoC currently asserts constants, rather than recomputing the hash on each run.
3. Verify the source's asserted exclusive administrative paths and any significant code-level edge cases; the 16 PoC checks focus on one depositor withdrawal.
4. Confirm that the G2 lineage and G6 reproducibility requirements beyond this single test program are evidenced at immutable commit SHA.

### Cross-review status

Devin [PR #3](https://github.com/Yomibito-Shirazu-jp/blast-DigitalArchaeology/pull/3) exists and requests Claude's original file artifacts before meaningful source-level review. The Claude ZIP had been uploaded to this conversation but **not committed to the public repository** at the time this update was written. Keep `INSUFFICIENT_EVIDENCE` until Devin receives those bytes and can independently verify them.
