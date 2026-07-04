---
title: "[EN] Google推出ScreenAI：端到端视觉语言模型，统一理解UI界面与信息图表"
date: "2026-07-04T06:39:25+08:00"
slug: "en-googlescreenaiui"
source: "Google AI Blog"
source_url: "http://blog.research.google/2024/03/screenai-visual-language-model-for-ui.html"
categories:
  - 人工智能
  - 多模态模型
  - 人机交互
tags:
  - ScreenAI
  - Google Research
  - UI理解
  - 视觉语言模型
  - 信息图表
  - PaLI
  - pix2struct
summary: "Google Research发布ScreenAI，一种基于PaLI架构并融合pix2struct灵活分块策略的5B参数视觉语言模型，专为理解用户界面与信息图表设计。通过自监督预训练和屏幕标注任务，ScreenAI在WebSRC、MoTIF、ChartQA等多项基准测试中达到或超越同规模模型的最优性能，同时发布了三个新数据集。"
aigc: true
---
Google Research发布ScreenAI，一种基于PaLI架构并融合pix2struct灵活分块策略的5B参数视觉语言模型，专为理解用户界面与信息图表设计。通过自监督预训练和屏幕标注任务，ScreenAI在WebSRC、MoTIF、ChartQA等多项基准测试中达到或超越同规模模型的最优性能，同时发布了三个新数据集。

## 关键要点

- **ScreenAI采用PaLI多模态编码器与自回归解码器架构，并结合pix2struct的灵活分块策略，保持输入图像原始宽高比。**
- **模型通过屏幕标注任务自动生成UI元素（类型、位置、描述）的文本标注，并利用LLM大规模生成问答、导航和摘要训练数据。**
- **在仅5B参数下，ScreenAI在WebSRC、MoTIF上取得最优成绩，并在ChartQA、DocVQA、InfographicVQA上超越同尺寸模型。**
- **Google同步开源了Screen Annotation、ScreenQA Short和Complex ScreenQA三个新数据集，用于评估布局理解和问答能力。**

ScreenAI将UI与信息图表理解统一为单一视觉语言模型，有望降低多模态人机交互的技术门槛，为自动化界面测试、无障碍访问和数据分析工具提供新基础能力。

> 原文：[Google AI Blog](http://blog.research.google/2024/03/screenai-visual-language-model-for-ui.html)