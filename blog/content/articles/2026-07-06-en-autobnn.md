---
title: "[EN] AutoBNN：用组合贝叶斯神经网络实现可解释的概率时间序列预测"
date: "2026-07-06T03:28:57+08:00"
slug: "en-autobnn"
source: "Google AI Blog"
source_url: "http://blog.research.google/2024/03/autobnn-probabilistic-time-series.html"
categories:
  - 人工智能
  - 机器学习
  - 时间序列分析
tags:
  - AutoBNN
  - 贝叶斯神经网络
  - 时间序列预测
  - 可解释AI
  - 开源工具
summary: "Google Research 发布了开源工具 AutoBNN，它结合了传统概率模型的可解释性与神经网络的扩展性，能自动发现时间序列数据的组合核结构并提供高质量的不确定性估计。"
aigc: true
---
Google Research 发布了开源工具 AutoBNN，它结合了传统概率模型的可解释性与神经网络的扩展性，能自动发现时间序列数据的组合核结构并提供高质量的不确定性估计。

## 关键要点

- **AutoBNN 基于 JAX 构建，通过贝叶斯神经网络（BNN）替代高斯过程（GP），使训练复杂度从数据的立方级降至近似线性级。**
- **该工具保留组合核结构（如线性、周期性、马特恩核等），用户无需深入掌握概率模型即可构建合理的先验假设。**
- **AutoBNN 支持 GPU/TPU 加速，并能与传统深度 BNN 混合使用，实现高层结构指定与自动特征发现。**

该工具降低贝叶斯时间序列建模的应用门槛，有望在金融、气候、供应链等需要可解释预测与置信度评估的领域产生广泛影响。

> 原文：[Google AI Blog](http://blog.research.google/2024/03/autobnn-probabilistic-time-series.html)