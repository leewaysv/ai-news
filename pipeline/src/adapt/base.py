"""适配器基类"""

from abc import ABC, abstractmethod

from ..models import DailyDigest, AdaptedContent


class BaseAdapter(ABC):
    """内容适配器 — 将 DailyDigest 转换为目标平台格式"""

    @abstractmethod
    def adapt(self, digest: DailyDigest) -> list[AdaptedContent]:
        """将早报适配为目标平台的内容格式"""
        ...
