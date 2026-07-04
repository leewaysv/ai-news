# Infrastructure 细节：CI/CD、Git、部署

理解了 Infrastructure 层的三个组件：GitHub Actions（定时触发 Pipeline）、Git（版本控制 + 触发部署）、Cloudflare Pages（Hugo 构建 + CDN 托管）。掌握了两条工作流（daily-digest + deploy-blog）的串联关系、GitHub Secrets 的密钥管理、cron 定时表达式、以及本地开发 vs 生产部署的差异。

**Evidence:** 用户主动要求学习 Infrastructure 的"具体细节"，说明对自动部署流程的运作机制感兴趣。

**Implications:** 后续可以按需深入到 Go Template 语法、Tailwind CSS 改样式、或 Pipeline 代码走读。
