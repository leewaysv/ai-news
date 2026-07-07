"""WeChatAdapter 原型 — 便携式逻辑模块

可被提升到 pipeline/src/adapt/wechat_adapter.py
"""

import re
from dataclasses import dataclass, field
from typing import Optional


# ── 数据模型（与 pipeline/src/models.py 对齐，无外部依赖）──


@dataclass
class ProtoProcessedArticle:
    """原型版 ProcessedArticle"""
    id: str
    raw_url: str
    source_name: str
    original_title: str
    title: str
    summary: str
    key_points: list[str] = field(default_factory=list)
    analysis: Optional[str] = None
    categories: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    aigc_label: bool = True


@dataclass
class ProtoDailyDigest:
    """原型版 DailyDigest"""
    date: str
    title: str
    articles: list[ProtoProcessedArticle] = field(default_factory=list)
    editor_note: Optional[str] = None


# ── 输出模型 ──


@dataclass
class WeChatDraftArticle:
    """微信草稿单篇文章"""
    title: str
    content: str               # 微信兼容 HTML
    content_source_url: str    # 原文链接
    thumb_media_id: str = ""
    need_open_comment: int = 0
    only_fans_can_comment: int = 0
    original_title: str = ""   # 截断前原标题（调试用）


@dataclass
class WeChatDraft:
    """微信草稿（多篇合并，最多 8 篇）"""
    articles: list[WeChatDraftArticle] = field(default_factory=list)


# ── 核心逻辑 ──

TITLE_MAX_CHARS = 32
MAX_ARTICLES_PER_DRAFT = 8


def truncate_title(title: str, max_chars: int = TITLE_MAX_CHARS) -> str:
    """截断标题到 max_chars 字符，超长则末尾加 …

    中英文均按 1 字符计算（微信公众平台的计法）。
    """
    if len(title) <= max_chars:
        return title
    return title[:max_chars - 1] + "…"


def sanitize_html(text: str) -> str:
    """将纯文本转义为微信安全的 HTML

    微信内容区支持标签:
    a, br, blockquote, code, div, em, h1-h6, hr, i, img,
    li, ol, p, pre, section, span, strong, u, ul
    不支持: script, iframe, table, form, input, style, svg
    """
    # 转义 HTML 特殊字符
    text = text.replace("&", "&amp;")
    text = text.replace("<", "&lt;")
    text = text.replace(">", "&gt;")
    text = text.replace('"', "&quot;")
    return text


def markdown_to_wechat_html(md_text: str) -> str:
    """简易 Markdown → 微信兼容 HTML 转换

    只处理微信支持的有序/无序列表、粗体、链接。
    其他内容保持转义后的纯文本。
    """
    html_parts = []
    lines = md_text.split("\n")

    for line in lines:
        stripped = line.strip()

        # 空行
        if not stripped:
            html_parts.append("<p></p>")
            continue

        # 无序列表
        if stripped.startswith("- ") or stripped.startswith("* "):
            content = sanitize_html(stripped[2:])
            content = _inline_format(content)
            html_parts.append(f"<li>{content}</li>")
            continue

        # 有序列表
        ordered_match = re.match(r"^\d+\.\s+(.*)", stripped)
        if ordered_match:
            content = sanitize_html(ordered_match.group(1))
            content = _inline_format(content)
            html_parts.append(f"<li>{content}</li>")
            continue

        # 普通段落
        content = sanitize_html(stripped)
        content = _inline_format(content)
        html_parts.append(f"<p>{content}</p>")

    return "".join(html_parts)


def _inline_format(text: str) -> str:
    """行内格式：粗体、链接"""
    # **粗体**
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    # [text](url) 链接
    text = re.sub(
        r"\[(.+?)\]\((https?://[^\s)]+)\)",
        r'<a href="\2">\1</a>',
        text,
    )
    return text


def make_aigc_notice(notice_text: str = "") -> str:
    """生成 AI 辅助生成声明 HTML"""
    text = notice_text or "本文内容由 AI 辅助生成，仅供参考。"
    return (
        '<section style="margin-top: 24px; padding: 12px; '
        'background: #f5f5f5; border-radius: 4px; '
        'font-size: 13px; color: #999;">'
        f'<p style="margin: 0;">⚠️ {sanitize_html(text)}</p>'
        "</section>"
    )


def article_to_html(article: ProtoProcessedArticle, aigc_notice: str = "") -> str:
    """单篇 ProcessedArticle → 微信兼容 HTML"""
    parts = []

    # 摘要段落
    if article.summary:
        parts.append(markdown_to_wechat_html(article.summary))

    # 关键要点
    if article.key_points:
        parts.append("<ul>")
        for pt in article.key_points:
            content = sanitize_html(pt)
            content = _inline_format(content)
            parts.append(f"<li><strong>{content}</strong></li>")
        parts.append("</ul>")

    # 分析
    if article.analysis:
        parts.append('<section style="margin-top: 16px;">')
        parts.append(markdown_to_wechat_html(article.analysis))
        parts.append("</section>")

    # 原文链接
    parts.append(
        '<p style="margin-top: 16px; font-size: 13px; color: #888;">'
        f'<a href="{sanitize_html(article.raw_url)}">📎 查看原文</a>'
        f" · {sanitize_html(article.source_name)}"
        "</p>"
    )

    # AIGC 标注
    if article.aigc_label:
        parts.append(make_aigc_notice(aigc_notice))

    return "".join(parts)


def digest_to_draft(digest: ProtoDailyDigest, aigc_notice: str = "") -> WeChatDraft:
    """DailyDigest → WeChatDraft（最多 8 篇）"""
    draft = WeChatDraft()

    for article in digest.articles[:MAX_ARTICLES_PER_DRAFT]:
        truncated = truncate_title(article.title)
        content_html = article_to_html(article, aigc_notice)

        draft.articles.append(WeChatDraftArticle(
            title=truncated,
            content=content_html,
            content_source_url=article.raw_url,
            original_title=article.original_title,
        ))

    return draft


def draft_to_json(draft: WeChatDraft) -> dict:
    """WeChatDraft → JSON 可序列化 dict（模拟微信草稿 API 格式）"""
    return {
        "articles": [
            {
                "title": a.title,
                "content": a.content,
                "content_source_url": a.content_source_url,
                "thumb_media_id": a.thumb_media_id,
                "need_open_comment": a.need_open_comment,
                "only_fans_can_comment": a.only_fans_can_comment,
            }
            for a in draft.articles
        ]
    }


# ── 示例数据生成（用于 TUI）──


def make_demo_digest() -> ProtoDailyDigest:
    """生成一个包含多种边缘情况的 DailyDigest"""
    articles = [
        ProtoProcessedArticle(
            id="demo-1",
            raw_url="https://example.com/gpt5",
            source_name="OpenAI Blog",
            original_title="Previewing GPT-5.6 Sol: a next-generation model",
            title="Previewing GPT-5.6 Sol: a next-generation model",
            summary="OpenAI 发布了 GPT-5.6 Sol，在推理、编程和多模态能力上取得显著提升。新模型采用稀疏 MoE 架构，参数量达到 8T，但推理成本比 GPT-4 降低了 40%。",
            key_points=[
                "稀疏 MoE 架构，8T 参数，推理成本降低 40%",
                "多模态能力大幅提升，支持视频理解",
                "编程能力在 SWE-bench 上达到 78%",
            ],
            analysis="GPT-5.6 Sol 的发布标志着 OpenAI 在保持推理能力提升的同时，显著优化了成本结构。稀疏 MoE 架构的采用是降低成本的关键。",
            categories=["llm", "research"],
            tags=["openai", "gpt", "moi"],
            aigc_label=True,
        ),
        ProtoProcessedArticle(
            id="demo-2",
            raw_url="https://example.com/claude-safety",
            source_name="Anthropic",
            original_title="Constitutional AI: a framework for scalable oversight",
            title="Constitutional AI: a framework for scalable oversight",
            summary="Anthropic 提出了 Constitutional AI 框架，通过一组原则指导模型行为，减少对人工反馈的依赖。",
            key_points=[],
            analysis=None,
            categories=["safety", "research"],
            tags=["anthropic", "constitutional-ai"],
            aigc_label=True,
        ),
        ProtoProcessedArticle(
            id="demo-3",
            raw_url="https://example.com/ai-chip",
            source_name="TechCrunch AI",
            original_title="OpenAI and Broadcom unveil LLM-optimized inference chip — a game changer for the entire AI industry supply chain ecosystem",
            title="OpenAI and Broadcom unveil LLM-optimized inference chip — a game changer for the entire AI industry supply chain ecosystem",
            summary="OpenAI 与 Broadcom 联合发布了专为 LLM 推理优化的 AI 芯片。",
            key_points=[
                "推理速度提升 5 倍",
                "功耗降低 60%",
            ],
            analysis="这是一颗超过 32 字符的标题，用于测试截断逻辑。",
            categories=["industry", "hardware"],
            tags=["openai", "broadcom", "chip"],
            aigc_label=True,
        ),
        ProtoProcessedArticle(
            id="demo-4",
            raw_url="https://example.com/mistral",
            source_name="TechCrunch AI",
            original_title="What is Mistral AI? Everything to know",
            title="Mistral AI",
            summary="Mistral AI 是一家法国 AI 初创公司，专注于开源大语言模型。",
            key_points=[
                "法国 AI 初创公司",
                "开源大语言模型",
                "获得 4.5 亿欧元融资",
            ],
            analysis=None,
            categories=["industry", "startup"],
            tags=["mistral", "france", "opensource"],
            aigc_label=True,
        ),
        ProtoProcessedArticle(
            id="demo-5",
            raw_url="https://example.com/safety",
            source_name="MIT News AI",
            original_title="AI safety researcher warns about rapid advancement",
            title="AI safety",
            summary="AI 安全研究人员警告，AI 发展速度超过安全研究。",
            key_points=[
                "对齐研究跟不上模型迭代",
            ],
            analysis=None,
            categories=["safety"],
            tags=[],
            aigc_label=True,
        ),
    ]

    # 复制几篇以测试 8 篇上限
    while len(articles) < 10:
        clone = ProtoProcessedArticle(
            id=f"demo-extra-{len(articles)}",
            raw_url="https://example.com/extra",
            source_name="Hacker News",
            original_title=f"Extra AI News Article #{len(articles) - 4}",
            title=f"Extra AI News Article #{len(articles) - 4}",
            summary=f"这是第 {len(articles) - 4} 篇额外新闻，用于测试多篇合并的截断行为。",
            key_points=[f"要点 {len(articles) - 4}"],
            analysis="多余文章用于测试上限。",
            categories=["news"],
            aigc_label=True,
        )
        articles.append(clone)

    return ProtoDailyDigest(
        date="2026-07-06",
        title="AI 早报：今日 AI 头条",
        articles=articles,
        editor_note="测试编辑器按语",
    )
