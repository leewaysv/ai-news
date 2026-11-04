---
title: "[EN] 谷歌发布ScreenAI：5B参数视觉语言模型，刷新UI与信息图理解多项基准"
date: "2026-11-04T02:10:42+08:00"
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
  - 信息图
  - PaLI
  - pix2struct
  - 谷歌
  - 多模态
  - 智能体
  - 数据集开源
summary: "谷歌研究院推出ScreenAI，一个仅5B参数的视觉语言模型，专门用于理解用户界面（UI）和信息图（图表、示意图、表格等）。该模型基于PaLI架构并采用pix2struct的灵活分块策略，通过新颖的屏幕标注任务自动生成大规模训练数据，在WebSRC、MoTIF、ChartQA、DocVQA和InfographicVQA等基准上取得同类规模模型中的最佳成绩，同时开源三个新数据集。"
aigc: true
---
谷歌研究院推出ScreenAI，一个仅5B参数的视觉语言模型，专门用于理解用户界面（UI）和信息图（图表、示意图、表格等）。该模型基于PaLI架构并采用pix2struct的灵活分块策略，通过新颖的屏幕标注任务自动生成大规模训练数据，在WebSRC、MoTIF、ChartQA、DocVQA和InfographicVQA等基准上取得同类规模模型中的最佳成绩，同时开源三个新数据集。

## 详细分析

ScreenAI的发布标志着视觉语言模型正从通用场景理解向高度结构化的专业领域纵深推进。UI和信息图是人类与数字世界交互的核心载体，但其设计语言虽相似却因设备、平台和呈现格式的多样性而构成独特的建模挑战。谷歌此次的切入点颇具战略眼光：不同于将UI理解视为OCR加规则引擎的传统路径，ScreenAI将屏幕视为一种需要整体推理的视觉语言，这契合了当前多模态大模型从感知走向认知的趋势。

从技术路线看，ScreenAI的务实之处在于数据工程创新。其核心贡献之一是Screen Annotation任务——模型需识别UI元素的类型、位置和描述，这些文本标注反过来为LLM提供屏幕描述，从而自动生成问答、导航和摘要训练数据。这一自举式数据生成闭环大幅降低了人工标注成本，是5B小模型能够匹敌更大模型的关键。配合DETR布局标注器、77类图标分类器、PaLI图像描述模型和OCR引擎的多源融合，ScreenAI构建了目前最精细的屏幕理解数据管线之一。

性能层面，5B参数在WebSRC和MoTIF上达到SOTA，在ChartQA、DocVQA和InfographicVQA上取得同类最佳，这一结果具有双重意义。其一，它证明在垂直领域，精心设计的数据策略可以显著弥补模型规模的不足，这对算力受限的研究者和中小企业具有参考价值。其二，UI理解是智能体（Agent）落地的关键能力——无论是自动化测试、无障碍辅助还是RPA流程自动化，都需要模型精确感知屏幕元素及其语义关系。ScreenAI的轻量化特征使其更适合端侧或边缘部署，这与谷歌将AI能力下沉到Android生态的长期战略一致。

竞争格局方面，UI理解赛道正变得拥挤。微软的OmniParser、Anthropic的Computer Use以及众多开源UI代理项目都在争夺同一战场，但多数工作聚焦于智能体执行层面，ScreenAI则更偏向基础理解能力与评测基准建设。谷歌同步开源Screen Annotation、ScreenQA Short和Complex ScreenQA三个数据集，意图明显：通过定义评测标准来掌握该领域的话语权，这与它在NLP领域通过GLUE、SuperGLUE建立影响力的路径如出一辙。

更深远的影响在于，UI理解正在成为多模态模型的新竞技场。随着AI智能体从对话走向操作，模型必须理解按钮、菜单、表单和图表背后的意图，而不仅仅是识别像素。ScreenAI的发布补上了谷歌在屏幕语义理解上的拼图，也为后续将Gemini能力嵌入ChromeOS、Android和Workspace埋下伏笔。不过，5B模型的局限同样明显——复杂动态界面、跨应用工作流和长上下文屏幕序列的理解仍有待验证，真实场景的鲁棒性也需更多独立评测。

> *谷歌用5B小模型加数据工程撬动UI理解赛道，既展示了自举式数据生成的效率，也暗含以开源数据集定义评测标准的生态野心。*

> 原文：[Google AI Blog](http://blog.research.google/2024/03/screenai-visual-language-model-for-ui.html)