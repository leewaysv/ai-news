---
title: "微信内容适配（WeChatAdapter）"
labels: ["ready-for-agent"]
---

## Parent

Parent issue: #1 (7-6 prd)

## What to build

新增 `WeChatAdapter`，将 `DailyDigest` 转换为微信公众号兼容的富文本 HTML。核心功能：

- Markdown → 微信支持的 HTML 子集（div, p, section, h1-h6, img, strong, blockquote, a, ul/ol/li）
- 标题截断：超过 32 字符自动截断加 `…`
- 多篇文章合并为一次推文（最多 8 篇）
- 每篇底部追加 AI 辅助生成声明
- 输出格式：微信草稿 API 所需的 JSON 结构

## Acceptance criteria

- [ ] 输入 `DailyDigest` 输出合法的微信 HTML
- [ ] 标题超过 32 字符自动截断
- [ ] 输出的 HTML 不包含微信禁止的标签
- [ ] 多篇文章正确合并为一次推文结构
- [ ] 每篇文章底部有 AI 辅助生成声明
- [ ] 新增 WeChatAdapter 单元测试

## Blocked by

- Prefactor：多平台编排架构
