"""WeChatPublisher TDD 测试

Seams（已确认）:
  1. WeChatAuth        — access_token 管理
  2. WeChatPublisher.publish — 完整发布流程
  3. 错误降级           — API 失败不阻塞管道
"""

import time
from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from src.config import PlatformConfig


# ── Cycle 1: WeChatAuth ──

from src.publish.wechat_publisher import WeChatAuth, WeChatPublisher


class TestWeChatAuth:
    """access_token 生命周期测试"""

    @pytest.fixture
    def auth(self):
        return WeChatAuth(app_id="test_app_id", app_secret="test_secret")

    @pytest.mark.asyncio
    async def test_get_token_first_call(self, auth):
        """首次调用获取新 token"""
        auth._request_token = AsyncMock(return_value=("mock_token", 7200))
        token = await auth.get_token()
        assert token == "mock_token"
        auth._request_token.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_cached_token_reused(self, auth):
        """未过期的 token 被缓存复用"""
        auth._request_token = AsyncMock(return_value=("cached_token", 7200))
        await auth.get_token()  # 首次调用
        auth._request_token.reset_mock()

        token = await auth.get_token()  # 第二次调用
        assert token == "cached_token"
        auth._request_token.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_expired_token_refresh(self, auth):
        """过期后自动刷新 token"""
        # mock 一个过期 token
        auth._token = "expired_token"
        auth._expires_at = time.time() - 10  # 10 秒前过期

        auth._request_token = AsyncMock(return_value=("new_token", 7200))
        token = await auth.get_token()
        assert token == "new_token"
        auth._request_token.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_almost_expired_token_refresh(self, auth):
        """5 分钟内即将过期的 token 也触发刷新"""
        auth._token = "old_token"
        auth._expires_at = time.time() + 120  # 2 分钟后过期（在 5 分钟缓冲区内）

        auth._request_token = AsyncMock(return_value=("fresh_token", 7200))
        token = await auth.get_token()
        assert token == "fresh_token"
        auth._request_token.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_api_error_raises(self, auth):
        """API 调用失败时抛出异常"""
        auth._request_token = AsyncMock(side_effect=httpx.HTTPStatusError(
            "401 Unauthorized", request=MagicMock(), response=MagicMock()
        ))
        with pytest.raises(httpx.HTTPStatusError):
            await auth.get_token()

    @pytest.mark.asyncio
    async def test_invalid_credentials(self, auth):
        """无效凭据返回空 token"""
        auth._request_token = AsyncMock(return_value=("", 0))
        token = await auth.get_token()
        assert token == ""

    @pytest.mark.asyncio
    async def test_config_based_init(self):
        """从 PlatformConfig 初始化"""
        cfg = PlatformConfig(
            enabled=True,
            app_id="cfg_app_id",
            app_secret="cfg_secret",
        )
        auth = WeChatAuth.from_config(cfg)
        assert auth.app_id == "cfg_app_id"
        assert auth.app_secret == "cfg_secret"


# ── Cycle 2: WeChatPublisher.publish ──


class TestWeChatPublisher:
    """完整发布流程测试"""

    @pytest.fixture
    def publisher(self):
        auth = WeChatAuth(app_id="test_id", app_secret="test_secret")
        return WeChatPublisher(auth=auth)

    @pytest.fixture
    def sample_contents(self):
        """一份有效的 WeChat AdaptedContent"""
        from src.models import AdaptedContent
        return [
            AdaptedContent(
                platform="wechat",
                content='{"articles":[{"title":"测试文章","content":"<p>正文</p>","content_source_url":"https://example.com"}]}',
                metadata={"article_count": 1, "digest_date": "2026-07-06"},
            )
        ]

    @pytest.mark.asyncio
    async def test_publish_empty_list(self, publisher):
        """空列表返回 0"""
        result = await publisher.publish([])
        assert result == 0

    @pytest.mark.asyncio
    async def test_publish_uses_access_token(self, publisher, sample_contents):
        """发布流程调用 access_token"""
        token_calls = []

        async def mock_post(url, **kwargs):
            # 执行 publish 逻辑时会调用 auth.get_token()
            if "draft/add" in url:
                token_calls.append(await publisher.auth.get_token())
                return MagicMock(status_code=200, json=lambda: {"errcode": 0, "media_id": "mock_mid"})
            return MagicMock(status_code=200, json=lambda: {"errcode": 0, "errmsg": "ok"})

        with patch.object(httpx, "AsyncClient") as mock_client:
            mock_instance = AsyncMock()
            mock_instance.post = AsyncMock(side_effect=mock_post)
            mock_client.return_value.__aenter__.return_value = mock_instance

            publisher.auth._request_token = AsyncMock(return_value=("test_token", 7200))
            await publisher.publish(sample_contents)

        assert len(token_calls) >= 1

    @pytest.mark.asyncio
    async def test_publish_creates_draft(self, publisher, sample_contents):
        """发布流程调用 draft/add API"""
        api_urls = []

        async def mock_post(url, **kwargs):
            api_urls.append(url)
            return MagicMock(status_code=200, json=lambda: {"errcode": 0, "media_id": "mock_mid"})

        with patch.object(httpx, "AsyncClient") as mock_client:
            mock_instance = AsyncMock()
            mock_instance.post = AsyncMock(side_effect=mock_post)
            mock_client.return_value.__aenter__.return_value = mock_instance

            publisher.auth._request_token = AsyncMock(return_value=("token", 7200))
            await publisher.publish(sample_contents)

        draft_calls = [u for u in api_urls if "draft/add" in u]
        assert len(draft_calls) == 1

    @pytest.mark.asyncio
    async def test_publish_submits_draft(self, publisher, sample_contents):
        """发布流程调用 freepublish/submit API"""
        api_urls = []

        def make_response(data):
            return MagicMock(status_code=200, json=lambda: data)

        async def mock_post(url, **kwargs):
            api_urls.append(url)
            if "draft/add" in url:
                return make_response({"errcode": 0, "media_id": "mock_media_id"})
            return make_response({"errcode": 0, "publish_id": "mock_pid"})

        with patch.object(httpx, "AsyncClient") as mock_client:
            mock_instance = AsyncMock()
            mock_instance.post = AsyncMock(side_effect=mock_post)
            mock_client.return_value.__aenter__.return_value = mock_instance

            publisher.auth._request_token = AsyncMock(return_value=("token", 7200))
            await publisher.publish(sample_contents)

        submit_calls = [u for u in api_urls if "freepublish/submit" in u]
        assert len(submit_calls) == 1

    @pytest.mark.asyncio
    async def test_publish_returns_article_count(self, publisher, sample_contents):
        """发布成功返回文章数"""
        def make_response(data):
            return MagicMock(status_code=200, json=lambda: data)

        async def mock_post(url, **kwargs):
            if "draft/add" in url:
                return make_response({"errcode": 0, "media_id": "mock_media_id"})
            # freepublish/submit 需要 publish_id
            return make_response({"errcode": 0, "publish_id": "12345"})

        with patch.object(httpx, "AsyncClient") as mock_client:
            mock_instance = AsyncMock()
            mock_instance.post = AsyncMock(side_effect=mock_post)
            mock_client.return_value.__aenter__.return_value = mock_instance

            publisher.auth._request_token = AsyncMock(return_value=("token", 7200))
            result = await publisher.publish(sample_contents)
            assert result == 1

    @pytest.mark.asyncio
    async def test_publish_with_images(self, publisher):
        """正文中的图片 URL 被上传到微信 CDN"""
        from src.models import AdaptedContent
        img_html = '<p><img src=\\"https://example.com/image.jpg\\" /></p>'
        content = AdaptedContent(
            platform="wechat",
            content=f'{{"articles":[{{"title":"test","content":"{img_html}","content_source_url":"https://example.com"}}]}}',
            metadata={"article_count": 1},
        )

        api_urls = []

        def make_response(data):
            return MagicMock(status_code=200, json=lambda: data)

        async def mock_post(url, **kwargs):
            api_urls.append(url)
            if "uploadimg" in url:
                return make_response({"url": "https://mmbiz.qpic.cn/new_image"})
            if "draft/add" in url:
                return make_response({"errcode": 0, "media_id": "mid"})
            # Return a successful response for the image download (GET)
            return MagicMock(status_code=200, json=lambda: {"errcode": 0})

        with patch.object(httpx, "AsyncClient") as mock_client:
            mock_instance = AsyncMock()
            # Both GET (image download) and POST (upload/draft/publish)
            mock_instance.get = AsyncMock(return_value=MagicMock(status_code=200, content=b"fake_image_data"))
            mock_instance.post = AsyncMock(side_effect=mock_post)
            mock_client.return_value.__aenter__.return_value = mock_instance

            publisher.auth._request_token = AsyncMock(return_value=("token", 7200))
            await publisher.publish([content])

        upload_calls = [u for u in api_urls if "uploadimg" in u]
        assert len(upload_calls) >= 1


# ── Cycle 3: 错误降级 ──


class TestWechatErrorResilience:
    """API 失败时不应阻断管道"""

    @pytest.fixture
    def publisher(self):
        return WeChatPublisher(auth=WeChatAuth(app_id="id", app_secret="secret"))

    @pytest.fixture
    def sample(self):
        from src.models import AdaptedContent
        return [AdaptedContent(
            platform="wechat",
            content='{"articles":[{"title":"t","content":"<p>c</p>","content_source_url":"https://ex.com"}]}',
        )]

    @pytest.mark.asyncio
    async def test_api_error_returns_zero(self, publisher, sample):
        """API 调用失败返回 0，不抛异常"""
        async def failing_post(url, **kwargs):
            raise httpx.HTTPStatusError("500", request=MagicMock(), response=MagicMock())

        with patch.object(httpx, "AsyncClient") as mock_client:
            mock_instance = AsyncMock()
            mock_instance.post = AsyncMock(side_effect=failing_post)
            mock_client.return_value.__aenter__.return_value = mock_instance
            publisher.auth._request_token = AsyncMock(return_value=("t", 7200))

            result = await publisher.publish(sample)
            assert result == 0

    @pytest.mark.asyncio
    async def test_empty_token_returns_zero(self, publisher, sample):
        """空 token 时跳过发布"""
        publisher.auth._request_token = AsyncMock(return_value=("", 0))
        result = await publisher.publish(sample)
        assert result == 0

    @pytest.mark.asyncio
    async def test_draft_failure_does_not_crash(self, publisher, sample):
        """草稿创建失败不阻断"""
        async def mock_post(url, **kwargs):
            if "draft/add" in url:
                return MagicMock(status_code=200, json=lambda: {"errcode": -1, "errmsg": "fail"})
            return MagicMock(status_code=200, json=lambda: {"errcode": 0, "publish_id": "ok"})

        with patch.object(httpx, "AsyncClient") as mock_client:
            mock_instance = AsyncMock()
            mock_instance.post = AsyncMock(side_effect=mock_post)
            mock_client.return_value.__aenter__.return_value = mock_instance
            publisher.auth._request_token = AsyncMock(return_value=("t", 7200))

            result = await publisher.publish(sample)  # 不应抛异常
            assert result == 0  # 草稿失败，发布 0 篇

    @pytest.mark.asyncio
    async def test_publish_failure_does_not_crash(self, publisher, sample):
        """发布提交失败不阻断"""
        async def mock_post(url, **kwargs):
            if "draft/add" in url:
                return MagicMock(status_code=200, json=lambda: {"errcode": 0, "media_id": "mid"})
            # freepublish/submit 失败
            return MagicMock(status_code=200, json=lambda: {"errcode": -1, "errmsg": "fail"})

        with patch.object(httpx, "AsyncClient") as mock_client:
            mock_instance = AsyncMock()
            mock_instance.post = AsyncMock(side_effect=mock_post)
            mock_client.return_value.__aenter__.return_value = mock_instance
            publisher.auth._request_token = AsyncMock(return_value=("t", 7200))

            result = await publisher.publish(sample)
            assert result == 0
