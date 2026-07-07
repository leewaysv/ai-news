---
title: "[EN] Google发布ScreenAI：面向UI与信息图的视觉语言模型"
date: "2026-07-07T09:50:10+08:00"
slug: "en-googlescreenaiui"
source: "Google AI Blog"
source_url: "http://blog.research.google/2024/03/screenai-visual-language-model-for-ui.html"
categories:
  - 人工智能
  - 多模态学习
  - 视觉语言模型
tags:
  - ScreenAI
  - Google Research
  - UI理解
  - 信息图
  - PaLI
  - pix2struct
  - 多模态模型
summary: "Google Research推出ScreenAI，一种基于PaLI架构并融合pix2struct灵活分块策略的视觉语言模型，专为理解用户界面和信息图设计。该模型仅5B参数，在WebSRC、MoTIF等UI及信息图任务上达到最先进水平，并在Chart QA、DocVQA等任务上同类最佳。"
aigc: true
---
Google Research推出ScreenAI，一种基于PaLI架构并融合pix2struct灵活分块策略的视觉语言模型，专为理解用户界面和信息图设计。该模型仅5B参数，在WebSRC、MoTIF等UI及信息图任务上达到最先进水平，并在Chart QA、DocVQA等任务上同类最佳。

## 关键要点

- **ScreenAI结合PaLI多模态编码器与pix2struct的宽高比保留分块策略，能处理不同比例的屏幕截图与信息图。**
- **通过自动布局标注、OCR、图标分类及PaLI图像描述生成大规模预训练数据，并利用LLM自动生成QA、导航和摘要训练集。**
- **在UI任务（WebSRC、MoTIF）上取得SOTA，在图表问答（Chart QA）、文档VQA和信息图VQA上相比同等规模模型表现最佳。**
- **开源三个新数据集：Screen Annotation（布局理解）、ScreenQA Short和Complex ScreenQA（综合问答评估）。**

ScreenAI通过统一建模UI和信息图，展示了多模态模型在交互式界面理解上的巨大潜力，其灵活的预训练数据生成策略有望降低对人工标注的依赖，推动UI自动化测试、无障碍访问等应用发展。

> 原文：[Google AI Blog](http://blog.research.google/2024/03/screenai-visual-language-model-for-ui.html)