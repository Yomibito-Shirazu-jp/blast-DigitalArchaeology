# Digital Archaeology | デジタル考古学

**Dig, Don't Hack.**

This is the top-level research directory for reproducible digital archaeology: excavation of historical smart-contract code, abandoned systems, stranded assets, and legitimate recovery mechanisms.

## Research principles

- Preserve original systems and evidence. Never overwrite an upstream codebase to make an archaeological finding appear successful.
- Distinguish historical observation, hypothesis, simulation, and independently reproduced state effects.
- Attribute assets to their legitimate claimants; discovery does not establish ownership or permission to transfer.
- Conduct only read-only production-chain investigation and permitted local simulation; never broadcast unauthorized asset movements.
- Record immutable commit SHAs, chain IDs, pinned block hashes, exact RPC outcomes/errors, commands, versions and exit codes.
- No PASS claims without verifiable code and artifacts.

## 発掘調査のご依頼・お問い合わせ

失われた可能性のあるトークン資産や停止したコントラクトなどのデジタル考古学的調査については、**[info@algorithm.dance](mailto:info@algorithm.dance)** までお問い合わせください。

**私たちは秘密鍵・シードフレーズ等を原則お預かりしません。** 対応は、調査に基づく**手順書の送付**、または**オフラインでの対面同席**に限ります。**調査・技術支援は原則無償です。** 対面同席の場合のみ、交通費を中心とした実費をご負担いただきます（事前にご案内・合意）。秘密情報をメールで送らないでください。調査や回収の成功を保証するものではありません。

詳細：[調査依頼・対応方針](./CONTACT.md)

## 進行中の調査

Claudeが現在のトークン資産残高・USD評価額・保有アドレス数、および管理権限や運営上の制約によって引き出せない資産の内訳を調査中です。**集計値は未検証で、まだ公表していません。** [調査の集計基準と提出要件](./cases/CLAUDE_ASSET_INVENTORY_BRIEF.md)

## 毎回の発掘報告書 — Recovery Map

すべての発掘案件について、**沈没船の所在・資産目録・正当な権利者・回収条件・証拠・未検証事項**を同じ書式で記録します。公開版には悪用可能な具体的手順や秘密情報を含めません。

- [Recovery Map テンプレート](./methodology/RECOVERY_MAP_TEMPLATE.md)
- [全案件への適用ルール](./methodology/RECOVERY_MAP_POLICY.md)
- [論文集計用JSONひな形](./methodology/recovery-map.example.json)

## Directory map

| Directory | Purpose |
|---|---|
| [methodology/](./methodology/) | Excavation standards, evidence tiers, evaluation methods |
| [cases/](./cases/) | Case index, including the existing Blast research |
| [evidence/](./evidence/) | Evidence schema and provenance requirements |
| [publications/](./publications/) | Working-paper and publication index; draft findings are not peer-reviewed |
| [blast/](./blast/) | Pointer to preserved Blast code and the current competition |

## Blast is preserved unchanged

The existing repository directories **[blast-geth](../blast-geth/)**, **[blast-optimism](../blast-optimism/)** and **[config](../config/)** remain in place. Existing [submissions](../submissions/) and [reviews](../reviews/) are retained.

This directory is a non-destructive umbrella for future excavations across chains and protocols. It does **not** relocate or rename the Blast implementation or existing competition artifacts.

## Research status

A research infrastructure directory does not mean a recovery is demonstrated. For the 2026-11-05 Blast eth_call competition, see [the submissions index](../submissions/2026-11-05/) and [cross-review index](../reviews/2026-11-05/). Always check the latest audited result, not the agent's self-reported verdict.
