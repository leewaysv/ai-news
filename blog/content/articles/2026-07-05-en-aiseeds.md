---
title: "[EN] 生成式AI量化天气预报不确定性：谷歌推出SEEDS模型"
date: "2026-07-05T01:51:59+08:00"
slug: "en-aiseeds"
source: "Google AI Blog"
source_url: "http://blog.research.google/2024/03/generative-ai-to-quantify-uncertainty.html"
categories:
  - 人工智能
  - 气象预报
  - 气候科技
tags:
  - Generative AI
  - Weather Forecasting
  - Diffusion Models
  - Probability Forecast
  - Google Research
  - SEEDS
summary: "谷歌发布基于扩散概率模型的生成式AI框架SEEDS，能以极低计算成本大规模生成天气预报集合，弥补传统物理模型在高分辨率、大集合生成上的不足，提升对极端天气事件的概率判断。"
aigc: true
---
谷歌发布基于扩散概率模型的生成式AI框架SEEDS，能以极低计算成本大规模生成天气预报集合，弥补传统物理模型在高分辨率、大集合生成上的不足，提升对极端天气事件的概率判断。

## 关键要点

- **SEEDS无需大量初始扰动，仅需1–2次业务预报即可生成256个集合成员，耗时仅3分钟（TPUv3-32），成本远低于传统超级计算机模拟。**
- **该模型在秩直方图、均方根误差和连续排名概率评分等指标上匹配或超越物理集合，尤其精度在±2σ、±3σ极端事件概率分布上表现更优。**
- **SEEDS是概率扩散模型在天气与气候集合预报领域的早期应用，为解决计算瓶颈与提升灾害预警提供新途径。**

SEEDS以AI之力破解传统集合预报的“计算-精度”两难，有望推动气象概率预报走向规模化与常态化，尤其在防洪、飓风、能源交易等对极端概率敏感的领域具有变革意义。

> 原文：[Google AI Blog](http://blog.research.google/2024/03/generative-ai-to-quantify-uncertainty.html)