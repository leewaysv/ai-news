---
title: "[EN] 谷歌发布ScreenAI：5B参数视觉语言模型，专攻UI与信息图理解"
date: "2026-11-28T03:51:58+08:00"
slug: "en-screenai5bui"
source: "Google AI Blog"
source_url: "http://blog.research.google/2024/03/screenai-visual-language-model-for-ui.html"
categories:
  - 人工智能
  - 多模态模型
  - 谷歌研究
tags:
  - ScreenAI
  - 视觉语言模型
  - UI理解
  - 信息图
  - PaLI
  - pix2struct
  - 数据集开源
  - 谷歌
summary: "谷歌研究团队推出ScreenAI，一个基于PaLI架构并采用pix2struct灵活分块策略的视觉语言模型，专门用于理解用户界面（UI）和信息图（如 charts、diagrams、tables）。该模型仅5B参数，在WebSRC、MoTIF等UI任务上取得SOTA，在Chart QA、DocVQA、InfographicVQA上达到同尺寸最佳性能，并开源了三个新数据集以推动该领域评估。"
aigc: true
---
谷歌研究团队推出ScreenAI，一个基于PaLI架构并采用pix2struct灵活分块策略的视觉语言模型，专门用于理解用户界面（UI）和信息图（如 charts、diagrams、tables）。该模型仅5B参数，在WebSRC、MoTIF等UI任务上取得SOTA，在Chart QA、DocVQA、InfographicVQA上达到同尺寸最佳性能，并开源了三个新数据集以推动该领域评估。

## 详细分析

ScreenAI的发布标志着视觉语言模型向更细分的专业场景——UI与信息图理解——迈出了重要一步。传统上，UI和信息图因其复杂的布局、多样的呈现格式和丰富的视觉语言（图标、布局等），一直是多模态模型面临的独特挑战。谷歌此次将PaLI架构与pix2struct的灵活分块策略结合，使模型能够适应不同长宽比的图像，这直接回应了UI截图和设备多样性带来的现实问题。更值得关注的是其数据生成策略：通过布局标注器（基于DETR）、图标分类器（可区分77种图标类型）、OCR引擎以及PaLI图像描述模型，自动生成大规模预训练数据，并利用大语言模型（LLM）自动生成QA、UI导航和摘要训练数据集。这种“以模型生成数据、以数据训练模型”的闭环，显著降低了人工标注成本，为多模态模型的规模化训练提供了可复用的范式。在性能上，仅5B参数的ScreenAI在WebSRC和MoTIF上达到SOTA，并在Chart QA、DocVQA、InfographicVQA上优于同尺寸模型，说明专业化的架构与数据策略可以在较小参数量下实现高效能，这对边缘部署和成本敏感的应用场景具有吸引力。此外，谷歌同步开源Screen Annotation、ScreenQA Short和Complex ScreenQA三个数据集，覆盖布局理解与问答能力评估，有望填补UI领域标准化评测的空白，促进学术与工业界的横向比较。从行业影响看，UI理解是智能助手、自动化测试、无障碍访问和RPA（机器人流程自动化）的核心能力，ScreenAI的进展将加速这些应用的智能化升级。同时，该模型与谷歌现有的PaLI、Gemini等形成互补，强化了其在多模态基础模型领域的布局。不过，UI和信息图的动态性、跨平台差异以及隐私问题仍是落地挑战，模型在真实复杂场景中的泛化能力有待进一步验证。总体而言，ScreenAI是一次兼顾架构创新、数据工程与评测体系建设的系统性工作，为视觉语言模型在垂直领域的深化提供了重要参考。

> *ScreenAI以5B参数实现UI与信息图理解的SOTA，证明了“专业架构+自动数据生成”在垂直多模态任务中的高效性，其开源数据集更值得关注。*

> 原文：[Google AI Blog](http://blog.research.google/2024/03/screenai-visual-language-model-for-ui.html)