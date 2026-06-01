# §3 系統設計

> 從感測器到語音回饋的端到端架構，含 AI 模型與硬體選型決策。

## 3.1 系統流程

全自動化流程——使用者不需要按任何按鈕，靠近即啟動、丟入即判定：

```
┌─────────────────┐
│    firmware     │  ① L515 depth 偵測使用者靠近（距離 < 閾值）
└────────┬────────┘
         │ user_detected（via Queue）
         ▼
┌─────────────────┐
│     vision      │  ② L515 RGB/depth camera 擷取互動場景 → YOLOv8n 推論
└────────┬────────┘
         │ recognition_result {class, confidence}（via Queue）
         ▼
┌─────────────────┐
│     display     │  ③ 自動播放 roast/accept 語音 + 紀錄事件 + LED 指示
└─────────────────┘
```

> 注意：不設蓋子機構、不設使用者按鈕。系統全自動運行，feedback 以語音 + LED + 螢幕為主。

## 3.2 AI 模型選型

### 候選比較

| 選項 | 準確率 ballpark | 推論速度 | 上手難度 | 是否需 GPU 訓練 |
|---|---|---|---|---|
| YOLOv8n / YOLOv11n | mAP 高、單物件分類 90%+ | Jetson AGX Orin Nano + TensorRT INT8 充分吞吐；RPi5 CPU INT8 約 13 FPS | 低（Ultralytics CLI 一行 train） | Colab 免費 T4 即可 |
| MobileNetV3 + 自訂分類頭 | TrashNet 上 transfer learning 通常 85–92% | 行動端極快、Coral 上可達數百 FPS | 中（Keras / PyTorch） | Colab 即可 |
| EfficientNet-Lite | 與 MobileNetV3 接近、略高 | 同級 | 中 | Colab 即可 |
| Cloud API（GCV / Azure Custom Vision） | 商用模型 90%+ | 200–800 ms 網路延遲 | 最低 | 不需 |

### 決策

- **主推**：**YOLOv8n / YOLOv11n** — 同時得到 bounding box 與 label，視覺化最直觀，Ultralytics 生態完整，期末 demo 截圖好看。
- **備案**：**MobileNetV3 + transfer learning**（如果 YOLO 在硬體上 latency 不行就退回來）。
- **不採用 Cloud API**：demo 場合 Wi-Fi 不穩、且失去「邊緣推論」的學術/技術賣點。

## 3.3 訓練資料集

| 資料集 | 圖片數 | 類別 | 用途 |
|---|---|---|---|
| **TrashNet** | 約 2,527 張 | 6 類（紙、紙板、玻璃、金屬、塑膠、其他） | **主資料集**：類別少、訓練快、與「丟入瞬間單物件」場景吻合 |
| **RealWaste** (HuggingFace) | 4,752 張，524×524 | 9 類 | **補強**：真實垃圾場拍攝、有髒污遮蔽，做 fine-tune 增強泛化 |
| **TACO** | 1,500 / 3,736 | 60 / 28 super | 不採用：類別過細、街拍場景不符 |

> 兩個主資料集都可在 GitHub / Hugging Face 直接下載。

## 3.4 硬體選型

### 候選比較與決策

| 硬體 | 角色 | 適合度 |
|---|---|---|
| **NVIDIA Jetson AGX Orin Nano** ★ | 邊緣運算 / 模型推論 | ◎ 採用：CUDA / TensorRT 生態完整、推論吞吐充裕 |
| **Intel RealSense L515** ★ | RGB-D/depth camera 影像取得 | ◎ 採用：提供 camera input 給互動辨識 pipeline，depth stream 給距離量測 |
| Raspberry Pi 5 (8GB) | 邊緣運算 | ✗ 不採：CPU 推論吞吐有限 |
| ESP32-CAM | 影像取得 | ✗ 不採：記憶體不足，無 depth 串流 |
| 筆電 + USB Webcam | 開發過渡 | △ 僅作為 Phase 2 開發階段使用，最終部署以 Jetson + L515 為主 |

### 決策

**採用 NVIDIA Jetson AGX Orin Nano + Intel RealSense L515** 作為正式部署之邊緣運算與感測組合。

**RealSense L515 之雙重角色**：
- **Camera input** → YOLOv8n 推論前的互動場景擷取（由 `vision` 模組管理）。
- **Depth 串流** → 偵測使用者靠近（距離 < 閾值，由 `firmware` 模組管理）。L515 同時取代外接超音波（HC-SR04 不再採用）。

> **備案**：若 L515 camera 取得或 driver 設定卡關，改用一般 USB Webcam（RGB only）+ 外接超音波感測器（HC-SR04）替代 demo 距離偵測功能。

**開發流程**：
- 模型訓練於 Google Colab（T4 GPU，免費），權重輸出為 ONNX。
- ONNX 於 Jetson 上轉換為 TensorRT engine 後執行推論。
- L515 透過 librealsense（Jetson 上 USB 3.0 介接）提供 RGB-D/depth camera 串流。Jetson AGX Orin Nano 仍作為邊緣推論平台。
- 開發過程中可先於筆電執行整條 pipeline 進行除錯，後再移植至 Jetson。

**緩解風險**：JetPack、TensorRT、librealsense 之安裝與相容性為主要學習曲線；建議於 Phase 1 結束前完成上述環境驗證。如延遲，臨時方案為直接於筆電執行推論進行 demo（不影響軟體主軸）。

## 3.5 通訊協定

三個模組全部運行在同一台 Jetson AGX Orin Nano 上，採 **方案 B：多 process + `multiprocessing.Queue`** 通訊。

### 為什麼選 Queue 而非網路協定

| 方案 | 說明 | 採用 |
|---|---|---|
| 單一 process（function call） | 最簡單，但三人 code 合在一起容易 git 衝突 | ✗ |
| **多 process + `multiprocessing.Queue`** | 各模組獨立 process，整合時啟動三個 process，透過 Queue 傳資料 | **◎ 採用** |
| 本機 WebSocket / ZeroMQ | 可擴展到多機，但對學生專題過度工程 | ✗ |

### 事件流與 Queue 定義

| Queue | 方向 | Payload | 說明 |
|---|---|---|---|
| `q_detected` | firmware → vision | `{ "event": "user_detected", "distance_cm": <number>, "ts": <iso8601> }` | L515 depth 偵測到使用者靠近 |
| `q_result` | vision → display | `{ "event": "recognition_result", "class": "accept" \| "reject", "confidence": <0-1>, "num_objects": <int>, "snapshot_path": <str>, "ts": <iso8601> }` | 推論結果，含物件數量與快照路徑 |

> 不再需要 display → firmware 的通訊——系統全自動，沒有使用者確認步驟，不做蓋子機構。

### 關於 class 集合

採 **binary 分類**：

```
accept   ←  一般垃圾 / 可燃垃圾（本垃圾桶接受之類別）
reject   ←  資源回收物（紙、塑膠、金屬、玻璃）、廚餘等
```

理由：
- 系統定位為「一般／可燃垃圾」專用桶，並非通用分流器；不需要多類別分類器。
- TrashNet 與 RealWaste 之原始 6／9 類標註可重新映射至此 binary：原 paper/plastic/metal/glass → reject；原 trash → accept；廚餘類別於 RealWaste 中亦歸為 reject。
- binary head 之模型較輕、訓練資料更易平衡、demo 時的判定邊界對使用者也更直觀（「這個桶子收／不收」）。
- 配合 §4 互動設計，roast 觸發條件單純化為「reject 投入」單一場景。

### 多物件偵測規則

- **YOLO 回傳 `len(detections) > 1`** → 直接判定 reject，觸發專屬 roast（「一次丟一堆是沒在分類」）。
- 理由：一次丟多個物件 = 使用者沒有分類就投入，符合 reject 的設計邏輯。

### Confidence 處理（全自動，不問使用者）

- **conf ≥ 0.5**：直接判定 accept / reject，觸發對應語音
- **conf < 0.5**：播放自嘲語音（「我看不太出來欸」），不做判定，不觸發 roast
- **不設「請使用者確認」流程**——全自動化設計，避免使用者欺騙系統

### Timestamp

本機時間 ISO8601 即可，不上 NTP。學生專題不需嚴格對時。

## 3.6 模組職責邊界

| 模組 | 職責 | 不負責 |
|---|---|---|
| `vision` | 模型訓練、即時推論、回傳 `{class, confidence, num_objects, snapshot_path}`；L515 camera 輸入管理 | 不負責語音、不負責 UI |
| `firmware` | L515 depth 串流 → 距離感測、LED 燈號控制 | 不負責推論、不負責語音 |
| `display` | 狀態機、roast 語音播放、admin 控制面板、使用者端公告螢幕、事件紀錄（本機照片 + JSON log） | 不負責模型、不負責硬體感測 |

> 「狀態機」（state machine）是 display 的核心職責 —— 從 idle / detecting / recognizing / playing-roast / cooldown 之間的轉換。不再有 asking 或 opening-lid 狀態。

下一章（§4 互動設計）展開 roast 語音與 UI 的細節設計。
