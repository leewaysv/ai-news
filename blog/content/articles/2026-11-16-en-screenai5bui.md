---
title: "[EN] ScreenAI：谷歌推出5B参数视觉语言模型，统一理解UI与信息图表"
date: "2026-11-16T01:50:33+08:00"
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
  - 信息图表
  - PaLI
  - pix2struct
  - 谷歌
  - 多模态
  - 数据集开源
summary: "谷歌发布ScreenAI，一个仅5B参数的视觉语言模型，基于PaLI架构与pix2struct弹性分块策略，在UI和信息图表理解任务上达到SOTA，并开源三个新数据集。"
aigc: true
---
谷歌发布ScreenAI，一个仅5B参数的视觉语言模型，基于PaLI架构与pix2struct弹性分块策略，在UI和信息图表理解任务上达到SOTA，并开源三个新数据集。

## 详细分析

谷歌此次发布的ScreenAI瞄准了一个长期被忽视但极具商业价值的领域：屏幕界面与信息图表的机器理解。与传统视觉语言模型聚焦自然图像不同，ScreenAI专门针对UI截图、图表、表格、信息图等“视觉情境化语言”进行优化，这背后是谷歌对AI交互入口的深远布局。从技术路径看，ScreenAI在PaLI架构上引入pix2struct的弹性分块策略，使模型能适应不同长宽比的屏幕图像，这一设计直接回应了UI截图尺寸多样化的现实挑战。更值得关注的是其数据生成思路：通过Screen Annotation任务自动标注UI元素的类型、位置和描述，再借助大语言模型规模化生成QA、导航和摘要训练数据，形成“自监督预训练+人工微调”的两阶段闭环。这种将标注成本从人力转向算力的策略，是当前多模态模型降本增效的典型范式。在性能上，5B参数的ScreenAI在WebSRC和MoTIF上取得SOTA，在Chart QA、DocVQA和InfographicVQA上与同规模模型相比表现最佳，说明专用化小模型在垂直场景中仍能与通用大模型形成差异化竞争。从行业影响看，UI理解是智能代理（Agent）自动操作软件、无障碍辅助技术、自动化测试和RPA等场景的核心能力。ScreenAI开源三个数据集（Screen Annotation、ScreenQA Short、Complex ScreenQA）的举动，有望降低该领域的研究门槛，加速UI理解从学术基准向产业应用的转化。不过，5B参数的模型在端侧部署仍有挑战，且UI理解的真实场景远比基准测试复杂——动态界面、多语言布局、暗黑模式等边缘情况仍需验证。总体而言，ScreenAI代表了多模态模型从“看懂世界”向“看懂工具”的演进方向，其数据生成方法论比模型本身更具复用价值。

> *当大模型竞赛聚焦参数规模时，谷歌用5B的ScreenAI提醒业界：理解人类与软件交互的界面语言，或许是AI成为真正生产力工具的关键一步。*

> 原文：[Google AI Blog](http://blog.research.google/2024/03/screenai-visual-language-model-for-ui.html)