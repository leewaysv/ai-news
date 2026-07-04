"""相关性预过滤器

策略：先用规则快速过滤 → 再用 LLM 精判候选项
"""

import re
from typing import Optional

from ..models import RawArticle


# AI 相关关键词（用于快速规则过滤）
AI_KEYWORDS = [
    # 英文
    "artificial intelligence", "machine learning", "deep learning",
    "large language model", "llm", "gpt", "openai", "anthropic",
    "claude", "chatgpt", "gemini", "bard", "llama", "mistral",
    "neural network", "transformer", "diffusion model",
    "generative ai", "aigc", "agent", "ai agent", "multimodal",
    "reasoning", "agi", "safety", "alignment",
    "hugging face", "tensorflow", "pytorch", "langchain",
    "rag", "retrieval augmented", "fine-tuning", "sft", "rlhf",
    "embedding", "vector database", "copilot", "codex",
    # 中文
    "人工智能", "大模型", "大语言模型", "深度学习", "机器学习",
    "神经网络", "生成式", "多模态", "智能体", "知识图谱",
    "语义理解", "自然语言处理", "计算机视觉", "强化学习",
]

# 明显不相关关键词（快速过滤）
IRRELEVANT_KEYWORDS = [
    "sports", "nfl", "nba", "baseball", "soccer",
    "recipe", "cooking", "food",
    "celebrity", "entertainment",
    "crypto", "bitcoin", "nft", "blockchain",  # Web3 非 AI
]


class RelevanceClassifier:
    """相关性分类器"""

    def __init__(self, threshold: float = 0.3):
        self.threshold = threshold

    def quick_filter(self, article: RawArticle) -> Optional[RawArticle]:
        """快速规则过滤 — 低成本筛掉明显无关内容"""
        text = f"{article.title} {article.content}".lower()

        # 不相关关键词
        for kw in IRRELEVANT_KEYWORDS:
            if kw in text:
                return None

        # 中文源: 默认通过（中文源集中在 AI 领域）
        if article.lang == "zh":
            article.score = 0.6
            return article

        # 英文源: 检查 AI 关键词
        matches = sum(1 for kw in AI_KEYWORDS if kw in text)
        score = min(matches / 5.0, 1.0)

        if score < self.threshold:
            return None

        article.score = score
        return article

    async def llm_filter(
        self, articles: list[RawArticle], llm_fn
    ) -> list[RawArticle]:
        """LLM 精判 — 从候选中挑出真正相关的"""
        if not articles:
            return []

        candidates = []
        batch_articles = []
        # 批量处理，减少 LLM 调用次数
        for a in articles:
            batch_articles.append(a)
            if len(batch_articles) >= 10:
                candidates.extend(await self._judge_batch(batch_articles, llm_fn))
                batch_articles = []

        if batch_articles:
            candidates.extend(await self._judge_batch(batch_articles, llm_fn))

        return candidates

    async def _judge_batch(self, articles: list[RawArticle], llm_fn) -> list[RawArticle]:
        """用 LLM 判断一批文章的相关性"""
        labels = [f"- [{a.source_name}] {a.title[:150]}" for a in articles]
        prompt = f"""你是一个 AI 新闻编辑。以下是一批新闻标题，请选出与 AI 行业**高度相关**的条目（回索引号，用逗号分隔）。

判断标准：
- 核心 AI 发布/公告：GPT、Claude、Gemini 等大模型发布
- AI 研究突破：有影响力的论文、新方法
- AI 行业动态：融资、并购、监管政策
- AI 工具/产品发布：对开发者有用的新工具

排除：
- 仅边缘提及 AI 的泛科技/商业新闻
- 纯教程/如何使用类内容

新闻列表：
{chr(10).join(labels)}

只返回索引号（从 0 开始），用逗号分隔，如：0,3,5"""
        try:
            response = await llm_fn(prompt, model="cheap")
            indices = [int(i.strip()) for i in response.split(",") if i.strip().isdigit()]
            return [articles[i] for i in indices if i < len(articles)]
        except Exception as e:
            print(f"  [WARN] LLM filter error: {e}")
            return []
