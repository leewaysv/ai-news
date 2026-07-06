---
title: "[EN] 生成式AI量化天气预报不确定性：Google发布SEEDS模型"
date: "2026-07-06T23:16:55+08:00"
slug: "en-aigoogleseeds"
source: "Google AI Blog"
source_url: "http://blog.research.google/2024/03/generative-ai-to-quantify-uncertainty.html"
categories:
  - 人工智能
  - 气象科学
tags:
  - 生成式AI
  - 天气预报
  - 扩散模型
  - SEEDS
  - Google Research
  - 概率预报
summary: "Google Research推出基于扩散概率模型的生成式AI技术SEEDS，能以极低成本生成大规模天气预报集合，准确量化极端天气概率，突破传统物理模型的计算瓶颈。"
aigc: true
---
Google Research推出基于扩散概率模型的生成式AI技术SEEDS，能以极低成本生成大规模天气预报集合，准确量化极端天气概率，突破传统物理模型的计算瓶颈。

## 关键要点

- **SEEDS基于去噪扩散概率模型，仅需1-2个数值天气预报结果即可生成大规模集合预报，计算成本仅为传统方法的极小部分。**
- **该方法在秩直方图、均方根误差和连续排序概率评分等指标上匹配或超越传统物理集合，并对±2σ和±3σ极端事件赋予更准确概率。**
- **在Google Cloud TPUv3-32上，SEEDS每3分钟可生成256个集合成员（2°分辨率），且易于扩展，为气象灾害预警和能源交易等场景提供新工具。**

SEEDS将生成式AI引入气象集合预报，有望大幅降低极端天气概率评估的门槛，推动气象预报从确定性向高效概率化转型，对气候适应和应急管理意义深远。

> 原文：[Google AI Blog](http://blog.research.google/2024/03/generative-ai-to-quantify-uncertainty.html)