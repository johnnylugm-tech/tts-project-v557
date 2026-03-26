# SRS - Software Requirements Specification
## 基於 edge-tts 之高品質簡報配音系統

---

## 1. 簡介 (Introduction)

### 1.1 目的
本文件定義基於 Microsoft Edge TTS 技術的簡報配音系統的軟體需求规格。

### 1.2 範圍
- 技術：edge-tts（非同步 WebSocket 流式傳輸）
- 目標：台灣市場簡報配音
- 音色：zh-TW-HsiaoHsiaoNeural

---

## 2. 功能需求 (Functional Requirements)

| REQ-ID | 需求名稱 | 描述 | 優先級 |
|--------|----------|------|--------|
| REQ-001 | 非同步語音合成 | 透過 edge-tts 進行 WebSocket 非同步語音合成 | P0 |
| REQ-002 | 自動文本分段 | 根據句號、問號、驚嘆號、換行符自動分段，每段 <= 800 字 | P0 |
| REQ-003 | 錯誤重試機制 | API 錯誤時自動重試 3 次，間隔遞增 | P0 |
| REQ-004 | 參數控制 | 支援 rate（語速）和 volume（音量）參數調整 | P0 |
| REQ-005 | 進度回調 | 合成過程中提供 Progress Callback | P1 |
| REQ-006 | 檔案合併輸出 | 將多個 MP3 片段合併為單一輸出檔案 | P1 |
| REQ-007 | 音色選擇 | 支援選擇不同 voice（預設 HsiaoHsiaoNeural） | P2 |

---

## 3. 非功能需求 (Non-Functional Requirements)

| 維度 | 目標 | 說明 |
|------|------|------|
| **正確性** | 100% | 所有功能必須完全符合本規格 |
| **安全性** | 100% | 無敏感資訊明文、API 有錯誤處理 |
| **可維護性** | >70% | 圈複雜度 <=10、函數 <=50 行 |
| **效能** | >=80% | 單次合成回應時間合理 |

---

## 4. 系統架構 (System Architecture)

### 4.1 模組設計
```
PresentationTTS
├── __init__()           # 初始化（voice, rate, volume）
├── _preprocess_text()   # 文本分段模組
├── _synthesize_chunk()  # 非同步合成模組
└── synthesize()         # 主流程（分段→合成→合併）
```

### 4.2 通訊協議
- WebSocket 非同步流式傳輸
- Single API 請求建議不超過 20,000 字

---

## 5. 錯誤處理 (Error Handling)

| 等級 | 類型 | 處理方式 |
|------|------|----------|
| L1 | 配置錯誤 | 不允許啟動，拋出异常 |
| L2 | API 錯誤（Timeout、Rate Limit） | 重試 3 次 + Fallback |
| L3 | 業務邏輯錯誤 | 記錄日誌 + 降級服務 |
| L4 | 預期異常（網路波動） | 記錄 + 忽略 |
| L5 | 環境錯誤（磁碟滿） | 告警 + 人工介入 |
| L6 | 災難錯誤 | 進入災難復原模式 |

---

## 6. 驗收標準 (Acceptance Criteria)

- [ ] REQ-001: 可透過 edge-tts 合成語音
- [ ] REQ-002: 文本自動分段正確，單段不超過 800 字
- [ ] REQ-003: API 錯誤時自動重試 3 次
- [ ] REQ-004: rate 和 volume 參數可調整
- [ ] REQ-005: 合成過程有進度回調
- [ ] REQ-006: 多檔案可合併為單一 MP3
- [ ] REQ-007: 可選擇不同 voice

---

## 7. 追溯矩陣 (Traceability Matrix)

| REQ-ID | 對應 Phase | 對應模組 | 狀態 |
|--------|------------|----------|------|
| REQ-001 | P3 | _synthesize_chunk | Pending |
| REQ-002 | P3 | _preprocess_text | Pending |
| REQ-003 | P3 | fault_tolerant | Pending |
| REQ-004 | P3 | __init__ | Pending |
| REQ-005 | P3 | synthesize | Pending |
| REQ-006 | P3 | synthesize | Pending |
| REQ-007 | P3 | __init__ | Pending |

---

*建立日期：2026-03-27*
*版本：1.0.0*
*符合 ASPICE SWE.1 標準*