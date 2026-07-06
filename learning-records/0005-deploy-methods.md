# 博客部署到公网的常见方法

理解了静态托管 vs 服务器托管的本质区别、四大静态托管平台（Cloudflare Pages / Vercel / Netlify / GitHub Pages）的对比、两种部署方式（平台自动构建 vs 外部 CI 推送）、以及部署 Hugo 站点的通用步骤。结合本项目的 Cloudflare Pages + GitHub Actions 方案理解了为什么这样选。

**Evidence:** 用户经过实际部署过程后主动要求系统学习部署方法，说明已验证了部署经验并想从理论上理解全貌。

**Implications:** 后续可以深入到 DNS 和域名解析、或 HTTPS/SSL 证书的原理。已补充服务器托管的完整知识：VPS 类型、国内外服务商、Nginx 配置、备案要求、以及"静态托管 + 轻量后端"的混合方案。
