---
title: "[EN] OpenAI 推进低资源编程语言支持，扩展 ChatGPT 代码能力"
date: "2026-10-21T00:32:37+08:00"
slug: "en-openai-chatgpt"
source: "OpenAI Blog"
source_url: "https://openai.com/index/low-resource-programming-languages"
categories:
  - AI 编程
  - 开发者工具
  - 企业软件
tags:
  - OpenAI
  - ChatGPT
  - 低资源编程语言
  - COBOL
  - SQLite
  - 遗留系统迁移
  - 代码评估基准
summary: "OpenAI 宣布改进 ChatGPT 在低资源编程语言上的表现，并针对软件工程、SQLite 和 COBOL 迁移场景推出新评估。此举旨在提升模型在非主流语言和遗留系统现代化中的实用性。"
aigc: true
---
OpenAI 宣布改进 ChatGPT 在低资源编程语言上的表现，并针对软件工程、SQLite 和 COBOL 迁移场景推出新评估。此举旨在提升模型在非主流语言和遗留系统现代化中的实用性。

## 详细分析

OpenAI 此次动作的核心信号并不只是“ChatGPT 又变强了”，而是其开始系统性地补齐编程语言覆盖面上的结构性短板。长期以来，主流大模型在 Python、JavaScript、Java 等高频语言上表现优异，但在 COBOL、Fortran、Ada、RPG 等低资源语言上能力明显不足。这些语言虽然在新项目中的使用频率不高，却大量存在于金融、政府、航空、保险等关键行业的遗留系统中。以 COBOL 为例，全球仍有大量核心银行和保险系统依赖其运行，而掌握 COBOL 的开发者数量持续下降，迁移和維護需求与人才供给之间存在显著缺口。OpenAI 针对 COBOL 迁移推出评估，实际上是瞄准了企业级存量系统现代化这一高价值场景。SQLite 评估的加入同样值得注意，它意味着 OpenAI 在关注“语言”之外，也在向嵌入式数据库、轻量级数据管理等实际工程任务延伸，这更贴近开发者的日常使用路径。从竞争格局看，GitHub Copilot、Anthropic 的 Claude 以及各类代码专用模型都在争夺开发者入口，而低资源语言和遗留系统迁移是一个相对空白但付费意愿较强的细分市场。OpenAI 通过发布评估基准而非单纯宣称能力提升，也在试图建立可量化的信任基础。更深层的影响在于，如果大模型能够可靠地辅助 COBOL 等语言的阅读、解释和迁移，将显著降低企业现代化改造的门槛和成本，可能加速金融和公共部门的技术债务清理进程。当然，低资源语言的核心难题在于训练数据稀缺，评估基准的推出只是第一步，实际迁移中的正确性、安全性和可审计性仍需长期验证。

> *低资源语言是代码大模型最后的硬骨头之一，谁先啃下 COBOL 迁移，谁就握住了金融和政府市场的钥匙。*

> 原文：[OpenAI Blog](https://openai.com/index/low-resource-programming-languages)