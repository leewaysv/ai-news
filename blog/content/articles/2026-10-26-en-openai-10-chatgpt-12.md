---
title: "[EN] OpenAI 为超10亿 ChatGPT 用户快速扩展在线存储，读取速度提升12倍"
date: "2026-10-26T00:06:30+08:00"
slug: "en-openai-10-chatgpt-12"
source: "OpenAI Blog"
source_url: "https://openai.com/index/scaling-storage-one-billion-users-part-two"
categories:
  - AI基础设施
  - 云计算
  - 技术工程
tags:
  - OpenAI
  - ChatGPT
  - Azure Cosmos DB
  - 存储扩展
  - 多租户
  - 全局缓存
  - 性能优化
summary: "OpenAI 通过可靠的多租户架构、全局缓存和 Azure Cosmos DB 扩展 Habitat 存储系统，为 ChatGPT 提供支持，实现读取速度提升 12 倍，以服务超过 10 亿用户。"
aigc: true
---
OpenAI 通过可靠的多租户架构、全局缓存和 Azure Cosmos DB 扩展 Habitat 存储系统，为 ChatGPT 提供支持，实现读取速度提升 12 倍，以服务超过 10 亿用户。

## 详细分析

OpenAI 此次披露的存储系统扩展细节，是其支撑 ChatGPT 超 10 亿用户规模的关键技术底座。Habitat 作为在线存储层，面临的核心挑战在于多租户环境下的数据隔离、一致性与低延迟访问。通过引入可靠的多租户机制、全局缓存层以及 Azure Cosmos DB 的分布式能力，OpenAI 将读取性能提升了 12 倍，这直接关系到 ChatGPT 在高并发场景下的响应速度和用户体验。从行业背景看，生成式 AI 应用的用户规模正以前所未有的速度增长，ChatGPT 作为头部产品，其基础设施压力具有代表性。传统云存储方案在面对 AI 工作负载时往往暴露出延迟高、扩展成本大等问题，OpenAI 的实践表明，结合全局缓存与托管数据库的混合架构可以在不牺牲可靠性的前提下实现线性扩展。市场层面，这一技术进展对云服务商和 AI 基础设施赛道具有信号意义：Azure Cosmos DB 作为核心组件被点名，强化了微软与 OpenAI 深度绑定的叙事，也可能促使其他 AI 公司重新评估其存储栈选型。竞争格局上，Anthropic、Google Gemini 等对手同样在扩大用户规模，存储与缓存效率将成为模型之外的第二战场。商业前景方面，更快的读取意味着更低的单位推理成本和更高的用户留存，对于 OpenAI 探索广告、企业版等变现路径构成支撑。值得注意的是，OpenAI 选择公开分享工程细节，既是对技术品牌的塑造，也有助于吸引基础设施人才。不过，12 倍提升的具体基准和成本影响尚未披露，实际生产环境中的长尾延迟和跨区域一致性仍是持续挑战。总体而言，这篇工程博客揭示了 AI 规模化落地的隐性门槛：模型能力之外，存储与数据层的工程创新同样决定产品能否承载十亿级用户。

> *当行业目光聚焦于模型参数时，OpenAI 用一篇存储工程博客提醒我们：十亿级 AI 产品的护城河，往往藏在缓存和数据库的毫秒之间。*

> 原文：[OpenAI Blog](https://openai.com/index/scaling-storage-one-billion-users-part-two)