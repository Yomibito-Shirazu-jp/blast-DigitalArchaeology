# Report — Blast eth_call Excavation: Munchables sunken BLAST

**Verdict: ALL_PASS** (all six gates, evidence-backed — simulated recovery only; no mainnet transfer performed or claimed)

## Selected case
Munchables `LockManager` `0xEA091311Fc07139d753A6BBfcA27aB0224854Bae` on Blast (chain 81457), pinned block **42502847** (`0x9fa65187…fc62c9`, ts 1793815509). The project suffered a $62.5M insider exploit (Mar 2024, legacy contract `0x29958e8e…`), redeployed this contract (Jun 2024), then shut down entirely — official gitbook directs users to self-rescue via `unlock`. Stranded: **122,315.1853 BLAST** + 90 USDB + 0.5634 ETH. A true wreck: assets intact, crew gone, recovery hatch still functional.

## Verified observations (each linked to logs/hashes)
- Depositor EOA `0x3a57e71046a29dcc47db9e0fc11a893631413d5a` holds `lockedTokens.quantity = 1e23` (100,000 BLAST), `unlockTime` 1734916739 expired 2024-12-23 (`calls.jsonl#lockedTokens-player-blast-FIXED`, deposit tx `0xdfc9fc3a…`).
- `eth_call unlock(BLAST, 1e23)` from depositor @PIN → `0x` success (`calls.jsonl#G4-unlock-eth_call-full`).
- `prestateTracer` diff at PIN — identical pre→post transition on upstream Alchemy archive and local anvil (`fork/*_tracecall*.json`): pre{`balanceOf[LM]`=122,315.1853e18 @`0x9a66ec…`, `balanceOf[player]`=0, lock qty=1e23 @`0xc3bb8a…`} → post{player=1e23 @`0x340bab…`, LM=22,315.1853e18, lock qty deleted→0}. Slot identities verified cryptographically (`balanceOf` at BLAST slot 0; `lockedTokens` at LockManager slot 11); conservation holds exactly (debit==credit==1e23, no mint/burn). `callTracer` trace (`fork/alchemy_calltracer.json`) captures the emitted `Unlocked`+`Transfer` events and the internal `forceHarvest`→AccountManager→SnuggeryManager call graph — all read-only, non-impersonated.
- Synthetic-actor fork diagnostic (disclosed): tx `0xa2f4e8…` status 1, gas 352,043, `Transfer`/`Unlocked` events for 1e23; post state matches trace diff exactly (`fork/unlock_tx.json`, `fork/run_log.txt`).
- Enforcement: non-depositor reverts `InsufficientLockAmountError`; post-claim double-unlock reverts — the authorization model held in every probe.

## Failed hypotheses
`getLogs` range limit (10k blocks) on the public RPC (HTTP 413) — worked around via explorer txlist; three wrong-selector eth_calls reverted and were re-run corrected (retained in calls.jsonl as honest error trail). See `hypotheses.md` H5.

## Publication-safety audit — can a third party steal these funds?

**Scope statement (corrected per peer review):** the claim is scoped to what was actually verified — LockManager + MigrationManager + BLAST token (verified sources) and on-chain probes. We do not assert impossibility over code we have not audited; residual dependencies are listed explicitly at the end.

### Principal-outflow paths — verified closed
- **`unlock()`** — the ONLY principal-moving function in LockManager (only `.call{value}`/`token.transfer` sites, L427/L431); pays `msg.sender` exclusively from `lockedTokens[msg.sender]`. Three distinct non-claimant callers revert `InsufficientLockAmountError` at PIN (logged).
- **`lockOnBehalf` lock-extension (griefing):** callable only BY `MigrationManager` (`onlyConfiguredContract`). Inside MigrationManager, `lockOnBehalf` is invoked solely from `_migrateNFTs` with quantity derived from **sealed** migration-snapshot data (`seal=true` — admin can no longer inject). Trigger requires `_userLockedAction[_user]==LOCKED_FULL_MIGRATION`, set only by the user themself funding `lockFundsForAllMigration()`. Our depositor has `getUserMigrateQuantityAll = (0,0)` → path cannot activate for them. **Closed by source + on-chain state.**
- **`claimERC20Yield`:** callable only by configured `RewardsManager`; calls `IERC20Rebasing.claim()` (yield-only semantics). For BLAST specifically the token is a plain OZ ERC20Votes with **no `claim()`** — the call is dead code for BLAST and reverts. **Closed.**
- **`MigrationManager.rescue`:** `onlyAdmin`, but moves only **its own balance** (`transferFrom(address(this),…)`) — cannot reach LockManager funds. **Closed.**
- **BLAST token admin (`GovernanceToken`):** sole extra function is `mint()` `onlyOwner` (`MintManager` `0xCa2e5b98…`) — dilution, not balance seizure; no blacklist/clawback/freeze/transfer-gating. Standard OZ `transfer` returns bool → unchecked-return in `unlock` is harmless for this token (a non-compliant ERC20 could cause accounting loss, not theft).
- **Governance/config:** USD-price/config functions move no funds; `Paused` is a liveness flag only.
- No `selfdestruct`, `delegatecall`, or proxy — immutable runtime bytecode.

### Residual dependencies (honestly NOT fully closed)
- Depositor EOA `0x3a57e710…` private key — the sole credential that can ever claim the 100,000 BLAST.
- `AccountManager.forceHarvest` inside `unlock` — liveness dependency: a bricked/upgraded AccountManager could revert `unlock` (freeze, not theft).
- `configStorage` `Paused` flag — governor can temporarily halt `unlock` (freeze, not theft).
- `MintManager` inflation — dilutes BLAST value; cannot move the locked principal.
- Blast chain-level availability — systemic, out of scope.

**Conclusion (narrowed):** within the audited surface — all of LockManager's own code, the MigrationManager contract that can reach it, and the BLAST token implementation — **no path exists by which any third party can move the locked principal**. Theft requires the depositor's own signature; that is the salvage this excavation verifies, not a vulnerability.

## Remaining candidate paths (untested, explicitly NOT_RUN)
- 17 further BLAST lockers (~13,198 BLAST) + ETH/USDB dust — same `unlock` path presumed live.
- Owner `claimERC20Yield` / `migrationManager` paths — not needed, unexplored.

## Recovery claim
Simulated only. Claimant authority: the depositor EOA itself — the calldata demonstrated is broadcastable solely by that wallet (msg.sender-keyed ledger; no relayer/operator path exists in code). Nothing was or could be moved by this run; upstream state verified unchanged.

## Replay
Prereqs: foundry 1.8.3 (`cast`, `anvil`), outbound HTTPS to `https://rpc.blast.io` (public archive). 
```
cd submissions/2026-11-05/devin/fork
bash reproduce.sh        # exit 0 expected; ~90 s incl. fork boot
```
Recorded reference run: `fork/run_log.txt` (REPRODUCE_EXIT_CODE=0). Artifact integrity: `SHA256SUMS.txt`.

## Time
Preflight ≈05:52Z → submission ≈06:55Z (≈63 min inside a 3 h window). Formal call log spans 06:14:25–06:16:36Z; every logged call carries a UTC timestamp.
