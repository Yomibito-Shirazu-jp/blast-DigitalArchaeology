# Blast リカバリーマップ
更新：2026-11-11（日本時間）／Case ID: BLAST-CLAIM-01／版1

## 0. 調査メタデータ

| 項目 | 記録 |
|---|---|
| 目的 | 本人の出金に対応するDAIを正当な受取先へ回収する |
| 対象user | 0xfd8db47e7371dc3751d8b84ebd040046d70df5d0 |
| 記録上の出金額 | 1,474,542.578998386262697028 DAI |
| chain | Ethereum 1／元の出金はBlast 81457 |
| 証拠の基準commit | 354c31e5bd68dc05eb91ba603ba9091503728195 |
| 状態の基準 | 各ユーザー実行ログ取得時。統一ブロック・block hashは未取得 |
| 地図作成 | 保存済み証拠の整理。今回の新規RPC照会は未実施 |
| 独立査読 | NOT_REVIEWED |
| 公開範囲 | PUBLIC_MAP：資産所在・本人の回収条件・不足証拠 |

## 1. 所在と履歴

経路は3本に分かれる。公式Exit claim、元のUSD出金キュー、管理者による割当・rootの整備。ExitとYieldManagerの権限を別々に追う。

| 証拠 | 識別子 |
|---|---|
| Blast L2送信／block 41941061 | 0xe1ce70e43bca67c38d91ce2005711dc66bbbff09f951a7305090c24f7c71f7e7 |
| L1 prove／block 26250036 | 0x37b190602da059727b780c4aed99e85fde68839eda0b769ad1a89548362093d9 |
| L1 finalizeとして記録／block 26279296 | 0x2072fc756d7ac5196ba9be7d5414baada30056430abcedd80f0a1cee3493ff73 |
| withdrawalHash | 0x8f72d51d52686ac895d10f7be5ec8371d9c852b6c8ef831f0247bd5a33f4eb8e |

履歴記録にはfinalizedWithdrawals=true、successfulMessages=trueがある。本人のDAI着金までを接続する証拠は未完了。

## 2. 資産目録

### 出力ログにある残高

| holding address | ETH | DAI | 根拠 |
|---|---:|---:|---|
| Exit1：0x9d31771458b421c7ea8a06cb8d12663e91617869 | 8835.161130613508156181 | 本表では未集約 | dead.js |
| Exit2：0x23ea8c6aceb5673bbd712137ce2aa33db36cb513 | 802.847250327264292274 | 本表では未集約 | dead.js |
| USDYM：0xa230285d5683C74935aD14c446e137c8c8828438 | 0 | 0 | ym.js |
| ETHYM：0x98078db053902644191f93988341E31289E1C8FE | 0.0017 | 0 | ym.js |

別途ユーザー提示集計にはExit1 DAI 7423885.93346847179810756、Exit2 DAI 1676753.505048250877599079とある。対応するbalanceOfの元出力・ブロックを揃える項目として扱う。

本人の記録上の出金額、保存claim内のETH/USD値、Exitの保有残高は別の項目。合計を本人の回収可能額としない。USD評価額は未算出。

## 3. 請求者と管理権限

| 対象 | 保存された観測 | 次に必要な証拠 |
|---|---|---|
| 本人 | 上記出金TX、user、保存claim | 出金と公式Exit割当の対応、現在の未受領額 |
| 保存redeemer | 0x01a58b188cf10272053bef7f6842e9b325d13073 | 本人の公式割当での認可、実際に呼ぶアカウントの制御 |
| Exit1・Exit2 | authority()はdead。試行した通常fromは権限エラー | 同一blockでの実装・権限状態、過去のroot設定履歴 |
| USDYM・ETHYM | owner()はSafe 0x4f72ee94b8ba3be7f886565d3583a7f636c58b05 | ownerが行える正規機能と依存先 |
| 過去の別EOA候補 | 0x32BB93599Eb77eD5d3A357d3898fcF8200f5b2E9が会話記録にある | 対象Vaultの完全アドレス、実際のsetRoots成功TX、内部caller、block |

過去EOA候補は現在のExit権限者として確定していない。現在のExitのdead観測も、Blast全体の権限消滅を意味しない。

## 4. 回収経路：何のために何が足りないか

| 優先 | 経路・目的 | 分かっていること | 足りないもの | 次の確認作業 | 完了条件 |
|---|---|---|---|---|---|
| 1 | 公式Exitから本人の割当をclaim | 公式静的データの取得構造・chunk位置計算は復元済み。別アドレスでleafFor一致 | 本人の両contractの公式行、root、proof、claimed、root有効性、受取先、redeemer認可 | 本人の行を公式データから取得し、同一blockでleafFor・roots・claimed・認可を照合 | 本人に認可された呼び出しで、本人の正当な受取先への資産増加を再現 |
| 2 | 元の出金に対応するDAI請求を特定 | 出金・prove・finalizeとして記録したTXがある。USDYM残高0 | finalize receiptの実ログ、WithdrawalRequested/requestId/recipient、キュー状態、既受領状態 | 元TXのreceiptと必要な内部処理から請求を追い、現在のrequest状態と依存先を照合 | 正当なrecipientと未受領額、利用可能な正規請求経路が特定される |
| 3 | 本人割当のroot登録が必要な場合に正当な設定者を特定 | 現在ログでは両Exit authority=dead。YM ownerはSafe | 昨日の別アドレスの根拠TX、権限変更時点、対象contract | 成功したroot設定TXとrelease等の前後を同一対象で比較 | 現在有効な設定経路・承認者が根拠付きで確定する |
| 4 | 実送信の準備 | 本人・保存redeemerのアドレスがある | 実行アカウント、署名可能性、送信時の残高・必要ガス、受取先の制御 | 経路1〜3のうち成立した経路で、本人用の実行条件を揃える | 署名できる正当な実行主体と、着金までの条件が揃う |

### 経路1で混同しない2種類のproof

| 記録 | 証明できたこと | まだ必要なこと |
|---|---|---|
| 本人の保存4要素proof／root 0xcfc12eab4937f6f3d3ceb501304adf8d9169a3bf79dc543a856fdc54889f9ba3 | 保存leafから保存rootを再計算できる。保存calldataを再現できる | 本人の公式割当との一致、非空redeemersでのオンチェーンleafFor一致、有効rootへの所属 |
| 別アドレス0x8D8B9c79196f32161BcB2A9728D274B3b45eB9AFの15要素proof | chunk 51でleaf一致・rootMatch trueの出力。空redeemersでleafForとローカル計算が一致 | 本人のproofへ置き換えて同じ検証を完了する |

保存4要素proofのrootは過去照会でfalse、呼び出しはInvalidRoot。新しい本人用公式proofがあれば、保存rootの追加を前提にせず確認できる。

### claimの完了判定

必要なのは関数内にCALLERがあるかではなく、送金命令に渡される宛先と実際の残高変化。本人の正規割当・認可されたcallerを使い、Exit側の減少と正当な受取先の増加を対応させる。過去のSIM OK表示のみを資産受領の証明にはしない。

## 5. 回収可能性の分類

**全体：U（本人の正規回収経路を確定する証拠が不足）。**

| 経路 | 状態 |
|---|---|
| 公式Exit claim | U：本人の公式割当・認可・効果が未接続 |
| 元のUSD出金キュー | U：requestIdから現在の請求状態まで未接続 |
| 管理者による整備 | C：設定経路と現在の権限者の根拠が未解決 |
| 本番回収 | 保存記録に本人への着金証拠なし |

dead指定の見積PASSは署名可能な設定者の発見ではない。dead鍵探索を回収計画の成立条件に置かない。

## 6. 証拠・反証・査読

| Gate | 状態 | 根拠・不足 |
|---|---|---|
| G1 TARGET | PARTIAL | 対象・実装アドレスは保存。code hash・統一block hashは未取得 |
| G2 HISTORY | PARTIAL | 出金3TXは識別。request接続とroot権限履歴が未完了 |
| G3 PATH | PARTIAL | 公式データ構造を復元。本人への正規経路は未確定 |
| G4 CALL | PARTIAL | 別アドレスleafFor一致、権限revert等あり。本人の有効claimは未確認 |
| G5 EFFECT | NOT_RUN | 正当な受取先の残高増加まで検証した記録なし |
| G6 REPRO | PARTIAL | 保存proofのオフライン再計算済み。独立した本人公式proofの再現は未完了 |

独立査読：NOT_REVIEWED。

証拠リンク：

- [本人の識別子・出金TX](README.md)
- [保存claim](claim-01.json)／[オフライン検証](offline-verification.json)
- [公式フロント・chunk](frontend-excerpts.md)／[leafFor照合](selector-and-leaffor-confirmation.md)
- [権限・初期化・upgradeの直接RPC照会](rpc-recheck-findings.md)
- [両Exitのfrom比較](who3-both-exits.md)／[102件の結果](hist-102-observations.md)
- [残高とガス見積](dead-balance-and-gas.md)
- [YieldManager owner照会](yieldmanager-owner-observations.md)

否定された解釈：DAI()の見積PASSを権限変更経路とすること、初期化・upgradeの先行OK表示を直接RPCのrevertより優先すること、別アドレスのproofを本人のproof完成とすること。

## 7. 次の作業を終えたと判断する基準

1. **本人の公式データ**：両Exitについて本人の行の有無、金額、redeemers、root、proofを保存し、同一blockの認可状態と対応する。
2. **元出金の請求追跡**：finalizeとして記録したTXからrequestId・recipient・処理済み/受領済みを確定する。該当ログが無ければtrace等で実際の処理先を特定する。
3. **昨日の設定者**：別EOAの成功TXを取得し、どのcontractをどの権限で呼んだかを確定する。
4. **本人への効果**：成立した正規経路で受取先・残高増加を確認し、実送信の要件を揃える。

## 8. 公開・索引

本地図は公開済み観測の整理と不足証拠の一覧。[機械可読版](recovery-map.json)。調査者による整理版で、独立査読は未実施。

金貨の所在、請求者、引き上げ条件を別々に示し、本人への回収を完了条件とする。
