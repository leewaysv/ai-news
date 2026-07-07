"""WeChatAdapter 原型 TUI

交互式驱动 adapter.py 中的逻辑，查看状态变化。
"""

import json
import os
import sys

# ── 确保可以导入同目录的 adapter ──
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from adapter import (
    truncate_title,
    article_to_html,
    digest_to_draft,
    draft_to_json,
    make_aigc_notice,
    make_demo_digest,
    TITLE_MAX_CHARS,
    MAX_ARTICLES_PER_DRAFT,
    ProtoDailyDigest,
    WeChatDraft,
)


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def bold(text: str) -> str:
    return f"\x1b[1m{text}\x1b[0m"


def dim(text: str) -> str:
    return f"\x1b[2m{text}\x1b[0m"


def green(text: str) -> str:
    return f"\x1b[32m{text}\x1b[0m"


def yellow(text: str) -> str:
    return f"\x1b[33m{text}\x1b[0m"


# ── 状态 ──

class State:
    def __init__(self):
        self.digest: ProtoDailyDigest | None = None
        self.draft: WeChatDraft | None = None
        self.selected_article_idx: int = 0
        self.show_json: bool = False
        self.show_title_chars: bool = False
        self.aigc_notice: str = "本文内容由 AI 辅助生成，仅供参考。"

    def reload_draft(self):
        if self.digest:
            self.draft = digest_to_draft(self.digest, self.aigc_notice)


state = State()


# ── 渲染 ──

def render():
    clear()

    # ── 头部 ──
    print(f"{bold('WeChatAdapter 原型')}")
    print(f"{dim('多平台发布 · 微信内容适配')}")
    print()

    if state.digest is None:
        print("按 [l] 加载示例数据")
        print()
        print_help()
        return

    # ── Digest 概览 ──
    digest = state.digest
    print(f"{bold('📋 DailyDigest')}: {digest.date} — {digest.title}")
    print(f"  文章总数: {len(digest.articles)} 篇")
    print(f"  草稿篇数: {min(len(digest.articles), MAX_ARTICLES_PER_DRAFT)} 篇（微信上限 {MAX_ARTICLES_PER_DRAFT} 篇）")
    print()

    # ── 文章列表 ──
    print(f"{bold('📄 文章列表')}:")
    for i, article in enumerate(digest.articles):
        marker = "▸" if i == state.selected_article_idx else " "
        truncated = truncate_title(article.title)
        is_truncated = truncated != article.title
        title_display = truncated
        if is_truncated:
            title_display += f" {yellow('(截断)')}"

        if state.show_title_chars:
            title_display += f" {dim(f'[{len(article.title)}→{len(truncated)}字符]')}"

        print(f"  {marker} [{i}] {title_display}")

    print()

    # ── 选中的文章详情 ──
    if state.selected_article_idx < len(digest.articles):
        article = digest.articles[state.selected_article_idx]
        print(f"{bold('🔍 选中文章详情')}:")
        print(f"  原标题: {article.original_title}")
        print(f"  截断后: {truncate_title(article.title)}")
        print(f"  摘要:   {article.summary[:60]}..." if len(article.summary) > 60 else f"  摘要:   {article.summary}")
        print(f"  要点数: {len(article.key_points)}")
        print(f"  分析:   {'有' if article.analysis else '无'}")
        print(f"  AIGC:   {'标注 ✓' if article.aigc_label else '未标注'}")
        print()

        if state.show_json and state.draft and state.selected_article_idx < len(state.draft.articles):
            print(f"{bold('📦 生成的微信 HTML (前 300 字符)')}:")
            html = state.draft.articles[state.selected_article_idx].content
            print(dim(html[:300] + ("..." if len(html) > 300 else "")))
            print()

    # ── 完整 JSON ──
    if state.show_json and state.draft:
        print(f"{bold('📦 完整草稿 JSON')}:")
        json_str = json.dumps(draft_to_json(state.draft), ensure_ascii=False, indent=2)
        # 截断展示以免 overflow
        if len(json_str) > 1500:
            json_str = json_str[:1500] + "\n  ... (截断)"
        print(dim(json_str))
        print()

    print_help()


def print_help():
    print(f"{bold('快捷键')}:")
    print(f"  [{bold('l')}] 加载示例 Digest     [{bold('1')}-{bold('9')}] 选择文章")
    print(f"  [{bold('j')}] 切换 JSON 视图       [{bold('c')}] 切换字符数显示")
    print(f"  [{bold('t')}] 切换 AIGC 声明文本   [{bold('h')}] 显示全部 HTML")
    print(f"  [{bold('q')}] 退出")
    print()


# ── 事件处理 ──

def handle(key: str) -> bool:
    """处理按键。返回 False 表示退出。"""
    global state

    if key == "q":
        return False

    if key == "l":
        state.digest = make_demo_digest()
        state.selected_article_idx = 0
        state.show_json = False
        state.show_title_chars = False
        state.reload_draft()
        return True

    if key == "j":
        state.show_json = not state.show_json
        return True

    if key == "c":
        state.show_title_chars = not state.show_title_chars
        return True

    if key == "t":
        if state.aigc_notice:
            state.aigc_notice = ""
        else:
            state.aigc_notice = "本文内容由 AI 辅助生成，仅供参考。"
        state.reload_draft()
        return True

    if key == "h" and state.draft and state.selected_article_idx < len(state.draft.articles):
        clear()
        html = state.draft.articles[state.selected_article_idx].content
        print(f"{bold('完整 HTML')} (文章 #{state.selected_article_idx}):")
        print(html)
        print()
        print("按任意键返回...")
        try:
            import msvcrt
            msvcrt.getch()
        except ImportError:
            input()
        return True

    if key.isdigit():
        idx = int(key)
        if state.digest and idx < len(state.digest.articles):
            state.selected_article_idx = idx
        return True

    return True


# ── 主循环 ──

def main():
    render()
    while True:
        try:
            if os.name == "nt":
                import msvcrt
                key = msvcrt.getch().decode("utf-8", errors="ignore").lower()
            else:
                import termios
                import tty
                fd = sys.stdin.fileno()
                old = termios.tcgetattr(fd)
                try:
                    tty.setraw(fd)
                    key = sys.stdin.read(1).lower()
                finally:
                    termios.tcsetattr(fd, termios.TCSADRAIN, old)
        except (KeyboardInterrupt, EOFError):
            break

        if not handle(key):
            break
        render()

    clear()
    print("原型退出。答案记录在 NOTES.md。")


if __name__ == "__main__":
    main()
