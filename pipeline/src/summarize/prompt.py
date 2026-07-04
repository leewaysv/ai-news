"""提示词模板"""

SUMMARIZE_PROMPT = """你是一个专业的 AI 新闻编辑。请将以下{lang}新闻提炼为中文摘要。

## 原文
标题：{title}
正文：{content}

## 要求
1. 输出严格的 JSON 格式，不要加 markdown 代码块
2. 中文标题（简洁有力，突出核心信息）
3. 用 1-2 句中文摘要概括核心内容
4. 列出 2-4 个关键要点（bullet points）
5. 如适合，加一句编辑点评（分析影响/意义）
6. 给出分类（categories）和标签（tags）
7. 如果是英文源，在标题前标注 [EN]

## 输出格式
{{
  "title": "中文标题",
  "summary": "中文摘要",
  "key_points": ["要点1", "要点2"],
  "analysis": "编辑点评（可选）",
  "categories": ["分类1", "分类2"],
  "tags": ["tag1", "tag2"]
}}"""


DIGEST_PROMPT = """你是一个 AI 新闻早报的主编。以下是今日精选文章，请为今日早报取一个总标题。

## 日期：{date}

## 文章列表
{articles}

## 要求
1. 输出严格的 JSON 格式，不要加 markdown 代码块
2. 中文标题，体现当日最重要的 AI 新闻，如 "AI 早报 | <核心新闻>"
3. editor_note 是可选的开场白/编辑寄语（1-2 句话）

## 输出格式
{{
  "title": "AI 早报 | 今日头条",
  "editor_note": "今日重点..."
}}"""
