"""博客发布器 — 将适配后的内容写入文件"""

import logging
from pathlib import Path

from ..models import AdaptedContent
from .base import BasePublisher

log = logging.getLogger(__name__)


class BlogPublisher(BasePublisher):
    """将适配后的内容写入 Hugo content 目录"""

    def __init__(self, output_dir: str):
        self.output_dir = Path(output_dir)

    async def publish(self, contents: list[AdaptedContent]) -> int:
        """写入所有文章文件，返回写入数量"""
        self.output_dir.mkdir(parents=True, exist_ok=True)
        count = 0

        for content in contents:
            if not content.file_path:
                continue

            file_path = Path(content.file_path)
            file_path.parent.mkdir(parents=True, exist_ok=True)

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content.content)

            log.info("[PUBLISH] %s", file_path.name)
            count += 1

        return count
