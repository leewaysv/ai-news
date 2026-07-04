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
            file_name = f"{digest.date}-{self._safe_slug(article.id)}.md"
            file_path = self.output_dir / file_name

            contents.append(AdaptedContent(
                platform="blog",
                file_path=str(file_path),
                content=md,
                metadata={
                    "title": article.title,
                    "date": digest.date,
                    "slug": article.id,
                },
            ))

        return contents

    def _article_to_md(self, article: ProcessedArticle, digest: DailyDigest) -> str:
        """单篇文章 → Hugo frontmatter + Markdown"""
        pub_time = article.published_at or datetime.now()
        frontmatter = {
            "title": article.title,
            "date": pub_time.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
            "slug": self._safe_slug(article.id),
            "source": article.source_name,
            "source_url": article.raw_url,
            "categories": article.categories,
            "tags": article.tags,
            "summary": article.summary,
            "aigc": article.aigc_label,
        }

        # 生成 YAML frontmatter
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
        body = f"{article.summary}\n\n"
        if article.key_points:
            body += "## 关键要点\n\n"
            for pt in article.key_points:
                body += f"- **{pt}**\n"
            body += "\n"
        body += article.analysis or ""
        body += f"\n\n> 原文：[{article.source_name}]({article.raw_url})"

        return "\n".join(yaml_lines) + "\n" + body

    @staticmethod
    def _safe_slug(text: str) -> str:
        import re
        slug = re.sub(r'[^a-zA-Z0-9一-鿿\s-]', '', text)
        slug = slug.strip().replace(' ', '-').lower()[:80]
        return slug.replace('--', '-')
