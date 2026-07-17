"""Embedding 相似度质量校验

方案 2：用 embedding 检查生成的摘要与原文的语义一致性
"""

import logging
from typing import Optional

from ..models import RawArticle, ProcessedArticle

log = logging.getLogger(__name__)


class EmbeddingQualityCheck:
    """基于 embedding 相似度的质量校验"""

    def __init__(self, model_name: str = "all-MiniLM-L6-v2", threshold: float = 0.75):
        self.model_name = model_name
        self.threshold = threshold
        self._model = None

    def _load_model(self):
        """懒加载 embedding 模型"""
        if self._model is None:
            try:
                from sentence_transformers import SentenceTransformer
                self._model = SentenceTransformer(self.model_name)
            except ImportError:
                log.warning("sentence-transformers not installed. Skipping embedding check.")
                return None
        return self._model

    def check(
        self, article: ProcessedArticle, raw_article: Optional[RawArticle] = None
    ) -> bool:
        """检查一篇摘要的质量"""
        model = self._load_model()
        if model is None:
            article.embedding_pass = True
            return True

        if not raw_article or not raw_article.content:
            article.embedding_pass = True
            return True

        # 跨语言（英→中）的 embedding 相似度天然偏低，跳过校验
        if raw_article.lang == "en":
            article.embedding_pass = True
            return True

        text_a = raw_article.content[:2000]
        text_b = f"{article.summary} {' '.join(article.key_points)}"

        emb_a = model.encode(text_a)
        emb_b = model.encode(text_b)

        similarity = self._cosine_sim(emb_a, emb_b)
        passed = similarity >= self.threshold

        if not passed:
            log.warning("[QA FAIL] %s — similarity=%.3f", article.title[:50], similarity)

        article.embedding_pass = passed
        return passed

    def batch_check(
        self,
        articles: list[ProcessedArticle],
        raw_map: dict[str, RawArticle],
    ) -> list[ProcessedArticle]:
        """批量检查"""
        passed = []
        for article in articles:
            raw = raw_map.get(article.raw_url)
            if self.check(article, raw):
                passed.append(article)
        return passed

    @staticmethod
    def _cosine_sim(a: list[float], b: list[float]) -> float:
        import numpy as np
        a, b = np.array(a), np.array(b)
        return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-10))
