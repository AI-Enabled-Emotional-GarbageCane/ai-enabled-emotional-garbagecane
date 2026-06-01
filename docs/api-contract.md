# 跨 Repo API 契約

> **v0.2 — 已定稿**。三模組全部運行於同一台 Jetson AGX Orin Nano，透過 Python `multiprocessing.Queue` 通訊。

## 系統流程（全自動化）

```
┌─────────────────┐
│    firmware     │  L515 depth 偵測使用者靠近（距離 < 閾值）
└────────┬────────┘
         │ ① user_detected（via q_detected）
         ▼
┌─────────────────┐
│     vision      │  L515 RGB/depth camera 擷取互動場景 → YOLOv8n 推論
└────────┬────────┘
         │ ② recognition_result（via q_result）
         ▼
┌─────────────────┐
│     display     │  自動播放 roast/accept 語音 + LED 指示 + 紀錄事件
└─────────────────┘
```

> **不再有 display → firmware 通訊**。系統全自動，無使用者按鈕、無蓋子機構。

## 通訊協定

**方案 B：多 process + `multiprocessing.Queue`**

三個模組各為獨立 Python process，透過共享的 Queue 物件傳遞事件。啟動時由一個 launcher script 建立 Queue 並 spawn 三個 process。

選擇理由：
- 三人各自開發獨立 repo，不易 git 衝突
- 同機運行，不需網路協定，延遲極低
- 比單一 process 更好拆分職責
- 不需 MQTT broker 或 WebSocket server 的額外基建

## 介面定義

### ① firmware → vision（觸發推論）

| 項目 | 定案 |
|---|---|
| 通訊方式 | `multiprocessing.Queue`（命名為 `q_detected`） |
| 事件名 | `user_detected` |
| Payload | `{ "event": "user_detected", "distance_cm": <number>, "ts": <iso8601> }` |
| 觸發條件 | L515 depth 串流偵測到物件／使用者距離 < 閾值（建議 30cm） |

### ② vision → display（推論結果）

| 項目 | 定案 |
|---|---|
| 通訊方式 | `multiprocessing.Queue`（命名為 `q_result`） |
| 事件名 | `recognition_result` |
| Payload | `{ "event": "recognition_result", "class": "accept" \| "reject", "confidence": <0-1>, "num_objects": <int>, "snapshot_path": <str>, "ts": <iso8601> }` |

Payload 欄位說明：
- `class`：binary 分類結果（`accept` = 一般垃圾、`reject` = 資源回收物/廚餘等）
- `confidence`：模型信心值（0-1）
- `num_objects`：YOLO 偵測到的物件數量
- `snapshot_path`：L515 camera 快照的本機檔案路徑（供 display 紀錄用）

### ③ display → firmware（已移除）

~~原設計為使用者按鈕確認後通知 firmware 開蓋。~~

現已移除：系統全自動化，不設使用者按鈕、不做蓋子機構。Display 直接根據 vision 結果播放語音與更新螢幕。

## 決策紀錄

### Class 集合：Binary

```
accept   ←  一般垃圾 / 可燃垃圾（本垃圾桶接受之類別）
reject   ←  資源回收物（紙、塑膠、金屬、玻璃）、廚餘等
```

TrashNet / RealWaste 原始多類標註重新映射至 binary。

### 多物件偵測規則

`num_objects > 1` → 直接判定 `reject`，觸發專屬 roast。

### Confidence 處理（全自動，不問使用者）

| 條件 | 行為 |
|---|---|
| `confidence ≥ 0.5` | 直接判定 accept/reject，觸發對應語音 |
| `confidence < 0.5` | 播放自嘲語音（「我看不太出來欸」），不做 accept/reject 判定 |

不設「請使用者確認」流程，避免使用者欺騙系統。

### Timestamp

本機時間 ISO8601，不上 NTP。學生專題不需嚴格對時。
