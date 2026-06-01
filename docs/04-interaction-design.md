# §4 互動與情緒設計

> 為什麼是「辱罵」而不是「鼓勵」？這是設計選擇，不是惡搞。

本章以 v0.3 全自動契約為準：L515 觸發、YOLOv11n binary classification、無使用者按鈕、無蓋子機構。

## 4.1 核心 hook：組員自錄的幽默 roast

**設計命題**：當使用者把垃圾丟錯，垃圾桶會用組員自己的聲音用幽默的方式吐槽他。

這個設計有三個刻意的選擇：

1. **是「同儕的聲音」而不是 TTS** — 製造熟悉感與社交存在感（parasocial）。
2. **是「幽默 roast」而不是「嚴肅警告」** — 降低心理抗拒、提升傳播性。
3. **是「即時觸發」而不是事後通知** — 對齊行為改變最有效的時機。

下面三節依序給出學術論證，最後一節展開實作細節。

## 4.2 行為設計理論支撐

### 4.2.1 Fogg Behavior Model（B = MAT）

Fogg 提出行為改變需三要素同時出現：**動機 (Motivation)**、**能力 (Ability)**、**觸發 (Trigger / Prompt)** [^fogg2009]。

智慧垃圾桶的即時語音回饋，是高效的「Trigger」——**在使用者剛丟錯垃圾的當下提供反饋**，而不是等到下個月看 LINE 環保公告。Comber & Thieme 將 persuasive technology 框架應用在垃圾分類上，論證即時回饋是 sustainable HCI 的核心策略 [^comber2013]。

### 4.2.2 情緒與規範聚焦型 nudge：負向情緒亦是設計工具

Trujillo, Estrada-Mejía & Rosa 2021 年發表於 *PLOS One* 的研究指出：**規範聚焦型 nudge 不僅推動親環境選擇，還會在事後同時引發正向（pride）與負向（guilt、regret）情緒反應**——其中正向情緒被觀察為主要驅力，但**負向情緒同樣是行為改變過程中的真實組成**，並非「只能用鼓勵」[^trujillo2021]。

更直接針對「aversive affect（厭惡 / 不適感）」在永續行為設計上的角色，Comber & Thieme 2013 在 *Personal and Ubiquitous Computing* 提出：persuasive technology 不應只追求愉悅與獎勵，而可有意識地利用 aversive affect（包含羞愧與不適感）作為打破「壞習慣」的設計策略，特別是在垃圾與回收這類已成自動化行為的場域 [^comber2013]。

> 關鍵點：學術文獻**不支持「只有溫柔鼓勵才算教育」**這個直覺。負向情緒（包括幽默包裝下的 shame nudge）是 sustainable HCI 設計工具箱中正當的選項，前提是要設計得當（見 §4.4 倫理）。

### 4.2.3 Humor in PSA：低抗拒、高黏著

Skurka 等人 2018 年發表於 *Journal of Communication* 的對比研究指出：**幽默訴求比恐懼訴求更能降低「心理抗拒 (psychological reactance)」，提升訊息態度與參與度**；恐懼訴求常因焦慮過高反而**降低**行為意圖 [^skurka2018]。

換言之：「被罵但好笑」遠比「被嚴肅警告」更有黏著度。

### 4.2.4 Gamification + Parasocial：情感連結放大效果

Berengueres 等人 2013 年在 ACM/IEEE HRI 發表的 **Emoticon-bin** 實驗顯示：**加入聲音 / 表情的遊戲化垃圾桶能讓回收率提升 3 倍** [^berengueres2013]。

而 Horton & Wohl 1956 年提出的 **Parasocial Interaction** 經典理論告訴我們：**當聲音是熟悉、有個性的人，使用者會產生「人際感」**，遠勝陌生機器音的冷淡通知 [^horton1956]。

組員自己的聲音 = 校園內的社交存在感 = 高參與。這是 emoticon-bin 「3 倍」效應的個人化加強版。

### 4.2.5 Elevator Pitch（給老師 / 評審）

> 我們的智慧垃圾桶不是要羞辱使用者，而是用 **Fogg 模型的「即時 Trigger」** + **Comber & Thieme 的「aversive affect 設計策略」** + **Skurka 的「幽默降低心理抗拒」** + **同儕聲音的「parasocial 黏著感」**，把分類錯誤的瞬間變成一次記得住的學習事件。學術證據顯示：負向情緒搭配幽默包裝可有效推動行為改變，且 emoticon-bin 已實證可讓回收率達 **3 倍（＝＋200%）**——我們做的，是把這套設計**本土化、人格化**。

## 4.3 互動腳本設計

### 4.3.1 狀態流（state machine）

全自動化流程，無使用者按鈕、無蓋子機構：

```
       (人離開超過 5 秒 or cooldown 結束)
   ┌──────────────────────────────────┐
   ▼                                  │
 [idle] ──距離<30cm──► [detecting] ──物件進入──► [recognizing]
                                                      │
                                          ┌───────────┴───────────┐
                                          │                       │
                                     conf ≥ 0.5              conf < 0.5
                                          │                       │
                                          ▼                       ▼
                                     [roasting/              [self_mock]
                                      accepting]                  │
                                          │                       │
                                          ▼                       ▼
                                       [cooldown] ◄───────────────┘
                                          │
                                          ▼
                                       (回到 idle)
```

> **移除的狀態**：`asking`（使用者確認）、`opening_lid`（蓋子）。全流程零手動操作。

### 4.3.2 Roast 語音內容分級

每一類丟對 / 丟錯各準備 **3-5 句**，避免短時間內聽到重複（重複 = 失去笑點）：

| 情境 | Roast 等級 | 範例風格（待組員自己改寫）|
|---|---|---|
| **正確分類（accept）** | 輕度肯定（不要太熱情，否則破壞反差） | 「⋯⋯算你會。」「這次給你 80 分。」 |
| **錯誤分類（reject）** | 中度吐槽 | 「這是塑膠不是紙，你眼睛被蛤蜊夾到了？」「保麗龍丟可回收，你以為這裡是樂高展？」 |
| **同 session 連續 2 次 reject**（間隔 < 30 秒） | 重度 roast | 「我已經第二次告訴你這是塑膠了，要不要去眼科？」 |
| **一次丟多個物件** | 中重度吐槽 | 「一次丟一堆是在趕投胎？分一下好嗎。」 |
| **conf 太低（< 0.5）** | 自嘲 | 「我看不太出來欸，可能是我老花。」 |
| **長時間沒人** | 寂寞 / 反差 | 「⋯⋯有人嗎⋯⋯。」 |

### 4.3.2.1 音效設計（戲劇張力）

不做蓋子機構，改以**音效**製造戲劇效果：辨識完成後先播一個短音效（如「叮」或吸氣聲），停頓約 0.5 秒，再播 roast 語音。這個短暫沉默創造「法官敲槌前的停頓感」，讓 roast 的衝擊力更強，且零機構成本。

> **內容創作守則**（必須寫進 README，避免錄音時失控）：
>
> 1. 不可涉及性別、種族、外貌、身材、性向等保護類屬性。
> 2. 不可使用具攻擊性的髒話（國中生等級的吐槽 = OK；F 開頭詞 = NO）。
> 3. 預設使用對象是「同學 / 同事」，不是「想被惡搞的對象」。
> 4. 一句話控制在 **8 秒以內**——超過會讓使用者下意識想關掉。
> 5. 每位組員至少錄 **5 句**，並對自己的聲音被使用簽署同意。

### 4.3.3 Display 設計

Display 有兩個角色：**使用者端公告螢幕** 與 **Admin 控制面板**。

#### 使用者端公告螢幕（面向垃圾桶使用者）

```
┌─────────────────────────────────────┐
│                                     │
│   📊 今日統計                       │
│   正確投入：47 次 ｜ 被抓到亂丟：12 次│
│                                     │
│   🐢 本月已救活 2.7 隻虛擬海龜      │
│                                     │
│   ─── 最近犯案紀錄 ───              │
│   14:32  [照片] 寶特瓶 → reject     │
│   14:28  [照片] 塑膠袋 → reject     │
│   14:15  [照片] 衛生紙 → accept ✓   │
│                                     │
└─────────────────────────────────────┘
```

設計重點：
- **無按鈕** — 純資訊顯示，使用者不需要操作。
- **「犯案紀錄」** — 每次 reject 事件自動記錄 L515 快照 + 時間 + 辨識結果，存為本機 JSON log + 照片。不上雲、不做人臉辨識。
- **session-based 連續犯錯** — 前後兩次 reject 間隔 < 30 秒視為同一 session，觸發加重版 roast。
- **「救活 N 隻虛擬海龜」** — 把累積正確分類數轉成具象指標，呼應 §1 的海龜符號。

#### Admin 控制面板（面向開發者 / 管理者）

```
┌─────────────────────────────────────┐
│  [Admin Panel]                      │
│                                     │
│  系統狀態：● 運行中                  │
│  L515：● 連線  │  模型：YOLOv11n ✓   │
│                                     │
│  Confidence 閾值：[0.5] (可調)      │
│  Roast 音量：[████████░░] 80%       │
│                                     │
│  今日事件 log（可匯出 CSV）          │
│  ┌──────────────────────────────┐   │
│  │ 14:32 reject conf=0.91 1obj │   │
│  │ 14:28 reject conf=0.87 1obj │   │
│  │ 14:15 accept conf=0.82 1obj │   │
│  └──────────────────────────────┘   │
│                                     │
└─────────────────────────────────────┘
```

Admin 面板用途：demo 時展示系統後台、調整參數、匯出紀錄。

## 4.4 倫理與風險

| 風險 | 緩解 |
|---|---|
| 有人覺得被冒犯 | 內容守則（4.3.2）；admin 面板可調 roast 音量或靜音 |
| 兒童使用場景 | 不部署在國小以下場域；roast 強度可調 |
| 重複聽久了不好笑 | 每月更新台詞庫；3-5 句一組隨機抽 |
| 老師質疑教育意義 | §4.2 的學術論證可直接搬到簡報 |
| 組員不想自己的聲音被使用 | 簽署使用同意書；隨時可撤回 |
| 犯案紀錄照片的隱私疑慮 | 照片僅存本機、不上雲、不做人臉辨識；僅記錄物件而非人臉 |

## 4.5 成功指標

供 §5 報告中作為評估用：

| 指標 | 量化方式 | 目標 |
|---|---|---|
| 辨識準確率 | 測試集 top-1 acc | ≥ 85% |
| 端到端延遲 | 從丟入到語音播放 | ≤ 2.5 秒 |
| 全自動化 | 全流程無使用者手動操作 | 零按鈕、零確認步驟 |
| 使用者笑出來的次數 | demo 影片標註 | 每 10 次互動至少 5 次有笑聲 |

下一章（§5 分工與時程）給出 1-2 個月怎麼把這套東西做出來。

---

## 引用

[^fogg2009]: Fogg, B. J. (2009). *A behavior model for persuasive design*. **Persuasive '09**. DOI: [10.1145/1541948.1541999](https://dl.acm.org/doi/10.1145/1541948.1541999)
[^comber2013]: Comber, R. & Thieme, A. (2013). *Designing beyond habit: Opening space for improved recycling and food waste behaviors through processes of persuasion, social influence and aversive affect*. **Personal and Ubiquitous Computing**.
[^trujillo2021]: Trujillo, C. A., Estrada-Mejía, C. & Rosa, J. A. (2021). *Norm-focused nudges influence pro-environmental choices and moderate post-choice emotional responses*. **PLOS One**, 16(3): e0247519. [連結](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0247519)
[^skurka2018]: Skurka, C. et al. (2018). *Pathways of Influence in Emotional Appeals: Benefits and Tradeoffs of Using Fear or Humor to Promote Climate Change-Related Intentions and Risk Perceptions*. **Journal of Communication**, 68(1), 169–193. [連結](https://academic.oup.com/joc/article/68/1/169/4958964)
[^berengueres2013]: Berengueres, J. et al. (2013). *Gamification of a Recycle Bin with Emoticons*. **ACM/IEEE HRI**. [連結](https://www.academia.edu/4873003/Gamification_of_a_Recycle_Bin_with_Emoticons)
[^horton1956]: Horton, D. & Wohl, R. R. (1956). *Mass Communication and Para-Social Interaction: Observations on Intimacy at a Distance*. **Psychiatry**, 19(3), 215–229.
