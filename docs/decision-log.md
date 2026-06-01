# Cross-Repo Decision Log

本文件只記錄會影響多個 repo 的方向性決策。子 repo 內部實作選型若不改 public contract，留在各自 repo。

## D-001: 使用 Queue 而非網路協定

- Status: Accepted
- Contract: `v0.3`
- Decision: 三模組同機運行，透過 Python `multiprocessing.Queue` 溝通；public Queue 為 `q_detected` 與 `q_result`，public event 為 `user_detected` 與 `recognition_result`。
- Rationale: 三人各自開發獨立 repo，但 demo 部署在同一台 Jetson；Queue 比 MQTT、WebSocket、ZeroMQ 更小且更少基建。
- Impact: `firmware`、`vision`、`display` 必須由 launcher 建立共享 Queue 後啟動。

## D-002: 採 binary class

- Status: Accepted
- Contract: `v0.3`
- Decision: `class` 只允許 `accept` 或 `reject`。
- Rationale: 專案定位為一般垃圾桶的互動教育 demo，不做完整回收分類機。
- Impact: `vision` 輸出 binary 判定；`display` 的語音與狀態機只依 binary 結果分流。

## D-003: L515 RGB/depth 分責

- Status: Accepted
- Contract: `v0.3`
- Decision: L515 RGB 串流歸 `vision`，L515 depth 距離感測歸 `firmware`。
- Rationale: 保持模型推論與硬體感測責任分離。
- Impact: `firmware` 不做模型推論；`vision` 不負責距離觸發與 LED。

## D-004: 移除使用者確認與蓋子機構

- Status: Accepted
- Contract: `v0.3`
- Decision: 系統全自動，不設使用者按鈕，不做蓋子機構，不保留 public `display -> firmware` flow。
- Rationale: 降低硬體複雜度，也避免使用者透過確認流程欺騙系統。
- Impact: `display` 消費 `recognition_result` 後直接播放語音與更新 UI；`firmware` 不等待 display 指令。

## D-005: 中央契約 + 子 repo lock

- Status: Accepted
- Contract: `v0.3`
- Decision: 中心 repo 保存 contract source；各子 repo 以 `contracts/contract.lock.json` 鎖定版本。
- Rationale: 組員可能只 clone 單一子 repo，因此不能假設所有人會讀中心 Fact Map。
- Impact: 子 repo 若改 public contract，必須先升級中心契約，再更新 lock。

## D-006: v0.3 採 L515 與 YOLOv11n classification

- Status: Accepted
- Contract: `v0.3`
- Decision: 以 Intel RealSense L515 取代原 RGB-D 鏡頭假設；`vision` v1 採 YOLOv11n binary classification。
- Rationale: 實際硬體改為 L515；classification 能先用 TrashNet / RealWaste 與少量 L515 實拍資料快速落地。
- Impact: `vision` 以 L515 RGB frame 做推論；`firmware` 以 L515 depth 做距離觸發；大型資料與模型產物不進 git。

## D-007: v0.3 `num_objects` v1 固定為 1

- Status: Accepted
- Contract: `v0.3`
- Decision: `vision` v1 固定輸出 `num_objects=1`，不實作多物件偵測。
- Rationale: v1 採 classification，公開資料集沒有 bbox 標註；強行做 detection 會提高資料與標註成本。
- Impact: `recognition_result` payload 仍保留 `num_objects` 欄位；`num_objects > 1` 的 reject 規則保留給未來 detection / foreground estimation 版本。
