---
title: "[EN] AutoBNN：谷歌开源可解释概率时间序列预测工具"
date: "2026-07-07T09:50:04+08:00"
slug: "en-autobnn"
source: "Google AI Blog"
source_url: "http://blog.research.google/2024/03/autobnn-probabilistic-time-series.html"
categories:
  - 机器学习
  - 时间序列分析
tags:
  - AutoBNN
  - 贝叶斯神经网络
  - 概率预测
  - 谷歌开源
  - JAX
  - 可解释AI
summary: "谷歌发布开源工具AutoBNN，结合贝叶斯神经网络与组合核结构，自动构建可解释的时间序列预测模型，提供高质量不确定性估计，并支持大规模数据集的高效训练。"
aigc: true
---
谷歌发布开源工具AutoBNN，结合贝叶斯神经网络与组合核结构，自动构建可解释的时间序列预测模型，提供高质量不确定性估计，并支持大规模数据集的高效训练。

## 关键要点

- **AutoBNN基于组合贝叶斯神经网络（BNN），替代传统高斯过程（GP）进行时间序列建模，兼具可解释性与可扩展性。**
- **相比GP，BNN训练复杂度线性于数据量，更适合GPU/TPU加速，且可与深度BNN结合实现特征发现。**
- **工具开源基于JAX，支持线性、周期等基础核通过加法、乘法等操作组合，用户无需精通GP即可构建合理先验。**

AutoBNN降低了概率时间序列建模的专家门槛，同时保持解释性，为金融、气象等需要可靠置信区间的场景提供实用工具。

> 原文：[Google AI Blog](http://blog.research.google/2024/03/autobnn-probabilistic-time-series.html)