# 02 — リカバリーマップ｜発掘地図・査読・コード証拠

**「沈没船を特定した。資産はここにある。誰が正当に引き上げられるかを示す地図」** を各発掘案件に添付します。

## ここで読むもの

| 内容 | 関連資料 |
|---|---|
| 毎回使う地図の雛形 | [Recovery Map テンプレート](../digital-archaeology/methodology/RECOVERY_MAP_TEMPLATE.md) |
| 毎回の提出ルール | [Recovery Map 運用基準](../digital-archaeology/methodology/RECOVERY_MAP_POLICY.md) |
| 論文集計用JSON | [JSONひな形](../digital-archaeology/methodology/recovery-map.example.json) |
| 査読コメント・相互検証 | [2026-11-05査読記録](../reviews/2026-11-05/) |
| Devin: Munchablesのコード・実験ログ | [提出PR #2](https://github.com/Yomibito-Shirazu-jp/blast-DigitalArchaeology/pull/2) |
| Devin → Claudeの査読 | [査読PR #3](https://github.com/Yomibito-Shirazu-jp/blast-DigitalArchaeology/pull/3) |
| Claude: LaunchBridge提出先 | [Claudeフォルダ](../submissions/2026-11-05/claude/) |
| 資産一覧・管理者依存調査の仕様 | [調査票](../digital-archaeology/cases/CLAUDE_ASSET_INVENTORY_BRIEF.md) |

## 全案件の報告構造

`recovery-map.md`（公開地図）と`recovery-map.json`（論文の集計データ）を用意します。

1. 対象・歴史とブロック固定
2. 船内資産・金額・アドレス数、二重計上の除外
3. 権利者と管理者、阻害要因
4. 認可された回収条件（安全な概要）
5. eth_call・トレース・状態差分による証拠
6. AI査読コメントと未実証部分
7. 公開審査（PUBLIC_MAP / REDACTED_MAP / PRIVATE_REVIEW）

**重要:** GitHubの公開PRに載ったコードは一般公開状態です。危険な操作コードや秘密情報はここへ複製しません。具体的な実行手順は正当な権利者に非公開で案内します。

[← トップへ](../README.md)
