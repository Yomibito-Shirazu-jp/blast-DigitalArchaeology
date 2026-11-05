# Claude research brief | Current token-asset inventory and administrative blockers

**Research assignment:** Claude (research in progress; no audited numbers entered yet)

## Two separate inventory tables

### A. Current on-chain token assets

Count and value assets that can be independently observed at a fixed reference block. Provide both **distinct holding addresses** and **unique token contracts**, since they are different statistics.

| Chain | Snapshot UTC / block hash | Token | Token address | Holder/contract address | Token amount (raw + decimals) | USD unit price / UTC source | USD valuation | Evidence |
|---|---|---|---|---|---|---|---|---|
| NOT_REPORTED | NOT_REPORTED | — | — | — | — | — | — | — |

**Totals (not yet audited):** USD amount = NOT_REPORTED; distinct holding addresses = NOT_REPORTED; distinct token contract addresses = NOT_REPORTED.

### B. Assets reportedly inaccessible because of administrator or governance conditions

Include only assets for which the **specific operational/authorization blocker is evidenced** (e.g., pause, inactive or inaccessible multisig, failed permitted withdrawal path, expired governance process, disabled bridge). Do not automatically attribute custody to administrator misconduct or claim irrecoverability merely because a withdrawal did not succeed.

| Chain | Snapshot UTC / block hash | Token | Holding contract address | Token amount | USD amount / price source | Number of affected addresses/claimants | Verified blocker and authority | Last successful recovery test / status | Evidence |
|---|---|---|---|---|---|---|---|---|---|
| NOT_REPORTED | — | — | — | — | — | — | — | — | — |

**Totals (not yet audited):** USD amount = NOT_REPORTED; distinct holding addresses = NOT_REPORTED; affected claimant addresses = NOT_REPORTED.

## Classification and accounting rules

1. Record chain ID, block **number and hash**, UTC snapshot time, token contract, holding contract, raw balance, decimals, exchange rate source and timestamp. Historical snapshots must not be mislabeled as current.
2. Define the address count precisely. Report unique **holding contract addresses**, **token contract addresses**, and **eligible claimant addresses** separately. Deduplicate using chain+address; do not mix wallet counts with contract counts.
3. Distinguish gross escrowed assets from **free surplus**, **contractual/user liabilities**, and **claimable balances**. Report uncertainty and avoid summing liabilities as recoverable surplus.
4. Avoid double counting rebasing tokens (such as stETH shares vs. displayed balances), bridge wrappers, pool receipt tokens, and positions representing the same underlying asset.
5. Verify governance/proxy/owner authorization from deployed bytecode and contract storage at the same reference block. Administrative inability, user inactivity, protocol downtime, legal limitations, and permanent inaccessibility are not equivalent.
6. For each inaccessible claim, provide the exact failing call, revert/traces, available permissions, and any known successful authorized route. A paused contract alone does not establish permanent loss.
7. A read-only `eth_call`, an impersonated fork transaction, or an overridden storage balance does not prove a live fund recovery.
8. Publish methodology, scripts, sanitized RPC logs, independent replay and SHA256 hashes; keep secrets out of the repository.
9. State **coverage**: scanned contracts, chains, block ranges, inclusion criteria, exclusions and how complete the result is. A partial census cannot be described as all stranded assets.
10. Preserve the original investigation under `submissions/` or a dedicated research branch; do not overwrite the Blast source code.

### Required reporting totals

- Current assets: number of holding addresses; number of token contract addresses; total USD estimate; verified snapshot UTC.
- Admin/governance-blocked assets: number of holding addresses; number of claimant addresses **when measurable**; total USD estimate; count and evidence per distinct blocker type.
- Explicit line-item links and unresolved uncertainty; **no numbers should be filled until actual evidence is recorded**.

**Contact and engagement policy:** [Requests for digital archaeology research](../CONTACT.md).
