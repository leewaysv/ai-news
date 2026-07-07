---
title: "[EN] 谷歌推出生成式AI模型SEEDS，低成本量化天气预报不确定性"
date: "2026-07-07T23:13:01+08:00"
slug: "en-aiseeds"
source: "Google AI Blog"
source_url: "http://blog.research.google/2024/03/generative-ai-to-quantify-uncertainty.html"
categories:
  - AI技术
  - 气象科学
  - 气候科技
tags:
  - 生成式AI
  - 天气预报
  - 不确定性量化
  - 扩散模型
  - 谷歌研究
  - 极端天气
summary: "谷歌发布基于扩散概率模型的SEEDS（可扩展集合包络扩散采样器），能以极低成本生成大规模天气预报集合，有效量化极端天气的不确定性。"
aigc: true
---
谷歌发布基于扩散概率模型的SEEDS（可扩展集合包络扩散采样器），能以极低成本生成大规模天气预报集合，有效量化极端天气的不确定性。

## 关键要点

- **SEEDS基于去噪扩散概率模型，仅需1-2个传统数值预报结果即可生成数百个高准确率集合成员。**
- **相比传统物理模型需超算数小时，SEEDS在Google Cloud TPU上3分钟可生成256个成员（2°分辨率），成本极低。**
- **该模型在集合分布尾部（如±2σ、±3σ事件）的预测准确性优于传统物理集合方法。**

SEEDS标志着生成式AI首次大规模应用于天气预报集合生成，有望显著降低极端天气（如飓风、洪水）概率预报的计算门槛，但对模型泛化能力和极端事件物理一致性仍需进一步验证。

> 原文：[Google AI Blog](http://blog.research.google/2024/03/generative-ai-to-quantify-uncertainty.html)