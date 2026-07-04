---
title: "[EN] AutoBNN：用组合贝叶斯神经网络实现概率时间序列预测"
date: "2026-07-04T06:39:19+08:00"
slug: "en-autobnn"
source: "Google AI Blog"
source_url: "http://blog.research.google/2024/03/autobnn-probabilistic-time-series.html"
categories:
  - 机器学习
  - 时间序列
  - 开源工具
tags:
  - AutoBNN
  - 贝叶斯神经网络
  - 概率预测
  - JAX
  - 谷歌开源
summary: "谷歌开源了AutoBNN，它结合了传统概率模型的可解释性与神经网络的可扩展性，自动化地发现可解释的时间序列预测模型，并提供高质量的不确定性估计。"
aigc: true
---
谷歌开源了AutoBNN，它结合了传统概率模型的可解释性与神经网络的可扩展性，自动化地发现可解释的时间序列预测模型，并提供高质量的不确定性估计。

## 关键要点

- **AutoBNN基于贝叶斯神经网络与组合核结构，替代了传统高斯过程的计算瓶颈，训练复杂度从数据量的立方级降为近似线性。**
- **它能自动组合线性、周期、趋势等基核，输出可解释的结构化预测结果，并支持GPU/TPU加速，适合大规模数据集。**
- **该框架还支持与传统深度BNN混合，构建用户自定义高层结构与自动特征发现的混合架构。**

AutoBNN的推出降低了贝叶斯时间序列建模的门槛，有望在金融、气象、物联网等需要可靠置信区间的场景中替代传统的高斯过程方法。

> 原文：[Google AI Blog](http://blog.research.google/2024/03/autobnn-probabilistic-time-series.html)