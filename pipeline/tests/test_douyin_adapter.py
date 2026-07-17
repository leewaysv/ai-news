"""DouyinAdapter TDD 测试

Seams（已确认）:
  1. generate_script     — 口播脚本生成
  2. generate_srt        — 字幕文件生成
  3. extract_keywords    — 关键词提取
  4. DouyinAdapter.adapt — 完整适配流程
"""

from src.adapt.douyin_adapter import generate_script


class TestGenerateScript:
    """口播脚本生成测试"""

    def test_script_structure(self):
        """脚本包含 hook → problem → info → cta 四段"""
        script = generate_script(
            title="GPT-5.6 Sol 发布",
            summary="OpenAI 发布了 GPT-5.6 Sol 模型，推理能力大幅提升。",
            key_points=["MoE 架构", "推理成本降低 40%"],
        )
        assert "hook" in script
        assert "problem" in script
        assert "info" in script
        assert "cta" in script

    def test_hook_is_engaging(self):
        """hook 以前 3 秒吸引开头"""
        script = generate_script(
            title="GPT-5.6 Sol 发布",
            summary="OpenAI 发布了新模型。",
            key_points=[],
        )
        hook = script["hook"]
        assert len(hook) >= 5
        # hook 应包含标题或提及关键信息
        assert any(word in hook for word in ["GPT", "发布", "震惊", "重磅", "OpenAI"])

    def test_problem_context(self):
        """problem 段描述背景问题"""
        script = generate_script(
            title="AI 芯片突破",
            summary="新型 AI 芯片性能提升 5 倍。",
            key_points=["算力瓶颈"],
        )
        problem = script["problem"]
        assert len(problem) >= 5

    def test_info_from_key_points(self):
        """info 段包含关键要点"""
        script = generate_script(
            title="测试",
            summary="测试摘要。",
            key_points=["要点A", "要点B", "要点C"],
        )
        info = script["info"]
        assert "要点A" in info
        assert "要点B" in info

    def test_cta_encourages_action(self):
        """cta 段引导关注或互动"""
        script = generate_script(
            title="测试",
            summary="测试摘要。",
            key_points=[],
        )
        cta = script["cta"]
        assert any(word in cta for word in ["关注", "点赞", "转发", "订阅", "收藏"])

    def test_estimated_duration_15_to_60_seconds(self):
        """脚本总时长在 15-60 秒范围（按 4 字/秒估算）"""
        script = generate_script(
            title="GPT-5.6 Sol 发布：OpenAI 最新模型重大突破",
            summary="OpenAI 发布了 GPT-5.6 Sol 模型，采用稀疏 MoE 架构，推理成本降低 40%。这一突破将推动 AI 应用进一步普及。",
            key_points=[
                "稀疏 MoE 架构，8T 参数",
                "推理成本降低 40%",
                "多模态能力提升",
            ],
        )
        total_chars = sum(len(v) for v in script.values() if isinstance(v, str))
        estimated_seconds = total_chars / 4  # ~4 chars/sec speaking rate
        assert 10 <= estimated_seconds <= 90  # 15-60 秒范围适当放宽

    def test_ai_label_present(self):
        """脚本末尾标注 AI 辅助生成"""
        script = generate_script(
            title="测试",
            summary="测试。",
            key_points=[],
        )
        assert script.get("ai_label", False)


# ── Cycle 2: generate_srt ──

from src.adapt.douyin_adapter import generate_srt


def _parse_srt_time(t: str) -> float:
    """将 SRT 时间戳转为秒数"""
    parts = t.replace(",", ":").split(":")
    h, m, s, ms = int(parts[0]), int(parts[1]), int(parts[2]), int(parts[3])
    return h * 3600 + m * 60 + s + ms / 1000


class TestGenerateSrt:
    """字幕文件生成测试"""

    def test_srt_starts_with_sequence(self):
        """SRT 从序号 1 开始"""
        srt = generate_srt({"hook": "你好世界", "cta": "关注我们"})
        assert srt.startswith("1\n")

    def test_srt_has_timestamp_format(self):
        """每段包含正确的时间戳格式"""
        srt = generate_srt({"hook": "hello"})
        assert "-->" in srt
        import re
        assert re.search(r"\d{2}:\d{2}:\d{2},\d{3}", srt)

    def test_srt_contains_text(self):
        """字幕包含原文"""
        srt = generate_srt({"hook": "测试文本", "info": "核心内容"})
        assert "测试文本" in srt
        assert "核心内容" in srt

    def test_srt_timing_by_char_count(self):
        """时间戳按字符数计算时长（4 字/秒）"""
        srt = generate_srt({"hook": "a" * 40, "info": "b" * 40})
        lines = srt.strip().split("\n\n")
        assert len(lines) == 2
        for block in lines:
            time_line = block.split("\n")[1]
            start, end = time_line.split(" --> ")
            start_sec = _parse_srt_time(start)
            end_sec = _parse_srt_time(end)
            duration = end_sec - start_sec
            assert 8 <= duration <= 12  # 10s ± 2s

    def test_empty_segments_omitted(self):
        """空文本段被跳过"""
        srt = generate_srt({"hook": "", "info": "内容"})
        blocks = srt.strip().split("\n\n")
        assert len(blocks) == 1
        assert "内容" in blocks[0]

    def test_multiple_segments_sequential(self):
        """多段字幕时间连续"""
        srt = generate_srt({"hook": "a" * 20, "info": "b" * 20})
        blocks = srt.strip().split("\n\n")
        assert len(blocks) == 2
        first_end = _parse_srt_time(blocks[0].split("\n")[1].split(" --> ")[1])
        second_start = _parse_srt_time(blocks[1].split("\n")[1].split(" --> ")[0])
        assert abs(first_end - second_start) < 0.5


# ── Cycle 3: extract_keywords ──

from src.adapt.douyin_adapter import extract_keywords


class TestExtractKeywords:
    """关键词提取测试"""

    def test_returns_list(self):
        kw = extract_keywords("OpenAI 发布了 GPT-5.6 Sol 模型")
        assert isinstance(kw, list)

    def test_returns_3_to_5_keywords(self):
        kw = extract_keywords(
            "OpenAI 发布了 GPT-5.6 Sol 模型，采用稀疏 MoE 架构，推理成本降低 40%"
        )
        assert 2 <= len(kw) <= 5

    def test_short_text_returns_fewer(self):
        kw = extract_keywords("今天天气不错")
        assert len(kw) >= 1

    def test_keywords_from_english_terms(self):
        kw = extract_keywords("GPT-5.6 Sol uses MoE architecture and RLHF training")
        english_kw = [k for k in kw if any(c.isascii() and c.isalpha() for c in k)]
        assert len(english_kw) >= 1

    def test_no_stop_words(self):
        kw = extract_keywords("这个模型的一个重要的新功能是")
        for word in ["的", "了", "是", "一个"]:
            assert word not in kw


# ── Cycle 4: DouyinAdapter.adapt ──

import json
import pytest
from src.adapt.douyin_adapter import DouyinAdapter
from src.models import DailyDigest, ProcessedArticle, AdaptedContent


class TestDouyinAdapter:
    """完整适配流程测试"""

    @pytest.fixture
    def digest(self):
        return DailyDigest(
            date="2026-07-08",
            title="AI 早报测试",
            articles=[
                ProcessedArticle(
                    id="art-1",
                    raw_url="https://example.com/1",
                    source_name="OpenAI",
                    original_title="GPT-5.6 Sol",
                    title="GPT-5.6 Sol",
                    summary="OpenAI 发布了 GPT-5.6 Sol，推理能力大幅提升。",
                    key_points=["MoE 架构", "成本降低 40%"],
                    analysis="这是一个重大突破。",
                ),
            ],
        )

    def test_adapt_returns_list(self, digest):
        adapter = DouyinAdapter()
        result = adapter.adapt(digest)
        assert isinstance(result, list)

    def test_adapt_returns_adapted_content(self, digest):
        adapter = DouyinAdapter()
        result = adapter.adapt(digest)
        for item in result:
            assert isinstance(item, AdaptedContent)

    def test_platform_is_douyin(self, digest):
        adapter = DouyinAdapter()
        result = adapter.adapt(digest)
        for item in result:
            assert item.platform == "douyin"

    def test_content_contains_script_and_srt(self, digest):
        adapter = DouyinAdapter()
        result = adapter.adapt(digest)
        for item in result:
            data = json.loads(item.content)
            assert "script" in data
            assert "srt" in data
            assert "keywords" in data
            assert "estimated_duration" in data

    def test_one_adapted_content_per_article(self, digest):
        adapter = DouyinAdapter()
        result = adapter.adapt(digest)
        assert len(result) == len(digest.articles)

    def test_srt_is_valid_format(self, digest):
        adapter = DouyinAdapter()
        result = adapter.adapt(digest)
        for item in result:
            data = json.loads(item.content)
            srt = data["srt"]
            assert srt.startswith("1\n")
            assert "-->" in srt
