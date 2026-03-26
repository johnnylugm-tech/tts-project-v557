"""
單元測試 - PresentationTTS
==========================

測試覆蓋對應需求: REQ-001, REQ-002, REQ-003, REQ-004, REQ-005, REQ-006, REQ-007

測試策略: 測試金字塔
- 單元測試: 70%
- 整合測試: 20%
- E2E: 10%
"""

import pytest
import asyncio
import os
import tempfile
import shutil
from unittest.mock import Mock, patch, AsyncMock

from presentation_tts import (
    PresentationTTS,
    TTSError,
    ErrorLevel,
    SynthesizeResult,
    quick_synthesize
)


# ============================================================================
# REQ-004: 參數控制測試
# ============================================================================

class TestInit:
    """測試初始化 - REQ-004, REQ-007"""
    
    def test_default_values(self):
        """測試預設值"""
        tts = PresentationTTS()
        assert tts.voice == "zh-TW-HsiaoHsiaoNeural"
        assert tts.rate == "+0%"
        assert tts.volume == "+0%"
        assert tts.max_chunk_size == 800
        assert tts.max_retries == 3
    
    def test_custom_values(self):
        """測試自訂值"""
        tts = PresentationTTS(
            voice="zh-TW-YunJingNeural",
            rate="+10%",
            volume="+20%",
            max_chunk_size=500,
            max_retries=5
        )
        assert tts.voice == "zh-TW-YunJingNeural"
        assert tts.rate == "+10%"
        assert tts.volume == "+20%"
        assert tts.max_chunk_size == 500
        assert tts.max_retries == 5
    
    def test_l1_config_error_empty_voice(self):
        """L1: 配置錯誤 - 空 voice"""
        with pytest.raises(TTSError) as exc_info:
            PresentationTTS(voice="")
        assert exc_info.value.level == ErrorLevel.L1_CONFIG
    
    def test_l1_config_error_invalid_chunk_size(self):
        """L1: 配置錯誤 - invalid chunk size"""
        with pytest.raises(TTSError) as exc_info:
            PresentationTTS(max_chunk_size=0)
        assert exc_info.value.level == ErrorLevel.L1_CONFIG


# ============================================================================
# REQ-002: 自動文本分段測試
# ============================================================================

class TestPreprocessText:
    """測試文本分段 - REQ-002"""
    
    def test_empty_text(self):
        """空文本"""
        tts = PresentationTTS()
        result = tts._preprocess_text("")
        assert result == []
    
    def test_single_sentence(self):
        """單一句子"""
        tts = PresentationTTS()
        result = tts._preprocess_text("這是一個測試")
        assert len(result) == 1
    
    def test_multiple_sentences(self):
        """多個句子 - 按句號分割"""
        tts = PresentationTTS()
        text = "第一句。第二句。第三句。"
        result = tts._preprocess_text(text)
        assert len(result) == 3
    
    def test_question_mark(self):
        """問號分割"""
        tts = PresentationTTS()
        text = "這是問題嗎？這是回答。"
        result = tts._preprocess_text(text)
        assert len(result) == 2
    
    def test_exclamation_mark(self):
        """驚嘆號分割"""
        tts = PresentationTTS()
        text = "太棒了！這是驚嘆。"
        result = tts._preprocess_text(text)
        assert len(result) == 2
    
    def test_newline_split(self):
        """換行符分割"""
        tts = PresentationTTS()
        text = "第一行\n第二行\n第三行"
        result = tts._preprocess_text(text)
        assert len(result) == 3
    
    def test_chunk_size_limit(self):
        """段落大小限制"""
        tts = PresentationTTS(max_chunk_size=10)
        text = "這是一個很長的文本需要被分段處理"
        result = tts._preprocess_text(text)
        for chunk in result:
            assert len(chunk) <= 10


# ============================================================================
# REQ-001: 非同步合成測試
# ============================================================================

class TestSynthesizeChunk:
    """測試非同步合成 - REQ-001"""
    
    @pytest.mark.asyncio
    async def test_synthesize_chunk_success(self):
        """成功合成"""
        tts = PresentationTTS()
        
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch('edge_tts.Communicate') as mock_communicate:
                mock_instance = AsyncMock()
                mock_instance.save = AsyncMock()
                mock_communicate.return_value = mock_instance
                
                result = await tts._synthesize_chunk("測試", 0, tmpdir)
                assert result is not None
    
    @pytest.mark.asyncio
    async def test_synthesize_chunk_retry(self):
        """重試機制 - REQ-003"""
        tts = PresentationTTS(max_retries=3)
        
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch('edge_tts.Communicate') as mock_communicate:
                mock_instance = Mock()
                mock_instance.save = AsyncMock(side_effect=[
                    Exception("Network error"),
                    Exception("Network error"),
                    None
                ])
                mock_communicate.return_value = mock_instance
                
                result = await tts._synthesize_chunk("測試", 0, tmpdir)
                assert result is not None


# ============================================================================
# REQ-005: 進度回調測試
# ============================================================================

class TestProgressCallback:
    """測試進度回調 - REQ-005"""
    
    @pytest.mark.asyncio
    async def test_progress_callback_called(self):
        """進度回調被調用"""
        tts = PresentationTTS()
        
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch('edge_tts.Communicate') as mock_communicate:
                mock_instance = AsyncMock()
                mock_instance.save = AsyncMock()
                mock_communicate.return_value = mock_instance
                
                progress_calls = []
                
                def progress_callback(current, total):
                    progress_calls.append((current, total))
                
                text = "第一句。第二句。"
                result = await tts.synthesize(text, tmpdir, progress_callback)
                
                assert len(progress_calls) == 2


# ============================================================================
# REQ-006: 檔案輸出測試
# ============================================================================

class TestSynthesizeResult:
    """測試合成結果 - REQ-006"""
    
    @pytest.mark.asyncio
    async def test_multiple_output_files(self):
        """多輸出檔案"""
        tts = PresentationTTS()
        
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch('edge_tts.Communicate') as mock_communicate:
                mock_instance = AsyncMock()
                mock_instance.save = AsyncMock()
                mock_communicate.return_value = mock_instance
                
                text = "第一句。第二句。第三句。"
                result = await tts.synthesize(text, tmpdir)
                
                assert result.success == True
                assert len(result.output_files) == 3


# ============================================================================
# REQ-007: 音色選擇測試
# ============================================================================

class TestVoiceSelection:
    """測試音色選擇 - REQ-007"""
    
    def test_voice_options(self):
        """支援多音色"""
        voices = [
            "zh-TW-HsiaoHsiaoNeural",
            "zh-TW-YunJingNeural",
        ]
        
        for voice in voices:
            tts = PresentationTTS(voice=voice)
            assert tts.voice == voice


if __name__ == "__main__":
    pytest.main([__file__, "-v"])