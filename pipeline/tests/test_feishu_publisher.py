"""FeishuPublisher TDD 测试"""

import json
from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from src.models import DailyDigest, ProcessedArticle, AdaptedContent
from src.publish.feishu_publisher import format_feishu_message, FeishuPublisher


class TestFormatFeishuMessage:
    """飞书消息格式测试"""

    @pytest.fixture
    def digest(self):
        return DailyDigest(
            date="2026-07-08",
            title="AI 早报",
            articles=[
                ProcessedArticle(
                    id="art-1", raw_url="https://example.com/1",
                    source_name="OpenAI", original_title="GPT-5.6 Sol",
                    title="GPT-5.6 Sol",
                    summary="OpenAI 发布了 GPT-5.6 Sol，推理能力大幅提升。",
                    key_points=["MoE 架构"], categories=["llm"], tags=["openai"],
                ),
                ProcessedArticle(
                    id="art-2", raw_url="https://example.com/2",
                    source_name="Anthropic", original_title="Claude Update",
                    title="Claude Update",
                    summary="Anthropic 更新了 Claude 模型。",
                    key_points=[], categories=["safety"], tags=["anthropic"],
                ),
            ],
        )

    def test_returns_dict(self, digest):
        result = format_feishu_message(digest)
        assert isinstance(result, dict)

    def test_has_msg_type_post(self, digest):
        result = format_feishu_message(digest)
        assert result["msg_type"] == "post"

    def test_has_title(self, digest):
        result = format_feishu_message(digest)
        post = json.loads(result["content"])
        title = post["post"]["zh_cn"]["title"]
        assert "AI 早报" in title
        assert "2026-07-08" in title

    def test_content_is_list(self, digest):
        result = format_feishu_message(digest)
        post = json.loads(result["content"])
        content_list = post["post"]["zh_cn"]["content"]
        assert isinstance(content_list, list)
        assert len(content_list) > 0

    def test_each_article_in_content(self, digest):
        result = format_feishu_message(digest)
        text = json.dumps(result, ensure_ascii=False)
        assert "GPT-5.6 Sol" in text
        assert "Claude Update" in text

    def test_source_links_included(self, digest):
        result = format_feishu_message(digest)
        text = json.dumps(result, ensure_ascii=False)
        assert "example.com" in text

    def test_empty_digest_returns_minimal(self):
        digest = DailyDigest(date="2026-07-08", title="", articles=[])
        result = format_feishu_message(digest)
        assert result["msg_type"] == "post"

    def test_content_contains_aigc_notice(self, digest):
        result = format_feishu_message(digest)
        text = json.dumps(result, ensure_ascii=False)
        assert "辅助生成" in text or "AI" in text


class TestFeishuPublisher:
    """完整发布流程测试"""

    @pytest.mark.asyncio
    async def test_empty_contents_returns_zero(self):
        pub = FeishuPublisher(webhook_url="https://ex.com/hook")
        result = await pub.publish([])
        assert result == 0

    @pytest.mark.asyncio
    async def test_no_webhook_url_returns_zero(self):
        pub = FeishuPublisher(webhook_url="")
        result = await pub.publish([AdaptedContent(platform="test", content="{}")])
        assert result == 0

    @pytest.mark.asyncio
    async def test_send_success(self):
        pub = FeishuPublisher(webhook_url="https://open.feishu.cn/hook/test")
        with patch.object(httpx, "AsyncClient") as mock_client:
            mock_instance = AsyncMock()
            mock_instance.post = AsyncMock(return_value=MagicMock(
                status_code=200, json=lambda: {"code": 0},
            ))
            mock_client.return_value.__aenter__.return_value = mock_instance
            content = AdaptedContent(
                platform="blog", content="# Test",
                metadata={"title": "GPT-5.6", "date": "2026-07-08",
                          "source": "OpenAI", "source_url": "https://ex.com",
                          "summary": "OpenAI 发布新模型"},
            )
            result = await pub.publish([content])
            assert result == 1

    @pytest.mark.asyncio
    async def test_send_failure_returns_zero(self):
        pub = FeishuPublisher(webhook_url="https://open.feishu.cn/hook/test")
        with patch.object(httpx, "AsyncClient") as mock_client:
            mock_instance = AsyncMock()
            mock_instance.post = AsyncMock(side_effect=httpx.HTTPStatusError(
                "500", request=MagicMock(), response=MagicMock()
            ))
            mock_client.return_value.__aenter__.return_value = mock_instance
            content = AdaptedContent(
                platform="blog", content="# Test",
                metadata={"title": "Test", "date": "2026-07-08"},
            )
            result = await pub.publish([content])
            assert result == 0
