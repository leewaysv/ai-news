"""兜底策略

方案 3：当天有效文章不足 N 篇则跳过发布
"""


class FallbackHandler:
    """兜底处理逻辑"""

    def __init__(self, min_articles: int = 3):
        self.min_articles = min_articles

    def should_publish(self, article_count: int) -> bool:
        """判断当天是否应该发布"""
        if article_count == 0:
            print(f"  [FALLBACK] No articles today — skipping")
            return False
        if article_count < self.min_articles:
            print(f"  [FALLBACK] Only {article_count} articles (min {self.min_articles}) — skipping")
            return False
        return True

    def log_skip(self, date: str, reason: str):
        """记录跳过日志"""
        import logging
        logging.warning(f"[{date}] Skipped: {reason}")
