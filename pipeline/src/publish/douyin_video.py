"""抖音视频渲染 + 自动上传

流程: TTS → 背景素材 → 视频合成 → 字幕嵌入 → 上传抖音
"""
from __future__ import annotations

import json
import logging
import os
import re
import subprocess
from pathlib import Path
from typing import Optional

from ..models import AdaptedContent
from .base import BasePublisher

log = logging.getLogger(__name__)


# ── 常量 ──

DEFAULT_OUTPUT_DIR = "output/douyin"
VIDEO_SIZE = "720x1280"  # 9:16 竖屏
FPS = 24
TTS_VOICE = "zh-CN-XiaoxiaoNeural"  # edge-tts 中文女声


class DouyinVideoPublisher(BasePublisher):
    """抖音视频渲染 + 发布器

    将 DouyinAdapter 生成的脚本转换为实际视频并上传。
    需要: FFmpeg, edge-tts, moviepy
    """

    def __init__(
        self,
        output_dir: str = DEFAULT_OUTPUT_DIR,
        pexels_api_key: str = "",
        headless: bool = True,
    ):
        self.output_dir = Path(output_dir)
        self.pexels_api_key = pexels_api_key or os.environ.get("PEXELS_API_KEY", "")
        self.headless = headless

    async def publish(self, contents: list[AdaptedContent]) -> int:
        """渲染并发布视频，返回成功数"""
        if not contents:
            return 0

        total = 0
        for item in contents:
            try:
                ok = await self._render_and_upload(item)
                if ok:
                    total += 1
            except Exception as e:
                log.warning(f"[douyin-video] Failed: {e}")

        return total

    async def _render_and_upload(self, item: AdaptedContent) -> bool:
        """单条内容：渲染 + 上传"""
        data = json.loads(item.content)
        title = item.metadata.get("title", "video")
        safe_title = re.sub(r"[^\w\-]", "_", title)[:30]

        # 输出路径
        self.output_dir.mkdir(parents=True, exist_ok=True)
        audio_path = self.output_dir / f"{safe_title}.mp3"
        video_path = self.output_dir / f"{safe_title}.mp4"

        # 1. TTS
        tts_text = data.get("tts_text", "")
        if tts_text:
            audio_path = await self._generate_tts(tts_text, audio_path)
            if not audio_path:
                log.warning("[douyin-video] TTS failed, skipping")
                return False

        # 2. 搜索背景素材
        keywords = data.get("keywords", ["AI", "technology"])
        bg_url = await self._search_background(keywords)

        # 3. 合成视频
        srt_text = data.get("srt", "")
        result = await self._compose_video(
            background_url=bg_url,
            audio_path=audio_path,
            subtitles=srt_text,
            output_path=video_path,
        )
        if not result:
            log.warning("[douyin-video] Video composition failed")
            return False

        # 4. 上传抖音
        upload_ok = await self._upload_to_douyin(video_path)
        if upload_ok:
            log.info(f"[douyin-video] Uploaded: {video_path.name}")

        return upload_ok

    # ── TTS ──

    async def _generate_tts(self, text: str, output_path: Path) -> Optional[Path]:
        """用 edge-tts 生成语音"""
        try:
            import edge_tts
            communicate = edge_tts.Communicate(text, TTS_VOICE)
            await communicate.save(str(output_path))
            log.info(f"[douyin-video] TTS generated: {output_path.name} ({len(text)} chars)")
            return output_path
        except ImportError:
            log.error("[douyin-video] edge_tts not installed. Run: pip install edge-tts")
            return None
        except Exception as e:
            log.warning(f"[douyin-video] TTS failed: {e}")
            return None

    # ── 背景素材 ──

    async def _search_background(self, keywords: list[str]) -> str:
        """从 Pexels 搜索免费商用视频素材，返回 URL"""
        if not self.pexels_api_key:
            log.warning("[douyin-video] No Pexels API key, using fallback background")
            return ""

        try:
            import httpx
            query = " ".join(keywords[:3])
            url = "https://api.pexels.com/videos/search"
            headers = {"Authorization": self.pexels_api_key}
            params = {"query": query, "per_page": 5, "orientation": "portrait"}

            async with httpx.AsyncClient() as client:
                resp = await client.get(url, headers=headers, params=params)
                resp.raise_for_status()
                data = resp.json()

            videos = data.get("videos", [])
            if videos:
                # 选择第一个视频的最高质量链接
                for video in videos:
                    for file in video.get("video_files", []):
                        if file.get("quality") in ("hd", "sd") and file.get("link"):
                            log.info(f"[douyin-video] Background: {file['link'][:60]}...")
                            return file["link"]

        except Exception as e:
            log.warning(f"[douyin-video] Pexels search failed: {e}")

        return ""

    # ── 视频合成 ──

    async def _compose_video(
        self,
        background_url: str,
        audio_path: Path,
        subtitles: str,
        output_path: Path,
    ) -> bool:
        """合成最终视频"""
        # 检查 FFmpeg
        if not self._check_ffmpeg():
            log.warning("[douyin-video] FFmpeg not found")
            return False

        if not audio_path.exists():
            # 无音频时生成静音视频
            return await self._render_silent_video(output_path)

        # 步骤1: 合成带音频 + 字幕的视频
        # 如果有背景视频，下载并合成
        if background_url:
            return await self._compose_with_background(
                background_url, audio_path, subtitles, output_path
            )

        # 无背景视频：纯色背景 + 字幕
        return await self._compose_simple(audio_path, subtitles, output_path)

    def _check_ffmpeg(self) -> bool:
        """检查 FFmpeg 是否可用"""
        try:
            subprocess.run(
                ["ffmpeg", "-version"],
                capture_output=True,
                check=True,
            )
            return True
        except (subprocess.SubprocessError, FileNotFoundError):
            return False

    async def _render_silent_video(self, output_path: Path) -> bool:
        """生成纯色静默视频（占位）"""
        try:
            cmd = [
                "ffmpeg", "-y",
                "-f", "lavfi", "-i", f"color=c=black:s={VIDEO_SIZE}:d=10:r={FPS}",
                "-c:v", "libx264", "-pix_fmt", "yuv420p",
                str(output_path),
            ]
            subprocess.run(cmd, capture_output=True, check=True)
            log.info(f"[douyin-video] Silent video: {output_path.name}")
            return True
        except Exception as e:
            log.warning(f"[douyin-video] Silent video failed: {e}")
            return False

    async def _compose_simple(
        self, audio_path: Path, subtitles: str, output_path: Path,
    ) -> bool:
        """纯色背景 + 音频 + 字幕"""
        srt_file = self._write_srt(subtitles, output_path)

        try:
            # 获取音频时长
            duration = self._get_audio_duration(audio_path)

            cmd = [
                "ffmpeg", "-y",
                "-f", "lavfi", "-i", f"color=c=black:s={VIDEO_SIZE}:d={duration}:r={FPS}",
                "-i", str(audio_path),
                "-c:v", "libx264", "-pix_fmt", "yuv420p",
                "-c:a", "aac", "-b:a", "128k",
            ]
            if srt_file:
                # Windows: FFmpeg subtitles 滤镜需要正斜杠路径
                srt_posix = str(srt_file).replace("\\", "/")
                cmd += ["-vf", f"subtitles={srt_posix}"]
            cmd.append(str(output_path))

            subprocess.run(cmd, capture_output=True, check=True)
            log.info(f"[douyin-video] Composed: {output_path.name} ({duration}s)")
            return True
        except Exception as e:
            log.warning(f"[douyin-video] Composition failed: {e}")
            return False

    async def _compose_with_background(
        self, bg_url: str, audio_path: Path,
        subtitles: str, output_path: Path,
    ) -> bool:
        """背景视频 + 音频 + 字幕"""
        srt_file = self._write_srt(subtitles, output_path)
        bg_local = self.output_dir / "bg_temp.mp4"

        try:
            # 下载背景视频
            import httpx
            async with httpx.AsyncClient() as client:
                resp = await client.get(bg_url)
                resp.raise_for_status()
                bg_local.write_bytes(resp.content)

            duration = self._get_audio_duration(audio_path)

            cmd = [
                "ffmpeg", "-y",
                "-stream_loop", "-1" if duration > 10 else "0",
                "-i", str(bg_local),
                "-i", str(audio_path),
                "-t", str(duration),
                "-c:v", "libx264", "-pix_fmt", "yuv420p",
                "-c:a", "aac", "-b:a", "128k",
                "-vf", f"scale={VIDEO_SIZE.replace('x', ':')}:force_original_aspect_ratio=decrease,pad={VIDEO_SIZE.replace('x', ':')}:(ow-iw)/2:(oh-ih)/2",
            ]
            # Windows: FFmpeg subtitles 滤镜需要正斜杠路径
            srt_posix = str(srt_file).replace("\\", "/") if srt_file else ""
            if srt_file:
                cmd += [f"subtitles={srt_posix}:force_style='FontName=Microsoft YaHei,FontSize=18'"]
            cmd.append(str(output_path))

            subprocess.run(cmd, capture_output=True, check=True)
            log.info(f"[douyin-video] Composed with background: {output_path.name}")
            return True

        except Exception as e:
            log.warning(f"[douyin-video] Background composition failed: {e}")
            return False
        finally:
            if bg_local.exists():
                bg_local.unlink(missing_ok=True)

    def _write_srt(self, srt_text: str, video_path: Path) -> Optional[Path]:
        """将 SRT 字幕写入临时文件"""
        if not srt_text.strip():
            return None
        srt_path = video_path.with_suffix(".srt")
        srt_path.write_text(srt_text, encoding="utf-8")
        return srt_path

    def _get_audio_duration(self, audio_path: Path) -> float:
        """获取音频文件时长（秒）"""
        try:
            result = subprocess.run(
                ["ffprobe", "-v", "error", "-show_entries",
                 "format=duration", "-of", "default=noprint_wrappers=1:nokey=1",
                 str(audio_path)],
                capture_output=True, text=True, check=True,
            )
            return float(result.stdout.strip())
        except Exception:
            return 15.0  # 默认 15 秒

    # ── 抖音上传 ──

    async def _upload_to_douyin(self, video_path: Path) -> bool:
        """通过 Playwright 自动上传到抖音创作者平台"""
        if not video_path.exists():
            return False

        try:
            from playwright.async_api import async_playwright
        except ImportError:
            log.error("[douyin-video] playwright not installed")
            return False

        cookie_file = ".douyin_cookies.json"

        async with async_playwright() as pw:
            browser = await pw.chromium.launch(headless=self.headless)
            context = await browser.new_context(
                viewport={"width": 1280, "height": 800},
            )

            # 加载已保存的 Cookie
            if os.path.exists(cookie_file):
                with open(cookie_file) as f:
                    await context.add_cookies(json.load(f))

            page = await context.new_page()

            # 登录抖音创作者平台
            await page.goto(
                "https://creator.douyin.com/",
                wait_until="domcontentloaded",
            )
            await page.wait_for_timeout(5000)

            # 检查登录状态
            if "login" in page.url.lower():
                log.info("[douyin-video] Login required — showing QR code...")
                await page.screenshot(path="douyin_qrcode.png")
                print(f"\n{'='*60}")
                print(f"  ⚠️ 请用抖音扫描: douyin_qrcode.png")
                print(f"{'='*60}\n")
                try:
                    await page.wait_for_url(
                        "**/creator/**", timeout=120000,
                    )
                    cookies = await context.cookies()
                    with open(cookie_file, "w") as f:
                        json.dump(cookies, f)
                except Exception:
                    log.error("[douyin-video] Login timeout")
                    await browser.close()
                    return False

            # 导航到视频上传页
            await page.goto(
                "https://creator.douyin.com/creator-micro/content/upload",
                wait_until="domcontentloaded",
            )
            await page.wait_for_timeout(3000)

            # 上传视频文件
            file_input = page.locator("input[type=file]")
            if await file_input.count() > 0:
                await file_input.set_input_files(str(video_path))
                log.info(f"[douyin-video] Uploading: {video_path.name}")
                await page.wait_for_timeout(5000)

                # 等待上传完成
                await page.wait_for_timeout(10000)
                log.info("[douyin-video] Upload complete (manual publish may be needed)")
                await browser.close()
                return True
            else:
                log.warning("[douyin-video] No file input found")
                await browser.close()
                return False
