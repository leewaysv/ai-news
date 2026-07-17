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

    def test_all_platform_adapters(self, config_with_blog_enabled):
        """所有平台适配器均已注册"""
        pipeline = Pipeline(config_with_blog_enabled)
        from src.adapt.wechat_adapter import WeChatAdapter
        from src.adapt.douyin_adapter import DouyinAdapter
        assert isinstance(pipeline._get_adapter("wechat"), WeChatAdapter)
        assert isinstance(pipeline._get_adapter("douyin"), DouyinAdapter)
        assert pipeline._get_adapter("unknown") is None

    def test_wechat_publisher_needs_credentials(self, config_with_blog_enabled):
        """wechat publisher 需要 app_id/app_secret 才返回实例"""
        pipeline = Pipeline(config_with_blog_enabled)
        # mock 配置没有 app_id/app_secret，应返回 None
        assert pipeline._get_publisher("wechat") is None
