# holes.js：selector別のガス見積結果

記録日：2026-11-11（日本時間）。出典：ユーザー提供のPowerShell出力。

| 呼び出しラベル | Exit1 | Exit2 |
|---|---|---|
| 86d1a69f() | ng 0x91a7df1a | ng 0x91a7df1a |
| 02329a29(zero) | ng 0x91a7df1a | ng 0x91a7df1a |
| 4319e532(zero) | ng 0x | ng 0x |
| dd165cfe(zero) | ng 0x | ng 0x |
| e0bab4c4(zero) | PASS gas=0x6a22（27170） | PASS gas=0x6a22（27170） |
| upgradeToAndCall(other,0x) | ng 0x91a7df1a | ng 0x91a7df1a |

後続sig.jsによりe0bab4c4は `DAI()` と対応した。PASSはDAI getterのガス見積結果。[selector対応とleafFor照合](selector-and-leaffor-confirmation.md)。

## 実行出力

```text
PS C:\Users\ishij> node holes.js
=== 0x9d31771458b421c7ea8a06cb8d12663e91617869
  ng 86d1a69f() 0x91a7df1a
  ng 02329a29(zero) 0x91a7df1a
  ng 4319e532(zero) 0x
  ng dd165cfe(zero) 0x
  *** PASS *** e0bab4c4(zero) gas=0x6a22
  ng upgradeToAndCall(other,0x) 0x91a7df1a
=== 0x23ea8c6aceb5673bbd712137ce2aa33db36cb513
  ng 86d1a69f() 0x91a7df1a
  ng 02329a29(zero) 0x91a7df1a
  ng 4319e532(zero) 0x
  ng dd165cfe(zero) 0x
  *** PASS *** e0bab4c4(zero) gas=0x6a22
  ng upgradeToAndCall(other,0x) 0x91a7df1a
PS C:\Users\ishij>
```

[全体記録](README.md)
