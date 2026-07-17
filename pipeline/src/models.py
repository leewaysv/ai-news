"""AI News Pipeline 数据模型"""

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class SourceType(str, Enum):
    RSS = "rss"
    API = "api"
    SCRAPE = "scrape"


class NewsSource(BaseModel):
    """新闻源定义"""
    id: str
    name: str
    type: SourceType
    url: str
    lang: str = "en"
    categories: list[str] = Field(default_factory=list)
    weight: int = 5


class RawArticle(BaseModel):
    """采集后的原始文章"""
    source_id: str
    source_name: str
    url: str
    title: str
    content: str
    author: Optional[str] = None
    published_at: Optional[datetime] = None
    lang: str = "en"
    categories: list[str] = Field(default_factory=list)
    score: float = 0.5
    dedup_hash: Optional[str] = None


class ProcessedArticle(BaseModel):
    """LLM 处理后的文章"""
    id: str
    raw_url: str
    source_name: str
    original_title: str
    title: str
    summary: str
    key_points: list[str] = Field(default_factory=list)
    detailed_analysis: Optional[str] = None
    analysis: Optional[str] = None
    categories: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    published_at: Optional[datetime] = None
    aigc_label: bool = True
    embedding_pass: bool = True
    image_url: Optional[str] = None


class DailyDigest(BaseModel):
    """每日早报"""
    date: str  # YYYY-MM-DD
    title: str
    articles: list[ProcessedArticle] = Field(default_factory=list)
    editor_note: Optional[str] = None


class AdaptedContent(BaseModel):
    """适配后的内容 — 适配器输出格式"""
    platform: str  # "blog" | "wechat" | "douyin"
    file_path: Optional[str] = None
    content: str   # Markdown / HTML / script
    metadata: dict = Field(default_factory=dict)
