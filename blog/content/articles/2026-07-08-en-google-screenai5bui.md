---
title: "[EN] Google ScreenAI：5B参数视觉语言模型，在UI与信息图理解任务上达到最先进水平"
date: "2026-07-07T23:13:10+08:00"
slug: "en-google-screenai5bui"
source: "Google AI Blog"
source_url: "http://blog.research.google/2024/03/screenai-visual-language-model-for-ui.html"
categories:
  - AI技术
  - 多模态学习
tags:
  - Google
  - ScreenAI
  - 视觉语言模型
  - UI理解
  - 信息图
  - PaLI
  - pix2struct
summary: "Google Research推出的ScreenAI是一种基于PaLI架构与pix2struct灵活分块策略的视觉语言模型，能以5B参数在UI与信息图理解任务中取得领先效果，同时自动生成大规模训练数据。"
aigc: true
---
Google Research推出的ScreenAI是一种基于PaLI架构与pix2struct灵活分块策略的视觉语言模型，能以5B参数在UI与信息图理解任务中取得领先效果，同时自动生成大规模训练数据。

## 关键要点

- **ScreenAI结合PaLI多模态编码器与pix2struct自适应分块策略，可处理不同长宽比的图像。**
- **在WebSRC、MoTIF、Chart QA、DocVQA和InfographicVQA等基准上，以5B参数达到同类模型最佳或最先进水平。**
- **通过屏幕注释任务和LLM自动生成问答、导航和摘要数据集，大幅降低人工标注成本。**
- **发布三个新数据集：Screen Annotation、ScreenQA Short和Complex ScreenQA，用于评估布局理解和问答能力。**

ScreenAI展示了将UI与信息图理解统一到一个轻量级模型中的可行性，其自动化数据生成方法或将为多模态AI的规模化训练开辟新路径。

> 原文：[Google AI Blog](http://blog.research.google/2024/03/screenai-visual-language-model-for-ui.html)