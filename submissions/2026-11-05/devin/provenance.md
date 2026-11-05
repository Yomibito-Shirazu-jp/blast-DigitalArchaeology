# Provenance — Munchables LockManager (0xEA091311Fc07139d753A6BBfcA27aB0224854Bae)

Observed facts are marked **[ON-CHAIN]**; external-document claims are **[EXT]**; interpretations are **[HYP]**.

## Chain & pin
- **[ON-CHAIN]** Blast chainId 81457 (`0x13e31`); pinned block 42502847 (`0x2888abf`), hash `0x9fa65187eb7dd1f902ba4a3cf3ec682d293a6c948d9bfc564134297614fc62c9`, timestamp 1793815509 (2026-11-03). Head at capture: `0x2888bb5`. Archive access confirmed down to block 500,000 (WETH totalSupply query).

## Contract lineage
- **[ON-CHAIN]** LockManager deployed at block 4,233,706 (2024-06-01), tx `0xa73c806a5f2d808c6ea2d5a2e871b7b825af93c814b2c4c571100a08dfca9b6d` (`calls.jsonl#deploy-tx`). Non-proxy, 17,703-byte runtime bytecode, keccak `0x0b9373f057fba4b91d63403abcf250babfc3835aa62e567837d7f2a3914bccfd`.
- **[ON-CHAIN]** Verified source (Solidity 0.8.25, optimizer 200 runs, EVM paris) retrieved via routescan etherscan-compatible API (`evidence/source.json`, extracted `evidence/src/`). Constructor arg: `_configStorage = 0xef173bb4b36525974bf6711357d2c6c12b8001ec`.
- **[EXT]** Munchables suffered an insider exploit on 2024-03-26: a rogue developer back-doored the legacy lock contract `0x29958e8e4d8a9899cf1a0aba5883dbc7699a5e1f` (upgrade to implementation `0x910fFc04…`) and withdrew ~17,413 ETH (~$62.5M). Exploiter: `0x6e8836f050a315611208a5cd7e228701563d09c5` (Blastscan-labelled; Beosin/0xScope write-ups). Keys were surrendered; ~$97M was secured in a Blast-core multisig (statement by Blast founder "Pacman").
- **[ON-CHAIN]** The legacy contract today holds 0 ETH / 0 WETH / 0 USDB / 0 BLAST — fully salvaged.
- **[EXT]** Code4rena audit contest `2024-07-munchables` names this live LockManager address and the on-chain AccountManager proxy `0xfB5cd7507A3Cb0932029Df2E78165667954C8286` (finding #30 quotes the live `forceHarvest` code path).
- **[EXT]** Project gitbook "FAQs – End of Game" states the website is closed and instructs users to withdraw locked ETH/BLAST via `unlock` on `0xEA09…4Bae`. The game is dead; un-withdrawn locks are genuinely stranded — the "sunken ship".
- **[ON-CHAIN]** `accountManager()` = `0xfB5cd7507A3Cb0932029Df2E78165667954C8286` (has code; proxy). `lockdrop()` start=0, end=2671126036, minLockDuration=2592000.

## Asset
- **[ON-CHAIN]** BLAST ERC20 `0xb1a5700fA2358173Fe465e6eA4Ff52E36e88E2ad` (decimals 18, native-yield/rebasing token).
- **[ON-CHAIN]** LockManager balances @42502847: BLAST 122,315.1853; USDB 90.0; native ETH 0.5634; WETH 0.

## Claimant lineage (from `evidence/txlist_p1.json`, 5,270 txs)
- **[ON-CHAIN]** `0x3a57e71046a29dcc47db9e0fc11a893631413d5a` (EOA — `eth_getCode` = `0x`):
  - `0xfce46ed7…` @10,404,826 — `lock(BLAST, 99999.99999999999e18)`
  - `0x8a721c47…` @11,757,429 — `unlock(BLAST, 99999.99999999999e18)` (prior lock withdrawn)
  - `0xc0fa0d0b…` @11,757,457 — `setLockDuration` (extended)
  - `0xdfc9fc3a…` @11,757,462 — `lock(BLAST, 99999.99999999999e18)` → live lock: `lastLockTime=1732324739` (2024-11-23), `unlockTime=1734916739` (2024-12-23)
- **[ON-CHAIN]** `lockedTokens(player, BLAST)` @42502847 = quantity `1e23` (the extra ~100000 wei over the raw input is ledger remainder merged at lock time), remainder 0.
- **[HYP]** The depositor extended their lock duration twice; unlockTime elapsed 2024-12-23 and the position was never reclaimed — consistent with an abandoned/dead-account scenario typical of a dead game.

## Stranded population
- **[ON-CHAIN]** `getLocked` scan of all 1,658 lock/unlock participants @42502847: 18 players hold 113,198 BLAST total (top: this case 100,000; then 2,500 / 2,098 / 1,200 / ~500-class), 195 ETH-dust locks (~0.049 ETH), 1 USDB lock (10). See `evidence/still_locked_all.json`.
