# AI 情緒垃圾筒

> 因為海龜每天都在被吸管攻擊。

一個能辨識垃圾、提供互動回饋,讓丟垃圾這件事變得有意義的智慧垃圾桶專案。

## 1. 背景

海洋垃圾(尤其是塑膠吸管)正威脅海洋生物的生存。我們希望透過一個結合 AI 辨識與互動裝置的垃圾桶,提醒使用者每一次丟垃圾的選擇都會影響環境。

## 2. 技術

- **AI 影像辨識**:以攝影機擷取畫面,經訓練好的模型分類垃圾種類
- **感測**:紅外線 / 距離感測偵測使用者靠近與投入動作
- **推論輸出**:即時將辨識結果回饋至 UI 與互動裝置

## 3. 設備

- **顯示螢幕**:呈現辨識結果與互動畫面
- **互動 Option 按鈕**:讓使用者選擇 / 確認
- **喇叭 / LED**:聲光回饋
- **垃圾桶機構**:依辨識結果觸發對應動作

## 4. 目標

打造一個結合教育與互動的智慧垃圾桶,讓使用者意識到正確分類垃圾與減少海洋污染的關係。

---

## 倉庫架構

本專案以 monorepo 為整合中心,各分工子系統獨立為 repo。

| Repo | 內容 |
|------|------|
| [`ai-enabled-emotional-garbagecane`](https://github.com/AI-Enabled-Emotional-GarbageCane/ai-enabled-emotional-garbagecane)(本 repo) | Monorepo:系統整合、文件 (`docs/`)、整體說明 |
| [`ai`](https://github.com/AI-Enabled-Emotional-GarbageCane/ai) | AI 辨識 + 資料整理 |
| [`hardware`](https://github.com/AI-Enabled-Emotional-GarbageCane/hardware) | 硬體感測 + 互動裝置 |
| [`ui`](https://github.com/AI-Enabled-Emotional-GarbageCane/ui) | 系統整合 + UI / 報告 |

## 分工

| 人員 | 主要負責 | 具體工作 | Repo |
|------|----------|----------|------|
| TBD | AI 辨識 + 資料整理 | 收集垃圾圖片、訓練 / 測試模型、紅外線 / 距離感測、攝影機辨識垃圾、輸出辨識結果 | [`ai`](https://github.com/AI-Enabled-Emotional-GarbageCane/ai) |
| TBD | 硬體感測 + 互動裝置 | 喇叭 / 螢幕 / LED、垃圾桶觸發流程 | [`hardware`](https://github.com/AI-Enabled-Emotional-GarbageCane/hardware) |
| TBD | 系統整合 + UI / 報告 | 把 AI 結果接到畫面 / 語音、設計互動畫面、整理 README、簡報與影片 Demo | [`ui`](https://github.com/AI-Enabled-Emotional-GarbageCane/ui)、本 repo `docs/` |
