# key.js / key2.js：実行結果

記録日：2026-11-11（日本時間）。出典：ユーザー提供のPowerShell実行出力。

| 項目 | 観測値 |
|---|---|
| 対象 | 0x000000000000000000000000000000000000dEaD |
| codeSize | 0 |
| key2.js tried | 35 |
| key2.js hits | 0 |
| nonce(dEaD) | 0 |

key2.jsに渡された35候補について、一致するアドレスは出力されなかった。

## key.js 出力

```text
PS C:\Users\ishij> node key.js
dEaD codeSize 0
  bad 0xdead
  bad 0xdeadbeef
  bad 0xdeaddead
  bad dec57005
  keccak(dead) -> 0xb66125c7434A52a86E8e9B281A17E126dE8F546d
  keccak(Dead) -> 0x7315EC91ff28025f0b87E824391E9A7e79ceDC1E
  keccak(0xdead) -> 0x19c197a533Eec91b3f0450a2FC665923C265C9d7
  keccak(DEAD) -> 0xb0Abd7173A6b193EB8Ed0b8a1C221cD4367DfCfC
  keccak(optimism) -> 0xA47B05Ca3fa0104f21ca47944Ba3230d74B960Fd
  keccak(dEaD) -> 0x86a81847653b9390AB2a37BF400633779E77aEa4
  anvil0 -> 0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266
  anvil1 -> 0x70997970C51812dc3A010C7d01b50e0d17dc79C8
  op-dev1 -> 0x9965507D1a55bcC2695C58ba16FB37d819B0A4dc
  op-dev2 -> 0x976EA74026E726554dB657fA54763abd0C3a0aa9
  testtest..junk0 -> 0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266
  junk0xdead -> 0x7B1aFE2745533D852d6fD5A677F14c074210d896
  0xdead0000 -> 0xe1AB69E519d887765cF0bb51D0cFFF2264B38080
```

## key2.js 出力

```text
PS C:\Users\ishij> node key2.js
tried 35 hits 0
nonce(dEaD) 0
PS C:\Users\ishij>
```

[残高・nonce・ガス見積](dead-balance-and-gas.md) · [全体記録](README.md)
