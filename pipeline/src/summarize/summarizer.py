"""LLM 摘要生成器"""

import json
from datetime import datetime, timezone
from typing import Callable, Optional

from ..models import ProcessedArticle, RawArticle
from .prompt import SUMMARIZE_PROMPT, DIGEST_PROMPT


class Summarizer:
    """用 LLM 生成文章摘要和每日早报"""

    def __init__(self, llm_fn: Callable):
        self.llm = llm_fn

    async def summarize_one(self, article: RawArticle) -> Optional[ProcessedArticle]:
        """单篇文章摘要"""
        prompt = SUMMARIZE_PROMPT.format(
            title=article.title,
            content=article.content[:8000],  # 截断以防超 token
            lang=article.lang,
        )
        try:
            response = await self.llm(prompt)
            data = json.loads(response)

            # 生成唯一 ID — 用标题前 40 个字符做 slug
            slug = self._to_slug(data.get("title", article.title))[:40]

            return ProcessedArticle(
                id=slug,
                raw_url=article.url,
                source_name=article.source_name,
                original_title=article.title,
                title=data.get("title", article.title),
                summary=data.get("summary", ""),
                key_points=data.get("key_points", []),
                analysis=data.get("analysis", ""),
                categories=data.get("categories", article.categories),
                tags=data.get("tags", []),
                published_at=datetime.now(timezone.utc),
                aigc_label=True,
            )
        except Exception as e:
            print(f"  [WARN] Summarize failed: {article.title[:50]} — {e}")
            return None

    async def create_digest(
        self, articles: list[ProcessedArticle], date_str: str
    ) -> dict:
        """创建每日早报（含标题 + 编辑点评）"""
        if not articles:
            return {"date": date_str, "title": "", "articles": []}

        # 拼接文章列表
        article_list = "\n".join(
            f"{i+1}. {a.title}\n   {a.summary[:100]}"
            for i, a in enumerate(articles[:8])
        )
        prompt = DIGEST_PROMPT.format(
            date=date_str,
            articles=article_list,
        )

        try:
            response = await self.llm(prompt)
            data = json.loads(response)
        except Exception as e:
            print(f"  [WARN] Digest creation failed: {e}")
            data = {}

        return {
            "date": date_str,
            "title": data.get("title", f"AI 早报 | {date_str}"),
            "articles": articles,
            "editor_note": data.get("editor_note", ""),
        }

    @staticmethod
    def _to_slug(title: str) -> str:
        """标题转 slug（仅英文+数字）"""
        import re
        slug = re.sub(r'[^a-zA-Z0-9\s-]', '', title)
        slug = slug.strip().replace(' ', '-')
        slug = re.sub(r'-+', '-', slug)
        return slug.lower().strip('-')
