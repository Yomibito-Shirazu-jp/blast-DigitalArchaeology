# Hypotheses — tested paths and falsifying observations

## H0 — "Sunken assets exist on Blast and are recoverable by a legitimate path"
Candidate selection: Blast ecosystem graveyards — Munchables (insider exploit + game shutdown), Thruster (exploit), Super Sushi Samurai (self-transfer bug), Risk on Blast (rug). Munchables chosen: documented incident + post-incident contract still live + official end-of-game withdrawal instructions = clean claim-rights case.

## H1 — "LockManager still holds locked user assets" → CONFIRMED
`balanceOf(LockManager)` @42502847: 122,315 BLAST / 90 USDB / 0.5634 ETH / 0 WETH. Legacy contract = 0 everywhere (already salvaged). Discovery method: full `txlist` → all lock/unlock participants → batch `eth_call getLocked` → 18 BLAST lockers (113,198 BLAST), biggest `0x3a57e710` with exactly 100,000 BLAST.

## H2 — "unlock() is blocked (paused / dead dependency / time-lock)" → REJECTED
- `lockedTokens.quantity = 1e23 >= qty`; `unlockTime = 1734916739 < block.timestamp 1793815509`.
- `notPaused` passes; `nonReentrant` passes.
- Internal `accountManager.forceHarvest(msg.sender)` → AccountManager proxy `0xfB5cd7…` is live and the call does not revert at PIN.
- `eth_call unlock(BLAST, 1e23)` from depositor @PIN → `0x` success (verbatim `calls.jsonl#G4-unlock-eth_call-full`).

## H3 — "Path is permissionless or exploitable by third party" → REJECTED (and required for legitimacy)
Ledger keyed by `msg.sender`; `unlock` from `0x…dEaD` reverts `InsufficientLockAmountError (0x57e6e23d)` (`calls.jsonl#G3-negative-nonowner`). Only the depositor's wallet can produce the authorized call — the path is a legitimate self-claim, not a third-party transfer. This is the boundary between salvage verification and unauthorized movement; we verify the former only.

## H4 — "eth_call success is enough to claim EFFECT" → REJECTED by our own methodology
eth_call proves non-reversion, not the asset diff. Effect was demonstrated two ways:
- (a) `debug_traceCall` + `prestateTracer{diffMode}` at PIN — upstream Alchemy archive and local anvil fork both produce identical storage diffs: BLAST `balanceOf[player]` → `1e23`, `balanceOf[LockManager]` → `22,315.1853e18`. Read-only; evaluates under the depositor's real on-chain authorization; no cheatcodes.
- (b) Synthetic-actor diagnostic (clearly marked): `anvil_impersonateAccount` + `anvil_setBalance` (gas only) → real fork tx `0xa2f4e8…` status 1, gas 352,043, `Transfer(LockManager→player, 1e23)` + `Unlocked` events. This produces a full receipt incl. event logs but impersonates the claimant, so it is filed as supplementary/synthetic — per the spec it does not claim real-world authority.
- Second unlock reverts → no double spend. Upstream `balanceOf(player)` still 0 → mainnet untouched.

## H5 — "getLogs-based discovery was feasible on public RPC" → REJECTED
`eth_getLogs` limited to 10,000-block ranges on `rpc.blast.io` (HTTP 413, error -32614) — logged infrastructure limitation; replaced by explorer txlist + direct mapping reads. Also three initial `eth_call`s used wrong guessed selectors and reverted `0xd8fa635d`; retained in `calls.jsonl` and re-run with corrected selectors (`*-FIXED` entries).

## Failed / unexplored alternatives (explicitly NOT_RUN)
- `claimERC20Yield` owner path: owner could skim ERC20 rebasing yield — out of scope (not user-principal salvage).
- `migrationManager` path for migrating locks — not needed once `unlock` proved live.
- Larger dig across the other 287 stranded entries — inventory delivered, per-entry unlock simulation left as future work.
