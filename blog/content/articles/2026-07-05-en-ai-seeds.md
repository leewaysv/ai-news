---
title: "[EN] 生成式AI SEEDS：以极低成本量化天气预报不确定性"
date: "2026-07-05T23:11:10+08:00"
slug: "en-ai-seeds"
source: "Google AI Blog"
source_url: "http://blog.research.google/2024/03/generative-ai-to-quantify-uncertainty.html"
categories:
  - 人工智能
  - 气象科学
  - 气候变化
tags:
  - 生成式AI
  - 天气预报
  - 不确定性量化
  - 扩散模型
  - SEEDS
  - Google Research
summary: "谷歌研究团队推出基于扩散概率模型的生成式AI工具SEEDS，能以传统物理模型极小成本生成大规模天气预报集合，有效量化极端天气事件的不确定性，提升预测可靠性。"
aigc: true
---
谷歌研究团队推出基于扩散概率模型的生成式AI工具SEEDS，能以传统物理模型极小成本生成大规模天气预报集合，有效量化极端天气事件的不确定性，提升预测可靠性。

## 关键要点

- **SEEDS基于去噪扩散概率模型，仅需1-2个初始预报即可生成大规模集合预报，计算成本仅为传统方法的极小部分。**
- **该模型在秩直方图、均方根误差和连续等级概率评分等指标上媲美甚至超越物理集合预报，尤其对±2σ和±3σ的极端天气事件概率估计更准确。**
- **在Google Cloud TPUv3-32上，SEEDS每3分钟可生成256个集合成员（2°分辨率），且易于通过扩展加速器提高吞吐量。**

SEEDS突破了传统集合预报的计算瓶颈，使大规模概率预报在气象和气候科学中变得可行，尤其对飓风、热浪等罕见高影响事件的应急管理和能源交易等应用具有重大意义。

> 原文：[Google AI Blog](http://blog.research.google/2024/03/generative-ai-to-quantify-uncertainty.html)