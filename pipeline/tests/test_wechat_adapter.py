"""WeChatAdapter TDD 测试

Seams（已确认）:
  1. truncate_title        — 标题截断
  2. markdown_to_wechat_html — Markdown → 微信安全 HTML
  3. WeChatAdapter.adapt   — 完整适配流程
"""

# ── Cycle 1: truncate_title ──

from src.adapt.wechat_adapter import truncate_title

TITLE_MAX = 32


class TestTruncateTitle:
    """标题截断逻辑"""

    def test_short_title_unchanged(self):
        """不超过 32 字符的标题保持不变"""
        assert truncate_title("短标题") == "短标题"

    def test_exactly_32_chars(self):
        """正好 32 字符不截断"""
        title = "a" * TITLE_MAX
        assert truncate_title(title) == title
        assert len(truncate_title(title)) == TITLE_MAX

    def test_33_chars_truncated(self):
        """33 字符截断为 31 字符 + …"""
        title = "a" * 33
        result = truncate_title(title)
        assert len(result) == TITLE_MAX
        assert result.endswith("…")

    def test_long_title_truncated(self):
        """超长标题被截断"""
        title = "a" * 50
        result = truncate_title(title)
        assert len(result) == TITLE_MAX
        assert result.endswith("…")

    def test_chinese_mixed(self):
        """中英文混合标题正确处理"""
        title = "OpenAI 发布 GPT-5.6 Sol：下一代 AI 模型的重大突破与创新"  # ~30 chars
        result = truncate_title(title)
        assert len(result) <= TITLE_MAX

    def test_all_chinese_long(self):
        """纯中文超长标题"""
        title = "你好世界" * 10  # 40 chars
        result = truncate_title(title)
        assert len(result) == TITLE_MAX
        assert result.endswith("…")

    def test_empty_title(self):
        """空字符串"""
        assert truncate_title("") == ""

    def test_single_char(self):
        """单字符"""
        assert truncate_title("x") == "x"


# ── Cycle 2: markdown_to_wechat_html ──

from src.adapt.wechat_adapter import markdown_to_wechat_html


class TestMarkdownToWeChatHtml:
    """Markdown → 微信兼容 HTML 转换"""

    def test_plain_text_paragraph(self):
        """纯文本包裹在 p 标签中"""
        assert markdown_to_wechat_html("hello") == "<p>hello</p>"

    def test_multiple_paragraphs(self):
        """多段落用 p 标签分隔"""
        result = markdown_to_wechat_html("hello\n\nworld")
        assert result == "<p>hello</p><p>world</p>"

    def test_bold_text(self):
        """**bold** → <strong>bold</strong>"""
        assert markdown_to_wechat_html("**bold**") == "<p><strong>bold</strong></p>"

    def test_link_conversion(self):
        """[text](url) → <a href='url'>text</a>"""
        result = markdown_to_wechat_html("[click](https://example.com)")
        assert result == '<p><a href="https://example.com">click</a></p>'

    def test_unordered_list_dash(self):
        """- item → <li>item</li>"""
        result = markdown_to_wechat_html("- item1\n- item2")
        assert "<li>item1</li>" in result
        assert "<li>item2</li>" in result

    def test_html_chars_escaped(self):
        """<>& 被正确转义"""
        result = markdown_to_wechat_html("a < b & c > d")
        assert "&lt;" in result
        assert "&gt;" in result
        assert "&amp;" in result
        # 去掉 HTML 标签后，内容中不应有裸 <
        import re
        text_only = re.sub(r"<[^>]+>", "", result)
        assert "<" not in text_only

    def test_empty_string(self):
        """空字符串返回空"""
        assert markdown_to_wechat_html("") == ""

    def test_ordered_list(self):
        """1. item → <li>item</li>"""
        result = markdown_to_wechat_html("1. first\n2. second")
        assert "<li>first</li>" in result
        assert "<li>second</li>" in result

    def test_bold_in_list(self):
        """列表项中的粗体标记被转换"""
        result = markdown_to_wechat_html("- **key point**")
        assert "<li><strong>key point</strong></li>" in result


# ── Cycle 3: WeChatAdapter.adapt ──

import json
from datetime import datetime

import pytest

from src.models import DailyDigest, ProcessedArticle, AdaptedContent
from src.adapt.wechat_adapter import WeChatAdapter


@pytest.fixture
def sample_digest() -> DailyDigest:
    """带 3 篇测试文章的 DailyDigest"""
    articles = [
        ProcessedArticle(
            id="art-1",
            raw_url="https://example.com/1",
            source_name="OpenAI Blog",
            original_title="GPT-5.6 Sol Released",
            title="GPT-5.6 Sol Released",
            summary="OpenAI 发布了 GPT-5.6 Sol，推理能力大幅提升。",
            key_points=["MoE 架构", "推理成本降低 40%"],
            analysis="这是重大突破。",
            categories=["llm"],
            tags=["openai"],
        ),
        ProcessedArticle(
            id="art-2",
            raw_url="https://example.com/2",
            source_name="Anthropic",
            original_title="Constitutional AI Update",
            title="Constitutional AI Update",
            summary="Anthropic 更新了 Constitutional AI 框架。",
            key_points=[],
            analysis=None,
            categories=["safety"],
            tags=["anthropic"],
        ),
        ProcessedArticle(
            id="art-3",
            raw_url="https://example.com/3",
            source_name="TechCrunch AI",
            original_title="Very Long Article Title That Definitely Exceeds Thirty Two Characters For Sure Yes",
            title="Very Long Article Title That Definitely Exceeds Thirty Two Characters For Sure Yes",
            summary="这是一篇超长标题的新闻。",
            key_points=["测试截断"],
            analysis="测试标题截断。",
            categories=["news"],
            tags=["test"],
        ),
    ]
    return DailyDigest(
        date="2026-07-06",
        title="AI 早报测试",
        articles=articles,
    )


class TestWeChatAdapter:
    """WeChatAdapter 完整适配流程"""

    def test_adapt_returns_list(self, sample_digest):
        """adapt 返回 list[AdaptedContent]"""
        adapter = WeChatAdapter()
        result = adapter.adapt(sample_digest)
        assert isinstance(result, list)
        assert len(result) > 0

    def test_adapt_returns_adapted_content(self, sample_digest):
        """每个元素是 AdaptedContent 类型"""
        adapter = WeChatAdapter()
        result = adapter.adapt(sample_digest)
        for item in result:
            assert isinstance(item, AdaptedContent)

    def test_platform_is_wechat(self, sample_digest):
        """platform 字段为 wechat"""
        adapter = WeChatAdapter()
        result = adapter.adapt(sample_digest)
        for item in result:
            assert item.platform == "wechat"

    def test_title_truncated_in_content(self, sample_digest):
        """标题在 JSON content 中被截断"""
        adapter = WeChatAdapter()
        result = adapter.adapt(sample_digest)
        # 微信多图文合并为一个 draft，文章在 draft["articles"] 中
        data = json.loads(result[0].content)
        third = data["articles"][2]
        assert len(third["title"]) <= 32
        assert third["title"].endswith("…")

    def test_max_eight_articles(self):
        """超过 8 篇文章时截断（微信多图文上限）"""
        articles = [
            ProcessedArticle(
                id=f"art-{i}",
                raw_url=f"https://example.com/{i}",
                source_name="Test",
                original_title=f"Article {i}",
                title=f"Article {i}",
                summary=f"Summary {i}",
            )
            for i in range(10)
        ]
        digest = DailyDigest(date="2026-07-06", title="Test", articles=articles)
        adapter = WeChatAdapter()
        result = adapter.adapt(digest)
        # 微信多图文合并为一次推文
        assert len(result) == 1
        data = json.loads(result[0].content)
        assert len(data["articles"]) <= 8  # type: ignore

    def test_no_forbidden_html_tags(self, sample_digest):
        """输出的 HTML 不含微信禁止标签"""
        adapter = WeChatAdapter()
        result = adapter.adapt(sample_digest)
        forbidden = ["script", "iframe", "table", "form", "style", "svg"]
        for item in result:
            first = json.loads(item.content)
            for article in first["articles"]:  # type: ignore
                content = article["content"]
                for tag in forbidden:
                    assert f"<{tag}" not in content, f"禁止标签 <{tag}> 出现在输出中"

    def test_aigc_notice_in_each_article(self, sample_digest):
        """每篇文章底部有 AI 辅助生成声明"""
        adapter = WeChatAdapter()
        result = adapter.adapt(sample_digest)
        for item in result:
            first = json.loads(item.content)
            for article in first["articles"]:  # type: ignore
                assert "辅助生成" in article["content"]

    def test_output_is_valid_wechat_draft_json(self, sample_digest):
        """输出可解析为合法的微信草稿 JSON 结构"""
        adapter = WeChatAdapter()
        result = adapter.adapt(sample_digest)
        for item in result:
            data = json.loads(item.content)
            assert "articles" in data
            for article in data["articles"]:
                assert "title" in article
                assert "content" in article
                assert "content_source_url" in article

    def test_empty_digest(self):
        """空 Digest 返回空列表"""
        digest = DailyDigest(date="2026-07-06", title="", articles=[])
        adapter = WeChatAdapter()
        result = adapter.adapt(digest)
        assert result == []
