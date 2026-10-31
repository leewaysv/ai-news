---
title: "[EN] 谷歌发布ScreenAI：5B参数视觉语言模型，刷新UI与信息图理解多项基准"
date: "2026-10-31T01:32:18+08:00"
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
  - 数据生成
  - 谷歌
summary: "谷歌研究院推出ScreenAI，一个基于PaLI架构并采用pix2struct灵活分块策略的视觉语言模型，专门用于理解用户界面（UI）和信息图（图表、示意图、表格）。该模型仅5B参数，却在WebSRC、MoTIF、ChartQA、DocVQA和InfographicVQA等任务上达到同级最佳或业界领先水平，并同步开源三个新数据集。"
aigc: true
---
谷歌研究院推出ScreenAI，一个基于PaLI架构并采用pix2struct灵活分块策略的视觉语言模型，专门用于理解用户界面（UI）和信息图（图表、示意图、表格）。该模型仅5B参数，却在WebSRC、MoTIF、ChartQA、DocVQA和InfographicVQA等任务上达到同级最佳或业界领先水平，并同步开源三个新数据集。

## 详细分析

ScreenAI的发布标志着视觉语言模型正从通用场景理解向高度结构化的专业领域纵深推进。UI和信息图是人类数字交互的核心载体，但其设计原则相似却呈现格式多变，长期构成建模难题。谷歌此次的巧思在于：利用UI与信息图共享的视觉语言（图标、布局）构建单一模型，并通过创新的“屏幕标注”任务——让模型识别UI元素的类型、位置和描述——将标注文本反哺给大语言模型，从而大规模自动生成问答、导航和摘要训练数据。这一数据飞轮策略显著降低了对人工标注的依赖，是模型仅以5B参数便斩获多项SOTA的关键。从行业影响看，该工作直接利好无障碍技术（屏幕阅读器智能化）、自动化测试（UI理解）、文档智能（图表问答）和移动端AI助手等场景。5B的参数量意味着模型具备端侧部署的潜力，这与当前AI向边缘迁移的趋势高度契合。同时，谷歌开源Screen Annotation、ScreenQA Short和Complex ScreenQA三个数据集，有望像RICO数据集那样成为UI理解领域的社区基准，进一步巩固其在多模态研究生态中的话语权。竞争格局上，ScreenAI与微软、Anthropic等多模态产品形成差异化——后者多聚焦通用图文理解，而谷歌选择在UI与信息图这一垂直赛道建立技术壁垒，背后是对企业级文档自动化与智能交互市场的前瞻卡位。值得注意的是，模型采用ViT冻结的两阶段训练策略，在微调阶段主要依赖人工标注数据，这暗示纯自监督数据在精细化UI理解上仍有天花板，未来如何平衡合成数据与高质量人工标注将是该领域的关键课题。

> *5B参数刷新多项SOTA，数据生成飞轮比模型本身更值得关注——谷歌正在用LLM反哺多模态训练，这一范式或成行业标配。*

> 原文：[Google AI Blog](http://blog.research.google/2024/03/screenai-visual-language-model-for-ui.html)