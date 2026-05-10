# 文件中心

本目錄存放 **跨 repo 的整合性文件**。各子 repo 的技術細節留在各自 repo 內,這裡只保留共識與契約。

## 索引

- [api-contract.md](./api-contract.md) — 跨 repo API 契約(`vision` ↔ `firmware` ↔ `display`)

## 原則

- 任何會被多個 repo 同時讀寫的「介面」、「協定」、「事件」都寫在這裡
- 子 repo 的內部實作不寫進來
- 文件以「契約 / 規格」為主,而非教學或日誌
