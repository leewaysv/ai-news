---
title: "抖音脚本生成（DouyinAdapter）"
labels: ["ready-for-agent"]
---

## Parent

Parent issue: #1 (7-6 prd)

## What to build

新增 `DouyinAdapter`，将 `DailyDigest` 中的每篇文章转换为抖音短视频的脚本和辅助文件：

- 口播脚本生成：hook（前 3 秒吸引）→ 问题呈现 → 核心信息 → CTA（引导关注）
- 字幕文件（.srt）生成，与口播脚本同步
- TTS 配置：标记需要语音合成的文本段落
- 素材关键词提取：从摘要中提取 3-5 个关键词，用于后续搜索背景素材
- AI 标注：在脚本末尾标注"AI 辅助生成"
- 输出文件可本地审查（脚本 + 字幕），确认后再渲染

## Acceptance criteria

- [ ] 输入 `ProcessedArticle` 输出口播脚本
- [ ] 脚本时长在 15-60 秒范围（按语速估算）
- [ ] 输出正确的 .srt 字幕文件
- [ ] 从摘要提取 3-5 个素材搜索关键词
- [ ] 生成的脚本文件可人工预览和修改后再渲染
- [ ] 新增 DouyinAdapter 单元测试

## Blocked by

- Prefactor：多平台编排架构
