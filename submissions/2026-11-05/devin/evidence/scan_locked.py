import json, urllib.request, sys

RPC = "https://rpc.blast.io"
LM  = "0xEA091311Fc07139d753A6BBfcA27aB0224854Bae"
PIN = hex(42502847)          # pinned block
TOKENS = {
    "0x4300000000000000000000000000000000000003": "USDB",
    "0x4300000000000000000000000000000000000004": "WETH",
    "0x0000000000000000000000000000000000000000": "ETH",
    "0xb1a5700fa2358173fe465e6ea4ff52e36e88e2ad": "BLAST",
}
SEL = "0xbc22fd1b"  # getLocked(address)

d = json.load(open('txlist_p1.json'))
txs = d['result']
locks=set(); unlocks=set()
for t in txs:
    if t.get('isError')=='0':
        n=(t.get('functionName') or '').split('(')[0]
        if n in ('lock','lockOnBehalf'): locks.add(t['from'].lower())
        elif n=='unlock': unlocks.add(t['from'].lower())
players = sorted(locks - unlocks)
print("candidates:", len(players))

def batch(reqs):
    body = json.dumps(reqs).encode()
    r = urllib.request.Request(RPC, body, {"Content-Type":"application/json"})
    return json.loads(urllib.request.urlopen(r, timeout=60).read())

found = []
for i in range(0, len(players), 50):
    chunk = players[i:i+50]
    reqs = [{"jsonrpc":"2.0","id":j,"method":"eth_call","params":[
        {"to":LM,"data":SEL + p[2:].rjust(64,'0')}, PIN]} for j,p in enumerate(chunk)]
    try:
        out = batch(reqs)
    except Exception as e:
        print("batch err", e); continue
    resmap = {r['id']: r for r in out}
    for j,p in enumerate(chunk):
        r = resmap[j]
        if 'error' in r:
            continue
        data = r.get('result','0x')
        if data in ('0x','0x0'): continue
        raw = bytes.fromhex(data[2:])
        # ABI: offset -> array of structs (quantity,remainder,lastLockTime,unlockTime,tokenContract)
        try:
            off = int.from_bytes(raw[0:32],'big')
            n = int.from_bytes(raw[off:off+32],'big')
            pos = off+32
            for k in range(n):
                q  = int.from_bytes(raw[pos:pos+32],'big')
                rem= int.from_bytes(raw[pos+32:pos+64],'big')
                ut = int.from_bytes(raw[pos+96:pos+128],'big')
                tc = '0x'+raw[pos+128+12:pos+160].hex()
                pos += 160
                if q > 0:
                    found.append((p, TOKENS.get(tc.lower(),tc), q, ut))
        except Exception as e:
            print("decode err", p, e)

json.dump(found, open('still_locked.json','w'), indent=1)
for f in found:
    print(f[0], f[1], f[2]/1e18, 'unlockTime=',f[3])
print("total still locked:", len(found))
