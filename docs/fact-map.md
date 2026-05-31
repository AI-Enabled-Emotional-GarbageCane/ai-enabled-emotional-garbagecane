# Cross-Repo Fact Map

本文件只記錄會影響 `vision`、`firmware`、`display` 三個 repo 的穩定事實。子 repo 的內部實作細節不放在這裡。

## Source Of Truth

| 項目 | 目前事實 |
|---|---|
| Contract version | `v0.2` |
| Human-readable contract | `docs/api-contract.md` |
| Machine-readable contract | `contracts/contract.v0.2.json` |
| Governance model | 中央契約優先；子 repo 以 `contract.lock.json` 鎖定版本 |
| Runtime target | Jetson AGX Orin Nano，同機多 process |
| Transport | Python `multiprocessing.Queue` |

## Module Boundaries

| Module | Owns | Consumes | Must not own |
|---|---|---|---|
| `firmware` | D435 depth 距離感測、LED、`user_detected` | 無跨 repo event | 模型推論、UI、語音、使用者確認流程 |
| `vision` | D435 RGB 串流、YOLO 推論、`recognition_result` | `user_detected` | 語音、UI、LED、硬體互動 |
| `display` | 狀態機、roast/accept 語音、公告螢幕、admin panel、事件紀錄 | `recognition_result` | 模型推論、D435 depth 感測、public `display -> firmware` flow |

## Event Contract

| Queue | Direction | Event | Required payload fields |
|---|---|---|---|
| `q_detected` | `firmware -> vision` | `user_detected` | `event`, `distance_cm`, `ts` |
| `q_result` | `vision -> display` | `recognition_result` | `event`, `class`, `confidence`, `num_objects`, `snapshot_path`, `ts` |

## Behavioral Invariants

- `class` 只允許 `accept` 或 `reject`。
- `confidence >= 0.5` 時直接判定 `accept` 或 `reject`。
- `confidence < 0.5` 時播放自嘲語音，不做 accept/reject 判定。
- `num_objects > 1` 直接判定 `reject`。
- 系統全自動，無使用者按鈕。
- v0.2 不做蓋子機構。
- v0.2 不存在 public `display -> firmware` 通訊。

## Drift Policy

| Drift type | 處理方式 |
|---|---|
| Public contract drift | 先更新中心 `docs/api-contract.md`、`contracts/contract.v*.json`、`docs/decision-log.md`，再更新子 repo lock。 |
| Internal implementation drift | 子 repo 自行記錄；只要 public contract 不變，不回寫中心 Fact Map。 |
| Experiment drift | 不覆蓋 `contract.lock.json`；用 mock 或 adapter 維持舊 contract。 |
| Emergency drift | 可先在子 repo 落地，但需留下 drift note，之後補中心決策或回復原 contract。 |

## Known Current Gaps

- 三個子 repo 的本地 adapter 尚未落地於各 repo；中心 repo 先提供 `contracts/subrepo-locks/*.contract.lock.json` 作為 lock 來源。
- `contracts/subrepo-locks/*.contract.lock.json` 的 `source_commit` 目前使用 `pending-center-contract-commit`；中心 harness commit 完成後，子 repo 實際 lock 必須改成該中心 commit。
- 若只 clone 單一子 repo，必須在該 repo 補上 `AGENTS.md`、`contracts/contract.lock.json` 與本地 `validate.sh`，才算完整落地。
