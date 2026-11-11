# Blast：証拠・ハッシュ・proof復元記録

記録日：2026-11-11（日本時間）。出典：ユーザー提供のPowerShell実行ログ、保存claimデータ、既存の調査記録。以下のオンチェーン値は各ログ取得時の観測値。

## 追加確認（RPC直接照会）

[初期化・root設定・upgradeの再確認結果](rpc-recheck-findings.md)：initializeは `0xf92ee8a9`、本人からのsetRootsと両Exitのupgradeは `0x91a7df1a` でrevert。Exit1のsetRootsはfrom=dead指定の見積がPASS。who.jsのExit2はアドレス桁不足による入力エラー。原本ログも保存。

## 本人のアドレスと出金識別子

| 項目 | 値 |
|---|---|
| user | `0xfd8db47e7371dc3751d8b84ebd040046d70df5d0` |
| redeemer | `0x01a58b188cf10272053bef7f6842e9b325d13073` |
| withdrawalHash | `0x8f72d51d52686ac895d10f7be5ec8371d9c852b6c8ef831f0247bd5a33f4eb8e` |
| ETH amount（保存claim、wei） | `1661530021300664950544` |
| USD amount（保存claim、base units） | `1474542578998386262697028` |
| USD amount（18 decimals） | `1474542.578998386262697028` |

| 処理 | chain | block | TX hash |
|---|---|---:|---|
| L2送信 | Blast | 41941061 | [`0xe1ce70e43bca67c38d91ce2005711dc66bbbff09f951a7305090c24f7c71f7e7`](https://blastscan.io/tx/0xe1ce70e43bca67c38d91ce2005711dc66bbbff09f951a7305090c24f7c71f7e7) |
| L1証明 | Ethereum | 26250036 | [`0x37b190602da059727b780c4aed99e85fde68839eda0b769ad1a89548362093d9`](https://etherscan.io/tx/0x37b190602da059727b780c4aed99e85fde68839eda0b769ad1a89548362093d9) |
| L1確定として記録されたTX | Ethereum | 26279296 | [`0x2072fc756d7ac5196ba9be7d5414baada30056430abcedd80f0a1cee3493ff73`](https://etherscan.io/tx/0x2072fc756d7ac5196ba9be7d5414baada30056430abcedd80f0a1cee3493ff73) |

既存調査記録：prove timestamp `1792694735`、challenge period `86400` 秒、`finalizedWithdrawals[withdrawalHash]=true`、L1 Messengerの`successfulMessages=true`。ウォレットのDAI受領とは別段階として記録されている。BlastのDAI出金ではfinalizeからUSDYieldManagerのWithdrawalRequestedとrequestIdを追い、claimWithdrawalへ接続する。

## コントラクト

| 役割 | address |
|---|---|
| Exit1 proxy | `0x9d31771458b421c7ea8a06cb8d12663e91617869` |
| Exit1 implementation（owner.js出力） | `0xc0ed1264c60540591d3d9fe224c7b957d24f69df` |
| Exit2 proxy | `0x23ea8c6aceb5673bbd712137ce2aa33db36cb513` |
| Exit2 implementation（owner.js出力） | `0xbd905d3d62f5d72ab18c4c2d3edcfe549cbea46d` |
| OptimismPortal | `0x0Ec68c5B10F21EFFb74f2A5C61DFe6b08C0Db6Cb` |
| USDYieldManager | `0xa230285d5683C74935aD14c446e137c8c8828438` |
| L1CrossDomainMessenger | `0x5D4472f31Bd9385709ec61305AFc749F0fA8e9d0` |
| L1BlastBridge | `0x3a05E5d33d7Ab3864D53aaEc93c8301C1Fa49115` |
| DAI | `0x6B175474E89094C44Da98b954EedeAC495271d0F` |

## 公式フロントから発見したデータ構造

取得ログ：`https://blast.io/` のHTMLは5079文字、参照先は `./assets/index-E2w4LnB3.js`。取得したJSは309600バイト。ログにはExit1・Exit2のアドレス、claim ABI、静的データ取得処理が含まれる。

| contract ID | データ起点 |
|---|---|
| contract-1 | `https://blast.io/claims/contract-1/` |
| contract-2 | `https://blast.io/claims/contract-2/` |

| ファイル | 内容 |
|---|---|
| `manifest.json` | version、shardPrefixLength、redeemerPrefixLength、chunkDepth、trees |
| `shards/<prefix>.json` | 小文字アドレスから割当行を取得 |
| `trees/<treeIndex>/<chunkIndex>.bin` | 32-byte単位のMerkleノード |

割当行：`[ethAmount, usdAmount, treeIndex, leafIndex, redeemers = [], pendingWithdrawals = 0]`。

`fetchClaim()` はmanifest→shard→chunkの順で取得し、葉から親方向へ兄弟ノードを収集する。戻り値は `{pendingWithdrawals, ethAmount, usdAmount, redeemers, proof, root}`。chunk内のleaf一致と、proofから計算したroot一致の両方を検査する。

**保存済み4要素proofはチャンクから兄弟ノードを抽出した後の配列。chunkバイナリそのものではない。**

chunk位置計算では `s` の初期値は `i = min(2**(chunkDepth+1)-1, totalNodes)`。今回の調査例では127。各chunkは先頭に上位127ノードを重複して持つ。0から始める計算との差分が127となり、調査中の位置638に対応した。

公式JS抜粋と位置計算は [frontend-excerpts.md](frontend-excerpts.md) に保存。

## 本人の保存claimと再計算

| 項目 | 値 |
|---|---|
| 保存leaf | `0xd03615583169ade864282ea8d5e88420d144127ed1534c27460c335089523544` |
| 保存root | `0xcfc12eab4937f6f3d3ceb501304adf8d9169a3bf79dc543a856fdc54889f9ba3` |
| proof要素数 | 4 |
| claim selector | `0x06301e28` |
| claim calldata | 420 bytes |

proof（順序を保持）：

```text
0x5d5b9c9a3520ad8b3cd0b2e469e321c2ab44537ef34cba68b45f49e0a8412032
0xc6bd14f3d773645c2bc3257b51194b13e7d1ebd47b648dfa5cf7ceeb7cc4e38c
0x567febc2981df3320b438c0ce96f2229d12bd0a3b4893dc35922e94d695cf43f
0xbc41a733d843c63c97f08f11cf435bf546e6053a67c315839ff8493168955170
```

兄弟ノードを小さい値→大きい値の順に連結し、各段でKeccak-256を計算した結果：

```text
0xd493129acf7346232ac0d7ea708db01304d7af7a5ea454f58968dd60c89a15f6
0x294af4d0cfa761b354a1e1db2f088f14046e2f52f8e71a371b95dd2648babf32
0x57b4e3e9e333363684be5869866cf26fff8ed9bdbdd16839719bccc79a521cab
0xcfc12eab4937f6f3d3ceb501304adf8d9169a3bf79dc543a856fdc54889f9ba3
```

オフライン検証：保存leaf→4要素proof→保存rootの一致、保存calldataとABI再エンコード結果の一致を確認。11行すべてで、保存leafと各proofから同じ保存rootを再計算できた。

leaf計算の記録も分離して保存する。貼付JSの `hd([address[]],[r])` を `abi.encode(address[])` として計算したleafは `0x455bbf72cec644479140c4b960c3179951ef2943c17021468fcdd8eb756826c3`。保存leafは上記 `0xd036...3544`。この比較結果は [offline-verification.json](offline-verification.json) にある。

過去の実行ログ：この保存rootの `roots(root)` は `false`、保存claimへの呼び出しは `InvalidRoot`（`0x504570e3`）を返している。

## 11行の保存データ

原本： [saved-candidates-11.json](saved-candidates-11.json)。出典はユーザー提供の保存claim JSON。各行のuser、金額、redeemers、leaf、proof、calldataと、root-update calldataを含む。

| ID | ETH wei | USD base units | proof数 |
|---|---:|---:|---:|
| 01_DAI_USDYieldManager | 1661530021300664950544 | 1474542578998386262697028 | 4 |
| 03_BAG_Orphan2_2 | 2253620946543698 | 2000000000000000000 | 4 |
| 04_KAP_Orphan1_2.19M | 2474595241215148015424 | 2196106000000000000000000 | 4 |
| 05_KAP_Orphan2_0.5 | 563405236635924 | 500000000000000000 | 4 |
| 06_OLE_Orphan1_94.7K | 106721346734050124943 | 94711000000000000000000 | 4 |
| 07_OLE_Orphan2_35.8K | 40393004314177430325 | 35847203475923311660823 | 4 |
| 08_USDC_Orphan_11 | 12394 | 11000000 | 4 |
| 09_ezETH_Orphan_0.015 | 16899329035287 | 14997490204557189 | 3 |
| 10_RBX_Orphan_1 | 1126810473271849 | 1000000000000000000 | 3 |
| 11_RBX_QuasiOrphan_80.6K | 90864611573429657227 | 80638770874743244240433 | 2 |
| 02_BAG_Orphan1_44M | 4592840552474015801258 | 4075965445314038357003053 | 4 |

原本のSHA-256：`bc81c5d885fd01ed25d7c70ff35a22f702a10c2c1c99b9fee657dce8e9107d26`。

| 集計項目 | base units |
|---|---:|
| ETH：保存されたExit値 | 8966949738347471478873 |
| ETH：11行合計 | 8966948738347471478873 |
| ETH差分 | 1000000000000000 |
| DAI：保存されたExit値 | 7957814514660581391158526 |
| DAI：11行合計 | 7957814513660581391158526 |
| DAI差分 | 1000000000000000 |

## 公式chunkから復元した別アドレスのproof

対象：`0x8D8B9c79196f32161BcB2A9728D274B3b45eB9AF`。本人の `0xfd8d...df5d0` と区別する。

```text
chunk 51 http 200
bytes 36768 words 1149
calcLeaf 0x465909272ffe136b754597907b333d42ba18dcd988a3bf6a00fb5c096882f897
atLeaf   0x465909272ffe136b754597907b333d42ba18dcd988a3bf6a00fb5c096882f897 match true
rootMatch true len 15
SIM 0xfd8dB47e7371dC3751D8B84EBd040046D70dF5d0 OK
SIM 0x1111111111111111111111111111111111111111 OK
```

この実行ログではleaf計算に `keccak256(concat(redeemers))` を用いている。15要素proofの実値とroot実値はこの出力には表示されていない。

## 管理・初期化・upgradeの実行ログ

[control-observations.txt](control-observations.txt) にowner.js、sel.js、own2.js、init.jsの出力を保存。

- owner.js：両Exitでadmin・beaconスロットはゼロ。owner/pendingOwner/admin/guardian/rootSetter/setter/upgraderの各呼び出し出力は `0x`。
- sel.js：`setRoots(bytes32[],bool)`、`initialize(address)`、`upgradeToAndCall(address,bytes)`などのselector対応を取得。
- own2.js：両Exitでselector `0xbf7e214f` の返却値とslot0に `0x...dead`。`0xad3cb1cc` は文字列 `5.0.0` のABIエンコード値。
- init.js：両Exitで `paused 00`。2つの送信元からinitializeおよびupgradeToAndCallについて、スクリプトが `OK` を出力。観測種別はユーザー側シミュレーション出力。

記録上の区別：adminスロットのゼロ値、slot0のdead値、関数呼び出しの空バイト列 `0x` はそれぞれ別の観測。「Blast全体のadminがdead」「root設定経路がすべて消滅した」という以前の説明は撤回された。

## 再確認用ファイル

- [claim-01.json](claim-01.json)：本人の保存claimパラメータ。
- [claim-01-calldata.txt](claim-01-calldata.txt)：保存calldata原本。
- [verify_claim.py](verify_claim.py)：Python標準ライブラリだけを用いるオフライン検証。`python verify_claim.py`。
- [offline-verification.json](offline-verification.json)：今回の検証結果。
- [SHA256SUMS.txt](SHA256SUMS.txt)：保存ファイルのSHA-256。
