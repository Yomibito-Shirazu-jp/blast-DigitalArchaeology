# RPC再確認：初期化・root設定・upgrade

記録日：2026-11-11（日本時間）。出典：[ユーザー提供の実行ログ原本](rpc-recheck-original.txt)。

## 確認結果

| 対象・呼び出し | eth_call | eth_estimateGas |
|---|---|---|
| Exit1 claimed(0x8D8B9c79196f32161BcB2A9728D274B3b45eB9AF) | 0（false） | 0x73d9 |
| Exit1 initialize(me) | revert 0xf92ee8a9 | revert 0xf92ee8a9 |
| Exit1 setRoots([0x11…11],true)、from=本人 | revert 0x91a7df1a | revert 0x91a7df1a |
| Exit1 bogus 0xdeadbeef | revert 0x | revert 0x |

上表は ethereum-rpc.publicnode.com にJSON-RPCを直接送った rev.js の結果。eth.llamarpc.com と eth.merkle.io は全項目で bad response と出力された。

gas.jsではExit1・Exit2とも、initialize(me)、setRoots([root],true)、bogusがREVERTと出力された。

## upgradeの見積結果

| proxy | 指定したimplementation | from | 結果 |
|---|---|---|---|
| Exit1 | 0xbd905d3d62f5d72ab18c4c2d3edcfe549cbea46d | 0xfd8dB47e7371dC3751D8B84EBd040046D70dF5d0 | revert 0x91a7df1a |
| Exit1 | 同上 | 0x1111111111111111111111111111111111111111 | revert 0x91a7df1a |
| Exit2 | 0xc0ed1264c60540591d3d9fe224c7b957d24f69df | 0xfd8dB47e7371dC3751D8B84EBd040046D70dF5d0 | revert 0x91a7df1a |
| Exit2 | 同上 | 0x1111111111111111111111111111111111111111 | revert 0x91a7df1a |

出典：upg.js。呼び出しはupgradeToAndCall(address,bytes)、bytes引数は空。

## setRootsのfrom別結果

Exit1、setRoots([0x11…11],true)、eth_estimateGas：

| from | 結果 |
|---|---|
| 0x000000000000000000000000000000000000dEaD | PASS、gas=0xcf22（53026） |
| 0x480Ea8bA8De8d05A30F4f4CBedE1e28E05aE1B2C | revert 0x91a7df1a |
| 0xf97eC9b92Efda3afe52945B4e9adE0394C9E705d | revert 0x91a7df1a |
| 0xAb5972612e8CEe66f246feaCB8D500DF3C6cfADA | revert 0x91a7df1a |
| 0x7DbDFbb265bF26e626B44132eF4e3A3E6eEc1282 | revert 0x91a7df1a |
| 0xfd8dB47e7371dC3751D8B84EBd040046D70dF5d0 | revert 0x91a7df1a |
| 0xc154A0CC408e9B94333B40AB408f6E443AceFA0b | revert 0x91a7df1a |

PASSは指定したfromによるガス見積の成功。署名・送信・root変更を伴う実行結果ではない。

who.jsのExit2指定値は `0x23ea8caceb5673bbd712137ce2aa33db36cb513`。正しいproxy `0x23ea8c6aceb5673bbd712137ce2aa33db36cb513` に対して1文字不足しており、全fromが `odd number of digits` で終了した。この行は権限判定ではなく入力形式エラー。

## 先行ログとの対応

- initSlotは両Exitとも1。
- 先行init.jsのOKはスクリプトの表示として保持する。
- 今回、直接のeth_call / eth_estimateGasでinitializeとroot設定のrevertデータを取得した。
- upgradeはupg.jsで両proxy・2送信元のrevertを取得した。
- 初期化・root設定・upgradeの成功という解釈は、上記の直接RPC結果で修正する。
- 先行の別アドレスclaimのSIM OKは表示ログとして保持する。今回のrev.jsが直接確認したそのアドレスの値はclaimed=false。

## 原本識別

- ファイル：Pasted text(20261111-073211).txt
- バイト数：10565
- SHA-256：`4c0eb1361ced9807b9cf28ef03df8bb855bf84ded2670dd2aa4d3ad6d1c89aa2`
- 保存：[rpc-recheck-original.txt](rpc-recheck-original.txt)

[全体記録・本人のTXハッシュ・proof](README.md)
