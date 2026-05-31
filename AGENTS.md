# AI 情緒垃圾筒中心 Repo Agent 指引

本 repo 是 `vision`、`firmware`、`display` 三個子 repo 的跨 repo 契約來源與方向治理入口，不是子 repo 內部實作細節倉庫。

## 必讀順序

1. 先讀 `docs/api-contract.md`，確認目前採用的跨 repo contract version。
2. 再讀 `docs/fact-map.md`，只把其中的跨 repo 事實當成穩定事實。
3. 若要改事件流、payload、模組責任或全自動流程，必須同步更新 `docs/decision-log.md` 與 `contracts/contract.v*.json`。

## 穩定契約

- v0.2 採 Python `multiprocessing.Queue`，三個 process 同機運行於 Jetson AGX Orin Nano。
- `firmware` 只透過 `q_detected` 送出 `user_detected`。
- `vision` 消費 `user_detected`，並透過 `q_result` 送出 `recognition_result`。
- `display` 消費 `recognition_result`，播放語音、更新螢幕與紀錄事件。
- 系統全自動；沒有使用者確認按鈕、沒有蓋子機構、沒有 `display -> firmware` public flow。

## 修改邊界

- 中心 repo 只收跨 repo 共識、契約、決策、驗證入口。
- 子 repo 內部模型、UI framework、硬體 library、資料處理細節應留在各自 repo。
- 如果子 repo 的實作改動不影響 public contract，不要把內部細節搬進中心 Fact Map。
- 如果 public contract 需要改，先更新中心 repo，再更新子 repo 的 `contracts/contract.lock.json`。

## 驗證

- 修改中心契約後必須跑 `./validate.sh`。
- 不要把 Office lock file、`.tmp`、簡報匯出暫存檔、未確認的大型媒體檔納入 harness commit。
- 目前中心 repo 的 validator 只驗證中心文件與契約來源；子 repo adapter 需在各子 repo 落地後各自執行。
