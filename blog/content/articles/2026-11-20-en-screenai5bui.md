---
title: "[EN] 谷歌发布ScreenAI：5B参数视觉语言模型，刷新UI与信息图理解多项基准"
date: "2026-11-20T03:00:39+08:00"
slug: "en-screenai5bui"
source: "Google AI Blog"
source_url: "http://blog.research.google/2024/03/screenai-visual-language-model-for-ui.html"
categories:
  - 人工智能
  - 多模态大模型
  - 学术研究
tags:
  - ScreenAI
  - 视觉语言模型
  - UI理解
  - 信息图
  - 谷歌
  - PaLI
  - pix2struct
  - 数据集开源
summary: "谷歌研究团队推出ScreenAI，一种基于PaLI架构并融合pix2struct灵活分块策略的视觉语言模型，专门用于理解用户界面和信息图。该模型仅5B参数便在WebSRC、MoTIF等UI理解任务上达到SOTA，并在Chart QA、DocVQA、InfographicVQA上表现领先，同时开源三个新数据集。"
aigc: true
---
谷歌研究团队推出ScreenAI，一种基于PaLI架构并融合pix2struct灵活分块策略的视觉语言模型，专门用于理解用户界面和信息图。该模型仅5B参数便在WebSRC、MoTIF等UI理解任务上达到SOTA，并在Chart QA、DocVQA、InfographicVQA上表现领先，同时开源三个新数据集。

## 详细分析

ScreenAI的发布标志着视觉语言模型正从通用场景理解向高度结构化的专业领域纵深发展。UI界面与信息图（图表、示意图、表格）是人类数字交互的核心载体，但其设计语言虽共享图标、布局等原则，却因呈现格式多变、元素密集而构成独特的建模挑战。谷歌此次将PaLI的多模态编码器-自回归解码器架构与pix2struct的灵活分块策略结合，使模型能自适应保持输入图像的原始宽高比，从而在桌面、移动、平板等多设备截图间泛化。这一技术路径的巧妙之处在于：它不追求参数规模的军备竞赛，而是以5B的轻量级体量实现专精性能，在WebSRC和MoTIF上超越同规模甚至更大模型，在Chart QA、DocVQA、InfographicVQA上亦表现领先，这为端侧部署和实时UI交互提供了现实可能。更值得关注的是其数据生成流水线——利用DETR布局标注器、77类图标分类器、PaLI图像描述模型与OCR引擎协同构建屏幕的详细文本描述，再借助LLM自动生成QA、导航和摘要训练数据。这种“用模型造数据、用数据训模型”的飞轮效应，有效缓解了UI领域人工标注成本高昂的瓶颈。谷歌同步开源Screen Annotation、ScreenQA Short和Complex ScreenQA三个数据集，既为学术社区建立了可复现的评测基准，也透露出其争夺UI理解领域标准制定权的意图。从行业影响看，ScreenAI直接指向RPA自动化、无障碍辅助、智能客服和移动应用测试等场景——模型能识别UI元素类型、位置与描述，意味着软件代理可更精准地“看懂”屏幕并执行导航操作。当前多模态大模型竞争聚焦于图文问答和文档理解，而UI与信息图这一垂直赛道的专用模型尚属稀缺，谷歌以轻量级模型加开源数据集的组合拳切入，有望加速该领域从实验室走向产品化。不过，UI的跨平台多样性、动态内容加载和隐私敏感截图处理仍是落地挑战，ScreenAI的后续迭代值得持续观察。

> *谷歌用5B参数在垂直赛道打出差异化的同时开源数据集，意在把UI理解从“通用模型的副产物”变成有独立评测标准的子领域——这既是技术卡位，也是生态圈地。*

> 原文：[Google AI Blog](http://blog.research.google/2024/03/screenai-visual-language-model-for-ui.html)