"""Pipeline 配置管理"""

from pathlib import Path
from typing import Optional

import yaml
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class LLMConfig(BaseModel):
    api_key: str = ""
    model: str = "claude-sonnet-5-20251001"
    cheap_model: str = "claude-haiku-4-5-20251001"
    max_tokens: int = 4096


class EmbeddingConfig(BaseModel):
    model: str = "all-MiniLM-L6-v2"
    threshold: float = 0.75


class PipelineConfig(BaseModel):
    timezone: str = "Asia/Shanghai"
    output_dir: str = "../blog/content/articles"
    max_articles_per_digest: int = 8
    min_articles_to_publish: int = 3
    source_weights: dict[str, int] = Field(default_factory=dict)


class NewsSourceConfig(BaseModel):
    """Config 文件中的源定义"""
    id: str
    name: str
    type: str
    url: str
    lang: str = "en"
    categories: list[str] = Field(default_factory=list)
    weight: int = 5


class AppConfig(BaseSettings):
    """合并文件配置 + 环境变量"""
    model_config = SettingsConfigDict(
        env_prefix="AI_NEWS_",
        env_file=".env",
        extra="ignore",
    )

    llm: LLMConfig = LLMConfig()
    embedding: EmbeddingConfig = EmbeddingConfig()
    pipeline: PipelineConfig = PipelineConfig()
    news_sources: list[NewsSourceConfig] = Field(default_factory=list)

    # 从环境变量覆盖
    anthropic_api_key: str = ""

    @classmethod
    def load(cls, config_path: str = "config.yaml") -> "AppConfig":
        path = Path(config_path)
        if not path.exists():
            print(f"[WARN] Config file not found: {config_path}, using defaults")
            return cls()

        with open(path, encoding="utf-8") as f:
            raw = yaml.safe_load(f)

        llm_cfg = raw.get("llm", {})
        llm = LLMConfig(
            api_key=llm_cfg.get("api_key", ""),
            model=llm_cfg.get("model", LLMConfig.model),
            cheap_model=llm_cfg.get("cheap_model", LLMConfig.cheap_model),
            max_tokens=llm_cfg.get("max_tokens", LLMConfig.max_tokens),
        )

        emb_cfg = raw.get("embedding", {})
        embedding = EmbeddingConfig(
            model=emb_cfg.get("model", EmbeddingConfig.model),
            threshold=emb_cfg.get("threshold", EmbeddingConfig.threshold),
        )

        pipe_cfg = raw.get("pipeline", {})
        pipeline = PipelineConfig(
            timezone=pipe_cfg.get("timezone", PipelineConfig.timezone),
            output_dir=pipe_cfg.get("output_dir", PipelineConfig.output_dir),
            max_articles_per_digest=pipe_cfg.get(
                "max_articles_per_digest", PipelineConfig.max_articles_per_digest
            ),
            min_articles_to_publish=pipe_cfg.get(
                "min_articles_to_publish", PipelineConfig.min_articles_to_publish
            ),
            source_weights=pipe_cfg.get("source_weights", {}),
        )

        sources = [NewsSourceConfig(**s) for s in raw.get("news_sources", [])]

        return cls(
            llm=llm,
            embedding=embedding,
            pipeline=pipeline,
            news_sources=sources,
        )

    def get_api_key(self) -> str:
        return self.anthropic_api_key or self.llm.api_key or ""
