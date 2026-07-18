"""飞书机器人推送 — Webhook 发送每日 AI 早报"""

from __future__ import annotations

import json
import logging
import os
from typing import Optional

import httpx

from ..models import DailyDigest, AdaptedContent
from .base import BasePublisher

log = logging.getLogger(__name__)

BLOG_BASE_URL = "https://ai-news-2li.pages.dev"
TRUNCATE_TITLE = 60
TRUNCATE_SUMMARY = 100
SEPARATOR = "─" * 24


def format_feishu_message(digest: DailyDigest) -> dict:
    """将 DailyDigest 格式化为飞书富文本消息"""
    content = []
    divider = _post_text(SEPARATOR)

    # ── 标题 ──
    title_text = f"📰 AI 早报 | {digest.date}" if digest.date else "📰 AI 早报"
    content.append(_post_text(title_text))
    content.append(_post_text(""))
    content.append(divider)
    content.append(_post_text(""))

    # ── 文章列表 ──
    for i, article in enumerate(digest.articles[:10], 1):
        content.append(_post_text(str(i)))

        title = article.title[:TRUNCATE_TITLE]
        content.append(_post_text(f"📰 {title}"))

        blog_url = article.raw_url or BLOG_BASE_URL
        content.append(_post_link(f"🔗 {blog_url}", blog_url))

        if article.summary:
            summary = article.summary[:TRUNCATE_SUMMARY]
            content.append(_post_text(f"📝 {summary}"))

        content.append(_post_text(""))
        content.append(divider)
        content.append(_post_text(""))

    post_content = json.dumps({
        "post": {
            "zh_cn": {
                "title": title_text,
                "content": [[c] if isinstance(c, dict) else c
                            for c in content],
            }
        }
    }, ensure_ascii=False)

    return {
        "msg_type": "post",
        "content": post_content,
    }


def _post_text(text: str) -> dict:
    return {"tag": "text", "text": text}


def _post_link(text: str, url: str) -> dict:
    return {"tag": "a", "text": text, "href": url}


class FeishuPublisher(BasePublisher):
    """飞书 Webhook 机器人发布器"""

    def __init__(self, webhook_url: str = ""):
        self.webhook_url = webhook_url or os.environ.get("FEISHU_WEBHOOK_URL", "")

    async def publish(self, contents: list[AdaptedContent]) -> int:
        if not contents or not self.webhook_url:
            return 0

        digest = self._build_digest(contents)
        if not digest.articles:
            return 0

        payload = format_feishu_message(digest)
        return await self._send(payload)

    def _build_digest(self, contents: list[AdaptedContent]) -> DailyDigest:
        from ..models import ProcessedArticle

        articles = []
        for item in contents:
            meta = item.metadata or {}

            data = None
            try:
                data = json.loads(item.content)
            except json.JSONDecodeError:
                pass

            if data and isinstance(data, dict) and "articles" in data:
                for art in data["articles"]:
                    articles.append(ProcessedArticle(
                        id=meta.get("slug", ""),
                        raw_url=meta.get("blog_url", art.get("content_source_url", "")),
                        source_name=meta.get("source", ""),
                        original_title=art.get("title", ""),
                        title=art.get("title", ""),
                        summary=_extract_text(art.get("content", "")),
                    ))
            else:
                articles.append(ProcessedArticle(
                    id=meta.get("slug", ""),
                    raw_url=meta.get("blog_url", meta.get("source_url", "")),
                    source_name=meta.get("source", ""),
                    original_title=meta.get("title", ""),
                    title=meta.get("title", ""),
                    summary=meta.get("summary", ""),
                ))

        return DailyDigest(
            date=contents[0].metadata.get("date", "") if contents[0].metadata else "",
            title=contents[0].metadata.get("title", "AI 早报") if contents[0].metadata else "AI 早报",
            articles=articles,
        )

    async def _send(self, payload: dict) -> int:
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.post(
                    self.webhook_url,
                    content=json.dumps(payload, ensure_ascii=False),
                    headers={"Content-Type": "application/json; charset=utf-8"},
                    timeout=10.0,
                )
                resp.raise_for_status()
                result = resp.json()

            if result.get("code") == 0:
                log.info("[feishu] Message sent successfully")
                return 1
            else:
                log.warning(f"[feishu] API error: {result}")
                return 0

        except Exception as e:
            log.warning(f"[feishu] Send failed: {e}")
            return 0


def _extract_text(html: str) -> str:
    import re
    text = re.sub(r"<[^>]+>", "", html)
    text = text.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
    return text.strip()[:150]
