---
title: "[EN] OpenAI 为超10亿 ChatGPT 用户快速扩展在线存储：读取速度提升12倍"
date: "2026-10-25T00:13:30+08:00"
slug: "en-openai-10-chatgpt-12"
source: "OpenAI Blog"
source_url: "https://openai.com/index/scaling-storage-one-billion-users-part-two"
categories:
  - 人工智能
  - 云计算基础设施
  - 科技公司动态
tags:
  - OpenAI
  - ChatGPT
  - Azure Cosmos DB
  - 存储扩展
  - 多租户
  - 全局缓存
  - 基础设施
summary: "OpenAI 详细介绍了如何通过可靠的多租户架构、全局缓存和 Azure Cosmos DB 扩展 Habitat 存储系统，为 ChatGPT 提供支持，实现读取速度提升 12 倍，以服务超过 10 亿用户。"
aigc: true
---
OpenAI 详细介绍了如何通过可靠的多租户架构、全局缓存和 Azure Cosmos DB 扩展 Habitat 存储系统，为 ChatGPT 提供支持，实现读取速度提升 12 倍，以服务超过 10 亿用户。

## 详细分析

OpenAI 此次披露的存储系统扩展细节，是其支撑 ChatGPT 海量用户规模的关键基础设施实践。随着 ChatGPT 用户数突破 10 亿量级，在线存储系统面临的核心挑战在于如何在高并发、多租户共享的环境中保证数据隔离、低延迟和高可靠性。OpenAI 选择以 Habitat 作为存储抽象层，结合可靠的多租户机制、全局缓存策略以及 Azure Cosmos DB 作为底层分布式数据库，最终实现读取性能提升 12 倍，这直接反映了 AI 应用规模化落地对底层基础设施提出的严苛要求。从行业背景看，生成式 AI 的爆发式增长正在重塑云基础设施的竞争格局。传统云存储方案难以满足大模型应用对元数据高频读取、会话状态快速恢复和跨区域一致性的需求，而 OpenAI 与微软 Azure 的深度绑定使其能够针对性地优化 Cosmos DB 的使用方式，形成差异化优势。这一案例也向市场传递出明确信号：AI 公司的护城河不仅在于模型能力，更在于工程化与基础设施的规模化能力。对于竞争对手而言，Anthropic、Google DeepMind 等同样在构建支撑数百万乃至数亿用户的推理与存储架构，但 OpenAI 公开的 12 倍读取提升数据为其在用户体验层面建立了可量化的优势。从商业前景看，存储读取速度的提升直接降低了 ChatGPT 的响应延迟和单位请求成本，有助于 OpenAI 在免费与付费用户之间实现更优的资源调度，并为未来多模态、长上下文等更重存储负载的功能铺平道路。此外，多租户可靠性的强调也暗示 OpenAI 正在为企业和开发者场景做准备，这与 ChatGPT 向平台化演进的战略一致。值得注意的是，OpenAI 选择在此时发布技术博客，既是对外界关于其规模化能力质疑的回应，也是一种技术品牌建设，旨在吸引基础设施人才和 enterprise 客户的信任。总体而言，这一新闻虽属技术细节披露，但折射出 AI 竞争已从模型参数竞赛延伸至存储、缓存、数据库等底层工程能力的全面较量，规模化交付能力将成为决定 AI 产品市场地位的关键变量。

> *当模型能力逐渐趋同，存储与推理基础设施的工程效率将成为 AI 产品体验分化的隐形战场。*

> 原文：[OpenAI Blog](https://openai.com/index/scaling-storage-one-billion-users-part-two)