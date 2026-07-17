"""抖音内容适配器 — DailyDigest → 短视频脚本 + 字幕"""

from __future__ import annotations

import json
import math
import re
from typing import Optional

from ..models import DailyDigest, AdaptedContent, ProcessedArticle
from .base import BaseAdapter


# ── Cycle 1: generate_script ──

CHARS_PER_SECOND = 4  # 中文语速约 4 字/秒


def generate_script(
    title: str,
    summary: str,
    key_points: list[str],
) -> dict:
    """生成口播脚本

    返回:
        hook:    前 3 秒吸引句
        problem: 问题/背景
        info:    核心信息
        cta:     引导关注
        ai_label: AI 辅助标注
    """
    hook = _make_hook(title, summary)
    problem = _make_problem(summary)
    info = _make_info(summary, key_points)
    cta = _make_cta()

    return {
        "hook": hook,
        "problem": problem,
        "info": info,
        "cta": cta,
        "ai_label": True,
    }


def _make_hook(title: str, summary: str) -> str:
    """生成 hook 句（前 3 秒吸引）"""
    # 尝试从标题提取吸睛内容
    teaser_words = ["重磅", "震惊", "刚刚", "突发", "惊人", "没想到"]
    for word in teaser_words:
        if word in title:
            return f"{word}！{title[:40]}"

    # 从摘要提取亮点
    if len(summary) > 10:
        return f"你知道吗？{summary[:30]}…"

    return f"重磅消息！{title[:30]}"


def _make_problem(summary: str) -> str:
    """生成问题/背景描述"""
    if len(summary) > 15:
        return summary[:60]
    return f"最近 AI 行业又有了新变化：{summary}"


def _make_info(summary: str, key_points: list[str]) -> str:
    """生成核心信息"""
    parts = []
    if key_points:
        parts.append("关键信息来了：")
        for pt in key_points[:3]:
            parts.append(f"· {pt}")
    elif summary:
        parts.append(summary[:60])
    return " ".join(parts)


def _make_cta() -> str:
    """生成引导关注"""
    return "觉得有用的话，点赞关注我们，每天带来最新 AI 资讯！"


# ── Cycle 2: generate_srt ──


def generate_srt(segments: dict[str, str]) -> str:
    """生成 .srt 字幕文件

    segments: {"段名": "文本", ...}
    """
    lines = []
    seq = 1
    current_time = 0.0  # 秒

    for seg_name in ["hook", "problem", "info", "cta"]:
        text = segments.get(seg_name, "")
        if not text.strip():
            continue

        duration = max(1.5, len(text) / CHARS_PER_SECOND)
        start_time = current_time
        end_time = current_time + duration

        lines.append(str(seq))
        lines.append(f"{_format_srt_time(start_time)} --> {_format_srt_time(end_time)}")
        lines.append(text)
        lines.append("")

        current_time = end_time
        seq += 1

    return "\n".join(lines)


def _format_srt_time(seconds: float) -> str:
    """将秒数转为 SRT 时间戳格式 HH:MM:SS,mmm"""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds - int(seconds)) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


# ── Cycle 3: extract_keywords ──


_STOP_WORDS = frozenset([
    "的", "了", "是", "在", "和", "就", "都", "而", "及", "与",
    "着", "或", "一个", "没有", "我们", "你们", "他们", "这个",
    "那个", "这些", "那些", "不", "也", "很", "有", "被", "把",
    "从", "对", "到", "让", "上", "下", "中", "大", "小", "多",
    "少", "好", "要", "会", "可以", "能", "已经", "还", "更",
    "最", "但", "如果", "因为", "所以", "然后", "而", "且",
])


def extract_keywords(text: str, max_keywords: int = 5) -> list[str]:
    """从文本中提取 3-5 个关键词

    使用简单的词频统计，过滤停用词，按频率排序返回。
    中英文混合文本均支持。
    """
    # 提取英文词和中文词
    words = []

    # 英文词（至少 3 个字符的技术术语）
    eng_words = re.findall(r"[A-Za-z][A-Za-z0-9.-]{2,}", text)
    words.extend(eng_words)

    # 中文词（2-6 字）
    chinese_chars = re.findall(r"[一-鿿]{2,6}", text)
    words.extend(chinese_chars)

    # 过滤停用词，统计频率
    freq: dict[str, int] = {}
    for w in words:
        w_clean = w.strip().lower()
        if w_clean not in _STOP_WORDS and len(w_clean) >= 2:
            freq[w_clean] = freq.get(w_clean, 0) + 1

    # 按频率排序，优先保留英文技术术语
    sorted_words = sorted(freq.items(), key=lambda x: (-x[1], x[0]))

    # 去重，保留原始大小写
    seen = set()
    result = []
    for w, _ in sorted_words:
        if w not in seen:
            seen.add(w)
            result.append(w)
        if len(result) >= max_keywords:
            break

    return result if result else [text[:10]]


# ── Cycle 4: DouyinAdapter ──

import json


class DouyinAdapter(BaseAdapter):
    """将 DailyDigest 适配为抖音短视频脚本"""

    def adapt(self, digest: DailyDigest) -> list[AdaptedContent]:
        if not digest.articles:
            return []

        results = []
        for article in digest.articles:
            script = generate_script(
                title=article.title,
                summary=article.summary,
                key_points=article.key_points,
            )

            srt = generate_srt(script)

            search_text = f"{article.title} {article.summary} {' '.join(article.key_points)}"
            keywords = extract_keywords(search_text)

            tts_text = "。".join(v for v in script.values() if isinstance(v, str))

            total_chars = sum(len(v) for v in script.values() if isinstance(v, str))
            estimated_duration = max(15, round(total_chars / CHARS_PER_SECOND))

            content = {
                "script": script,
                "srt": srt,
                "keywords": keywords,
                "tts_text": tts_text,
                "estimated_duration": estimated_duration,
                "ai_label": True,
            }

            results.append(AdaptedContent(
                platform="douyin",
                content=json.dumps(content, ensure_ascii=False),
                metadata={
                    "article_id": article.id,
                    "title": article.title,
                    "duration": estimated_duration,
                },
            ))

        return results
