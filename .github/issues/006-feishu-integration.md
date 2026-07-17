---
title: "飞书机器人推送（FeishuPublisher）"
labels: ["ready-for-agent"]
---

## Parent

Parent issue: #1 (7-6 prd)

## What to build

新增 `FeishuPublisher`，将每日 AI 新闻早报推送到飞书群聊。支持两种接入方式：

### 方式一：Webhook 机器人（零代码，推荐）
飞书群聊添加自定义机器人 → 获取 Webhook URL → 直接 POST JSON 消息。

- 支持飞书富文本消息格式（标题 + 多行摘要 + 原文链接）
- 每条新闻作为独立消息块发送
- 整体 digest 头部 + 分隔线

### 方式二：飞书开放 API（预留）
后续使用飞书 Open API 发送更丰富的消息卡片（Card Mode）。

## 消息格式设计

```
📰 AI 早报 | 2026-07-08
━━━━━━━━━━━━━━━━━━

1. GPT-5.6 Sol 发布
   OpenAI 发布了新一代模型...
   🔗 查看原文 | 来源: OpenAI Blog

2. ...

──── powered by AI ────
```

## Acceptance criteria

- [ ] 支持 Webhook URL 配置（飞书群机器人）
- [ ] 支持富文本消息格式（标题 + 摘要 + 链接）
- [ ] 每日 digest 发送到飞书群
- [ ] 发送失败时跳过，不阻塞博客和其他平台
- [ ] 新增 FeishuPublisher 单元测试（mock HTTP）

## Config

```yaml
platforms:
  feishu:
    enabled: true
    webhook_url: "https://open.feishu.cn/open-apis/bot/v2/hook/xxx"
```

## Blocked by

- Prefactor：多平台编排架构（已完成）

## Notes

- Webhook URL 可通过环境变量 `FEISHU_WEBHOOK_URL` 传入
- 飞书机器人 Webhook 是零成本方案，无需认证
- 消息内容需符合飞书消息格式规范：https://open.feishu.cn/document/server-docs/im-v1/message-content-description
