# AI 情緒垃圾筒

> 因為海龜每天都在被吸管攻擊。

一個能辨識垃圾、提供互動回饋，讓丟垃圾這件事變得有意義的智慧垃圾桶專案。

## 1. 背景

海洋垃圾（尤其是塑膠吸管）正威脅海洋生物的生存。我們希望透過一個結合 AI 辨識與互動裝置的垃圾桶，提醒使用者每一次丟垃圾的選擇都會影響環境。

## 2. 技術

- **AI 影像辨識**：以 L515 RGB 擷取畫面，經 YOLOv11n binary classification 模型分類垃圾種類
- **感測**：以 L515 depth 距離感測偵測使用者靠近
- **推論輸出**：透過 Python `multiprocessing.Queue` 將辨識結果回饋至 display

## 3. 設備

- **顯示螢幕**:呈現辨識結果與互動畫面
- **全自動互動流程**:靠近、辨識、回饋皆自動完成，無使用者按鈕
- **喇叭 / LED**:聲光回饋
- **垃圾桶機構**:v0.3 不做蓋子機構，互動以語音、LED、螢幕為主

## 4. 目標

打造一個結合教育與互動的智慧垃圾桶，讓使用者意識到正確分類垃圾與減少海洋污染的關係。

---

## Repo 分工與實際目錄

本 repo 是**中心治理 repo**，負責整體說明、跨 repo 契約、Fact Map、決策紀錄與文件驗證。`vision`、`firmware`、`display` 是獨立 GitHub repo，**不會以子目錄形式放在本 repo 裡**。

本 repo 的實際目錄：

| 路徑 | 內容 |
|------|------|
| `AGENTS.md` | 中心 repo 的 agent / 維護指引 |
| `docs/` | 實作前報告、跨 repo API 契約、Fact Map、Decision Log |
| `contracts/` | machine-readable contract source 與子 repo lock 來源 |
| `scripts/` | 中心契約驗證腳本 |
| `validate.sh` | 中心 repo 驗證入口 |
| `validate.ps1` | Windows PowerShell 驗證入口 |

外部子 repo：

| Repo | 內容 |
|------|------|
| [`ai-enabled-emotional-garbagecane`](https://github.com/AI-Enabled-Emotional-GarbageCane/ai-enabled-emotional-garbagecane)(本 repo) | 中心治理 repo：整體說明、文件、跨 repo 契約與方向治理 |
| [`vision`](https://github.com/AI-Enabled-Emotional-GarbageCane/vision) | AI 影像辨識 + 資料整理 |
| [`firmware`](https://github.com/AI-Enabled-Emotional-GarbageCane/firmware) | 硬體感測（L515 depth 距離）+ LED |
| [`display`](https://github.com/AI-Enabled-Emotional-GarbageCane/display) | 顯示 UI + 互動畫面 + 報告 |

## 分工

|   人員   | 主要負責 | 具體工作 | Repo |
|------|----------|----------|------|
| 黃教丞 | AI 辨識 + 資料整理 | 收集垃圾圖片、訓練 / 測試模型、攝影機辨識垃圾、輸出辨識結果 | [`vision`](https://github.com/AI-Enabled-Emotional-GarbageCane/vision) |
| 張世鵬 | 硬體感測 + LED | L515 depth 距離感測、LED 燈號、透過 `q_detected` 送出 `user_detected` | [`firmware`](https://github.com/AI-Enabled-Emotional-GarbageCane/firmware) |
| 林欣螢 | 系統整合 + UI / 報告 | 接收 `q_result`、把 AI 結果接到畫面 / 語音、設計互動畫面、整理 README、簡報與影片 Demo | [`display`](https://github.com/AI-Enabled-Emotional-GarbageCane/display)、本 repo `docs/` |
