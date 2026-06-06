# 2026-06-04-harness-trace-structure

## Metadata

| Field | Value |
|---|---|
| Date | 2026-06-04 |
| Author / Agent | Codex |
| Related repo(s) | ai-enabled-emotional-garbagecane |
| Contract version | v0.3 |
| Status | implemented |

## Goal

新增 harness 層級的實作 trace 文件結構，讓後續 agent 在實作時能記錄做法、問題、驗證與後續風險，並能從 `AGENTS.md` 進入這套流程。

## Scope

本次只修改中心治理 repo 的文件與 validator。沒有修改 `vision`、`firmware`、`display` 的實作，也沒有改 v0.3 queue payload。

## Starting Context

中心 repo 已有 `AGENTS.md`、`docs/README.md`、`scripts/validate-contract.py` 作為 harness 文件與驗證入口，但缺少可持續追加的實作紀錄區塊。後續實作若發現問題，缺少一個能回頭查「當時怎麼做」的 trace 位置。

## Implementation Steps

1. 新增 `docs/implementation-traces/README.md`，定義何時要寫 trace、命名規則、最低必要段落。
2. 新增 `docs/implementation-traces/TEMPLATE.md`，提供每次實作可複製填寫的固定格式。
3. 新增本 trace 作為第一筆範例紀錄。
4. 更新 `AGENTS.md`，把 trace protocol 放進 agent 入口指引。
5. 更新 `docs/README.md`，讓文件中心能找到 implementation traces。
6. 更新 `scripts/validate-contract.py`，把 trace 入口與 template 必要段落納入驗證。

## Decisions and Tradeoffs

選擇把 trace 放在中心 repo 的 `docs/implementation-traces/`，因為這裡是跨 repo contract 與 harness governance 的來源。子 repo 內部細節仍應留在各自 repo，但只要會影響整合、契約或 handoff，就應在中心 trace 留下脈絡。

## Problems Encountered

目前沒有實作阻塞。需要注意的是，trace 文件不應變成大型日誌或完整 diff；它只記錄足夠讓後續接手者理解脈絡的資訊。

## Files Changed

- `AGENTS.md`
- `docs/README.md`
- `docs/implementation-traces/README.md`
- `docs/implementation-traces/TEMPLATE.md`
- `docs/implementation-traces/2026-06-04-harness-trace-structure.md`
- `scripts/validate-contract.py`

## Verification

```text
command: ./validate.sh
result: PASS
notes: center contract, docs, and subrepo lock sources are consistent.
```

## Follow-up

後續跨 repo 實作時，先複製 `TEMPLATE.md` 建立 trace，再開始記錄實作假設、問題與驗證。若只是子 repo 純內部改動，只有在影響 public contract 或整合 handoff 時才需要回到中心 repo 補 trace。

## Rollback Notes

若要回退這套 trace 結構，移除 `docs/implementation-traces/`、`AGENTS.md` 的 implementation trace protocol、`docs/README.md` 的 trace 入口，以及 validator 內的 trace 檢查。

## Revision Notes

- 2026-06-04: 初版 trace 結構建立。
