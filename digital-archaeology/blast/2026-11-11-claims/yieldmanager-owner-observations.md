# ym.js：USD・ETH YieldManagerのownerと残高

記録日：2026-11-11（日本時間）。出典：ユーザー提供のPowerShell実行出力。

| 項目 | USDYieldManager | ETHYieldManager |
|---|---|---|
| address | 0xa230285d5683C74935aD14c446e137c8c8828438 | 0x98078db053902644191f93988341E31289E1C8FE |
| code（スクリプト出力値） | 1883 | 1883 |
| ETH | 0.0 | 0.0017 |
| DAI | 0.0 | 0.0 |
| owner() | 0x4f72ee94b8ba3be7f886565d3583a7f636c58b05 | 0x4f72ee94b8ba3be7f886565d3583a7f636c58b05 |
| authority() | 0x | 0x |
| paused() | 0x | 0x |
| admin() | 0x | 0x |
| proxiableUUID() | 0x | 0x |

両YieldManagerのowner()返却値は同じSafeアドレス。Exit1・Exit2のauthority()返却値とは対象コントラクトおよび関数を分けて記録する。空の返却値0xはそのまま保持。

## 実行出力

```text
PS C:\Users\ishij> node ym.js
=== USD 0xa230285d5683C74935aD14c446e137c8c8828438
  code 1883
  ETH 0.0
  DAI 0.0
  bf7e214f authority() -> 0x
  8da5cb5b owner() -> 0x4f72ee94b8ba3be7f886565d3583a7f636c58b05
  5c975abb paused() -> 0x
  f0f44260 admin() -> 0x
  52d1902d proxiableUUID() -> 0x
  c4d66de8  -> 0x
  init ng 0x 0xfd8dB47e7371dC3751D8B84EBd040046D70dF5d0
  init ng 0x 0x1111111111111111111111111111111111111111
=== ETH 0x98078db053902644191f93988341E31289E1C8FE
  code 1883
  ETH 0.0017
  DAI 0.0
  bf7e214f authority() -> 0x
  8da5cb5b owner() -> 0x4f72ee94b8ba3be7f886565d3583a7f636c58b05
  5c975abb paused() -> 0x
  f0f44260 admin() -> 0x
  52d1902d proxiableUUID() -> 0x
  c4d66de8  -> 0x
  init ng 0x 0xfd8dB47e7371dC3751D8B84EBd040046D70dF5d0
  init ng 0x 0x1111111111111111111111111111111111111111
PS C:\Users\ishij>
```

[全体記録](README.md)
