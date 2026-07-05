---
title: "[EN] ScreenAI：谷歌发布5B参数视觉语言模型，统一理解UI与信息图"
date: "2026-07-05T23:11:18+08:00"
slug: "en-screenai5bui"
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
  - 谷歌
  - PaLI
  - pix2struct
summary: "谷歌研究团队推出ScreenAI，一个仅5B参数的视觉语言模型，基于PaLI架构和pix2struct的灵活分块策略，在UI元素识别、图表问答等任务上达到最优性能，并开源了Screen Annotation、ScreenQA Short和Complex ScreenQA三个新数据集。"
aigc: true
---
谷歌研究团队推出ScreenAI，一个仅5B参数的视觉语言模型，基于PaLI架构和pix2struct的灵活分块策略，在UI元素识别、图表问答等任务上达到最优性能，并开源了Screen Annotation、ScreenQA Short和Complex ScreenQA三个新数据集。

## 关键要点

- **ScreenAI采用PaLI多模态编码器+自回归解码器架构，并引入pix2struct的灵活分块策略以保持输入图像原始宽高比。**
- **模型通过两阶段训练：先自监督预训练（自动标注屏幕元素、图标和OCR文本），再在人工标注数据上微调，最终在WebSRC、MoTIF、Chart QA等基准上取得领先。**
- **利用LLM自动生成问答、UI导航和摘要训练数据，解决了大规模标注难题；发布的Screen Annotation数据集用于评估布局理解。**

ScreenAI以较小参数量统一处理UI与信息图，证实了视觉语言模型在界面理解和人机交互中的潜力，其自动化数据生成管线或加速下游应用落地。

> 原文：[Google AI Blog](http://blog.research.google/2024/03/screenai-visual-language-model-for-ui.html)