---
title: "[EN]谷歌发布生成式AI模型SEEDS，量化天气预报不确定性"
date: "2026-07-10T23:09:15+08:00"
slug: "enaiseeds"
source: "Google AI Blog"
source_url: "http://blog.research.google/2024/03/generative-ai-to-quantify-uncertainty.html"
categories:
  - 人工智能
  - 气象科学
tags:
  - Google Research
  - SEEDS
  - 扩散模型
  - 天气预报集合
  - 概率预报
  - AI气象
summary: "谷歌推出新型生成式AI模型Scalable Ensemble Envelope Diffusion Sampler (SEEDS)，能够以传统物理模型极小成本高效生成大规模天气预报集合，量化预测不确定性，为极端天气事件预测提供更精准的概率支持。"
aigc: true
---
谷歌推出新型生成式AI模型Scalable Ensemble Envelope Diffusion Sampler (SEEDS)，能够以传统物理模型极小成本高效生成大规模天气预报集合，量化预测不确定性，为极端天气事件预测提供更精准的概率支持。

## 关键要点

- **SEEDS基于去噪扩散概率模型，仅需一两个传统预报即可生成大规模集合，计算成本远低于物理模拟。**
- **该模型在秩直方图、RMSE、CRPS等技能指标上匹配甚至超越传统物理集合，尤其在±2σ和±3σ极端事件尾部概率分配上更准确。**
- **SEEDS在Google Cloud TPUv3-32上3分钟可生成256个集合成员（2°分辨率），易于通过增加加速器扩展吞吐量。**

SEEDS代表着扩散模型在气象预报领域的重要应用突破，将显著降低概率预报的计算门槛，提升对罕见但高影响天气事件的预警能力，对应急管理与能源交易等领域具有实际价值。

> 原文：[Google AI Blog](http://blog.research.google/2024/03/generative-ai-to-quantify-uncertainty.html)