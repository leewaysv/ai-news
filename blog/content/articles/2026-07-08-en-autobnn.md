---
title: "[EN] AutoBNN：用组合贝叶斯神经网络实现概率时间序列预测"
date: "2026-07-07T23:13:05+08:00"
slug: "en-autobnn"
source: "Google AI Blog"
source_url: "http://blog.research.google/2024/03/autobnn-probabilistic-time-series.html"
categories:
  - 人工智能
  - 时间序列分析
tags:
  - AutoBNN
  - 贝叶斯神经网络
  - 概率预测
  - JAX
  - 高斯过程
summary: "谷歌研究团队发布开源工具AutoBNN，基于JAX，用贝叶斯神经网络替代高斯过程，在保留组合核结构可解释性的同时，实现大规模时间序列数据的高效概率预测与不确定性量化。"
aigc: true
---
谷歌研究团队发布开源工具AutoBNN，基于JAX，用贝叶斯神经网络替代高斯过程，在保留组合核结构可解释性的同时，实现大规模时间序列数据的高效概率预测与不确定性量化。

## 关键要点

- **AutoBNN通过组合基核（如线性、周期性）和运算符（加法、乘法）构建可解释的预测模型，自动发现时间序列结构。**
- **相比传统高斯过程（计算成本随数据量立方增长），BNN训练近似线性扩展，且更适合GPU/TPU加速。**
- **支持与深度BNN混合，允许用户指定高层结构（如Add(Linear, Periodic, Deep)），由深度网络自动学习高维协变量贡献。**

AutoBNN填补了传统概率模型可解释性与神经网络可扩展性之间的鸿沟，为非专家用户提供了开箱即用的高质量时间序列分析工具，可能推动气象、金融等领域预测的实用化。

> 原文：[Google AI Blog](http://blog.research.google/2024/03/autobnn-probabilistic-time-series.html)