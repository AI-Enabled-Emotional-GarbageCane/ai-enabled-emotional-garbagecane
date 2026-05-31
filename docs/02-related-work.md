# §2 相關工作 / 競品分析

> 既有方案做了什麼？沒做什麼？我們的空白在哪？

## 2.1 商業產品

| 產品 | 國家 | 做什麼 | 技術 | 部署場域 | 來源 |
|---|---|---|---|---|---|
| **Bin-e** | 波蘭 | 自動辨識並分流四類回收物，內建壓縮機制，雲端後台監控 | AI 影像辨識，宣稱 92%+ 準確率；可外接 50 吋螢幕播放教育 / 廣告內容 | B2B：辦公室、購物中心 | [bine.world](https://www.bine.world/) ／ [Solar Impulse 認證](https://solarimpulse.com/solutions-explorer/bin-e-waste-management-system) |
| **CleanRobotics TrashBot** | 美國 | 投入口辨識後機械手臂分流到內部正確桶 | 電腦視覺＋ML，宣稱 90–95% 準確率（隨部署環境變動）；LoRa 連線；大螢幕顯示 | 機場、醫院、體育館 | [cleanrobotics.com/trashbot](https://cleanrobotics.com/trashbot/) ／ [Recycling Today](https://www.recyclingtoday.com/news/clean-robotics-announces-features-for-trash-bot-scrap-sorting-bin/) |
| **Intuitive AI – Oscar Sort** | 加拿大 | 加裝在現有垃圾桶旁，用螢幕指示丟哪一桶 | 視覺辨識，現場分類準確率提升至約 96% | 舊金山 Ferry Building、Tim Hortons、JPMorgan、Nike、TD Garden | [intuitiveai.ca/oscar-sort](https://intuitiveai.ca/oscar-sort) ／ [Axios 報導](https://www.axios.com/2023/06/05/ai-recycling-garbage-sorting-trash-oscar-intuitive) |

> **價格說明**：三家皆採 B2B 報價／訂閱制，公開資料無確切數字，故未列價格欄位以避免捏造。

## 2.2 學術 / 學生專案

| 專案 | 模型 | 硬體 | 報告準確率 | 來源 |
|---|---|---|---|---|
| **WasteNet**（學術） | CNN | Jetson Nano | 6 類分類 97% | [arXiv 2210.00448](https://arxiv.org/pdf/2210.00448) |
| **YOLO-Based Recyclables**（MDPI Electronics, 2022） | YOLOv4 系列 | Raspberry Pi | 最佳環境 91%，部署到 Pi 後降至 75% | [MDPI](https://www.mdpi.com/2079-9292/11/9/1323) |
| **Plastic Waste Detection YOLOv5s on Pi 4**（GitHub） | YOLOv5s | Raspberry Pi 4 | 6 類，~2 FPS | [GitHub – has-bi](https://github.com/has-bi/Plastic-Waste-Detection-YOLOv5s-Raspberry-Pi4) |
| **SMART-BIN**（GitHub） | CNN, 200 epochs | — | 二分類 89% | [GitHub – nsankethreddy](https://github.com/nsankethreddy/SMART-BIN) |

## 2.3 缺口檢視：情緒回饋是空白

逐一檢視上述 7 個方案：**沒有任何一個既有方案使用「同儕個人化語音」「幽默 roast」「負向情緒 nudge」作為回饋機制**。

- **商業產品**（Bin-e / TrashBot / Oscar）一致採用「中性指示 + 教育內容 + 正向鼓勵」路線。
- **學術／GitHub 專案**普遍止步於辨識準確率，連語音輸出都很少做。
- 唯一沾到邊的是 Waste Management 公司一支電視廣告把垃圾桶擬人化講笑話 [^ispot]，但那是行銷影片，不是產品。

## 2.4 差異化定位

```
辨識準確率                                互動／情緒層
[                          擁擠的紅海                          ]
[ 90%-97%                                                      ]
   ▲
   │
   │   ◆ Bin-e / TrashBot / Oscar
   │   ◆ WasteNet / YOLO PoC
   │
   └────────────────────────────────────────────────────────────►
                                                                ▲
                                                                │
                                                          ★ 本專題
                                                       「會辱罵你的垃圾桶」
```

**核心 insight**：辨識準確率這條路線已高度擁擠（90–97%），再往上做邊際效益低。本專題真正的空白是**互動層／情緒層**：把垃圾桶從「沉默的分類器」轉成「會吐槽你的同學」，用組員自錄的辱罵語音做個人化負向 nudge，結合幽默化解尷尬。

這條路在商業產品（皆為正向 UX）與學術文獻（多停在分類精度）都尚未被佔領，可作為本期末專題的核心差異點與簡報主軸。

下一章（§3 系統設計）會展開技術選型，下下章（§4 互動設計）會論證為什麼「辱罵」不是隨便的設計，而是有行為設計理論支撐的選擇。

---

## 引用

[^ispot]: Waste Management（廣告影片）。*Joke*. [iSpot 連結](https://www.ispot.tv/ad/AO_A/waste-management-joke)
