# Hugo 工作过程：md + 模板 → 网页

理解了 Hugo 的核心公式：内容（.md）+ 模板（HTML）= 网站。掌握了 frontmatter（元数据）和正文（Markdown）的分离、baseof.html 骨架 + single.html 填充的插槽机制、List vs Single 两种页面类型、以及模板查找规则。认识到 Pipeline 生成 .md 后必须触发构建才能上线。

**Evidence:** 用户主动要求学习 Hugo 工作过程，特别指定了"如何将 md 文件和 layout 模板合并成完整的网页"。用户打开了 params.toml 查看配置文件。

**Implications:** 下一课可以深入 Go Template 语法（. 上下文、range、with、函数管道），或者按用户意愿探索其他方向。
