# SAD - Software Architecture Design
## 基於 edge-tts 之高品質簡報配音系統

---

## 1. 概述 (Overview)

### 1.1 目的
定義系統的軟體架構設計，確保滿足 SRS 中所有需求。

### 1.2 設計原則
- **單一職責**: 每個模組只做一件事
- **依賴注入**: 使用構造函數注入依賴
- **錯誤分類**: L1-L6 錯誤處理（參照 Constitution）

---

## 2. 系統架構圖 (System Architecture)

```
┌─────────────────────────────────────────────────────────────┐
│                      PresentationTTS                         │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐    │
│  │  初始化模組  │  │  文本處理模組 │  │   合成引擎模組   │    │
│  │  __init__   │→ │ _preprocess_ │→ │ _synthesize_    │    │
│  │             │  │    text()    │  │    chunk()      │    │
│  └─────────────┘  └─────────────┘  └─────────────────┘    │
│         ↓                ↓                   ↓              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              錯誤處理模組 (Fault Tolerant)             │   │
│  │  L1-L6 分類 / 重試機制 / 熔斷器                        │   │
│  └─────────────────────────────────────────────────────┘   │
│                              ↓                               │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              檔案輸出模組 (File Output)               │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. 模組設計 (Module Design)

### 3.1 PresentationTTS 類

```python
class PresentationTTS:
    """高品質簡報配音引擎 - 基於 edge-tts"""
    
    def __init__(
        self,
        voice: str = "zh-TW-HsiaoHsiaoNeural",
        rate: str = "+0%",
        volume: str = "+0%"
    ) -> None:
        """
        初始化合成引擎
        對應 REQ-004, REQ-007
        """
        self.voice = voice
        self.rate = rate
        self.volume = volume
        self.max_chunk_size = 800  # 對應 REQ-002
    
    def _preprocess_text(self, text: str) -> List[str]:
        """
        自動分段模組
        對應 REQ-002
        """
        pass
    
    async def _synthesize_chunk(
        self,
        chunk: str,
        index: int,
        output_dir: str
    ) -> Optional[str]:
        """
        非同步合成模組
        對應 REQ-001
        """
        pass
    
    async def synthesize(
        self,
        text: str,
        output_dir: str,
        progress_callback: Callable = None
    ) -> List[str]:
        """
        主流程
        對應 REQ-005, REQ-006
        """
        pass
```

---

## 4. 錯誤處理架構 (Error Handling Architecture)

### 4.1 錯誤分類（L1-L6）

```
┌────────────────────────────────────────────────────────────┐
│                     錯誤處理分層                              │
├──────────┬─────────────────────────────────────────────────┤
│   L1     │ 配置錯誤 → 不允許啟動                             │
│   L2     │ API 錯誤 → 重試 3 次 + Fallback                  │
│   L3     │ 業務錯誤 → 記錄日誌 + 降級                         │
│   L4     │ 預期異常 → 記錄 + 忽略                            │
│   L5     │ 環境錯誤 → 告警 + 人工介入                        │
│   L6     │ 災難錯誤 → 災難復原模式                            │
└──────────┴─────────────────────────────────────────────────┘
```

### 4.2 熔斷器配置

```python
CIRCUIT_BREAKER_THRESHOLD = {
    "failure_count": 5,
    "timeout_seconds": 60,
    "half_open_retries": 3
}
```

---

## 5. 數據流 (Data Flow)

```
輸入文本 → [分段] → [非同步合成] → [合併] → MP3 輸出
              ↓            ↓            ↓
           REQ-002     REQ-001     REQ-006
```

---

## 6. 外部依賴

| 依賴 | 版本 | 用途 |
|------|------|------|
| edge-tts | >= 6.0 | 語音合成 |
| asyncio | 内置 | 非同步處理 |
| typing | 内置 | 型別標註 |

---

## 7. Phase 產物引用

- **P1 引用**: SRS_TEMPLATE.md 中的所有 REQ-ID
- **驗證**: 每個模組都有對應的 REQ-ID 標註

---

## 8. 驗收標準

- [ ] 架構圖清晰表達模組關係
- [ ] 每個 REQ-ID 都有對應模組
- [ ] 錯誤處理 L1-L6 完整
- [ ] 依賴關係無循環

---

*建立日期：2026-03-27*
*版本：1.0.0*
*符合 ASPICE SWE.5 標準*
*引用 P1 產物: SRS_TEMPLATE.md*