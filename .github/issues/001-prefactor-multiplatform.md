---
title: "Prefactor：多平台编排架构"
labels: ["ready-for-agent"]
---

## Parent

Parent issue: #1 (7-6 prd)

## What to build

对 Pipeline 编排层做前置重构，使多平台发布成为可能。当前 `main.py` 的 `run()` 方法在适配和发布步骤硬编码了博客平台。本次重构将其改为可扩展的平台迭代模式。

具体变更：
1. **config.yaml**：新增 `platforms` 配置段
2. **config.py**：新增 `PlatformConfig` 模型
3. **main.py**：适配+发布改为遍历已启用平台

Blog 平台仍然是唯一启用的平台，重构后行为不变。

## Acceptance criteria

- [ ] config.yaml 能正常加载 platforms 配置
- [ ] 平台可单独启用/禁用
- [ ] Blog 默认启用，WeChat/Douyin 默认禁用
- [ ] main.py 适配+发布步骤遍历已启用平台
- [ ] 只启用 Blog 时结果与重构前完全一致
- [ ] 新增 PlatformConfig 单元测试

## Blocked by

None - can start immediately
