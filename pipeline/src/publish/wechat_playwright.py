"""Playwright 微信公众号发布器 — 浏览器自动化发布

适用于个人订阅号（无需 API 认证）。
流程：扫码登录 → 持久化 Cookie → 新建草稿 → 填入内容 → 提交发布
"""
from __future__ import annotations

import json
import logging
import os
from pathlib import Path
from typing import Optional

from ..models import AdaptedContent
from .base import BasePublisher

log = logging.getLogger(__name__)

# 默认 Cookie 文件路径（相对于项目根目录）
DEFAULT_COOKIE_FILE = ".wechat_cookies.json"
# 登录超时（秒）
LOGIN_TIMEOUT = 120
# 草稿编辑器 URL
DRAFT_EDITOR_URL = (
    "https://mp.weixin.qq.com/cgi-bin/appmsg"
    "?t=media/appmsg_edit&action=edit"
    "&type=10&create=1&sub=create"
)


class PlaywrightWeChatPublisher(BasePublisher):
    """基于 Playwright 的微信公众号内容发布器

    通过浏览器自动登录 mp.weixin.qq.com，创建草稿并提交发布。
    首次运行需要扫码登录，之后自动复用 Cookie。
    """

    def __init__(
        self,
        cookie_file: str = DEFAULT_COOKIE_FILE,
        headless: bool = True,
        auto_publish: bool = True,
    ):
        self.cookie_file = cookie_file
        self.headless = headless
        self.auto_publish = auto_publish  # 发布 or 仅存草稿

    async def publish(self, contents: list[AdaptedContent]) -> int:
        """发布适配后的内容到微信公众号"""
        if not contents:
            return 0

        try:
            from playwright.async_api import async_playwright
        except ImportError:
            log.error("[wechat-playwright] playwright not installed. Run: pip install playwright && playwright install chromium")
            return 0

        total = 0
        async with async_playwright() as pw:
            browser = await pw.chromium.launch(headless=self.headless)
            context = await browser.new_context(
                viewport={"width": 1280, "height": 800},
                locale="zh-CN",
            )

            # 尝试加载已保存的 Cookie
            if os.path.exists(self.cookie_file):
                with open(self.cookie_file) as f:
                    cookies = json.load(f)
                await context.add_cookies(cookies)
                log.info(f"[wechat-playwright] Loaded {len(cookies)} cookies from {self.cookie_file}")

            page = await context.new_page()

            # 登录
            if not await self._ensure_login(page, context):
                log.error("[wechat-playwright] Login failed — aborting")
                await browser.close()
                return 0

            # 遍历每一篇内容
            for item in contents:
                try:
                    data = json.loads(item.content)
                    articles = data.get("articles", [])
                    for article in articles:
                        ok = await self._create_and_publish(page, article)
                        if ok:
                            total += 1
                except Exception as e:
                    log.warning(f"[wechat-playwright] Publish error (skipping): {e}")

            await browser.close()

        log.info(f"[wechat-playwright] Published {total} articles")
        return total

    async def _ensure_login(self, page, context) -> bool:
        """确保已登录。返回是否登录成功。"""
        # 直接访问后台列表页
        await page.goto(
            "https://mp.weixin.qq.com/cgi-bin/appmsg?t=media/appmsg_list&action=list&lang=zh_CN",
            wait_until="domcontentloaded",
        )
        await page.wait_for_timeout(4000)

        # 检查是否已登录（页面包含后台内容而非登录页或超时）
        body_text = (await page.text_content("body") or "").lower()
        is_logged_in = "登录超时" not in body_text and "请重新登录" not in body_text

        if is_logged_in:
            log.info("[wechat-playwright] Already logged in")
            await self._save_cookies(context)
            return True

        # 需要登录：清空过期 cookie，等待扫码
        log.info("[wechat-playwright] Session expired or not logged in — showing QR code...")
        await page.goto("https://mp.weixin.qq.com/", wait_until="domcontentloaded")
        await page.wait_for_timeout(3000)

        # 保存二维码截图
        qr_path = "wechat_qrcode.png"
        await page.screenshot(path=qr_path)
        print(f"\n{'='*60}")
        print(f"  ⚠️ 请用微信扫描: {os.path.abspath(qr_path)}")
        print(f"  超时: {LOGIN_TIMEOUT}s")
        print(f"{'='*60}\n")

        # 等待登录成功后页面跳转到后台
        try:
            await page.wait_for_function(
                "() => window.location.href.includes('/cgi-bin/')",
                timeout=LOGIN_TIMEOUT * 1000,
            )
            log.info("[wechat-playwright] Login successful!")
            await self._save_cookies(context)
            return True
        except Exception:
            log.error("[wechat-playwright] Login timeout or failed")
            return False

    async def _save_cookies(self, context):
        """保存 Cookie 到文件"""
        cookies = await context.cookies()
        with open(self.cookie_file, "w") as f:
            json.dump(cookies, f)
        log.info(f"[wechat-playwright] Saved {len(cookies)} cookies to {self.cookie_file}")

    async def _create_and_publish(self, page, article: dict) -> bool:
        """创建草稿并发布"""
        title = article.get("title", "")
        content = article.get("content", "")
        source_url = article.get("content_source_url", "")

        if not title or not content:
            log.warning("[wechat-playwright] Skipping article with empty title or content")
            return False

        try:
            # 1. 从当前 URL 提取 token
            import re
            token_match = re.search(r'token=(\d+)', page.url)
            token = token_match.group(1) if token_match else ""

            # 2. 导航到草稿箱列表页
            list_url = (
                "https://mp.weixin.qq.com/cgi-bin/appmsg"
                f"?begin=0&count=10&type=77&action=list_card"
                f"&token={token}&lang=zh_CN"
            )
            await page.goto(list_url, wait_until="domcontentloaded")
            await page.wait_for_timeout(5000)

            # 3. 点击"新的创作"按钮
            create_btn = page.locator(
                "button:has-text('新的创作'), "
                ".weui-desktop-btn_primary:has-text('创作')"
            )
            if await create_btn.count() > 0:
                await create_btn.first.click()
                log.info("[wechat-playwright] Clicked '新的创作'")
            else:
                log.warning("[wechat-playwright] No '新的创作' button")
                return False

            # 4. 等待编辑器弹窗完全加载
            await page.wait_for_timeout(4000)

            # 5. 用 JS 强制填入标题
            await page.evaluate("""(t) => {
                const el = document.querySelector('#title');
                if (el) {
                    el.style.visibility = 'visible';
                    el.style.height = 'auto';
                    el.value = t;
                }
            }""", title)
            log.info(f"[wechat-playwright] Title set via JS: {title[:30]}...")

            # 6. 设置内容（通过 JS 直接操作编辑器 DOM）
            await page.evaluate("""(html) => {
                const el = document.querySelector(
                    '.editor-content-area, .rich_media_content, [contenteditable="true"]'
                );
                if (el) el.innerHTML = html;
            }""", content)
            log.info("[wechat-playwright] Content set via JS")

            # 7. 设置原文链接
            if source_url:
                await page.evaluate("""(url) => {
                    const el = document.querySelector(
                        '#original_url, #content_url, input[name="source_url"]'
                    );
                    if (el) el.value = url;
                }""", source_url)

            # 8. 保存草稿（用 JS 触发）
            await page.evaluate("""() => {
                const btn = document.querySelector(
                    '#sbar_btn_save, .save-btn, .weui-desktop-btn_primary'
                );
                if (btn) btn.click();
            }""")
            await page.wait_for_timeout(3000)
            log.info("[wechat-playwright] Save triggered")

            if self.auto_publish:
                await self._submit_publish(page)

            return True

        except Exception as e:
            log.warning(f"[wechat-playwright] Draft creation failed: {e}")
            return False

    async def _set_editor_content(self, page, html_content: str):
        """在编辑器中设置 HTML 内容"""
        # 尝试多种方式定位编辑器

        # 方式1: 通过 iframe 找到编辑器
        editor_frame = page.frame_locator("#ueditor_0 iframe")
        if await editor_frame.locator("body").count() > 0:
            await editor_frame.locator("body").evaluate(
                "el => el.innerHTML = arguments[0]", html_content
            )
            log.info("[wechat-playwright] Content set via iframe body")
            return

        # 方式2: 直接查找 contenteditable 元素
        editor = page.locator('[contenteditable="true"]')
        if await editor.count() > 0:
            await editor.evaluate(
                "el => el.innerHTML = arguments[0]", html_content
            )
            log.info("[wechat-playwright] Content set via contenteditable")
            return

        # 方式3: 先点击"源代码"按钮，填入 HTML，再切换回来
        source_btn = page.locator("button:has-text('源代码'), .source-btn")
        if await source_btn.count() > 0:
            await source_btn.click()
            await page.wait_for_timeout(500)
            source_editor = page.locator(".source-editor textarea, .CodeMirror textarea")
            if await source_editor.count() > 0:
                await source_editor.fill(html_content)
                await source_btn.click()  # 切回可视模式
                log.info("[wechat-playwright] Content set via source mode")
                return

        log.warning("[wechat-playwright] Could not locate editor — content not set")

    async def _submit_publish(self, page):
        """提交发布"""
        try:
            # 点击发布/群发按钮
            publish_btn = page.locator(
                "#publish_bar a:has-text('发布'), "
                "#publish_bar a:has-text('群发'), "
                "a:has-text('发布并群发')"
            )
            if await publish_btn.count() > 0:
                await publish_btn.click()
                await page.wait_for_timeout(3000)

                # 确认发布对话框
                confirm_btn = page.locator(
                    "button:has-text('确定'), "
                    "a:has-text('确定'), "
                    ".dialog-btn-primary"
                )
                if await confirm_btn.count() > 0:
                    await confirm_btn.click()
                    await page.wait_for_timeout(3000)

                log.info("[wechat-playwright] Published successfully!")
            else:
                log.info("[wechat-playwright] Publish button not found — draft saved only")

        except Exception as e:
            log.warning(f"[wechat-playwright] Publish submission failed: {e}")
