---
title: "[EN] ScreenAI：谷歌发布针对UI和信息图表的视觉语言模型"
date: "2026-07-06T23:17:03+08:00"
slug: "en-screenaiui"
source: "Google AI Blog"
source_url: "http://blog.research.google/2024/03/screenai-visual-language-model-for-ui.html"
categories:
  - 人工智能
  - 计算机视觉
  - 自然语言处理
tags:
  - ScreenAI
  - Visual Language Model
  - Google Research
  - UI Understanding
  - Infographic Understanding
  - PaLI
  - pix2struct
summary: "Google Research 推出了 ScreenAI，一个仅 5B 参数的视觉语言模型，专门用于理解用户界面和信息图表。该模型基于 PaLI 架构与 pix2struct 的灵活分块策略，在多个基准测试中取得领先结果，并配套发布了三个新数据集以评估布局理解与问答能力。"
aigc: true
---
Google Research 推出了 ScreenAI，一个仅 5B 参数的视觉语言模型，专门用于理解用户界面和信息图表。该模型基于 PaLI 架构与 pix2struct 的灵活分块策略，在多个基准测试中取得领先结果，并配套发布了三个新数据集以评估布局理解与问答能力。

## 关键要点

- **ScreenAI 结合了 PaLI 多模态架构与 pix2struct 的宽高比自适应分块策略，能够处理不同尺寸的 UI 截图与信息图。**
- **该模型通过自监督预训练与人工标注微调两阶段训练，在 WebSRC、MoTIF 等 UI 任务以及 ChartQA、DocVQA 等图表任务上达到最优性能。**
- **研究团队开源了 Screen Annotation、ScreenQA Short 和 Complex ScreenQA 三个新数据集，用于评估模型的布局理解与复杂问答能力。**
- **数据生成流程利用了 DETR 布局标注器、图标分类器、OCR 以及 PaLI 描述生成器，并结合大语言模型自动生产问答和导航训练样本。**

ScreenAI 仅用 5B 参数就在多个 UI 与视觉语言理解任务上实现最佳性能，证明了混合数据策略和灵活架构的有效性，为用户界面自动化与无障碍交互提供了低成本、高精度的新方案。

> 原文：[Google AI Blog](http://blog.research.google/2024/03/screenai-visual-language-model-for-ui.html)