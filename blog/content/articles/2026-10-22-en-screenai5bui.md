---
title: "[EN] 谷歌发布ScreenAI：5B参数视觉语言模型，刷新UI与信息图理解多项基准"
date: "2026-10-22T00:36:37+08:00"
slug: "en-screenai5bui"
source: "Google AI Blog"
source_url: "http://blog.research.google/2024/03/screenai-visual-language-model-for-ui.html"
categories:
  - 人工智能
  - 多模态研究
  - 技术开源
tags:
  - ScreenAI
  - 视觉语言模型
  - UI理解
  - 信息图
  - 谷歌研究
  - PaLI
  - 数据集开源
summary: "谷歌推出ScreenAI视觉语言模型，基于PaLI架构并引入灵活分块策略，仅5B参数即在UI与信息图理解任务上达到SOTA，同时开源三个新数据集以推动屏幕理解研究。"
aigc: true
---
谷歌推出ScreenAI视觉语言模型，基于PaLI架构并引入灵活分块策略，仅5B参数即在UI与信息图理解任务上达到SOTA，同时开源三个新数据集以推动屏幕理解研究。

## 详细分析

ScreenAI的发布标志着视觉语言模型正从通用场景理解向高度结构化的界面与信息图领域纵深发展。UI和信息图虽然共享相似的设计语言（图标、布局、文本层级），但其复杂性和多样的呈现格式长期构成建模挑战。谷歌此次基于PaLI架构，融合pix2struct的灵活分块策略，使模型能够自适应保持输入图像的原始宽高比，从而在不同比例的屏幕截图上表现稳健。更值得注意的是其数据生成策略：通过DETR布局标注器、图标分类器（覆盖77类）、PaLI图像描述模型与OCR引擎的协同，自动生成大规模预训练标注；再利用LLM基于这些标注合成QA、导航和摘要训练数据，形成从自监督预训练到人工标注微调的完整流水线。仅5B参数便在WebSRC和MoTIF上取得SOTA，在ChartQA、DocVQA和InfographicVQA上与同规模模型相比表现最佳，说明高质量领域数据与架构适配比单纯扩大参数更具性价比。ScreenAI的意义在于，它为软件自动化测试、无障碍访问、智能代理操作界面等场景提供了可落地的技术底座。同时，谷歌开源Screen Annotation、ScreenQA Short和Complex ScreenQA三个数据集，有望降低该领域的研究门槛，推动屏幕理解成为多模态研究的新热点。从竞争格局看，这一方向正吸引微软、OpenAI及众多初创公司布局，但公开的专用数据集和模型权重仍稀缺，谷歌的先发开源策略可能加速生态形成，并为其在AI代理和RPA市场的长期竞争埋下伏笔。

> *ScreenAI以小参数+高质量领域数据取胜，开源数据集更是点睛之笔，UI理解赛道或将迎来新一轮军备竞赛。*

> 原文：[Google AI Blog](http://blog.research.google/2024/03/screenai-visual-language-model-for-ui.html)