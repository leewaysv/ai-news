"""WeChat 内容适配器 — DailyDigest → 微信草稿 HTML"""
from __future__ import annotations

import json
import re
from typing import Optional

from ..models import DailyDigest, AdaptedContent
from .base import BaseAdapter


TITLE_MAX_CHARS = 32
MAX_ARTICLES_PER_DRAFT = 8
AIGC_NOTICE_TEXT = "本文内容由 AI 辅助生成，仅供参考。"


def truncate_title(title: str, max_chars: int = TITLE_MAX_CHARS) -> str:
    """截断标题到 max_chars 字符，超长则末尾加 …"""
    if len(title) <= max_chars:
        return title
    return title[: max_chars - 1] + "…"


# ── Markdown → 微信 HTML ──

def sanitize_html(text: str) -> str:
    """将纯文本中的 HTML 特殊字符转义"""
    text = text.replace("&", "&amp;")
    text = text.replace("<", "&lt;")
    text = text.replace(">", "&gt;")
    text = text.replace('"', "&quot;")
    return text


def _inline_format(text: str) -> str:
    """行内格式：**粗体**、[链接](url)"""
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(
        r"\[(.+?)\]\((https?://[^\s)]+)\)",
        r'<a href="\2">\1</a>',
        text,
    )
    return text


def markdown_to_wechat_html(md_text: str) -> str:
    """简易 Markdown → 微信兼容 HTML"""
    if not md_text.strip():
        return ""

    html_parts = []
    lines = md_text.split("\n")
    in_list = False

    for line in lines:
        stripped = line.strip()

        if not stripped:
            # 空行 — 段落分隔符，不输出内容
            if in_list:
                in_list = False
            continue

        # 无序列表
        if stripped.startswith("- ") or stripped.startswith("* "):
            content = sanitize_html(stripped[2:])
            content = _inline_format(content)
            if not in_list:
                html_parts.append("<ul>")
                in_list = True
            html_parts.append(f"<li>{content}</li>")
            continue

        # 有序列表
        ordered_match = re.match(r"^\d+\.\s+(.*)", stripped)
        if ordered_match:
            content = sanitize_html(ordered_match.group(1))
            content = _inline_format(content)
            if not in_list:
                html_parts.append("<ol>")
                in_list = True
            html_parts.append(f"<li>{content}</li>")
            continue

        # 关闭列表（如有）
        if in_list:
            in_list = False

        # 普通段落
        content = sanitize_html(stripped)
        content = _inline_format(content)
        html_parts.append(f"<p>{content}</p>")

    if in_list:
        # 文件末尾未关闭的列表
        html_parts.append("</ul>" if "<ol>" not in "".join(html_parts) else "</ol>")

    return "".join(html_parts)


# ── 文章 → HTML ──


def _article_to_html(article, notice_text: str = AIGC_NOTICE_TEXT) -> str:
    """单篇 ProcessedArticle → 微信兼容 HTML"""
    parts = []

    if article.summary:
        parts.append(markdown_to_wechat_html(article.summary))

    if article.key_points:
        parts.append("<ul>")
        for pt in article.key_points:
            content = sanitize_html(pt)
            content = _inline_format(content)
            parts.append(f"<li><strong>{content}</strong></li>")
        parts.append("</ul>")

    if article.analysis:
        parts.append(markdown_to_wechat_html(article.analysis))

    # 原文链接
    source_html = sanitize_html(article.source_name)
    url_html = sanitize_html(article.raw_url)
    parts.append(
        f'<p><a href="{url_html}">查看原文</a>'
        f" &middot; {source_html}</p>"
    )

    # AIGC 标注
    if article.aigc_label:
        escaped = sanitize_html(notice_text)
        parts.append(
            '<section style="margin-top:24px;padding:12px;'
            'background:#f5f5f5;border-radius:4px;font-size:13px;color:#999;">'
            f"<p>⚠️ {escaped}</p></section>"
        )

    return "".join(parts)


# ── WeChatAdapter ──


class WeChatAdapter(BaseAdapter):
    """将 DailyDigest 适配为微信公众号草稿 JSON"""

    def adapt(self, digest: DailyDigest) -> list[AdaptedContent]:
        if not digest.articles:
            return []

        draft_articles = []
        for article in digest.articles[:MAX_ARTICLES_PER_DRAFT]:
            truncated = truncate_title(article.title)
            content_html = _article_to_html(article)
            draft_articles.append({
                "title": truncated,
                "content": content_html,
                "content_source_url": article.raw_url,
                "thumb_media_id": "",
                "need_open_comment": 0,
                "only_fans_can_comment": 0,
            })

        draft_json = json.dumps(
            {"articles": draft_articles},
            ensure_ascii=False,
        )

        return [
            AdaptedContent(
                platform="wechat",
                content=draft_json,
                metadata={
                    "article_count": len(draft_articles),
                    "digest_date": digest.date,
                    "digest_title": digest.title,
                },
            )
        ]
