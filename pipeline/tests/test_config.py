"""PlatformConfig 加载与解析测试"""

from pathlib import Path
from tempfile import NamedTemporaryFile

import yaml
import pytest

from src.config import AppConfig, PlatformConfig


class TestPlatformConfig:
    """PlatformConfig 模型基础测试"""

    def test_default_disabled(self):
        """平台默认禁用"""
        cfg = PlatformConfig()
        assert cfg.enabled is False

    def test_enabled_explicitly(self):
        """显式启用"""
        cfg = PlatformConfig(enabled=True)
        assert cfg.enabled is True

    def test_with_output_dir(self):
        """可指定独立输出目录"""
        cfg = PlatformConfig(enabled=True, output_dir="/tmp/test")
        assert cfg.output_dir == "/tmp/test"

    def test_output_dir_optional(self):
        """output_dir 可为 None"""
        cfg = PlatformConfig(enabled=True)
        assert cfg.output_dir is None


class TestAppConfigPlatformLoading:
    """AppConfig 中 platforms 加载测试"""

    def test_no_platforms_in_yaml(self, tmp_path: Path):
        """不配置 platforms 时回退为空字典"""
        yml = tmp_path / "config.yaml"
        yml.write_text(yaml.dump({
            "news_sources": [],
        }))
        cfg = AppConfig.load(str(yml))
        assert cfg.platforms == {}

    def test_load_platforms_from_yaml(self, tmp_path: Path):
        """从 YAML 正确加载三个平台"""
        yml = tmp_path / "config.yaml"
        yml.write_text(yaml.dump({
            "platforms": {
                "blog": {"enabled": True},
                "wechat": {"enabled": False},
                "douyin": {"enabled": False},
            },
            "news_sources": [],
        }))
        cfg = AppConfig.load(str(yml))

        assert "blog" in cfg.platforms
        assert "wechat" in cfg.platforms
        assert "douyin" in cfg.platforms

        assert cfg.platforms["blog"].enabled is True
        assert cfg.platforms["wechat"].enabled is False
        assert cfg.platforms["douyin"].enabled is False

    def test_blog_enabled_by_default(self, tmp_path: Path):
        """确认博客默认已启用"""
        yml = tmp_path / "config.yaml"
        yml.write_text(yaml.dump({
            "platforms": {
                "blog": {"enabled": True},
            },
            "news_sources": [],
        }))
        cfg = AppConfig.load(str(yml))
        assert cfg.platforms["blog"].enabled is True

    def test_platform_enable_disable(self, tmp_path: Path):
        """平台可单独启用/禁用"""
        yml = tmp_path / "config.yaml"
        yml.write_text(yaml.dump({
            "platforms": {
                "blog": {"enabled": True},
                "wechat": {"enabled": False},
                "douyin": {"enabled": True},
            },
            "news_sources": [],
        }))
        cfg = AppConfig.load(str(yml))

        assert cfg.platforms["blog"].enabled is True
        assert cfg.platforms["wechat"].enabled is False
        assert cfg.platforms["douyin"].enabled is True

    def test_bool_shorthand_parsing(self, tmp_path: Path):
        """兼容旧格式：直接 bool 值"""
        yml = tmp_path / "config.yaml"
        yml.write_text(yaml.dump({
            "platforms": {
                "blog": True,
                "wechat": False,
            },
            "news_sources": [],
        }))
        cfg = AppConfig.load(str(yml))
        assert cfg.platforms["blog"].enabled is True
        assert cfg.platforms["wechat"].enabled is False

    def test_platform_with_output_dir(self, tmp_path: Path):
        """平台可指定独立 output_dir"""
        yml = tmp_path / "config.yaml"
        yml.write_text(yaml.dump({
            "platforms": {
                "blog": {"enabled": True, "output_dir": "/custom/path"},
            },
            "news_sources": [],
        }))
        cfg = AppConfig.load(str(yml))
        assert cfg.platforms["blog"].output_dir == "/custom/path"
