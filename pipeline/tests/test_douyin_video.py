"""DouyinVideoPublisher TDD 测试

测试视频渲染 + 上传的编排逻辑（mock 所有外部依赖）
"""

import json
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.models import AdaptedContent
from src.publish.douyin_video import DouyinVideoPublisher


def make_content(article_id: str = "art-1", **kwargs) -> AdaptedContent:
    """生成测试用的 AdaptedContent"""
    data = {
        "script": {"hook": "测试", "info": "内容", "cta": "关注"},
        "srt": "1\n00:00:01,000 --> 00:00:03,000\n测试",
        "keywords": ["AI", "test", "科技"],
        "tts_text": "测试文本内容",
        "estimated_duration": 15,
        "ai_label": True,
    }
    data.update(kwargs)
    return AdaptedContent(
        platform="douyin",
        content=json.dumps(data, ensure_ascii=False),
        metadata={"article_id": article_id, "title": "测试视频", "duration": 15},
    )


class TestDouyinVideoPublisher:
    """视频发布器编排测试"""

    @pytest.fixture
    def publisher(self, tmp_path: Path):
        pub = DouyinVideoPublisher(
            output_dir=str(tmp_path / "output"),
            pexels_api_key="test_key",
            headless=True,
        )
        # Mock FFmpeg check to pass
        pub._check_ffmpeg = MagicMock(return_value=True)
        return pub

    @pytest.mark.asyncio
    async def test_publish_empty(self, publisher):
        """空列表返回 0"""
        result = await publisher.publish([])
        assert result == 0

    @pytest.mark.asyncio
    async def test_publish_single_content(self, publisher):
        """单条内容走通完整流程"""
        publisher._generate_tts = AsyncMock(return_value=Path("test.mp3"))
        publisher._search_background = AsyncMock(return_value="")
        publisher._compose_video = AsyncMock(return_value=True)
        publisher._upload_to_douyin = AsyncMock(return_value=True)

        result = await publisher.publish([make_content()])
        assert result == 1

    @pytest.mark.asyncio
    async def test_tts_failure_skips(self, publisher):
        """TTS 失败跳过该条"""
        publisher._generate_tts = AsyncMock(return_value=None)
        publisher._search_background = AsyncMock(return_value="")
        publisher._compose_video = AsyncMock(return_value=True)
        publisher._upload_to_douyin = AsyncMock(return_value=True)

        result = await publisher.publish([make_content()])
        assert result == 0

    @pytest.mark.asyncio
    async def test_compose_failure_skips(self, publisher):
        """视频合成失败跳过"""
        publisher._generate_tts = AsyncMock(return_value=Path("test.mp3"))
        publisher._compose_video = AsyncMock(return_value=False)

        result = await publisher.publish([make_content()])
        assert result == 0

    @pytest.mark.asyncio
    async def test_upload_failure_skips(self, publisher):
        """上传失败跳过"""
        publisher._generate_tts = AsyncMock(return_value=Path("test.mp3"))
        publisher._search_background = AsyncMock(return_value="")
        publisher._compose_video = AsyncMock(return_value=True)
        publisher._upload_to_douyin = AsyncMock(return_value=False)

        result = await publisher.publish([make_content()])
        assert result == 0

    @pytest.mark.asyncio
    async def test_multiple_articles(self, publisher):
        """多篇文章独立处理"""
        publisher._generate_tts = AsyncMock(return_value=Path("test.mp3"))
        publisher._search_background = AsyncMock(return_value="")
        publisher._compose_video = AsyncMock(return_value=True)
        publisher._upload_to_douyin = AsyncMock(return_value=True)

        contents = [make_content("art-1"), make_content("art-2")]
        result = await publisher.publish(contents)
        assert result == 2

    @pytest.mark.asyncio
    async def test_partial_failure(self, publisher):
        """部分失败不影响其他条"""
        call_count = 0

        async def failing_compose(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            return call_count != 2  # 第二条失败

        publisher._generate_tts = AsyncMock(return_value=Path("test.mp3"))
        publisher._search_background = AsyncMock(return_value="")
        publisher._compose_video = AsyncMock(side_effect=failing_compose)
        publisher._upload_to_douyin = AsyncMock(return_value=True)

        contents = [make_content("a"), make_content("b"), make_content("c")]
        result = await publisher.publish(contents)
        assert result == 2  # 3 条中第 2 条失败 → 成功 2 条

    @pytest.mark.asyncio
    async def test_api_error_does_not_crash(self, publisher):
        """任意步骤抛异常不崩"""
        publisher._generate_tts = AsyncMock(side_effect=RuntimeError("boom"))

        # 不应抛异常
        result = await publisher.publish([make_content()])
        assert result == 0  # 优雅降级为 0


class TestTTS:
    """TTS 生成测试"""

    @pytest.mark.asyncio
    async def test_generate_tts_calls_edge_tts(self):
        """_generate_tts 调用 edge-tts"""
        import sys
        from unittest.mock import MagicMock
        # Mock edge_tts module before it's lazily imported
        mock_module = MagicMock()
        sys.modules["edge_tts"] = mock_module

        publisher = DouyinVideoPublisher()
        mock_module.Communicate.return_value.save = AsyncMock()
        result = await publisher._generate_tts("测试", Path("test.mp3"))
        assert result is not None

        del sys.modules["edge_tts"]


class TestFFmpeg:
    """FFmpeg 检测测试"""

    def test_check_ffmpeg_found(self):
        """FFmpeg 可用时返回 True"""
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock()
            publisher = DouyinVideoPublisher()
            assert publisher._check_ffmpeg()

    def test_check_ffmpeg_not_found(self):
        """FFmpeg 不可用时返回 False"""
        with patch("subprocess.run", side_effect=FileNotFoundError):
            publisher = DouyinVideoPublisher()
            assert not publisher._check_ffmpeg()
