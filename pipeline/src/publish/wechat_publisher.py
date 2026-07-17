"""微信 API 发布器 — access_token 管理 + 草稿创建 + 发布提交"""
from __future__ import annotations

import json
import logging
import re
import time
from typing import Optional

import httpx

from ..config import PlatformConfig
from ..models import AdaptedContent
from .base import BasePublisher

log = logging.getLogger(__name__)


# ── 常量 ──

WECHAT_API_BASE = "https://api.weixin.qq.com/cgi-bin"
TOKEN_REFRESH_BUFFER = 300  # 提前 5 分钟刷新


# ── WeChatAuth ──


class WeChatAuth:
    """微信公众号 access_token 管理"""

    def __init__(self, app_id: str, app_secret: str):
        self.app_id = app_id
        self.app_secret = app_secret
        self._token: str = ""
        self._expires_at: float = 0

    @classmethod
    def from_config(cls, cfg: PlatformConfig) -> "WeChatAuth":
        return cls(app_id=cfg.app_id, app_secret=cfg.app_secret)

    async def _request_token(self) -> tuple[str, int]:
        """向微信 API 请求新的 access_token，返回 (token, expires_in)"""
        url = f"{WECHAT_API_BASE}/token"
        params = {
            "grant_type": "client_credential",
            "appid": self.app_id,
            "secret": self.app_secret,
        }
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, params=params)
            resp.raise_for_status()
            data = resp.json()
            return data.get("access_token", ""), data.get("expires_in", 0)

    async def get_token(self) -> str:
        """获取有效的 access_token（缓存 or 刷新）"""
        if self._token and time.time() + TOKEN_REFRESH_BUFFER < self._expires_at:
            return self._token
        self._token, expires_in = await self._request_token()
        if expires_in:
            self._expires_at = time.time() + expires_in
        return self._token


# ── WeChatPublisher ──


class WeChatPublisher(BasePublisher):
    """微信公众号发布器"""

    def __init__(self, auth: WeChatAuth):
        self.auth = auth

    async def publish(self, contents: list[AdaptedContent]) -> int:
        """发布适配后的内容到微信公众号"""
        if not contents:
            return 0

        token = await self.auth.get_token()
        if not token:
            log.warning("[wechat] No access_token — skipping publish")
            return 0

        total = 0
        for content_item in contents:
            try:
                total += await self._publish_one(content_item, token)
            except Exception as e:
                log.warning(f"[wechat] Publish error (skipping): {e}")

        return total

    async def _publish_one(self, item: AdaptedContent, token: str) -> int:
        """发布单次草稿，返回文章数"""
        data = json.loads(item.content)
        articles = data.get("articles", [])
        if not articles:
            return 0

        # 1. 上传正文图片到微信 CDN
        for article in articles:
            article["content"] = await self._upload_images(article["content"], token)

        # 2. 创建草稿
        media_id = await self._create_draft(articles, token)
        if not media_id:
            return 0

        # 3. 提交发布
        publish_id = await self._submit_publish(media_id, token)
        if not publish_id:
            log.warning("[wechat] Draft created but publish submission failed")
            return 0

        log.info(f"[wechat] Published {len(articles)} articles (publish_id={publish_id})")
        return len(articles)

    async def _upload_images(self, html_content: str, token: str) -> str:
        """将 HTML 中的外部图片上传到微信 CDN，替换 URL"""
        urls = re.findall(r'<img[^>]+src=["\'](https?://[^"\']+)["\']', html_content)
        if not urls:
            return html_content

        async with httpx.AsyncClient() as client:
            for original_url in urls:
                try:
                    # 下载图片
                    img_resp = await client.get(original_url)
                    img_resp.raise_for_status()

                    # 上传到微信 CDN
                    upload_url = f"{WECHAT_API_BASE}/media/uploadimg?access_token={token}"
                    files = {"media": ("image.jpg", img_resp.content, "image/jpeg")}
                    upload_resp = await client.post(upload_url, files=files)
                    upload_resp.raise_for_status()
                    result = upload_resp.json()

                    if result.get("url"):
                        html_content = html_content.replace(original_url, result["url"])
                except Exception as e:
                    log.warning(f"[wechat] Image upload failed for {original_url}: {e}")

        return html_content

    async def _create_draft(self, articles: list[dict], token: str) -> str:
        """创建草稿，返回 media_id"""
        url = f"{WECHAT_API_BASE}/draft/add?access_token={token}"
        payload = {"articles": articles}

        async with httpx.AsyncClient() as client:
            resp = await client.post(url, json=payload)
            resp.raise_for_status()
            result = resp.json()

        if result.get("errcode", 0) != 0:
            log.warning(f"[wechat] Draft creation failed: {result}")
            return ""

        media_id = result.get("media_id", "")
        if not media_id:
            log.warning("[wechat] No media_id in draft response")
            return ""

        log.info(f"[wechat] Draft created: media_id={media_id}")
        return media_id

    async def _submit_publish(self, media_id: str, token: str) -> str:
        """提交草稿发布，返回 publish_id"""
        url = f"{WECHAT_API_BASE}/freepublish/submit?access_token={token}"
        payload = {"media_id": media_id}

        async with httpx.AsyncClient() as client:
            resp = await client.post(url, json=payload)
            resp.raise_for_status()
            result = resp.json()

        if result.get("errcode", 0) != 0:
            log.warning(f"[wechat] Publish submission failed: {result}")
            return ""

        publish_id = result.get("publish_id", "")
        return str(publish_id) if publish_id else ""
