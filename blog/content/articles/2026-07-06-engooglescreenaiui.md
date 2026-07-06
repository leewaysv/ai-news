---
title: "[EN]Google提出ScreenAI：统一理解UI与信息图的视觉语言模型"
date: "2026-07-06T03:29:01+08:00"
slug: "engooglescreenaiui"
source: "Google AI Blog"
source_url: "http://blog.research.google/2024/03/screenai-visual-language-model-for-ui.html"
categories:
  - 人工智能
  - 计算机视觉
  - 自然语言处理
tags:
  - ScreenAI
  - 视觉语言模型
  - UI理解
  - 信息图
  - PaLI
  - pix2struct
  - Google Research
  - 屏幕注释
summary: "Google研究人员推出ScreenAI，一种基于PaLI架构与pix2struct灵活分片策略的视觉语言模型，仅5B参数即可在UI与信息图理解任务上达到业界领先水平。模型通过自监督预训练与人工标注微调，结合大规模屏幕标注数据，能完成UI元素识别、导航、问答等任务，并开源了三个新数据集。"
aigc: true
---
Google研究人员推出ScreenAI，一种基于PaLI架构与pix2struct灵活分片策略的视觉语言模型，仅5B参数即可在UI与信息图理解任务上达到业界领先水平。模型通过自监督预训练与人工标注微调，结合大规模屏幕标注数据，能完成UI元素识别、导航、问答等任务，并开源了三个新数据集。

## 关键要点

- **ScreenAI融合PaLI多模态编码器与pix2struct的动态分片策略，适应不同宽高比的屏幕图像。**
- **在WebSRC、MoTIF、Chart QA、DocVQA、InfographicVQA等基准上，以5B参数实现最佳或同类最优性能。**
- **研究团队开源Screen Annotation、ScreenQA Short和Complex ScreenQA三个数据集，用于评估布局理解与问答能力。**
- **采用两阶段训练：自监督预训练（自动生成标签）后冻结ViT，再用人工标注数据微调语言模型。**

ScreenAI统一了UI与信息图的理解范式，其‘屏幕注释+LLM自动生成训练数据’策略可能大幅降低领域标注成本，推动下一代交互界面智能化。

> 原文：[Google AI Blog](http://blog.research.google/2024/03/screenai-visual-language-model-for-ui.html)