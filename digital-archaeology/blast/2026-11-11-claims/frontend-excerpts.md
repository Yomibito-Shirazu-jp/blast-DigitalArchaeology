# 公式フロントJSの抽出記録

出典：ユーザーが取得した `https://blast.io/assets/index-E2w4LnB3.js` のPowerShell抜粋。以下は表示用に整形した転記。

## ABI

```solidity
function roots(bytes32 root) view returns (bool);
function claimed(address user) view returns (bool);
function isApprovedRedeemer(address user, address[] _redeemers, address redeemer) view returns (bool);
function claim(address user, uint256 ethAmount, uint256 usdAmount, address[] _redeemers, bytes32[] proof, bytes32 root);
```

エラー名：`InvalidRedeemer`, `AlreadyClaimed`, `InvalidProof`, `InvalidRoot`, `ETHTransferFailed`, `Unapproved`, `UpgradesRevoked`。

## leafとpairの関数

```javascript
function n_(e,t,n,r){
  let i=A(hd([`address[]`],[r]));
  return A(A(gr(Ke(`address, uint256, uint256, bytes32`),[e,t,n,i])));
}
function p_(e,t){return A(or(e<t?[e,t]:[t,e]));}
```

## chunkの位置計算

```javascript
var u_=e=>31-Math.clz32(e+1);
function d_(e,t){
  for(;u_(e)>t;) e=e-1>>1;
  return e-(2**t-1);
}
function f_(e,t,n,r){
  let i=Math.min(2**(n+1)-1,r),a=u_(e);
  if(a<=n)return e;
  let o=2**n-1+t,s=i;
  for(let e=1;e<a-n;e++){
    let t=(o+1)*2**e-1;
    s+=Math.max(0,Math.min(r,t+2**e)-t);
  }
  let c=(o+1)*2**(a-n)-1;
  if(e<c||e>=c+2**(a-n))
    throw Error(`node ${e} is not in chunk ${t}`);
  return s+(e-c);
}
```

`s=i` を保持する。調査例の `i` は127。

## fetchClaim

```javascript
async fetchClaim(e){
  let t=await this.loadManifest();
  if(!t)return null;
  let n=e.toLowerCase(),
      r=n.slice(2,2+t.shardPrefixLength),
      i=(await s_(this.shards,r,()=>l_(`${this.url}shards/${r}.json`,{})))[n];
  if(!i)return null;
  let [a,o,s,c,l=[],u=0]=i,
      d=l.map(e=>e),
      {root:f,leaves:p}=t.trees[s],
      m=2*p-1,
      {chunkDepth:h}=t,
      g=d_(c,h),
      _=await this.loadChunk(s,g),
      v=e=>{
        let t=f_(e,g,h,m)*32;
        if(t+32>_.length)throw Error(`Proof data is truncated`);
        return O(_.subarray(t,t+32));
      },
      y=[];
  for(let e=c;e>0;e=e-1>>1)y.push(v(e%2?e+1:e-1));
  let b=n_(e,BigInt(a),BigInt(o),d),x=y.reduce(p_,b);
  if(v(c)!==b||x!==f.toLowerCase())
    throw Error(`Proof data for this account is inconsistent. Please contact support.`);
  return {pendingWithdrawals:u,ethAmount:BigInt(a),usdAmount:BigInt(o),redeemers:d,proof:y,root:f};
}
```

`loadManifest` は `manifest.json` を取得しversionを確認。`loadChunk` は `trees/<tree>/<chunk>.bin` を取得。返却 `proof:y` は兄弟ノード抽出後の配列。

## 公式chunk復元のユーザー実行結果

対象：`0x8D8B9c79196f32161BcB2A9728D274B3b45eB9AF`

```text
chunk 51 http 200
bytes 36768 words 1149
calcLeaf 0x465909272ffe136b754597907b333d42ba18dcd988a3bf6a00fb5c096882f897
atLeaf   0x465909272ffe136b754597907b333d42ba18dcd988a3bf6a00fb5c096882f897 match true
rootMatch true len 15
SIM 0xfd8dB47e7371dC3751D8B84EBd040046D70dF5d0 OK
SIM 0x1111111111111111111111111111111111111111 OK
```
