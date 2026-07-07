---
title: "微信 API 发布（WeChatPublisher）"
labels: ["ready-for-agent"]
---

## Parent

Parent issue: #1 (7-6 prd)

## What to build

新增 `WeChatPublisher`，封装微信公众号发布 API 的完整调用流程：

- `access_token` 自动获取和刷新（有效期 7200s）
- 正文图片通过 `uploadimg` API 上传到微信 CDN
- 封面图通过 `add_material` API 上传为永久素材
- 创建草稿：调用 `draft/add` API
- 提交发布：调用 `freepublish/submit` API
- 轮询发布状态：调用 `freepublish/get` API
- 错误重试和降级：API 失败时跳过微信发布，不影响博客

## Acceptance criteria

- [ ] access_token 首次获取正常，过期后自动刷新
- [ ] 正文图片上传到微信 CDN，URL 正确嵌入 HTML
- [ ] 草稿创建成功，返回 media_id
- [ ] 发布提交成功，返回 publish_id
- [ ] 发布失败时跳过微信发布，不阻塞博客和其他平台
- [ ] 新增 WeChatPublisher 单元测试（mock API）

## Blocked by

- 微信内容适配（WeChatAdapter）
