---
title: "[EN] 生成式AI量化天气预报不确定性：Google推出SEEDS模型"
date: "2026-07-04T06:39:14+08:00"
slug: "en-aigoogleseeds"
source: "Google AI Blog"
source_url: "http://blog.research.google/2024/03/generative-ai-to-quantify-uncertainty.html"
categories:
  - 人工智能
  - 气象科学
tags:
  - 生成式AI
  - 天气预报
  - 不确定性量化
  - 扩散模型
  - Google Research
summary: "Google Research发布基于扩散概率模型的生成式AI技术SEEDS，能以极低计算成本大规模生成天气预报集合，量化传统方法难以捕捉的极端天气不确定性，性能媲美甚至超越物理模型。"
aigc: true
---
Google Research发布基于扩散概率模型的生成式AI技术SEEDS，能以极低计算成本大规模生成天气预报集合，量化传统方法难以捕捉的极端天气不确定性，性能媲美甚至超越物理模型。

## 关键要点

- **SEEDS可基于仅1-2个数值预报结果，生成数百个集合成员，3分钟内产出256个成员（2°分辨率），成本远低于传统超级计算机模拟。**
- **生成的集合在秩直方图、均方根误差和连续排名概率评分上匹配或超越物理模型，尤其对±2σ和±3σ极端事件概率估计更准确。**
- **该技术是概率扩散模型在天气预报领域的首批应用之一，有望提升飓风、热浪、洪水等灾害性天气的预警能力。**

SEEDS标志着AI从替代单一天气预报走向概率集合预测，在保持精度的同时大幅降低计算门槛，将推动气象部门向更精细化、低成本的风险管理转型。

> 原文：[Google AI Blog](http://blog.research.google/2024/03/generative-ai-to-quantify-uncertainty.html)