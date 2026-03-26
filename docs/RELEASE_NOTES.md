# RELEASE_NOTES.md

## v1.0.0 (2026-03-27)

### 新功能
- REQ-001: edge-tts 非同步語音合成
- REQ-002: 自動文本分段（800字）
- REQ-003: 錯誤重試機制（3次）
- REQ-004: 參數控制（rate/volume）
- REQ-005: 進度回調
- REQ-006: 檔案合併輸出
- REQ-007: 音色選擇

### 技術規格
- Python 3.8+
- edge-tts >= 6.0
- 錯誤處理: L1-L6 分類
- 符合 ASPICE 標準

### 路徑
- Source: src/presentation_tts.py
- Tests: tests/test_presentation_tts.py
