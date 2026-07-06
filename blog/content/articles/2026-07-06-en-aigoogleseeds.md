---
title: "[EN] 生成式AI量化天气预报不确定性：Google发布SEEDS模型"
date: "2026-07-06T03:28:54+08:00"
slug: "en-aigoogleseeds"
source: "Google AI Blog"
source_url: "http://blog.research.google/2024/03/generative-ai-to-quantify-uncertainty.html"
categories:
  - AI技术
  - 气象科学
tags:
  - 生成式AI
  - 天气预报
  - SEEDS
  - 集合预报
  - 不确定性量化
  - Google Research
summary: "谷歌研究团队推出基于扩散模型的生成式AI天气预报集合采样技术SEEDS，能以极低成本高效生成大规模天气预测集合，量化极端天气事件概率，弥补传统方法在计算开销和稀有事件预测上的不足。"
aigc: true
---
谷歌研究团队推出基于扩散模型的生成式AI天气预报集合采样技术SEEDS，能以极低成本高效生成大规模天气预测集合，量化极端天气事件概率，弥补传统方法在计算开销和稀有事件预测上的不足。

## 关键要点

- **SEEDS是一种可扩展的集合包络扩散采样器，利用生成式AI在几分钟内生成256个成员（2°分辨率），成本仅为传统物理模型的极小部分。**
- **该模型基于去噪扩散概率模型，能从少数几个操作预报出发，生成在秩直方图、均方根误差等指标上匹配或超越物理集合的高质量预报。**
- **SEEDS特别擅长准确分配±2σ和±3σ极端天气事件的概率，对应急管理和能源交易等场景具有重要价值。**
- **传统概率预报因计算昂贵通常仅用10-50个集合成员，而SEEDS可轻松扩展到更高通量，填补了稀有事件概率评估的空白。**

SEEDS标志着生成式AI从图像生成向气象科学的实质性跨界，有望大幅降低高精度集合预报的门槛，提升对极端天气的预判能力。

> 原文：[Google AI Blog](http://blog.research.google/2024/03/generative-ai-to-quantify-uncertainty.html)