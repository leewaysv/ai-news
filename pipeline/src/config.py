"""Pipeline 配置管理"""

import os
import re
from pathlib import Path
from typing import Optional

import yaml
from pydantic import BaseModel, Field


def _load_env(env_path: str = ".env") -> None:
    """加载 .env 文件到环境变量"""
    path = Path(env_path)
    if not path.exists():
        return
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, val = line.partition("=")
            key, val = key.strip(), val.strip().strip("\"'")
            if key and not os.environ.get(key):
                os.environ[key] = val


def _resolve_env_vars(value: str) -> str:
    """将字符串中的 ${VAR} 替换为环境变量值"""
    def _replace(m):
        var_name = m.group(1)
        return os.environ.get(var_name, m.group(0))
    return re.sub(r"\$\{(\w+)\}", _replace, value)


class LLMConfig(BaseModel):
    provider: str = "openai"
    api_key: str = ""
    base_url: str = "https://api.deepseek.com"
    model: str = "deepseek-chat"
    cheap_model: str = "deepseek-chat"
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


class PlatformConfig(BaseModel):
    """平台发布配置"""
    enabled: bool = False
    output_dir: str | None = None  # 覆盖 pipeline.output_dir
    app_id: str = ""               # API 凭据（微信等平台）
    app_secret: str = ""           # API 凭据
    method: str = "api"            # 发布方式: "api" | "playwright"


class NewsSourceConfig(BaseModel):
    """Config 文件中的源定义"""
    id: str
    name: str
    type: str
    url: str
    lang: str = "en"
    categories: list[str] = Field(default_factory=list)
    weight: int = 5


class AppConfig(BaseModel):
    """合并文件配置 + 环境变量"""

    llm: LLMConfig = LLMConfig()
    embedding: EmbeddingConfig = EmbeddingConfig()
    pipeline: PipelineConfig = PipelineConfig()
    platforms: dict[str, PlatformConfig] = Field(default_factory=dict)
    news_sources: list[NewsSourceConfig] = Field(default_factory=list)

    @classmethod
    def load(cls, config_path: str = "config.yaml") -> "AppConfig":
        # 1. 加载 .env 到环境变量
        _load_env(".env")

        # 2. 加载 YAML 配置
        path = Path(config_path)
        if not path.exists():
            print(f"[WARN] Config file not found: {config_path}, using defaults")
            return cls()

        with open(path, encoding="utf-8") as f:
            raw = yaml.safe_load(f)

        # 3. 递归解析 env vars
        raw = _resolve_env_vars_recursive(raw)

        llm_cfg = raw.get("llm", {})

        # 4. 确定 API key
        provider = llm_cfg.get("provider", "openai")
        api_key = llm_cfg.get("api_key", "")
        # 如果 api_key 是 "${XXX}" 格式但没被展开，尝试从环境变量读取
        if api_key.startswith("${") and api_key.endswith("}"):
            env_name = api_key[2:-1]
            api_key = os.environ.get(env_name, "")

        llm = LLMConfig(
            provider=provider,
            api_key=api_key,
            base_url=llm_cfg.get("base_url", "https://api.deepseek.com"),
            model=llm_cfg.get("model", "deepseek-chat"),
            cheap_model=llm_cfg.get("cheap_model", "deepseek-chat"),
            max_tokens=llm_cfg.get("max_tokens", 4096),
        )

        emb_cfg = raw.get("embedding", {})
        embedding = EmbeddingConfig(
            model=emb_cfg.get("model", "all-MiniLM-L6-v2"),
            threshold=emb_cfg.get("threshold", 0.75),
        )

        pipe_cfg = raw.get("pipeline", {})
        pipeline = PipelineConfig(
            timezone=pipe_cfg.get("timezone", "Asia/Shanghai"),
            output_dir=pipe_cfg.get("output_dir", "../blog/content/articles"),
            max_articles_per_digest=pipe_cfg.get("max_articles_per_digest", 8),
            min_articles_to_publish=pipe_cfg.get("min_articles_to_publish", 3),
            source_weights=pipe_cfg.get("source_weights", {}),
        )

        sources = [NewsSourceConfig(**s) for s in raw.get("news_sources", [])]

        # 6. 解析平台配置
        raw_platforms = raw.get("platforms", {})
        platforms = {}
        for name, pc in raw_platforms.items():
            if isinstance(pc, dict):
                platforms[name] = PlatformConfig(**pc)
            else:
                platforms[name] = PlatformConfig(enabled=bool(pc))

        return cls(
            llm=llm,
            embedding=embedding,
            pipeline=pipeline,
            platforms=platforms,
            news_sources=sources,
        )

    def get_api_key(self) -> str:
        """获取有效的 API key"""
        key = getattr(self.llm, "api_key", "")
        if key.startswith("${"):
            env_name = key[2:-1]
            key = os.environ.get(env_name, "")
        return key


def _resolve_env_vars_recursive(obj):
    """递归替换对象中所有字符串的 ${VAR}"""
    if isinstance(obj, str):
        return _resolve_env_vars(obj)
    elif isinstance(obj, dict):
        return {k: _resolve_env_vars_recursive(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [_resolve_env_vars_recursive(v) for v in obj]
    return obj
