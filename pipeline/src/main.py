"""AI News Pipeline — 主入口

工作流：gather → filter → summarize → qa → adapt → publish
"""

import asyncio
import logging
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional

import click

from .config import AppConfig
from .gather.rss_collector import RSSCollector
from .gather.api_collector import APICollector
from .gather.scraper import Scraper
from .filter.classifier import RelevanceClassifier
from .filter.dedup import Deduplicator
from .summarize.summarizer import Summarizer
from .adapt.base import BaseAdapter
from .adapt.blog_adapter import BlogAdapter
from .publish.base import BasePublisher
from .publish.blog_publisher import BlogPublisher
from .qa.embedding_check import EmbeddingQualityCheck
from .qa.fallback import FallbackHandler
from .compliance.aigc_label import AIGCLabeler

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger(__name__)


class Pipeline:
    """完整 AI 新闻管道"""

    def __init__(self, config: AppConfig):
        self.config = config
        self.rss_collector = RSSCollector()
        self.api_collector = APICollector()
        self.scraper = Scraper()
        self.classifier = RelevanceClassifier()
        self.dedup = Deduplicator()
        self.llm_client = None  # 运行时初始化
        self.summarizer = None
        self.qa_check = EmbeddingQualityCheck(
            model_name=config.embedding.model,
            threshold=config.embedding.threshold,
        )
        self.fallback = FallbackHandler(
            min_articles=config.pipeline.min_articles_to_publish
        )
        self.labeler = AIGCLabeler()

    # ── 平台适配器/发布器工厂 ──

    def _get_adapter(self, platform: str) -> BaseAdapter | None:
        """根据平台名获取适配器实例"""
        cfg = self.config.platforms.get(platform)
        output_dir = (cfg.output_dir or self.config.pipeline.output_dir) if cfg else self.config.pipeline.output_dir

        if platform == "blog":
            return BlogAdapter(output_dir)
        # 未来扩展：wechat → WeChatAdapter, douyin → DouyinAdapter
        return None

    def _get_publisher(self, platform: str) -> BasePublisher | None:
        """根据平台名获取发布器实例"""
        cfg = self.config.platforms.get(platform)
        output_dir = (cfg.output_dir or self.config.pipeline.output_dir) if cfg else self.config.pipeline.output_dir

        if platform == "blog":
            return BlogPublisher(output_dir)
        return None

    async def _llm_call(self, prompt: str, model: str = "main") -> str:
        """LLM 调用封装（支持 OpenAI 兼容接口 / Anthropic）"""
        model_id = (
            self.config.llm.model
            if model == "main"
            else self.config.llm.cheap_model
        )
        key = self.config.get_api_key()
        if not key:
            raise ValueError("API key not configured")

        if self.config.llm.provider == "anthropic":
            return await self._call_anthropic(prompt, model_id, key)
        else:
            return await self._call_openai(prompt, model_id, key)

    async def _call_openai(self, prompt: str, model_id: str, key: str) -> str:
        """调用 OpenAI 兼容接口（DeepSeek 等）"""
        from openai import AsyncOpenAI
        client = AsyncOpenAI(
            api_key=key,
            base_url=self.config.llm.base_url,
        )
        response = await client.chat.completions.create(
            model=model_id,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=self.config.llm.max_tokens,
        )
        return response.choices[0].message.content or ""

    async def _call_anthropic(self, prompt: str, model_id: str, key: str) -> str:
        """调用 Anthropic Claude API"""
        import anthropic
        client = anthropic.AsyncAnthropic(api_key=key)
        response = await client.messages.create(
            model=model_id,
            max_tokens=self.config.llm.max_tokens,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.content[0].text

    def _get_weight(self, source_id: str) -> int:
        """获取源权重"""
        return self.config.pipeline.source_weights.get(
            source_id,
            self.config.pipeline.source_weights.get("default", 5),
        )

    async def run(self, dry_run: bool = False) -> int:
        """执行单次管道运行"""
        date_str = (datetime.now(timezone.utc) + timedelta(hours=8)).strftime("%Y-%m-%d")
        log.info(f"=== AI News Pipeline — {date_str} ===")

        # ── Step 1: Gather ──
        log.info("[1/6] Gathering news...")
        all_articles = []

        # RSS 源
        rss_sources = [s for s in self.config.news_sources if s.type == "rss"]
        for src in rss_sources:
            articles = self.rss_collector.fetch(src)
            all_articles.extend(articles)

        # API 源
        api_sources = [s for s in self.config.news_sources if s.type == "api"]
        for src in api_sources:
            articles = await self.api_collector.fetch(src)
            all_articles.extend(articles)

        # Scrape 源
        scrape_sources = [s for s in self.config.news_sources if s.type == "scrape"]
        for src in scrape_sources:
            articles = await self.scraper.fetch(src)
            all_articles.extend(articles)

        log.info(f"  Total raw: {len(all_articles)}")

        # ── Step 2: Dedup ──
        log.info("[2/6] Deduplicating...")
        self.dedup.reset()
        all_articles = self.dedup.dedup(all_articles)
        log.info(f"  After dedup: {len(all_articles)}")

        # ── Step 3: Filter ──
        log.info("[3/6] Filtering...")
        filtered = []
        for article in all_articles:
            result = self.classifier.quick_filter(article)
            if result:
                filtered.append(result)

        # LLM 精判（英文源）
        en_candidates = [a for a in filtered if a.lang == "en"]
        en_filtered = await self.classifier.llm_filter(en_candidates, self._llm_call)
        zh_candidates = [a for a in filtered if a.lang == "zh"]
        filtered = zh_candidates + en_filtered
        log.info(f"  After filter: {len(filtered)}")

        if dry_run:
            log.info(f"[DRY-RUN] Stopping after filter. Would summarize {len(filtered)} articles.")
            for a in filtered[:5]:
                log.info(f"  → {a.source_name}: {a.title[:80]}")
            return len(filtered)

        if not filtered:
            log.warning("No articles after filter — skipping today")
            return 0

        # ── Step 4: Summarize ──
        log.info("[4/6] Summarizing...")
        if self.summarizer is None:
            self.summarizer = Summarizer(self._llm_call)

        processed = []
        raw_map = {}
        for article in filtered:
            result = await self.summarizer.summarize_one(article)
            if result:
                processed.append(result)
                raw_map[result.raw_url] = article

        log.info(f"  Summarized: {len(processed)}")

        # ── Step 5: QA ──
        log.info("[5/6] Quality check...")
        # embedding 一致性检查
        passed = self.qa_check.batch_check(processed, raw_map)
        log.info(f"  QA passed: {len(passed)}")

        # 兜底检查
        if not self.fallback.should_publish(len(passed)):
            self.fallback.log_skip(date_str, f"Only {len(passed)} articles passed QA")
            return 0

        # 分配权重排序（热度优先）
        for article in passed:
            pass  # 已按来源权重排序
        passed.sort(
            key=lambda a: self._get_weight(
                next((s.id for s in self.config.news_sources if s.name == a.source_name), "default")
            ),
            reverse=True,
        )

        # 截断到每日最大篇数
        passed = passed[: self.config.pipeline.max_articles_per_digest]

        # AIGC 标注
        for article in passed:
            self.labeler.label(article)

        # ── Step 6: Adapt & Publish ──
        log.info("[6/6] Adapting & publishing...")

        # 创建 daily digest
        digest_data = await self.summarizer.create_digest(passed, date_str)

        from .models import DailyDigest
        digest = DailyDigest(**digest_data)

        # 遍历已启用平台
        total_count = 0
        for platform_name, platform_cfg in self.config.platforms.items():
            if not platform_cfg.enabled:
                log.info(f"  [{platform_name}] Skipped (disabled)")
                continue

            adapter = self._get_adapter(platform_name)
            publisher = self._get_publisher(platform_name)
            if not adapter or not publisher:
                log.warning(f"  [{platform_name}] No adapter/publisher registered")
                continue

            adapted = adapter.adapt(digest)
            count = publisher.publish(adapted)
            log.info(f"  [{platform_name}] Published: {count} articles")
            total_count += count

        if not self.config.platforms:
            # 无 platforms 配置时，回退到原 blog-only 行为
            adapted = BlogAdapter(self.config.pipeline.output_dir).adapt(digest)
            total_count = BlogPublisher(self.config.pipeline.output_dir).publish(adapted)
            log.info(f"  [blog] Published: {total_count} articles (legacy fallback)")

        log.info("=== Done ===")
        return total_count


@click.command()
@click.option("--config", "-c", default="config.yaml", help="配置文件路径")
@click.option("--dry-run", is_flag=True, help="只收集和过滤，不发布")
def cli(config: str, dry_run: bool):
    """AI News 早报管道 — 每日自动化"""
    cfg = AppConfig.load(config)

    if not cfg.get_api_key():
        click.echo("ERROR: LLM API key not set", err=True)
        click.echo(f"Set it via: export DEEPSEEK_API_KEY=sk-... (provider: {cfg.llm.provider})", err=True)
        raise SystemExit(1)

    pipeline = Pipeline(cfg)
    count = asyncio.run(pipeline.run(dry_run=dry_run))
    click.echo(f"\nPublished {count} articles.")


if __name__ == "__main__":
    cli()
