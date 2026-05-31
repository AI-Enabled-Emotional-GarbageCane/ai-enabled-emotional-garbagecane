# AI 情緒垃圾筒 — 實作前報告

> 一個會用組員聲音吐槽你的智慧垃圾桶，
> 因為海龜每天都在被吸管攻擊。

| 項目 | 內容 |
|---|---|
| 專題類別 | 學校期末 / 畢業專題 |
| 報告性質 | **實作前報告**（規劃與設計收斂，尚未進入實作） |
| 預計時程 | 8 週（期末前 1-2 個月） |
| 團隊規模 | 3 人 |
| 文件版本 | v0.2 |

---

## 摘要

本專題規劃打造一個結合 RGB-D 影像辨識與情緒互動回饋的「一般／可燃垃圾」專用智慧垃圾桶。系統採**全自動化設計**——使用者靠近後自動偵測、辨識、回饋，無需任何手動操作。系統由三個模組組成：`vision`（Intel RealSense D435 + YOLOv8n on Jetson AGX Orin Nano，輸出 accept / reject binary 判定）、`firmware`（距離感測、LED 燈號）、`display`（admin 控制面板 + 使用者端公告螢幕 + 語音反饋）。三模組以 Python `multiprocessing.Queue` 在同一台 Jetson 上通訊。**核心差異化**在於：當投入物件被判定為 reject 時，系統自動觸發**團隊成員自錄的幽默化負向反饋語音**——這在既有的商業產品（Bin-e、TrashBot、Oscar）與學術專案中皆為空白。

設計選擇有學術支撐：Fogg Behavior Model 的「即時 Trigger」、Comber & Thieme 2013 的「aversive affect 設計策略」、Skurka 2018 的「幽默訴求降低心理抗拒」、Trujillo 2021 的「規範聚焦 nudge 同時引發正負向情緒反應」、Berengueres 2013 的「emoticon-bin 回收率達 3 倍」。

本份報告為**實作前的規劃與設計收斂成果**。預計期末產出包括：可實機 demo 的智慧垃圾桶（邊緣運算硬體採 NVIDIA Jetson AGX Orin Nano）、demo 影片、完整報告、PowerPoint 簡報。

## 目錄

| 章節 | 內容 | 連結 |
|---|---|---|
| §1 | 問題背景：海洋塑膠數據、台灣回收現況、源頭分類重要性 | [01-background.md](./01-background.md) |
| §2 | 相關工作：商業 / 學術競品分析、差異化定位 | [02-related-work.md](./02-related-work.md) |
| §3 | 系統設計：架構、AI 選型、硬體選型、API 收斂 | [03-system-design.md](./03-system-design.md) |
| §4 | 互動與情緒設計：roast 設計、行為理論、UX、倫理 | [04-interaction-design.md](./04-interaction-design.md) |
| §5 | 分工與時程：分工 review、8 週計畫、風險清單 | [05-team-and-plan.md](./05-team-and-plan.md) |
| 附錄 | 跨 repo API 契約 | [api-contract.md](./api-contract.md) |

---

## 一頁 Pitch（給簡報第一頁用）

**問題**：海洋塑膠是年增百萬噸的工程問題，但家戶分類錯誤會在後段被放大成 17–40% 的 MRF 污染率，整車回收物可能整批進掩埋場。

**現況**：市面上的 AI 智慧垃圾桶（Bin-e、TrashBot、Oscar）都在拼辨識準確率（90–97%），但互動層全是「中性 + 鼓勵」路線，沒有人在做情緒層的差異化。

**解法**：用 YOLOv8n 做影像辨識，用**組員自錄的幽默 roast 語音**做即時負向回饋。全自動化流程——使用者靠近即啟動、丟入即判定、無需任何手動操作。理論基礎是 Fogg Behavior Model + Skurka 2018 幽默訴求 + Berengueres 2013 emoticon-bin（回收率 3 倍）+ parasocial 個人化。

**為什麼是我們**：3 人團隊、8 週、學生預算；Jetson AGX Orin Nano 邊緣運算全自動化；學術論證硬，記憶點強，對外傳播性好。

---

## 關鍵設計決策一覽（對外簡報用）

| 決策 | 選擇 | 為什麼 | 詳見 |
|---|---|---|---|
| AI 模型 | YOLOv8n / v11n | 同時得 bbox + label、Ultralytics 生態完整 | §3.2 |
| 訓練資料集 | TrashNet 主 + RealWaste 補 | 類別貼合 demo 場景；快速可訓 | §3.3 |
| 硬體 | Intel RealSense D435（RGB-D） + NVIDIA Jetson AGX Orin Nano | RGB 給推論、Depth 給 ROI 分割／距離偵測；全部跑在同一台機器 | §3.4 |
| 通訊 | Python `multiprocessing.Queue` | 三模組同機運行，不需網路協定；簡單且低延遲 | §3.5 |
| 類別 | binary（accept ／ reject） | 系統定位為「一般垃圾」專用桶；roast 場景單一化 | §3.5 |
| 流程 | 全自動化，無使用者按鈕 | 靠近即偵測、丟入即判定、自動播語音；不做蓋子機構 | §3.5, §4.3 |
| 多物件 | 直接 reject | 一次丟多個 = 沒分類 = 該被 roast | §3.5 |
| 回饋 | 幽默 roast 而非鼓勵 | Comber & Thieme 2013 + Skurka 2018 + Trujillo 2021 + Berengueres 2013 | §4.2 |
| 聲音 | 組員自錄而非 TTS | Parasocial、社交存在感 | §4.1 |

---

## 風險與退路（對外簡報用）

| 風險 | 退路 |
|---|---|
| Jetson 環境配置（JetPack / TensorRT）學習曲線過陡 | 預先完成環境驗證；臨時退路為筆電執行推論 |
| D435 深度鏡頭借不到 | 改用一般 USB Webcam + 外接超音波感測器替代距離偵測 |
| 老師質疑 roast 教育意義 | §4.2 學術引用直接搬到簡報前三頁 |
| 組員不敢錄狠話 | 內容守則 §4.3.2，「中度吐槽」是 baseline |

---

## 成功指標（要在報告/答辯中可量化的）

| 類別 | 指標 | 目標 |
|---|---|---|
| 技術 | 辨識準確率（test set top-1）| ≥ 85% |
| 技術 | 端到端延遲（丟入 → 語音播放）| ≤ 2.5 秒 |
| 互動 | demo 中使用者笑出來次數 | 每 10 次互動 ≥ 5 次 |
| 自動化 | 全流程無需使用者手動操作 | 靠近 → 丟入 → 自動回饋，零按鈕 |

---

## 後續工作（實作階段待辦）

- [ ] 與全組對齊本份 docs/，正式簽收
- [ ] 修正 `image1.png` 的「感測歸 vision」描述（應歸 firmware）
- [ ] 採購硬體（Jetson AGX Orin Nano、D435 或替代方案）
- [ ] 找老師確認「幽默 roast」的學術立場
- [ ] 開始 Phase 2 PoC

---

> **此份報告為實作前的規劃與設計收斂成果**。後續實作章節（PoC 結果、實機照片、demo 影片連結、測試數據）將於實作階段補入。
