# 跨 Repo API 契約

> 進行中 — 通訊協定與 payload 細節待三個 repo 開工後正式定稿。

## 系統流程

```
┌─────────────────┐
│    firmware     │  紅外線偵測使用者靠近(距離 < 閾值)
└────────┬────────┘
         │ ① trigger 訊號
         ▼
┌─────────────────┐
│     vision      │  攝影機拍照 → 模型推論
└────────┬────────┘
         │ ② 推論結果 {class, confidence}
         ▼
┌─────────────────┐
│     display     │  渲染 UI、播放聲光、等待使用者確認
└────────┬────────┘
         │ ③ 使用者選擇(丟入 / 取消)
         ▼
┌─────────────────┐
│    firmware     │  開蓋 / 蜂鳴器 / LED 對應動作
└─────────────────┘
```

## 介面草案

### ① firmware → vision(觸發推論)

| 項目 | 草案 |
|---|---|
| 通訊協定 | TBD(MQTT / HTTP webhook / 串口擇一) |
| 事件名 | `user_detected` |
| Payload | `{ "event": "user_detected", "distance_cm": <number>, "ts": <iso8601> }` |

### ② vision → display(推論結果)

| 項目 | 草案 |
|---|---|
| 通訊協定 | TBD(REST / WebSocket) |
| 事件名 | `recognition_result` |
| Payload | `{ "class": <string>, "confidence": <0-1>, "ts": <iso8601> }` |

### ③ display → firmware(使用者確認)

| 項目 | 草案 |
|---|---|
| 通訊協定 | TBD |
| 事件名 | `user_action` |
| Payload | `{ "action": "open_lid" \| "cancel", "ts": <iso8601> }` |

## 待決定事項

- [ ] 統一通訊匯流(全用 MQTT?還是 vision 走 HTTP、firmware 走串口?)
- [ ] 垃圾分類的 class 集合(只有「可回收 / 不可回收」?還是更細的多類?)
- [ ] confidence 閾值低於多少要走 fallback(例如要使用者手動選類)
- [ ] 整體事件 timestamp 是否需要對時(NTP)
