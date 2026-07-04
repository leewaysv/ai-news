"""RSS 新闻源采集器"""

import hashlib
from datetime import datetime, timezone
from typing import Optional

import feedparser

from ..models import NewsSource, RawArticle


class RSSCollector:
    """从 RSS/Atom feed 采集新闻"""

    def __init__(self, timeout: int = 30):
        self.timeout = timeout

    def fetch(self, source: NewsSource) -> list[RawArticle]:
        """获取单个 RSS 源的最近文章"""
        try:
            feed = feedparser.parse(source.url)
        except Exception as e:
            print(f"  [ERROR] RSS fetch failed: {source.id} — {e}")
            return []

        articles = []
        for entry in feed.entries[:15]:  # 每源最多取 15 篇
            try:
                article = self._entry_to_article(entry, source)
                if article:
                    articles.append(article)
            except Exception as e:
                print(f"  [WARN] Failed to parse entry: {source.id} — {e}")
                continue

        print(f"  [OK] {source.id}: {len(articles)} articles")
        return articles

    def _entry_to_article(
        self, entry: dict, source: NewsSource
    ) -> Optional[RawArticle]:
        title = entry.get("title", "")
        link = entry.get("link", "")
        content = ""

        # 提取正文
        if hasattr(entry, "content") and entry.content:
            content = entry.content[0].get("value", "")
        elif hasattr(entry, "summary") and entry.summary:
            content = entry.summary
        elif hasattr(entry, "description") and entry.description:
            content = entry.description

        if not title or not link:
            return None

        # 解析发布时间
        published = None
        if hasattr(entry, "published_parsed") and entry.published_parsed:
            published = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
        elif hasattr(entry, "updated_parsed") and entry.updated_parsed:
            published = datetime(*entry.updated_parsed[:6], tzinfo=timezone.utc)

        # 去重 hash
        dedup = hashlib.md5(link.encode()).hexdigest()[:12]

        return RawArticle(
            source_id=source.id,
            source_name=source.name,
            url=link,
            title=title.strip(),
            content=content.strip(),
            published_at=published,
            lang=source.lang,
            categories=source.categories,
            dedup_hash=dedup,
        )
