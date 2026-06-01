# §5 分工與時程

> 對既有分工的 review、調整建議，以及 1-2 個月期末時程規劃。

## 5.1 對既有分工的 review

### 既有分工（README）

| 人員 | 主要負責 | Repo |
|---|---|---|
| TBD | AI 辨識 + 資料整理 | `vision` |
| TBD | 硬體感測 + 互動裝置 | `firmware` |
| TBD | 系統整合 + UI / 報告 | `display` |

### 觀察 1：image1.png 與 README 不一致 ⚠️

`image1.png`（分工表）裡寫**「AI 辨識 + 資料整理」包含「紅外線/距離感測」**——這跟 README 寫的「硬體感測歸 firmware」**衝突**。**應以 README 為準**（感測屬 firmware），`image1.png` 的描述需更正。

### 觀察 2：「組員聲音 roast」是隱形工作 ⚠️

§4 的 roast 設計需要**錄音、寫台詞、剪音檔、版本管理**——建議歸 display 統籌，但**錄音是全員工作**（每人至少 5 句，見 §4.3.2）。

### 觀察 3：不做蓋子，firmware 大幅簡化

決定不做蓋子機構、不做使用者按鈕（見 §3.5），firmware 的工作量簡化為：
- L515 depth 串流 → 距離感測（偵測使用者靠近）
- LED 燈號控制
- 透過 `multiprocessing.Queue` 與 vision 通訊

不再需要：~~伺服馬達~~、~~按鈕讀取~~、~~開蓋機構~~。

### 分工表

| 人員 | 主要負責 | 具體工作 | Repo |
|---|---|---|---|
| TBD | **Vision／模型** | 整理 TrashNet + RealWaste 資料集；fine-tune YOLOv8n（binary: accept/reject）；輸出 `{class, confidence, num_objects, snapshot_path}`；準確率測試報告 | `vision` |
| TBD | **Firmware／感測** | L515 depth 距離感測；LED 燈號；透過 Queue 送 `user_detected` 給 vision | `firmware` |
| TBD | **Display／整合／UX** | 狀態機；roast 語音播放器（含音效設計）；admin 控制面板；使用者公告螢幕；事件紀錄（本機 JSON log + 照片）；接 vision Queue；**統籌錄音與台詞庫** | `display` |
| 全員 | **錄音、台詞** | 每人至少寫並錄 5 句 roast | （音檔放在 `display/assets/audio/`） |
| 全員 | **報告與 demo 影片** | display 負責人主筆，其餘提供各自模組的章節素材 | `docs/`、本 repo |

## 5.2 期末時程（8 週版本）

假設「期末前 1-2 個月」≈ 8 週。建議分為 4 個階段：

```
W1 ──┬── W2 ──┬── W3 ──┬── W4 ──┬── W5 ──┬── W6 ──┬── W7 ──┬── W8
     │        │        │        │        │        │        │
[ Phase 1 ]   [ Phase 2 ]       [ Phase 3 ]                 [ Phase 4 ]
  設計收斂      各自 PoC          整合 + 錄音                 demo + 報告
```

### Phase 1（W1-W2）：設計收斂

| Owner | 任務 |
|---|---|
| 全員 | 確認本份 docs/ 的 §1-§5 內容、簽收 |
| 全員 | 確認硬體取得方案（Jetson AGX Orin Nano 已確定；L515 若取得或 driver 設定卡關則備案 USB Webcam + HC-SR04） |
| Vision | 下載 TrashNet + RealWaste，跑出 baseline（不調參）的準確率 |
| Display | admin 面板 + 公告螢幕 mockup（Figma 或紙本）；roast 台詞模板 v0 |

**Phase 1 出口指標**：每個人都知道自己第 W3 開始要做什麼。

### Phase 2（W3-W4）：各自 PoC

| Owner | 任務 |
|---|---|
| Vision | YOLOv8n fine-tune（binary: accept/reject）；準確率 ≥ 85% on test set；輸出可呼叫的 inference function |
| Firmware | L515 depth 距離感測可運作；LED 控制可運作；可透過 Queue 送 `user_detected` |
| Display | 狀態機可手動觸發（給 mock 資料）；roast 語音播放器可工作；台詞庫 v1（每類 3 句） |
| 全員 | **W4 結束前完成全員錄音第一輪**（roast 台詞 v1） |

**Phase 2 出口指標**：三個模組各自 standalone 可 demo。

### Phase 3（W5-W6）：整合

| Owner | 任務 |
|---|---|
| Display | 把 vision Queue 接到狀態機；把 firmware Queue 接進來；三個 process 聯合啟動測試 |
| Vision | 把 model 部署到 Jetson AGX Orin Nano（TensorRT engine）；測 latency |
| Firmware | L515 depth 感測與 vision camera 串流同時運行的穩定性測試；LED 固定在桶子上 |
| 全員 | 第一次 end-to-end demo（W5 結束）；找 5-10 個同學試丟，紀錄 bug |
| 全員 | 根據 bug 與台詞反饋，做 W6 的修正 |

**Phase 3 出口指標**：丟進去能自動辨識 + 播語音 + 狀態機不會卡死 + 公告螢幕有紀錄。

### Phase 4（W7-W8）：Demo 與報告

| Owner | 任務 |
|---|---|
| Display | 主筆期末報告（基於本 docs/ 內容），轉成 PowerPoint |
| Vision | 補實驗章節：準確率、混淆矩陣、推論時間圖表 |
| Firmware | 補硬體章節：BOM、接線圖、實體照片 |
| 全員 | 拍 demo 影片（30-60 秒，剪輯版）|
| 全員 | W8 期末展演 |

**Phase 4 出口指標**：報告交了、影片拍了、台上講完。

## 5.3 風險清單

| 風險 | 機率 | 影響 | 緩解 |
|---|---|---|---|
| Jetson 環境（JetPack/TensorRT）配置卡關 | 中 | 高 | 於 Phase 1 結束前完成 JetPack 安裝與 YOLOv8n TensorRT 編譯驗證；臨時退路為直接於筆電執行推論 demo |
| L515 camera 取得或 driver 設定卡關 | 中 | 中 | 備案：USB Webcam（RGB only）+ HC-SR04 超音波替代 demo 距離偵測 |
| 錄音時組員不敢罵 | 高 | 中 | 由 display 負責人寫好台詞，組員只負責念；先錄「中度版」再決定要不要加重 |
| 老師質疑「辱罵」教育意義 | 中 | 高 | §4.2 學術論證直接搬到簡報前三頁 |
| 期中報告與期末報告打架 | 高 | 中 | Phase 1 結束（W2）剛好可以交期中提案 |

## 5.4 與其他 repo 的同步機制

| 機制 | 頻率 |
|---|---|
| 每週 standup（15 分鐘）| W1-W8 每週固定一天 |
| Phase 結束 demo（30 分鐘）| W2 / W4 / W6 / W7 |
| `docs/` 內容更新 PR review | 任何人 push 都需 1 人 review |

## 5.5 給組長 / 報告主筆的 next step 建議

1. **本週**：把這份 docs/ 五個檔給組員看，確認沒人對「主打 roast」這件事退縮。
2. **下週**：確認硬體取得（Jetson AGX Orin Nano 已確定；L515 或備案）。
3. **W3 開工前**：跑一次「假動作 demo」——用 mock 資料 + multiprocessing.Queue 把整條 pipeline 走過一次，找出整合風險。
4. **同步問老師**：「我們的 hook 是 humorous negative feedback，學術依據是 Comber & Thieme 2013（aversive affect 設計策略）+ Skurka 2018（幽默降低心理抗拒）+ Trujillo 2021（規範聚焦 nudge 同時引發正負情緒），您覺得 OK 嗎？」——避免到期末才被打槍。
