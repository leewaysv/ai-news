"""AIGC 合规标签处理"""

from ..models import ProcessedArticle


AIGC_DISCLAIMER_ZH = "> 🤖 本文由 AI 辅助生成，仅供参考。如有不准确之处，欢迎指正。"
AIGC_DISCLAIMER_EN = "> 🤖 This article is AI-assisted. For reference only."


class AIGCLabeler:
    """为 AI 生成内容添加合规标签"""

    def __init__(self, disclaimer: str = AIGC_DISCLAIMER_ZH):
        self.disclaimer = disclaimer

    def label(self, article: ProcessedArticle) -> ProcessedArticle:
        """标记文章为 AI 生成"""
        article.aigc_label = True
        return article

    def get_disclaimer(self) -> str:
        """获取合规声明文本"""
        return self.disclaimer
