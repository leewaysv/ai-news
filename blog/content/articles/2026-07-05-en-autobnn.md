---
title: "[EN] AutoBNN：谷歌开源概率时间序列预测工具，结合贝叶斯神经网络与可解释性"
date: "2026-07-05T01:52:03+08:00"
slug: "en-autobnn"
source: "Google AI Blog"
source_url: "http://blog.research.google/2024/03/autobnn-probabilistic-time-series.html"
categories:
  - AI工具
  - 时间序列
  - 概率模型
tags:
  - AutoBNN
  - 贝叶斯神经网络
  - 时间序列预测
  - 开源
  - Google
summary: "谷歌推出开源工具AutoBNN，基于组合贝叶斯神经网络，自动发现可解释的时间序列预测模型，提供高质量的不确定性估计，并在大规模数据集上高效扩展。"
aigc: true
---
谷歌推出开源工具AutoBNN，基于组合贝叶斯神经网络，自动发现可解释的时间序列预测模型，提供高质量的不确定性估计，并在大规模数据集上高效扩展。

## 关键要点

- **AutoBNN用贝叶斯神经网络（BNN）替代高斯过程（GP），保留组合核结构，提升可扩展性与硬件加速能力。**
- **相比传统GP方法，BNN训练复杂度从O(N³)降至近似线性，且更适配GPU/TPU。**
- **该工具支持用户通过Add、Multiplication等算子组合基核（如Linear、Periodic），并可与深度BNN融合，实现特征发现。**

AutoBNN将传统概率模型的解释性与深度学习的高效性结合，降低了时间序列预测的领域专家门槛，有望推动天气预报、经济趋势等实际应用。

> 原文：[Google AI Blog](http://blog.research.google/2024/03/autobnn-probabilistic-time-series.html)