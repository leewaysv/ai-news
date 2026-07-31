---
title: "[EN] 两个API设置让GPT-5.6在ARC-AGI-3基准上得分翻三倍"
date: "2026-07-31T23:15:01+08:00"
slug: "en-apigpt-56arc-agi-3"
source: "OpenAI Blog"
source_url: "https://openai.com/index/how-two-settings-tripled-our-arc-agi-3-scores"
categories:
  - AI技术
  - 基准测试
tags:
  - GPT-5.6
  - ARC-AGI-3
  - API设置
  - 推理优化
  - 上下文压缩
summary: "通过调整保留推理和启用压缩两个API设置，GPT-5.6在ARC-AGI-3基准测试上的得分和效率显著提升，性能实现三倍增长。"
aigc: true
---
通过调整保留推理和启用压缩两个API设置，GPT-5.6在ARC-AGI-3基准测试上的得分和效率显著提升，性能实现三倍增长。

## 详细分析

近日，一则关于GPT-5.6在ARC-AGI-3基准测试上的突破性进展引发AI行业广泛关注。据相关报道，仅通过调整两个API设置——保留推理（retaining reasoning）和启用压缩（enabling compaction）——模型得分便实现了三倍增长。这一发现不仅揭示了API参数配置对模型性能的巨大影响，更反映出当前大语言模型在推理能力与效率平衡方面的核心挑战。ARC-AGI-3作为衡量通用人工智能（AGI）能力的重要基准，其难度远超传统自然语言处理任务，要求模型具备抽象推理和模式识别能力。GPT-5.6在此基准上的显著提升，意味着通过精细化的推理流程管理，可以在不增加模型规模的前提下大幅增强其高阶认知能力。从行业背景来看，目前各大AI实验室对AGI的追求已从单纯的参数竞赛转向推理效率与成本控制的综合优化。OpenAI、Google DeepMind等企业均在探索如何通过推理时计算（inference-time compute）和上下文压缩来提升模型表现。此次案例表明，API级别的配置优化有望成为未来模型迭代之外的又一重要增量来源，尤其对于企业用户而言，合理的参数调优可能带来数倍于默认设置的实际收益。市场方面，这一发现可能促使更多企业加大对API调优的投入，衍生出针对特定基准的配置优化服务，进一步推动AI工程化生态的成熟。尽管其具体技术细节尚待公开，但可以预见，推理保留与压缩机制的协同优化将成为后续模型版本的核心卖点之一。整体而言，这一进展不仅为AGI研究提供了新的思路，也为商业化部署中的性能调优指明了方向，其影响或将辐射至整个AI产业链的研发与运营模式。

> *在模型能力日趋同质化的当下，参数配置的精细优化可能成为拉开差距的关键，这为AI工程化领域注入了新的想象空间。*

> 原文：[OpenAI Blog](https://openai.com/index/how-two-settings-tripled-our-arc-agi-3-scores)