---
title: "[EN] OpenAI 扩展 ChatGPT 对低资源编程语言的支持，新增软件工程、SQLite 与 COBOL 迁移评估"
date: "2026-10-20T01:03:36+08:00"
slug: "en-openai-chatgpt-sqlite-cobol"
source: "OpenAI Blog"
source_url: "https://openai.com/index/low-resource-programming-languages"
categories:
  - 人工智能
  - 软件开发
  - 企业技术
tags:
  - OpenAI
  - ChatGPT
  - 低资源编程语言
  - COBOL
  - SQLite
  - 代码迁移
  - 评估基准
summary: "OpenAI 宣布正在提升 ChatGPT 在低资源编程语言上的能力，并推出了针对软件工程、SQLite 和 COBOL 迁移的新评估基准，以衡量和推动模型在非主流语言场景下的编码表现。"
aigc: true
---
OpenAI 宣布正在提升 ChatGPT 在低资源编程语言上的能力，并推出了针对软件工程、SQLite 和 COBOL 迁移的新评估基准，以衡量和推动模型在非主流语言场景下的编码表现。

## 详细分析

OpenAI 此次针对低资源编程语言的改进，表面上是一次模型能力的常规扩展，实则触及了 AI 编程助手市场一个长期被忽视的结构性缺口。过去两年，ChatGPT、GitHub Copilot 等工具在 Python、JavaScript、TypeScript 等主流语言上的表现突飞猛进，但在 COBOL、Fortran、Ada、RPG 等“老牌”语言以及 SQLite 这类嵌入式数据库场景中，模型输出质量参差不齐。原因并不复杂：训练语料中低资源语言的代码占比极低，公开基准也几乎不覆盖这些场景，导致模型在遇到此类任务时容易产生看似合理实则错误的代码，而这类错误在金融、政府、航空等仍大量运行 COBOL 系统的关键行业中代价极高。

从行业背景看，低资源编程语言并非小众玩具。以 COBOL 为例，全球仍有大量核心银行、保险和政务系统运行在 COBOL 之上，而掌握这些语言的开发者正加速退休，人才断层已成为 CIO 们公开承认的风险。IBM 等厂商多年来推动 COBOL 现代化迁移，但自动迁移工具的实际成功率有限，大量工作仍依赖人工审校。如果 ChatGPT 能在 COBOL 代码理解、迁移建议和 SQLite 查询优化等任务上给出可靠输出，其商业价值将直接指向企业级现代化改造预算。OpenAI 此次专门为 COBOL 迁移和 SQLite 建立评估，说明其目标不仅是“能写”，而是“能评估、可度量”，这是向企业客户证明可靠性的必要一步。

从竞争格局看，这一动作也有明确的防御意味。GitHub Copilot 依托 GitHub 代码语料和 Visual Studio 生态，在企业存量代码库中具备天然入口优势；Anthropic 的 Claude 在代码任务上持续加码，并以长上下文和代码库理解能力争取企业客户；Google 则将 Gemini 嵌入 Cloud 和 Android 开发链路。OpenAI 若只在主流语言上保持领先，容易在企業存量系统这一高价值场景中被对手差异化切入。补齐低资源语言评估，等于在“遗留系统现代化”这一细分战场上提前布防。

更值得关注的是评估方法论本身。低资源语言缺乏大规模高质量测试集，OpenAI 需要自行构建评估基准，这既是技术投入也是话语权布局——谁定义了评估标准，谁就在一定程度上定义了“好用”的含义。不过，评估基准的公开程度、可复现性以及是否覆盖真实企业代码的复杂性，将决定这些指标是营销素材还是工程参考。对开发者而言，短期内的实际收益可能有限，但方向值得肯定：AI 编程助手的下一阶段竞争，很可能不在“写新代码”，而在“读懂旧代码”。

> *评估基准的建立比模型微调更能说明 OpenAI 的企业市场意图——低资源语言是 AI 编程助手最难啃、也最值钱的骨头。*

> 原文：[OpenAI Blog](https://openai.com/index/low-resource-programming-languages)