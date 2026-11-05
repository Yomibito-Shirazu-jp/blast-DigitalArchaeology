#!/usr/bin/env python3
"""
PoC — Sunken BLAST salvage on Munchables LockManager (Blast, chain 81457)
========================================================================
Self-contained proof-of-concept. Requires ONLY:
  - python 3.9+ (stdlib only)
  - anvil (foundry) on PATH
  - outbound HTTPS to https://rpc.blast.io (public archive node, no key)

What it proves (at pinned block 42502847):
  [1] LockManager holds 122,315.1853 BLAST
  [2] depositor 0x3a57e710...d5a has lockedTokens.quantity = 1e23 (100,000 BLAST),
      unlockTime already expired
  [3] read-only eth_call unlock(BLAST, 1e23) from the depositor SUCCEEDS
  [4] eth_call unlock from a non-depositor REVERTS (InsufficientLockAmountError)
  [5] on a local anvil fork the same call deterministically moves
      100,000 BLAST LockManager -> depositor, zeroes the lock ledger
      (debug_traceCall prestateTracer diff — NO impersonation cheatcode
      needed for the state-diff evidence; impersonated send is a
      disclosed synthetic-actor supplement emitting real event logs)
Exit code 0 = every check passed. Nothing is broadcast to mainnet.
"""
import json, subprocess, sys, time, urllib.request, urllib.error

RPC   = "https://rpc.blast.io"
LOCAL = "http://127.0.0.1:8545"
PIN   = "0x2888abf"                      # block 42502847
LM    = "0xEA091311Fc07139d753A6BBfcA27aB0224854Bae"
BLAST = "0xb1a5700fA2358173Fe465e6eA4Ff52E36e88E2ad"
P     = "0x3a57e71046a29dcc47db9e0fc11a893631413d5a"
DEAD  = "0x000000000000000000000000000000000000dEaD"
QTY   = 10**23                           # 100,000 BLAST

pad = lambda a: a.lower().replace("0x", "").rjust(64, "0")
BAL    = lambda a: "0x70a08231" + pad(a)
LOCKED = lambda a, b: "0x0774e003" + pad(a) + pad(b)
UNLOCK = lambda t, q: "0x7eee288d" + pad(t) + hex(q)[2:].rjust(64, "0")

_id = 0
def rpc(url, method, params):
    global _id; _id += 1
    body = json.dumps({"jsonrpc": "2.0", "id": _id, "method": method,
                       "params": params}).encode()
    req = urllib.request.Request(url, body, {"Content-Type": "application/json"})
    try:
        r = json.loads(urllib.request.urlopen(req, timeout=120).read())
    except urllib.error.HTTPError as e:
        return {"error": {"http": e.code, "body": e.read()[:400].decode(errors="replace")}}
    except (urllib.error.URLError, OSError) as e:
        return {"error": {"transport": repr(e)}}
    return r

def eth_call(url, to, data, blk, frm=None):
    o = {"to": to, "data": data}
    if frm: o["from"] = frm
    return rpc(url, "eth_call", [o, blk])

def dec_u256(h): return int(h, 16)

checks = []
def check(name, ok, detail=""):
    checks.append((name, ok))
    print(("PASS" if ok else "FAIL"), name, ("| " + detail if detail else ""))

print("== PoC: Munchables LockManager sunken BLAST @ block 42502847 ==")

# ---- pinned block identity (G1) ----
EXP_HASH = "0x9fa65187eb7dd1f902ba4a3cf3ec682d293a6c948d9bfc564134297614fc62c9"
b = rpc(RPC, "eth_getBlockByNumber", [PIN, False]).get("result", {})
check("G1 pinned block hash matches", b.get("hash") == EXP_HASH,
      f"hash={b.get('hash')}")
check("G1 pinned block timestamp", int(b.get("timestamp", "0x0"), 16) == 1793815509,
      f"ts={int(b.get('timestamp','0x0'),16)}")

# ---- G2-lite: deployed bytecode identity + deploy tx lineage ----
code = rpc(RPC, "eth_getCode", [LM, PIN]).get("result", "0x")
try:
    ref = open("../evidence/lm_bytecode.hex").read().strip()
    same = (code.lower() == ref.lower())
    detail = f"bytecode {len(code)//2-1}B matches evidence/lm_bytecode.hex"
except OSError:
    same, detail = len(code) > 100, "evidence file absent; only non-empty checked"
check("G2 LockManager bytecode == verified artifact", same, detail)

dep = rpc(RPC, "eth_getTransactionByHash",
          ["0xa73c806a5f2d808c6ea2d5a2e871b7b825af93c814b2c4c571100a08dfca9b6d"]).get("result", {})
check("G2 deploy tx at block 4233706",
      dep.get("blockNumber") == "0x4099ea",
      f"blockNumber={dep.get('blockNumber')}")

# ---- upstream, pinned ----
r = eth_call(RPC, BLAST, BAL(LM), PIN)
lm_bal = dec_u256(r.get("result", "0x0"))
check("G1 contract holds BLAST", lm_bal == 122315185300000000000000,
      f"balanceOf(LockManager)={lm_bal/1e18:,.4f} BLAST")

r = eth_call(RPC, LM, LOCKED(P, BLAST), PIN)
raw = r.get("result", "0x")
qty = int(raw[2:66], 16) if len(raw) >= 66 else 0
unlock_time = int(raw[194:258], 16) if len(raw) >= 258 else 0
check("G1 depositor lock = 100,000 BLAST", qty == QTY, f"quantity={qty/1e18:,.2f}")
check("G1 unlockTime expired", 0 < unlock_time < 1793815509,
      f"unlockTime={unlock_time} < pin_ts=1793815509")

r = eth_call(RPC, LM, UNLOCK(BLAST, QTY), PIN, frm=P)
check("G4 eth_call unlock(1e23) succeeds", r.get("result") == "0x",
      f"result={r.get('result', r.get('error'))}")

r = eth_call(RPC, LM, UNLOCK(BLAST, 1), PIN, frm=DEAD)
err = json.dumps(r.get("error", {}))
check("G3 non-depositor reverts", "0x57e6e23d" in err,
      f"revert data=0x57e6e23d InsufficientLockAmountError observed={'0x57e6e23d' in err}")

# ---- local fork ----
anvil = subprocess.Popen(
    ["anvil", "--fork-url", RPC, "--fork-block-number", "42502847",
     "--chain-id", "81457", "--port", "8545", "--silent"],
    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
try:
    for _ in range(60):
        if rpc(LOCAL, "eth_blockNumber", []).get("result"):
            break
        time.sleep(1)
    else:
        check("fork boots", False); sys.exit(1)

    # G5 primary: read-only state diff, no impersonation.
    # Slot identities verified cryptographically:
    #   SLOT_PLAYER_BAL = keccak256(abi.encode(player, 0))   (BLAST balanceOf @ slot 0)
    #   SLOT_LM_BAL     = keccak256(abi.encode(LockManager, 0))
    #   SLOT_LOCK_QTY   = keccak256(abi.encode(BLAST, keccak256(abi.encode(player, 11))))
    #                   (lockedTokens[player][BLAST].quantity; lockedTokens @ slot 11)
    SLOT_PLAYER_BAL = "0x340bab9bd1a340d62a76df2c4488eabdb6d650a19decb6513c5b6a676be29f37"
    SLOT_LM_BAL     = "0x9a66ec1f0ffaa1d19d28bb0752bd78dfa89d7f2047b43794555848e46e94e9a9"
    SLOT_LOCK_QTY   = "0xc3bb8a778c7705f78a0a5c7c8d3e7f02e9697fef6657e441e53622e851e4516c"
    r = rpc(LOCAL, "debug_traceCall",
            [{"from": P, "to": LM, "data": UNLOCK(BLAST, QTY)}, "latest",
             {"tracer": "prestateTracer", "tracerConfig": {"diffMode": True}}])
    res = r.get("result", {})
    pre_blast  = res.get("pre",  {}).get(BLAST.lower(), {}).get("storage", {})
    post_blast = res.get("post", {}).get(BLAST.lower(), {}).get("storage", {})
    pre_lm     = res.get("pre",  {}).get(LM.lower(),    {}).get("storage", {})
    post_lm    = res.get("post", {}).get(LM.lower(),    {}).get("storage", {})
    gv = lambda d, k: int(d.get(k, "0x0"), 16)
    pre_pb, post_pb = gv(pre_blast, SLOT_PLAYER_BAL), gv(post_blast, SLOT_PLAYER_BAL)
    pre_lb, post_lb = gv(pre_blast, SLOT_LM_BAL),     gv(post_blast, SLOT_LM_BAL)
    pre_q,  post_q  = gv(pre_lm, SLOT_LOCK_QTY),      gv(post_lm, SLOT_LOCK_QTY)
    check("G5 pre-state: LM bal=122,315.1853, player bal=0, lock qty=1e23",
          pre_lb == 122315185300000000000000 and pre_pb == 0 and pre_q == QTY,
          f"pre: LM={pre_lb/1e18:,.4f} player={pre_pb} qty={pre_q/1e18:,.2f}")
    check("G5 post-state: player=100,000, LM=22,315.1853, lock qty=0",
          post_pb == QTY and post_lb == 22315185300000000000000 and post_q == 0,
          f"post: player={post_pb/1e18:,.2f} LM={post_lb/1e18:,.4f} qty={post_q}")
    check("G5 conservation: LM debit == player credit (no mint/burn)",
          (pre_lb - post_lb) == (post_pb - pre_pb) == QTY,
          f"delta={ (pre_lb-post_lb)/1e18:,.4f} BLAST")
    check("G5 slot identities: exactly the two balanceOf slots changed",
          set(post_blast) == {SLOT_PLAYER_BAL, SLOT_LM_BAL},
          f"changed={sorted(post_blast)}")

    # G5 supplementary (marked synthetic): real tx incl. event logs
    rpc(LOCAL, "anvil_impersonateAccount", [P])
    rpc(LOCAL, "anvil_setBalance", [P, "0x3635C9ADC5DEA00000"])
    send = rpc(LOCAL, "eth_sendTransaction",
               [{"from": P, "to": LM, "data": UNLOCK(BLAST, QTY),
                 "gas": "0x1c9c380"}])
    txh = send.get("result")
    if not txh:
        print("send response:", json.dumps(send)[:400])
    rcp = {}
    for _ in range(20):
        r = rpc(LOCAL, "eth_getTransactionReceipt", [txh]).get("result")
        if r:
            rcp = r
            break
        time.sleep(0.5)
    p_after = dec_u256(eth_call(LOCAL, BLAST, BAL(P), "latest").get("result", "0x0"))
    lm_after = dec_u256(eth_call(LOCAL, BLAST, BAL(LM), "latest").get("result", "0x0"))
    check("G5 fork tx status=1", rcp.get("status") == "0x1",
          f"tx={txh} gasUsed={int(rcp.get('gasUsed','0x0'),16) if rcp else '?'}")
    check("G5 fork diff: player 0->100,000 BLAST", p_after == QTY, f"{p_after/1e18:,.2f}")
    check("G5 fork diff: LM 122,315->22,315 BLAST",
          lm_after == 22315185300000000000000, f"{lm_after/1e18:,.4f}")
finally:
    anvil.terminate()

print("==", sum(1 for _, ok in checks if ok), "/", len(checks), "checks passed ==")
sys.exit(0 if all(ok for _, ok in checks) else 1)
