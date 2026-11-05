# Methodology | 発掘方法論

## Excavation workflow

1. **TARGET:** identify chain, contract, legitimate claimant, asset, block number and hash.
2. **HISTORY:** reconstruct deployment, runtime bytecode and implementation lineage.
3. **PATH:** state a testable, authorized recovery hypothesis and independent enforcement conditions.
4. **CALL:** record real read-only `eth_call` responses at pinned block state, including failures.
5. **EFFECT:** test actual debit/credit and ledger transitions on a deterministic local fork with synthetic assumptions explicitly disclosed.
6. **REPRO:** provide executable scripts, input data, timestamps, hashes, versions, exit codes, and independent audit.

See the [Blast excavation challenge draft](https://github.com/Yomibito-Shirazu-jp/blast-DigitalArchaeology/pull/1) for the original six-gate specification.

## Evidence categories

- **Observed:** primary RPC, on-chain receipt, contract bytecode, timestamped source records.
- **Inferred:** interpretations supported by observed evidence but not directly measured.
- **Simulated:** a conditional run under declared historical state and caller assumptions.
- **Reproduced:** a second, independent execution with matching outputs.
- **Unverified:** statements without inspectable evidence.

Changing a token's balance storage to zero is **not proof of recovery**. Confirm the actual recipient credit, originating debit, execution path and legitimate authority.
