"""平台适配器/发布器分发测试"""

import pytest

from src.main import Pipeline
from src.config import AppConfig
from src.adapt.blog_adapter import BlogAdapter
from src.adapt.base import BaseAdapter
from src.publish.blog_publisher import BlogPublisher
from src.publish.base import BasePublisher


@pytest.fixture
def config_with_blog_enabled():
    """仅 blog 启用的配置"""
    cfg = AppConfig()
    cfg.platforms = {
        "blog": type("obj", (object,), {"enabled": True, "output_dir": None})(),
        "wechat": type("obj", (object,), {"enabled": False, "output_dir": None})(),
        "douyin": type("obj", (object,), {"enabled": False, "output_dir": None})(),
    }
    return cfg


class TestPlatformDispatch:
    """测试 Pipeline 平台分发逻辑"""

    def test_get_blog_adapter(self, config_with_blog_enabled):
        """blog 平台返回 BlogAdapter 实例"""
        pipeline = Pipeline(config_with_blog_enabled)
        adapter = pipeline._get_adapter("blog")
        assert adapter is not None
        assert isinstance(adapter, BlogAdapter)
        assert isinstance(adapter, BaseAdapter)

    def test_get_blog_publisher(self, config_with_blog_enabled):
        """blog 平台返回 BlogPublisher 实例"""
        pipeline = Pipeline(config_with_blog_enabled)
        publisher = pipeline._get_publisher("blog")
        assert publisher is not None
        assert isinstance(publisher, BlogPublisher)
        assert isinstance(publisher, BasePublisher)

    def test_get_unknown_platform_adapter(self, config_with_blog_enabled):
        """未注册的平台返回 None"""
        pipeline = Pipeline(config_with_blog_enabled)
        assert pipeline._get_adapter("unknown") is None

    def test_get_unknown_platform_publisher(self, config_with_blog_enabled):
        """未注册的平台发布器返回 None"""
        pipeline = Pipeline(config_with_blog_enabled)
        assert pipeline._get_publisher("unknown") is None

    def test_future_platforms_return_none(self, config_with_blog_enabled):
        """wechat 和 douyin 尚未实现，返回 None"""
        pipeline = Pipeline(config_with_blog_enabled)
        assert pipeline._get_adapter("wechat") is None
        assert pipeline._get_adapter("douyin") is None
