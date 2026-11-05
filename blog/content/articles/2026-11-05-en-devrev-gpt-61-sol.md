---
title: "[EN] DevRev 借助 GPT-6.1 Sol 实现自主自助服务"
date: "2026-11-05T02:14:01+08:00"
slug: "en-devrev-gpt-61-sol"
source: "OpenAI Blog"
source_url: "https://openai.com/index/devrev-enterprise-self-service"
categories:
  - 企业服务
  - 人工智能
  - SaaS
tags:
  - DevRev
  - GPT-6.1 Sol
  - 自助服务
  - 企业AI
  - 自主执行
  - 成本优化
summary: "DevRev 利用 GPT-6.1 Sol 驱动其 Computer 和 Operator 产品，在企业服务场景中平衡推理能力、响应速度与成本，实现自主自助服务。"
aigc: true
---
DevRev 利用 GPT-6.1 Sol 驱动其 Computer 和 Operator 产品，在企业服务场景中平衡推理能力、响应速度与成本，实现自主自助服务。

## 详细分析

DevRev 此次将 GPT-6.1 Sol 引入其 Computer 与 Operator 产品线，标志着企业服务自动化正从“辅助回答”阶段迈向“自主执行”阶段。过去一年，企业级 AI 客服与自助服务市场经历了从规则引擎到检索增强生成（RAG）的快速迭代，但推理深度、响应延迟与推理成本之间的“不可能三角”始终制约着规模化落地。GPT-6.1 Sol 的定位恰好切中这一痛点：它并非单纯追求基准测试分数，而是针对企业服务场景在推理链长度、首 token 延迟和单次调用成本之间做了工程化取舍。DevRev 选择将其嵌入 Computer（面向终端用户的自助服务入口）和 Operator（面向内部运营的自动化执行层），意味着同一模型底座同时覆盖对外服务与对内运营两条链路，这有助于降低企业客户的模型选型与集成复杂度。从竞争格局看，企业服务赛道正形成三类玩家：以 Salesforce 和 ServiceNow 为代表的传统 SaaS 巨头，凭借工作流沉淀和客户基础推进 AI 增强；以 DevRev 为代表的 AI 原生平台，从 Day One 即以模型能力重构工单、知识库与运营流程；以及云厂商提供的通用模型 API。DevRev 的差异化在于将模型能力与“计算机+操作员”的产品形态深度绑定，而非简单叠加一个聊天窗口。值得关注的是，GPT-6.1 Sol 在命名上暗示了“Solution”导向，若其推理成本可控，将显著降低中型企业部署自主自助服务的门槛。市场反应方面，企业客户对“自主解决率”和“人工转接率”两类指标最为敏感，DevRev 需在真实工单分布中证明 GPT-6.1 Sol 在长尾复杂问题上的稳定性。此外，自主执行带来的权限边界与审计合规问题，仍是企业采购决策中的关键顾虑。总体而言，这条新闻折射出企业服务 AI 的竞争焦点正从“模型能力展示”转向“单位经济模型下的可靠交付”，DevRev 能否借助 GPT-6.1 Sol 在成本与体验之间找到平衡点，将决定其在 AI 原生服务管理赛道中的排位。

> *模型选型的“场景适配”正在取代“参数竞赛”，DevRev 的赌注押在工程化平衡而非跑分领先上。*

> 原文：[OpenAI Blog](https://openai.com/index/devrev-enterprise-self-service)