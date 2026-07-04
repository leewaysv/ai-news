# 技术栈三层架构理解

建立了整个系统的三层架构理解：Pipeline（Python 数据流）、Blog（Hugo 静态站点）、Infrastructure（GitHub Actions + Cloudflare）。理解了管道将新闻加工为 .md 文件 → Hugo 构建为 HTML → 部署到 CDN 的完整数据流。

**Evidence:** 用户主动询问"整个项目的技术栈"，要求系统性地学习。确认了三层分工和数据流动方向。

**Implications:** 后续课程可以深入到每层的具体运作——Hugo 模板语法、Pipeline 模块设计、CI/CD 配置原理。
