---
title: "[EN] AutoBNN：用组合贝叶斯神经网络实现可解释的概率时间序列预测"
date: "2026-07-10T23:09:18+08:00"
slug: "en-autobnn"
source: "Google AI Blog"
source_url: "http://blog.research.google/2024/03/autobnn-probabilistic-time-series.html"
categories:
  - 人工智能
  - 时间序列预测
tags:
  - AutoBNN
  - 贝叶斯神经网络
  - 时间序列
  - 谷歌
  - 开源
summary: "谷歌开源AutoBNN，它结合了传统概率方法的可解释性与神经网络的可扩展性，能自动发现时间序列预测模型，并提供高质量的不确定性估计。"
aigc: true
---
谷歌开源AutoBNN，它结合了传统概率方法的可解释性与神经网络的可扩展性，能自动发现时间序列预测模型，并提供高质量的不确定性估计。

## 关键要点

- **AutoBNN基于JAX构建，用贝叶斯神经网络替代高斯过程，同时保留组合核结构，在大型数据集上训练更快且更适合GPU/TPU加速。**
- **该工具可自动组合线性、周期、趋势等基本核函数，无需大量人工调参，输出易于理解的结构化模型。**
- **AutoBNN能与深度贝叶斯神经网络结合，构建“混合”架构，适用于高维协变量场景。**

AutoBNN降低了时间序列建模的门槛，尤其适合非专家用户，同时在计算效率和可解释性之间取得了良好平衡，有望推动贝叶斯时间序列方法在工业界的广泛采用。

> 原文：[Google AI Blog](http://blog.research.google/2024/03/autobnn-probabilistic-time-series.html)