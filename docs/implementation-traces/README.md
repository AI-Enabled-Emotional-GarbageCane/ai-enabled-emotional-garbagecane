# Implementation Traces

本目錄用來保存 harness 層級的實作紀錄。目的不是取代 commit message，而是讓後續 agent 或組員能回頭追蹤「當時怎麼做、遇到什麼問題、為什麼這樣取捨、驗證跑了什麼」。

## 何時要新增 trace

- 有任何跨 repo contract、queue payload、module boundary、validator、handoff 流程的變更。
- 子 repo 實作會影響中心 v0.3 契約，或需要中心 repo 留下整合脈絡。
- 遇到實作阻塞、硬體限制、模型限制、環境差異，需要後續接手者知道。
- 一次實作橫跨 `vision`、`firmware`、`display` 任兩個以上 repo。

只改 typo、格式、純內部註解且不影響整合時，可以不新增 trace。

## 命名規則

使用：

```text
YYYY-MM-DD-<module-or-area>-<short-topic>.md
```

範例：

```text
2026-06-04-vision-model-runtime.md
2026-06-04-harness-trace-structure.md
```

## 撰寫規則

- 以 `TEMPLATE.md` 複製一份新 trace，再填內容。
- 實作開始時先記錄目標、範圍與假設；實作結束時補上步驟、問題、驗證與 follow-up。
- 指向檔案時使用 repo 相對路徑，例如 `vision/src/runtime.py`。
- 驗證結果要寫實際跑過的 command 與 PASS / FAIL；失敗也要保留摘要。
- 若後來發現問題，新增一段 `Revision Notes`，不要直接抹掉原本的判斷。

## 最低必要段落

每份 trace 至少要包含：

- `Goal`
- `Scope`
- `Implementation Steps`
- `Problems Encountered`
- `Verification`
- `Follow-up`
- `Revision Notes`
