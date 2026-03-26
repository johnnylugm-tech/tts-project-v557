# CONFIG_RECORDS.md - 配置管理記錄

## 1. 配置項目

### 1.1 軟體組件

| 組件名稱 | 版本 | 存放位置 |
|----------|------|----------|
| presentation_tts.py | 1.0.0 | /src |
| test_presentation_tts.py | 1.0.0 | /tests |

### 1.2 相依套件

| 套件名稱 | 版本需求 |
|----------|----------|
| edge-tts | >= 6.0 |
| pytest | >= 7.0 |

## 2. 變更紀錄

| 變更 ID | 日期 | 描述 |
|---------|------|------|
| C001 | 2026-03-27 | 初始版本 v1.0.0 |

## 3. 建置

```bash
pip install -r requirements.txt
python -m pytest tests/
```

*建立時間: 2026-03-27*
