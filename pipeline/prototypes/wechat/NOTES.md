# WeChatAdapter 原型 — 问题陈述

## 问题

WeChatAdapter 的数据转换逻辑能否正确处理以下边界情况：

1. **标题截断**：32 字符精确截断（英文单词边界/中文/正好 32/超过 32）
2. **HTML 标签安全性**：Markdown 转换 → 仅输出微信允许的标签子集
3. **多篇合并**：1 篇、正好 8 篇、超过 8 篇截断
4. **空字段容错**：key_points 为空、analysis 为 None、summary 为空字符串
5. **AIGC 合规标注**：每篇文章底部追加 AI 辅助生成声明

## 验证结果 (2026-07-06)

全部 10 项烟雾测试通过：
- ✅ 标题精确截断到 32 字符，超长末尾加 `…`
- ✅ 中英文混合标题均正确处理
- ✅ 草稿最多 8 篇（超出自动截断）
- ✅ 所有标题长度 ≤ 32 字符
- ✅ JSON 序列化格式正确
- ✅ AIGC 声明存在于每篇文章
- ✅ 无禁止标签（script, iframe, table 等）
- ✅ 空 key_points + None analysis 不报错
- ✅ 不生成空的 `<ul>` 标签

## 待设计的问题

- `thumb_media_id` 如何在 pipeline 中传递（当前留空）
- 封面图上传策略：适配阶段传 URL / 发布阶段传微信 CDN
- 是否需要为每篇生成单独草稿（而非合并一篇多图文）
- AI 声明的措辞是否满足中国 AIGC 法规

## 使用方法

```bash
cd pipeline
.venv/Scripts/python -m prototypes.wechat.tui
```

快捷键：
- `[l]` 加载示例数据
- `[1]-[9]` 选择文章查看详情
- `[j]` 切换 JSON/HTML 视图
- `[c]` 切换字符计数显示
- `[t]` 切换 AIGC 声明
- `[h]` 显示选中文章的完整 HTML
- `[q]` 退出
