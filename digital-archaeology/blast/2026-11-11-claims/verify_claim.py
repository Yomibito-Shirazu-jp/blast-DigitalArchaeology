#!/usr/bin/env python3
"""Offline Keccak/ABI/proof verification. Python standard library only."""
import json
from pathlib import Path
MASK = (1 << 64) - 1
RC = [0x0000000000000001,0x0000000000008082,0x800000000000808a,0x8000000080008000,0x000000000000808b,0x0000000080000001,0x8000000080008081,0x8000000000008009,0x000000000000008a,0x0000000000000088,0x0000000080008009,0x000000008000000a,0x000000008000808b,0x800000000000008b,0x8000000000008089,0x8000000000008003,0x8000000000008002,0x8000000000000080,0x000000000000800a,0x800000008000000a,0x8000000080008081,0x8000000000008080,0x0000000080000001,0x8000000080008008]
ROT = [[0,36,3,41,18],[1,44,10,45,2],[62,6,43,15,61],[28,55,25,21,56],[27,20,39,8,14]]
def rol(x, n):
    return ((x << n) | (x >> ((64-n) % 64))) & MASK
def permute(a):
    for rc in RC:
        c = [a[x]^a[x+5]^a[x+10]^a[x+15]^a[x+20] for x in range(5)]
        d = [c[(x-1)%5]^rol(c[(x+1)%5],1) for x in range(5)]
        for x in range(5):
            for y in range(5): a[x+5*y] ^= d[x]
        b = [0]*25
        for x in range(5):
            for y in range(5): b[y+5*((2*x+3*y)%5)] = rol(a[x+5*y], ROT[x][y])
        for x in range(5):
            for y in range(5): a[x+5*y] = b[x+5*y]^((~b[(x+1)%5+5*y]) & b[(x+2)%5+5*y])
        a[0] ^= rc
def keccak(data):
    rate = 136
    pad = rate - len(data)%rate
    data += b'\x81' if pad == 1 else b'\x01'+b'\x00'*(pad-2)+b'\x80'
    a = [0]*25
    for offset in range(0,len(data),rate):
        for i in range(rate//8): a[i] ^= int.from_bytes(data[offset+i*8:offset+(i+1)*8],'little')
        permute(a)
    return b''.join(x.to_bytes(8,'little') for x in a)[:32]
def word(n): return int(n).to_bytes(32,'big')
def addr(a): return bytes.fromhex(a[2:]).rjust(32,b'\0')
def main():
    assert keccak(b'').hex() == 'c5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470'
    assert keccak(b'abc').hex() == '4e03657aea45a94fc7d47ba826c8d667c0d1e6e33a64a036ec44f58fa12d6c45'
    row = json.loads(Path(__file__).with_name('claim-01.json').read_text())
    redeemers = b''.join(addr(a) for a in row['redeemers'])
    redeemer_hash = keccak(word(32)+word(len(row['redeemers']))+redeemers)
    leaf = keccak(keccak(addr(row['user'])+word(row['ethAmount'])+word(row['usdAmount'])+redeemer_hash))
    h = bytes.fromhex(row['leaf'][2:])
    steps = []
    for p in row['proof']:
        sibling = bytes.fromhex(p[2:])
        h = keccak(min(h,sibling)+max(h,sibling))
        steps.append('0x'+h.hex())
    selector = keccak(b'claim(address,uint256,uint256,address[],bytes32[],bytes32)')[:4]
    proof_bytes = b''.join(bytes.fromhex(p[2:]) for p in row['proof'])
    redeemer_tail = word(len(row['redeemers']))+redeemers
    payload = (addr(row['user'])+word(row['ethAmount'])+word(row['usdAmount'])+word(192)
        +word(192+len(redeemer_tail))+bytes.fromhex(row['root'][2:])
        +redeemer_tail+word(len(row['proof']))+proof_bytes)
    calldata = '0x'+(selector+payload).hex()
    result = {'keccak_vectors_pass':True,'abi_leaf':'0x'+leaf.hex(),
        'stored_leaf_matches_abi':('0x'+leaf.hex()==row['leaf']),
        'proof_steps':steps,'proof_root_matches':('0x'+h.hex()==row['root']),
        'selector':'0x'+selector.hex(),'calldata_bytes':len(selector+payload),
        'calldata_matches_saved':calldata==Path(__file__).with_name('claim-01-calldata.txt').read_text().strip()}
    print(json.dumps(result,indent=2))
    assert result['proof_root_matches'] and result['calldata_matches_saved']
if __name__ == '__main__': main()
