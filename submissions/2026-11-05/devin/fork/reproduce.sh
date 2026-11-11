#!/usr/bin/env bash
# Munchables LockManager sunken-BLAST salvage — full reproduction script
# Environment: foundry (cast/anvil) 1.8.3, blast public archive RPC
# Pinned block: 42502847 (hash 0x9fa65187eb7dd1f902ba4a3cf3ec682d293a6c948d9bfc564134297614fc62c9, ts 1793815509)
set -euo pipefail

R=https://rpc.blast.io
LM=0xEA091311Fc07139d753A6BBfcA27aB0224854Bae        # Munchables LockManager
BLAST=0xb1a5700fA2358173Fe465e6eA4Ff52E36e88E2ad       # BLAST ERC20
P=0x3a57e71046a29dcc47db9e0fc11a893631413d5a         # rightful locker (depositor)
PIN=42502847
QTY=100000000000000000000000                         # 100,000 BLAST (1e23)

echo "### TARGET: assets locked in sunken contract @ block $PIN"
cast call $LM "lockedTokens(address,address)(uint256,uint256,uint32,uint32)" $P $BLAST --block $PIN --rpc-url $R
cast call $BLAST "balanceOf(address)(uint256)" $LM    --block $PIN --rpc-url $R
cast call $BLAST "balanceOf(address)(uint256)" $P     --block $PIN --rpc-url $R
cast call $LM  "accountManager()(address)"            --block $PIN --rpc-url $R
cast call $LM  "lockdrop()(uint32,uint32,uint32)"     --block $PIN --rpc-url $R

echo "### CALL: eth_call unlock(BLAST, 1e23) from depositor @ $PIN"
cast call $LM "unlock(address,uint256)" $BLAST $QTY --from $P --block $PIN --rpc-url $R

echo "### CALL (negative): non-depositor cannot unlock"
cast call $LM "unlock(address,uint256)" $BLAST 1 --from 0x000000000000000000000000000000000000dEaD --block $PIN --rpc-url $R || echo "revert (expected): InsufficientLockAmountError"

echo "### EFFECT: local fork state diff"
anvil --fork-url $R --fork-block-number $PIN --chain-id 81457 --port 8545 --silent &
ANVIL_PID=$!; sleep 4
A=http://127.0.0.1:8545
cast rpc anvil_impersonateAccount $P --rpc-url $A
cast rpc anvil_setBalance $P 0x3635C9ADC5DEA00000 --rpc-url $A
echo "-- before --"
cast call $BLAST "balanceOf(address)(uint256)" $P  --rpc-url $A
cast call $BLAST "balanceOf(address)(uint256)" $LM --rpc-url $A
echo "-- exec --"
cast send $LM "unlock(address,uint256)" $BLAST $QTY --from $P --unlocked --rpc-url $A --gas-limit 30000000
echo "-- after --"
cast call $BLAST "balanceOf(address)(uint256)" $P  --rpc-url $A
cast call $BLAST "balanceOf(address)(uint256)" $LM --rpc-url $A
cast call $LM "lockedTokens(address,address)(uint256,uint256,uint32,uint32)" $P $BLAST --rpc-url $A
kill $ANVIL_PID
echo "### DONE"
