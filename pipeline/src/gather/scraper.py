"""通用网页爬虫（用于中文源等无 RSS 的站点）"""

import hashlib
import re
from datetime import datetime, timezone
from typing import Optional

import httpx
from bs4 import BeautifulSoup

from ..models import NewsSource, RawArticle


class Scraper:
    """通用网页新闻爬虫"""

    def __init__(self, timeout: int = 30):
        self.timeout = timeout
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        }

    async def fetch(self, source: NewsSource) -> list[RawArticle]:
        """爬取单个站点的新闻列表"""
        scrapers = {
            "liangzita": self._scrape_qbitai,
        }
        handler = scrapers.get(source.id)
        if not handler:
            print(f"  [WARN] No scraper handler for: {source.id}")
            return []

        try:
            articles = await handler(source)
            print(f"  [OK] {source.id}: {len(articles)} articles")
            return articles
        except Exception as e:
            print(f"  [ERROR] Scrape failed: {source.id} — {e}")
            return []

    async def _scrape_qbitai(self, source: NewsSource) -> list[RawArticle]:
        """爬取量子位首页文章列表"""
        async with httpx.AsyncClient(timeout=self.timeout, headers=self.headers) as client:
            resp = await client.get(source.url)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, "lxml")

        articles = []
        seen_urls = set()

        # 量子位的文章链接格式：/2026/07/XXXXX.html
        for a in soup.select("a[href*='/2026/']"):
            href = a.get("href", "")
            text = a.get_text(strip=True)
            if not text or not href.endswith(".html") or len(text) < 8:
                continue
            if href in seen_urls:
                continue
            seen_urls.add(href)

            full_url = href if href.startswith("http") else f"https://www.qbitai.com{href}"
            dedup = hashlib.md5(full_url.encode()).hexdigest()[:12]
            articles.append(RawArticle(
                source_id=source.id,
                source_name=source.name,
                url=full_url,
                title=text,
                content="",
                published_at=datetime.now(timezone.utc),
                lang="zh",
                categories=["industry"],
                dedup_hash=dedup,
            ))

        return articles[:15]
