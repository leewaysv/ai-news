---
title: "[EN] Third Moment Research 让万级智能体持续运行36小时以上"
date: "2026-10-20T01:03:51+08:00"
slug: "en-third-moment-research-36"
source: "OpenAI Blog"
source_url: "https://openai.com/index/third-moment-research"
categories:
  - AI 智能体
  - 人工智能
  - 网络安全
tags:
  - Third Moment Research
  - 长时程智能体
  - GPT-6 Astra
  - GPT-6.1 Sol
  - Codex
  - Daybreak
  - 多智能体系统
  - 模型编排
summary: "Third Moment Research 借助 GPT-6 Astra、GPT-6.1 Sol、Codex 及面向网络安全的 Daybreak，构建出能够连续数天保持专注、并随使用不断自我改进的 AI 智能体，单次可调度 1 万个智能体运行超过 36 小时。"
aigc: true
---
Third Moment Research 借助 GPT-6 Astra、GPT-6.1 Sol、Codex 及面向网络安全的 Daybreak，构建出能够连续数天保持专注、并随使用不断自我改进的 AI 智能体，单次可调度 1 万个智能体运行超过 36 小时。

## 详细分析

这则新闻的核心信息量在于两个数字：1 万个智能体和 36 小时以上的持续运行。当前主流 AI 智能体产品大多停留在单轮任务或短链条自动化的层面，长时间运行往往面临目标漂移、上下文退化、错误累积等工程难题。Third Moment Research 宣称其智能体能够「专注数天并随使用而改进」，如果属实，这意味着长时程自主智能体（long-horizon agent）在工程实现上迈出了实质性一步，其意义不亚于模型本身的能力提升。从技术栈看，该实验室同时调用了 GPT-6 Astra 与 GPT-6.1 Sol 两款基座模型，并引入 Codex 负责代码执行、Daybreak 负责网络安全场景，形成了一种「多模型分工 + 领域专用组件」的编排架构，这与业界从单一模型走向模型编排（model orchestration）的趋势一致。万级智能体并行运行 36 小时，对推理算力、任务调度、状态持久化和成本控制都提出了极高要求，其背后很可能是大规模推理基础设施与智能体运行时系统的结合。从行业影响看，长时程智能体的成熟将直接冲击自动化运维、安全攻防、软件工程和深度研究等场景——这些领域此前的瓶颈不在于单点智能，而在于能否让 AI 持续数天盯住一个目标。网络安全方向尤其值得关注：Daybreak 的引入暗示该实验室在为攻防对抗这类高对抗、长周期的任务做准备，而 36 小时的持续值守恰好对应真实安全运营的时间尺度。市场层面，智能体赛道竞争已从「能否完成任务」转向「能否可靠地长期完成任务」，可靠性、可观测性和单位任务成本将成为下一阶段的竞争焦点。当然，目前信息来自厂商自述，缺少第三方基准和成本披露，万级智能体 36 小时运行的实际有效产出、失败率与资源消耗仍有待验证。但可以确定的是，AI 智能体正在从演示走向生产级长时运行，这一方向已成为头部实验室的共识。

> *万级智能体连续运行 36 小时，真正的门槛不在模型智能，而在工程可靠性——谁能把长时程任务的失败率压下来，谁就能拿下企业级自动化市场。*

> 原文：[OpenAI Blog](https://openai.com/index/third-moment-research)