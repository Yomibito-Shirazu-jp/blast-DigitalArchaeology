# Digital Archaeology — Recovery Map / 発掘地図

> **公開用の考古学的調査記録。実行用の回収レシピではありません。** 正当な権利者への返還を目的とします。秘密情報、未修正の脆弱性、攻撃可能な詳細calldata、権限回避の具体的方法は載せません。

## 0. 調査メタデータ

| 項目 | 記録 |
|---|---|
| Case ID / 報告書版 | TODO |
| 調査担当 / 独立査読者 | TODO / NOT_REVIEWED |
| チェーン / chain ID | TODO |
| スナップショットUTC | TODO |
| 固定ブロック番号 / ブロックハッシュ | TODO |
| 対象コントラクト | TODO |
| 実装・ソースの不変コミットSHA / コードハッシュ | TODO |
| 対象範囲・除外条件 | TODO |
| 証拠アーカイブ・ハッシュ | TODO |
| 公開審査 | PENDING |

## 1. 沈没船の所在と歴史 / Site and provenance

**対象システム：** TODO

**なぜ調査対象か：** TODO

**状況：** OPERATING / PAUSED / DEPRECATED / SHUTDOWN / UNKNOWN

**配備・更新・停止の履歴（検証済み）：** TODO

**ソース・オンチェーン根拠：** TODO

> 「運営終了」と「資産回収不能」は別の主張です。根拠のない断定を避けます。

## 2. 船内資産の目録 / Asset manifest

| Chain | Token / token address | Holding address | Raw quantity / decimals | Display quantity | Price at UTC / source | Estimated USD | Evidence ID |
|---|---|---|---|---|---|---|---|
| TODO | TODO | TODO | TODO | TODO | TODO | TODO | TODO |

**合計USD：** NOT_VERIFIED

**保有コントラクト・アドレス数：** NOT_VERIFIED

**トークンコントラクト数：** NOT_VERIFIED

**権利者アドレス数（判明した範囲）：** NOT_VERIFIED

**会計上の注意：** 預託者への負債 / プロトコル所有資産 / 余剰資産を区別する。stETH等のsharesと残高、ラップ資産と原資産、プール持分、ETH換算値を二重計上しない。価格基準時・不確実性・調査網羅率を明記する。

## 3. 誰の財宝か / Ownership and authorization

- **正当な請求権の種類：** DEPOSITOR / BENEFICIARY / TREASURY / ESCROW / UNKNOWN
- **権利者と権利発生の根拠：** TODO（個人を特定できる非公開情報は掲載しない）
- **必要な承認類型：** 自己署名 / マルチシグ / ガバナンス / その他 / UNKNOWN
- **実行阻害要因：** PAUSE / KEY_LOSS / GOVERNANCE / DEPENDENCY / NONE_VERIFIED / UNKNOWN
- **未解消の権利関係・償還債務：** TODO

管理権限の保有と、預託者資産に対する経済的所有権は同一とは限りません。

## 4. サルベージ地図 / Recovery conditions

| 確認項目 | 状態・根拠 |
|---|---|
| 正当な回収経路の存在 | VERIFIED / CONDITIONAL / UNPROVEN |
| 既存の許可された機能・手続き（概要のみ） | TODO |
| 必要な権利・承認 | TODO |
| 停止条件、期限、外部依存 | TODO |
| 固定ブロックでのread-only呼び出し | PASS / FAIL / NOT_RUN + evidence ID |
| シミュレーションでの資産減少・正当な受取人増加 | PASS / FAIL / NOT_RUN + evidence ID |
| 現時点の本番実行可能性 | VERIFIED / CONDITIONAL / UNKNOWN |
| 本人への案内 | 高水準の説明に限定。詳細手順は権利確認後、非公開で提供 |

**公開しないもの：** 秘密鍵・署名データ、完成した送金calldata、権限回避方法、未修正の脆弱性、資産を危険にさらす操作シーケンス。

## 5. 回収可能性の分類 / Salvage class

- **A — Claimant-controlled:** 権利者自身に正規の回収経路あり
- **B — Administrator-dependent:** 正当な管理者・統治手続きによる承認が必要
- **C — Technically plausible, authority unresolved:** 経路の仮説はあるが権利・承認条件が未確定
- **D — Not presently recoverable:** 明示的な根拠により現在の回収が阻害されている。**永久回収不能を意味しない**
- **U — Unknown / insufficient evidence:** 判定に必要な証拠が不足

**分類：** U（初期値）

**根拠と条件：** TODO

## 6. 証拠・反証・査読 / Evidence

| Gate | 状態 | Evidence ID | 再実行者 / 実行環境 |
|---|---|---|---|
| G1 TARGET | NOT_RUN | — | — |
| G2 HISTORY | NOT_RUN | — | — |
| G3 PATH | NOT_RUN | — | — |
| G4 CALL | NOT_RUN | — | — |
| G5 EFFECT | NOT_RUN | — | — |
| G6 REPRO | NOT_RUN | — | — |

**反証された仮説と失敗ログ：** TODO

**未検証の依存先・異常条件：** TODO

**第三者悪用リスクの審査：** PENDING / CLEARED_WITH_SCOPE / PRIVATE_ONLY

**査読者の判定・不一致：** TODO

## 7. 考古学者の結論 / Archaeologist's statement

- **何が存在すると証明できたか：** TODO
- **どこにあり、いつ確認できたか：** TODO
- **誰が正当に引き上げられる可能性があるか：** TODO
- **何が未証明か：** TODO
- **本番回収の有無：** NOT_PERFORMED / CONFIRMED_BY_PUBLIC_CHAIN_EVIDENCE
- **次の研究課題：** TODO

> 私たちは沈没船の所在と回収条件を示す地図を作る。許可されたサルベージは正当な権利者が判断し、実行する。

## 8. 公開・問い合わせ

**公開審査：** 公開する詳細が悪用可能性を高めないか独立査読する。危険な原本・ログは非公開で保管し、公開地図は安全性を考慮した範囲に絞る。

**調査・技術支援：** 原則無償。鍵は原則預からず、手順書の提供かオフライン対面同席で対応（対面時は基本的に事前合意した交通費実費のみ）。

**お問い合わせ：** [info@algorithm.dance](mailto:info@algorithm.dance) ／ [詳細方針](../CONTACT.md)
