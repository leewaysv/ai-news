"""博客适配器 — DailyDigest → Hugo Markdown"""

from datetime import datetime
from pathlib import Path

from ..models import DailyDigest, AdaptedContent, ProcessedArticle
from .base import BaseAdapter


class BlogAdapter(BaseAdapter):
    """将早报适配为 Hugo Markdown 文件"""

    def __init__(self, output_dir: str):
        self.output_dir = Path(output_dir)

    def adapt(self, digest: DailyDigest) -> list[AdaptedContent]:
        """生成 Hugo 兼容的 .md 文件"""
        contents = []

        for article in digest.articles:
            md = self._article_to_md(article, digest)
            slug = self._safe_slug(article.title)[:60]
            file_name = f"{digest.date}-{slug}.md"
            file_path = self.output_dir / file_name
            blog_url = f"https://ai-news-2li.pages.dev/articles/{digest.date}-{slug}/"

            contents.append(AdaptedContent(
                platform="blog",
                file_path=str(file_path),
                content=md,
                metadata={
                    "title": article.title,
                    "date": digest.date,
                    "slug": slug,
                    "blog_url": blog_url,
                },
            ))

        return contents

    def _article_to_md(self, article: ProcessedArticle, digest: DailyDigest) -> str:
        """生成 Hugo 兼容的 Markdown — 标题 + 例图 + 摘要 + 详细分析"""
        pub_time = article.published_at or datetime.now()
        slug = self._safe_slug(article.title)[:40]

        frontmatter = {
            "title": article.title,
            "date": pub_time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
            "slug": slug,
            "source": article.source_name,
            "source_url": article.raw_url,
            "categories": article.categories,
            "tags": article.tags,
            "summary": article.summary,
            "aigc": article.aigc_label,
        }

        if article.image_url:
            frontmatter["image"] = article.image_url

        # YAML frontmatter
        yaml_lines = ["---"]
        for key, value in frontmatter.items():
            if isinstance(value, list):
                yaml_lines.append(f"{key}:")
                for v in value:
                    yaml_lines.append(f"  - {v}")
            elif isinstance(value, bool):
                yaml_lines.append(f"{key}: {str(value).lower()}")
            else:
                yaml_lines.append(f'{key}: "{value}"')
        yaml_lines.append("---")

        # 正文
        body_parts = []

        # 摘要
        body_parts.append(article.summary)
        body_parts.append("")

        # 详细分析
        if article.detailed_analysis:
            body_parts.append("## 详细分析\n")
            body_parts.append(article.detailed_analysis)
            body_parts.append("")

        # 编辑点评
        if article.analysis:
            body_parts.append(f"> *{article.analysis}*")
            body_parts.append("")

        # 原文链接
        body_parts.append(f"> 原文：[{article.source_name}]({article.raw_url})")

        return "\n".join(yaml_lines) + "\n" + "\n".join(body_parts)

    @staticmethod
    def _safe_slug(text: str) -> str:
        import re
        slug = re.sub(r'[^a-zA-Z0-9\s-]', '', text)
        slug = slug.strip().replace(' ', '-').lower()[:80]
        slug = re.sub(r'-+', '-', slug)
        return slug.strip('-')
