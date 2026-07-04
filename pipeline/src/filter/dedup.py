"""URL 去重 + 相似度去重"""

from typing import Callable

from ..models import RawArticle


class Deduplicator:
    """文章去重"""

    def __init__(self):
        self._seen_hashes: set[str] = set()
        self._seen_urls: set[str] = set()

    def reset(self):
        self._seen_hashes.clear()
        self._seen_urls.clear()

    def dedup(self, articles: list[RawArticle]) -> list[RawArticle]:
        """URL 去重 + 相似度去重"""
        results = []

        for article in articles:
            # URL 去重
            if article.url in self._seen_urls:
                continue
            self._seen_urls.add(article.url)

            # hash 去重
            if article.dedup_hash and article.dedup_hash in self._seen_hashes:
                continue
            if article.dedup_hash:
                self._seen_hashes.add(article.dedup_hash)

            results.append(article)

        return results

    def dedup_cross_sources(
        self, articles: list[RawArticle]
    ) -> list[RawArticle]:
        """跨源去重（不同源报道同一新闻）"""
        # 简单策略：相同 URL 的去重已在上面完成
        # 后续可用 embedding 相似度做语义级去重
        return articles
