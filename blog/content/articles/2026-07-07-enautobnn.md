---
title: "[EN]AutoBNN：用组合贝叶斯神经网络实现自动化概率时间序列预测"
date: "2026-07-06T23:16:58+08:00"
slug: "enautobnn"
source: "Google AI Blog"
source_url: "http://blog.research.google/2024/03/autobnn-probabilistic-time-series.html"
categories:
  - AI 研究
  - 时间序列分析
tags:
  - AutoBNN
  - 贝叶斯神经网络
  - 时间序列预测
  - 概率模型
  - 开源工具
summary: "Google 发布了开源工具 AutoBNN，将传统概率模型的可解释性与神经网络的可扩展性相结合，自动发现时间序列预测模型，并提供高质量的置信区间。"
aigc: true
---
Google 发布了开源工具 AutoBNN，将传统概率模型的可解释性与神经网络的可扩展性相结合，自动发现时间序列预测模型，并提供高质量的置信区间。

## 关键要点

- **AutoBNN 基于组合贝叶斯神经网络（BNN），替代了传统高斯过程（GP）的核结构，训练复杂度从 O(N³) 降至近似线性。**
- **该方法自动组合线性、周期性等基核函数，避免人工调参，并支持 GPU/TPU 加速和混合深度架构。**
- **通过引入权重上的概率分布，AutoBNN 能有效量化预测不确定性，同时保持模型的可解释性。**

AutoBNN 降低了时间序列建模的专业门槛，尤其适合非专家用户在大规模数据上快速获得可靠置信区间，推动了概率性预测的实用化。

> 原文：[Google AI Blog](http://blog.research.google/2024/03/autobnn-probabilistic-time-series.html)