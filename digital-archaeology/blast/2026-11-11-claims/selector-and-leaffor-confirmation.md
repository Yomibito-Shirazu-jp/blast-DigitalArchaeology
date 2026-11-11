# selector対応とleafForのオンチェーン照合

記録日：2026-11-11（日本時間）。出典：ユーザー提供のsig.js・lf.js実行ログ。

## selector対応表

| selector | 関数 |
|---|---|
| 0xe0bab4c4 | DAI() |
| 0x02329a29 | pause(bool) |
| 0x4319e532 | leafFor(address,uint256,uint256,address[]) |
| 0x86d1a69f | release() |
| 0xdd165cfe | setRedeemers(address,address[],bool) |
| 0xbf7e214f | authority() |
| 0xad3cb1cc | UPGRADE_INTERFACE_VERSION() |

先行holes.jsでPASSだったe0bab4c4はDAI()。DAIアドレスのgetterのガス見積結果として対応がついた。

## leafFor照合の入力

| 項目 | 値 |
|---|---|
| contract | 0x9d31771458b421c7ea8a06cb8d12663e91617869 |
| 対象user | 0x8D8B9c79196f32161BcB2A9728D274B3b45eB9AF |
| ethAmount | 176785462750 |
| usdAmount | 65808302600039 |
| redeemers | [] |

今回のローカル計算：

```text
redeemerHash = keccak256(concat(redeemers))
leaf = keccak256(keccak256(abi.encode(
    user, ethAmount, usdAmount, redeemerHash
)))
```

空redeemersのconcatは空バイト列0x。オンチェーンleafForの返却値とローカル計算値が一致し、先行chunk 51のatLeafとも同じ値になった。

本人0xfd8d...df5d0の保存claimとは別の入力として記録する。

## authority照会

Exit1のauthority()返却値は0x000000000000000000000000000000000000dead。getCodeの返却文字列長は2（0x、コード0バイト）。

## 実行出力

```text
PS C:\Users\ishij> node sig.js
e0bab4c4 -> DAI()
02329a29 -> pause(bool)
4319e532 -> leafFor(address,uint256,uint256,address[])
86d1a69f -> release()
dd165cfe -> setRedeemers(address,address[],bool)
bf7e214f -> authority()
ad3cb1cc -> UPGRADE_INTERFACE_VERSION()
PS C:\Users\ishij> node lf.js
onchain 0x465909272ffe136b754597907b333d42ba18dcd988a3bf6a00fb5c096882f897
mine    0x465909272ffe136b754597907b333d42ba18dcd988a3bf6a00fb5c096882f897
?? true
authority 0x000000000000000000000000000000000000dead code 2
PS C:\Users\ishij>
```

[公式chunk復元記録](frontend-excerpts.md) · [全体記録](README.md)
