# Blast Restoration Workspace

This directory organizes reproducible, isolated research to reconstruct historical Blast chain behavior and investigate failed L2-to-L1 withdrawals. It does **not** claim control over the original network, custody contracts, or recovery entitlement.

## Directory map

- [`node-deployment/`](./node-deployment/) — Deployment manifests, pinned versions, and host configuration for a standalone Blast node.
- [`chain-state/`](./chain-state/) — Historical block references, chain configuration, storage snapshots, and provenance notes.
- [`local-reproduction/`](./local-reproduction/) — Isolated L1/L2 forks, deterministic test fixtures, and withdrawal replays.
- [`validation/`](./validation/) — Cross-chain message checks, token accounting, contract verification, and test results.
- [`recovery-reports/`](./recovery-reports/) — Evidence-backed findings, limitations, and authorized recovery options.

## Principles

1. Preserve original source and evidence files; keep restoration work separate.
2. Record chain IDs, block heights, contract addresses, and source commit SHAs.
3. Distinguish historical observations from local simulations.
4. Do not commit private keys, RPC credentials, JWT secrets, raw chain databases, or sensitive account material.
5. Run experiments only on owned or explicitly authorized environments. Do not broadcast recovery simulations to production networks.

## Initial investigation

- Blast L2 transaction: `0xe1ce70e43bca67c38d91ce2005711dc66bbbff09f951a7305090c24f7c71f7e7`
- L2 block: `41941061`
- Withdrawal hash: `0x8f72d51d52686ac895d10f7be5ec8371d9c852b6c8ef831f0247bd5a33f4eb8e`
- L1 message hash: `0x49732e1a516c59ab4f17d9dd6688be7769f95f97eec9321473e599699bc08e54`

These are investigation identifiers, not verified proof of recoverable asset balances.
