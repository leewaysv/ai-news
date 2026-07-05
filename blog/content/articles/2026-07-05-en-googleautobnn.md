---
title: "[EN] Google开源AutoBNN：组合贝叶斯神经网络实现可解释时序预测"
date: "2026-07-05T23:11:14+08:00"
slug: "en-googleautobnn"
source: "Google AI Blog"
source_url: "http://blog.research.google/2024/03/autobnn-probabilistic-time-series.html"
categories:
  - 机器学习
  - 时间序列预测
  - 开源工具
tags:
  - AutoBNN
  - 贝叶斯神经网络
  - 时序预测
  - 高斯过程
  - JAX
  - 不确定性估计
  - 可解释AI
summary: "谷歌发布开源工具AutoBNN，将高斯过程的组合核结构与贝叶斯神经网络的灵活扩展性结合，自动发现可解释的时序预测模型并输出高质量不确定性估计，适用于大规模数据集。"
aigc: true
---
谷歌发布开源工具AutoBNN，将高斯过程的组合核结构与贝叶斯神经网络的灵活扩展性结合，自动发现可解释的时序预测模型并输出高质量不确定性估计，适用于大规模数据集。

## 关键要点

- **AutoBNN基于组合核结构（如Linear、Periodic等基核的组合），保持传统概率方法可解释性的同时，用贝叶斯神经网络替代高斯过程以获得更好的计算效率和硬件加速。**
- **训练复杂度从高斯过程的立方级降至近线性，且易于在GPU/TPU上部署，还能与深度学习模块混合使用处理高维特征。**
- **通过有限宽度神经网络逼近高斯过程核函数（如Matern、Periodic），在保持预测准确性的同时大幅降低计算成本。**

AutoBNN降低了时序预测门槛，尤其适合需要可解释性和不确定性量化的场景（如金融、气象），同时为大规模工业应用提供了高效方案。

> 原文：[Google AI Blog](http://blog.research.google/2024/03/autobnn-probabilistic-time-series.html)