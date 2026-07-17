"""发布器基类"""

from abc import ABC, abstractmethod

from ..models import AdaptedContent


class BasePublisher(ABC):
    """内容发布器 — 将适配后的内容发布到目标平台"""

    @abstractmethod
    async def publish(self, contents: list[AdaptedContent]) -> int:
        """发布适配后的内容，返回成功发布数量"""
        ...
