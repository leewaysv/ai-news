---
title: "[EN] 谷歌发布ScreenAI：5B参数视觉语言模型，刷新UI与信息图理解多项基准"
date: "2026-11-23T02:31:50+08:00"
slug: "en-screenai5bui"
source: "Google AI Blog"
source_url: "http://blog.research.google/2024/03/screenai-visual-language-model-for-ui.html"
categories:
  - 人工智能
  - 多模态研究
  - 人机交互
tags:
  - ScreenAI
  - 视觉语言模型
  - UI理解
  - 信息图
  - 谷歌研究
  - PaLI
  - 数据集开源
summary: "谷歌研究团队推出ScreenAI，一种基于PaLI架构并融合pix2struct灵活分块策略的视觉语言模型，专用于理解用户界面（UI）和信息图（图表、示意图、表格）。该模型仅5B参数，在WebSRC、MoTIF等UI与信息图任务上达到最先进水平，在Chart QA、DocVQA、InfographicVQA等基准上同类模型中表现最佳，并同步开源三个新数据集。"
aigc: true
---
谷歌研究团队推出ScreenAI，一种基于PaLI架构并融合pix2struct灵活分块策略的视觉语言模型，专用于理解用户界面（UI）和信息图（图表、示意图、表格）。该模型仅5B参数，在WebSRC、MoTIF等UI与信息图任务上达到最先进水平，在Chart QA、DocVQA、InfographicVQA等基准上同类模型中表现最佳，并同步开源三个新数据集。

## 详细分析

ScreenAI的发布标志着视觉语言模型正从通用场景理解向高度结构化的专业领域纵深推进。UI和信息图是人机交互的核心载体，但其设计原则相似而呈现格式千变万化，长期构成建模难题。谷歌此次的解法颇具巧思：以PaLI多模态编码器-解码器为骨架，引入pix2struct的灵活分块策略，按输入图像原生宽高比动态选择网格尺寸，使模型能稳健处理横屏、竖屏、桌面端、移动端等各种比例的界面截图。更关键的是数据工程创新——Screen Annotation任务要求模型识别UI元素的类型、位置和描述，这些文本标注反过来喂给大语言模型，自动规模化生成问答、导航和摘要训练数据，形成“标注-生成-训练”的飞轮效应。5B参数在WebSRC和MoTIF上取得SOTA，在Chart QA、DocVQA、InfographicVQA上同类最优，说明精巧的架构与高质量数据组合可以弥补参数规模的不足，这对算力受限的落地场景具有直接参考价值。同步开源的Screen Annotation、ScreenQA Short和Complex ScreenQA三个数据集，覆盖布局理解与问答能力的多维评估，有望成为UI理解领域的标准测试床。从竞争格局看，UI理解正成为多模态模型的重要战场：微软、Anthropic等均在探索屏幕代理（screen agent）能力，ScreenAI以轻量化和数据集开放为差异化抓手，可能加速浏览器自动化、无障碍辅助、智能办公助手等应用的成熟。值得留意的是，模型训练分两阶段——自监督预训练自动生成标签训练ViT和语言模型，微调阶段冻结ViT并使用人工标注数据，这种“自监督打底、人工精调”的范式在数据成本与质量间取得了平衡。总体而言，ScreenAI的价值不仅在于基准分数，更在于它提供了一套可复用的数据生成方法论和开放评估体系，为UI理解从实验室走向产品化铺平了道路。

> *5B参数即达SOTA，证明数据工程与架构适配比盲目堆参数更值得投入；三个数据集的开放或将催生UI理解领域的“ImageNet时刻”。*

> 原文：[Google AI Blog](http://blog.research.google/2024/03/screenai-visual-language-model-for-ui.html)