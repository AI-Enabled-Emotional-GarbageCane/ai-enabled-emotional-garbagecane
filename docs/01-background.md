# §1 問題背景

> 為什麼一個會辱罵你的垃圾桶值得做？

## 1.1 海洋塑膠垃圾的規模

陸源塑膠廢棄物大量流入海洋，已是被學界量化的事實。Jambeck 等人 2015 年發表於 *Science* 的研究估計，2010 年 192 個沿海國家共產生約 **2.75 億公噸**塑膠廢棄物，其中 **480 萬至 1,270 萬公噸**進入海洋；若管理方式不變，到 2025 年累積排入量將再增加一個數量級 [^jambeck2015]。Meijer 等人 2021 年於 *Science Advances* 進一步指出，每年約 **0.8–2.7 百萬公噸**塑膠經由河川進入海洋，且 **1,000 多條河川**就貢獻了全球 80% 的河源塑膠排放 [^meijer2021]。

換言之，海洋塑膠不是抽象議題：它是一個來源高度集中、可在源頭攔截的工程問題。

## 1.2 塑膠吸管：重量很小，象徵很大

從重量占比看，吸管在海洋塑膠中**僅約 1%**，常被反塑膠運動的批評者拿來說「不重要」。但從**符號動員**的角度，它的角色完全不同：

- Ocean Conservancy 的國際淨灘報告中，吸管/攪拌棒長年位列前 10 大廢棄物，單一年度志工撿到約 **94 萬支** [^ocean2020]。
- 2015 年 Christine Figgener 在哥斯大黎加拍攝的「橄欖綠蠵龜鼻孔吸管」影片，累計超過 **1 億次觀看**，直接催生 Starbucks、Disney 等企業的禁吸管政策 [^figgener]。

**這個符號性正是本專案的命名動機**：「海龜每天都在被吸管攻擊」不是字面陳述，而是借用一個高擴散性的視覺意象，去驅動行為改變。情緒回饋與符號性傷害在傳播學上是同一條光譜——這也預告了 §4 互動設計為什麼選「幽默 roast」而非「冷冰冰的辨識正確 / 錯誤」。

## 1.3 台灣回收現況：表面光鮮，背後有缺口

台灣的一般廢棄物回收率長期維持在約 **55–58%**，被多國媒體列為全球最高之一 [^moenv-recycle]。但綠色和平 2024 年的報告指出，這個高比率背後存在大量「暫置垃圾山」未真正進入再製流程，回收體系的後段壓力已顯現 [^greenpeace2024]。

一次性塑膠用量也持續上升：

- 台灣每年使用約 **30 億支**塑膠吸管（環團估算引述）[^taiwannews]。
- 環境資訊中心引用經濟部產銷數據，環保署列管之四大類一次性塑膠十年總用量**反增 22.8%**——限塑十年並未真正壓低使用 [^einfo]。

**家戶端的「分類錯誤率」目前找不到環境部統一公告的單一可信數字**——本報告在此明確標註不捏造，改以下方國際 MRF（物料回收廠）數據佐證。

## 1.4 為什麼源頭分類重要：後段成本是放大鏡

美國回收業界與 MRF（物料回收廠）的營運報告長期指出 [^wm2020][^mrf2024]：

- 單流回收（single-stream）的污染率在大型業者約為 **17–25%**（Waste Management 2020 年報告稱已從 25% 降至 17%），部分區域更高。
- 污染顯著推升 MRF 的處理與運輸成本（業界估算為數億美元等級），並可能因入料品質過差而導致**整車回收物被改送掩埋場**。

> 註：US EPA 2024 年發佈的回收體系財務評估報告 [^epa2024]，主軸為基建投資需求（365–434 億美元），而非家戶污染成本本身；上述「整車作廢」的具體門檻在學術文獻中未見統一數字，本報告以「業界估算」描述以避免誤引。

**這個放大效應正是「在投入瞬間擋下錯誤」的價值論述**：源頭一支吸管的歸類差異，會在後段被放大成整車作廢的風險。智慧垃圾桶的存在意義不是取代後段工人，而是把「可避免的污染」攔在第一公尺。

## 1.5 本專題的問題切入點

綜合以上：

| 觀察 | 對本專題的意涵 |
|---|---|
| 海洋塑膠是高集中度、可在源頭攔截的工程問題 | AI 影像辨識值得做 |
| 吸管/海龜是高擴散性符號 | 「情緒回饋」這條設計路線有傳播學支撐 |
| 台灣回收率高但仍有家戶端缺口 | 校園/公共場域是好的部署場景 |
| 後段污染放大效應強 | 「在投入瞬間擋下」比事後更有效 |

下一章將檢視既有方案（§2 相關工作），論證為什麼「會辱罵你的垃圾桶」這條路線目前是空白。

---

## 引用

[^jambeck2015]: Jambeck, J. R. et al. (2015). *Plastic waste inputs from land into the ocean*. **Science**, 347(6223), 768–771. DOI: [10.1126/science.1260352](https://www.science.org/doi/10.1126/science.1260352)
[^meijer2021]: Meijer, L. J. J. et al. (2021). *More than 1000 rivers account for 80% of global riverine plastic emissions into the ocean*. **Science Advances**, 7(18). [PMC8087412](https://pmc.ncbi.nlm.nih.gov/articles/PMC8087412/)
[^ocean2020]: Ocean Conservancy (2020). *International Coastal Cleanup 2020 Report*. [新聞稿](https://oceanconservancy.org/newsroom/press-release/2020/09/08/food-wrappers-top-beach-trash/)
[^figgener]: Figgener, C. (2015). 海龜鼻孔吸管事件背景。[Wikipedia](https://en.wikipedia.org/wiki/Christine_Figgener)；[Tico Times 報導](https://ticotimes.net/2015/08/18/watch-researchers-remove-plastic-straw-from-sea-turtles-nose)
[^moenv-recycle]: 環境部環境資料開放平臺（一般廢棄物回收率指標）。[資料連結](https://data.moenv.gov.tw/dataset/detail/STAT_P_46)
[^greenpeace2024]: 綠色和平（2024）。*垃圾山遍布全臺！揭露高回收率背後的錯誤政策*。[文章](https://www.greenpeace.org/taiwan/update/40591/)
[^taiwannews]: Taiwan News。*台灣年耗 30 億根塑膠吸管*。[報導](https://www.taiwannews.com.tw/ch/news/3388143)
[^einfo]: 環境資訊中心。*限塑 10 年政策失靈？一次性塑膠用量增 22.8%*。[文章](https://e-info.org.tw/node/227866)
[^epa2024]: U.S. EPA (2024). *An Assessment of the U.S. Recycling System: Financial Estimates*. [PDF](https://www.epa.gov/system/files/documents/2024-12/financial_assessment_of_us_recycling_system_infrastructure.pdf)
[^mrf2024]: *Material Recovery Facilities (MRFs) in the United States: Operations, revenue, and the impact of scale* (2024). **Waste Management**. [連結](https://www.sciencedirect.com/science/article/abs/pii/S0956053X24006408)
[^wm2020]: Waste Management（業界報告引述）— 單流回收污染率由約 25% 降至 17%。可參考 [Roadrunner: The Cost of Recycling Contamination](https://www.roadrunnerwm.com/blog/the-cost-of-recycling-contamination) 與相關產業資料。
