---
title: "[EN] ScreenAI：面向UI与信息图的视觉语言模型，5B参数达SOTA"
date: "2026-07-05T01:52:07+08:00"
slug: "en-screenaiui5bsota"
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
  - Google Research
  - PaLI
  - pix2struct
summary: "Google Research发布ScreenAI，一种基于PaLI架构并融合pix2struct灵活分块策略的视觉语言模型。该模型在仅有5B参数的情况下，在WebSRC、MoTIF等UI及信息图任务上达到最优水平，并在Chart QA、DocVQA等基准测试中超越同规模模型。研究团队还开源了Screen Annotation、ScreenQA Short和Complex ScreenQA三个新数据集。"
aigc: true
---
Google Research发布ScreenAI，一种基于PaLI架构并融合pix2struct灵活分块策略的视觉语言模型。该模型在仅有5B参数的情况下，在WebSRC、MoTIF等UI及信息图任务上达到最优水平，并在Chart QA、DocVQA等基准测试中超越同规模模型。研究团队还开源了Screen Annotation、ScreenQA Short和Complex ScreenQA三个新数据集。

## 关键要点

- **ScreenAI采用PaLI多模态编码器-解码器架构，并引入pix2struct的灵活分块策略，保持输入图像的原始宽高比。**
- **模型通过两阶段训练：先自监督预训练（自动生成标签），再在人工标注数据上微调。预训练基于大规模截图（桌面、移动、平板）和自动化布局标注（DETR、OCR、图标分类器）。**
- **利用大语言模型(LLM)自动生成问答、UI导航及摘要训练数据，大幅扩展了数据集规模。**
- **在UI元素识别（类型、位置、描述）任务上表现突出，Screen Annotation任务成为评估布局理解能力的新基准。**

ScreenAI展示了小参数模型在UI与信息图理解上追赶甚至超越大模型的潜力，其灵活的分块策略和LLM辅助数据生成方法或将为未来视觉语言模型的设计提供新思路，尤其适用于资源受限的设备端部署。

> 原文：[Google AI Blog](http://blog.research.google/2024/03/screenai-visual-language-model-for-ui.html)