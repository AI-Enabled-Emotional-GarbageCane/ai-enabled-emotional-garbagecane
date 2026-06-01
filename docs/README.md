# 文件中心

本目錄存放**跨 repo 的整合性文件**與**實作前報告**。各子 repo 的技術細節留在各自 repo 內，這裡只保留共識、契約與整體規劃。

## 實作前報告（Phase 1：研究與設計收斂）

| 檔案 | 內容 |
|---|---|
| [00-report.md](./00-report.md) | **報告主文件**：摘要、目錄、一頁 pitch、決策表、風險、成功指標 |
| [01-background.md](./01-background.md) | §1 問題背景：海洋塑膠數據、台灣回收現況、源頭分類重要性 |
| [02-related-work.md](./02-related-work.md) | §2 相關工作：商業／學術競品、差異化定位 |
| [03-system-design.md](./03-system-design.md) | §3 系統設計：架構、AI 選型、硬體選型、API 收斂 |
| [04-interaction-design.md](./04-interaction-design.md) | §4 互動與情緒設計：roast 設計、行為理論、UX、倫理 |
| [05-team-and-plan.md](./05-team-and-plan.md) | §5 分工與時程：分工 review、8 週計畫、風險清單 |

> **建議閱讀順序**：先看 `00-report.md`（10 分鐘掌握全貌），再依興趣展開個別章節。

## 跨 repo 契約

v0.3 定案為 Intel RealSense L515、YOLOv11n binary classification、Python `multiprocessing.Queue`、全自動流程。

| 檔案 | 內容 |
|---|---|
| [api-contract.md](./api-contract.md) | `vision` ↔ `firmware` ↔ `display` 的事件流與 payload（**已依 §3.5 定稿，v0.3**）|
| [fact-map.md](./fact-map.md) | 跨 repo 穩定事實、模組邊界、drift policy |
| [decision-log.md](./decision-log.md) | 會影響三個 repo 的方向決策 |
| [../contracts/contract.v0.3.json](../contracts/contract.v0.3.json) | machine-readable contract source |

## Harness 驗證

- 中心 repo 修改後，macOS / Linux 執行 `./validate.sh`
- Windows PowerShell 執行 `.\validate.ps1`
- 子 repo 實際落地時，從 `contracts/subrepo-locks/` 取得對應 module 的 lock 來源
- `contract.lock.json` 複製到子 repo 後，必須把 `source_commit` 改成中心 contract 所在 commit

## 文件原則

- 任何會被多個 repo 同時讀寫的「介面」、「協定」、「事件」都寫在這裡
- 子 repo 的內部實作不寫進來
- 文件以「契約 / 規格」為主，而非教學或日誌
- 報告章節保留可引用來源；不捏造數字
