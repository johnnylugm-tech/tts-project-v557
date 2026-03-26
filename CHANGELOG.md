# CHANGELOG.md

## [1.0.0] - 2026-03-27

### Added
- REQ-001: edge-tts 非同步語音合成
- REQ-002: 自動文本分段（800字）
- REQ-003: 錯誤重試機制（3次）
- REQ-004: 參數控制（rate/volume）
- REQ-005: 進度回調
- REQ-006: 檔案合併輸出
- REQ-007: 音色選擇

### Documentation
- SRS_TEMPLATE.md (P1)
- SAD_TEMPLATE.md (P2)
- TEST_PLAN_TEMPLATE.md (P4)
- QUALITY_REPORT_TEMPLATE.md (P6)
- RISK_ASSESSMENT_TEMPLATE.md (P7)
- RELEASE_NOTES.md (P5)

### Technical
- Python 3.8+
- edge-tts >= 6.0
- L1-L6 錯誤處理
- 符合 ASPICE 標準