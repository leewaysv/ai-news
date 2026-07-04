"""API 新闻源采集器

支持：HackerNews、GitHub Trending 等 API 源
"""

import hashlib
from datetime import datetime, timezone
from typing import Optional

import httpx

from ..models import NewsSource, RawArticle


class APICollector:
    """从 REST API 采集新闻"""

    def __init__(self, timeout: int = 30):
        self.timeout = timeout

    async def fetch(self, source: NewsSource) -> list[RawArticle]:
        """获取单个 API 源的最近文章"""
        handlers = {
            "hackernews": self._fetch_hackernews,
            "github-trending": self._fetch_github_trending,
        }
        handler = handlers.get(source.id)
        if not handler:
            print(f"  [WARN] No API handler for: {source.id}")
            return []

        try:
            articles = await handler(source)
            print(f"  [OK] {source.id}: {len(articles)} articles")
            return articles
        except Exception as e:
            print(f"  [ERROR] API fetch failed: {source.id} — {e}")
            return []

    async def _fetch_hackernews(self, source: NewsSource) -> list[RawArticle]:
        """从 HackerNews API 获取 AI 相关热帖"""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            resp = await client.get(
                "https://hacker-news.firebaseio.com/v0/topstories.json"
            )
            resp.raise_for_status()
            story_ids = resp.json()[:30]

        articles = []
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            for sid in story_ids:
                try:
                    resp = await client.get(
                        f"https://hacker-news.firebaseio.com/v0/item/{sid}.json"
                    )
                    resp.raise_for_status()
                    item = resp.json()
                    if not item or item.get("type") != "story":
                        continue

                    title = item.get("title", "")
                    url = item.get("url") or f"https://news.ycombinator.com/item?id={sid}"

                    # 只保留 AI 相关
                    ai_keywords = [
                        "ai", "gpt", "llm", "neural", "machine learning",
                        "deep learning", "openai", "anthropic", "claude",
                        "chatgpt", "transformer", "diffusion",
                    ]
                    if not any(kw in title.lower() for kw in ai_keywords):
                        continue

                    dedup = hashlib.md5(url.encode()).hexdigest()[:12]
                    articles.append(RawArticle(
                        source_id=source.id,
                        source_name=source.name,
                        url=url,
                        title=title.strip(),
                        content=item.get("text", "") or "",
                        published_at=datetime.fromtimestamp(
                            item.get("time", 0), tz=timezone.utc
                        ),
                        lang="en",
                        categories=["community"],
                        dedup_hash=dedup,
                    ))
                except Exception:
                    continue

        return articles

    async def _fetch_github_trending(
        self, source: NewsSource
    ) -> list[RawArticle]:
        """从 GitHub API 获取 AI 相关热门仓库"""
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "AI-News-Pipeline/1.0",
        }
        params = {
            "q": "topic:ai",
            "sort": "stars",
            "order": "desc",
            "per_page": 15,
        }

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            resp = await client.get(
                source.url, headers=headers, params=params
            )
            resp.raise_for_status()
            data = resp.json()

        articles = []
        for repo in data.get("items", []):
            url = repo.get("html_url", "")
            title = f"[GitHub] {repo.get('full_name', '')}: {repo.get('description', '') or 'No description'}"
            dedup = hashlib.md5(url.encode()).hexdigest()[:12]

            articles.append(RawArticle(
                source_id=source.id,
                source_name=source.name,
                url=url,
                title=title.strip(),
                content=repo.get("description", "") or "",
                published_at=datetime.now(timezone.utc),
                lang="en",
                categories=["open-source", "tools"],
                dedup_hash=dedup,
            ))

        return articles
