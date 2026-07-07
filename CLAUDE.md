# AI News 早报平台

每日精选 AI 新闻，自动生成中文早报，发布到多个平台。

## 项目定位

- 个人项目/副业
- 成本敏感，优先使用免费服务
- 全自动运行，无需人工干预

## 三层架构

```
Pipeline（Python） → 内容生产：采集 → 过滤 → 摘要 → QA → 适配 → 发布
    ↓ 生成 .md
Blog（Hugo）       → 网页渲染：从 .md 构建静态 HTML 站点
    ↓ git push
Infrastructure     → 自动运行：GitHub Actions 定时触发 + Cloudflare Pages 托管
```

## 项目结构

```
ai-news/
├── blog/                # Hugo 静态站点
│   ├── content/articles/   ← Pipeline 生成的 .md 文件
│   ├── layouts/            # Go HTML 模板
│   ├── assets/             # CSS (Tailwind v4) + JS
│   └── config/_default/    # Hugo 配置 (TOML)
├── pipeline/            # Python 新闻处理管道
│   ├── src/
│   │   ├── gather/         # 采集器 (RSS/API/Scrape)
│   │   ├── filter/         # 预过滤 + 去重
│   │   ├── summarize/      # LLM 摘要生成
│   │   ├── qa/             # 质量校验
│   │   ├── adapt/          # 平台适配器
│   │   ├── publish/        # 平台发布器
│   │   └── compliance/     # AIGC 合规标注
│   └── config.yaml         # 新闻源 + 管道参数
├── .github/workflows/   # CI/CD
│   ├── daily-digest.yml    # 每日 06:00 跑 Pipeline
│   └── deploy-blog.yml    # Hugo 构建 + Cloudflare 部署
└── lessons/             # 教学材料
```

## 技术栈

| 组件     | 技术                                   |
| -------- | -------------------------------------- |
| 博客框架 | Hugo 0.145（Go 模板）                  |
| 样式     | Tailwind CSS v4（PostCSS 集成）        |
| 管道     | Python 3.12                            |
| LLM      | DeepSeek API（OpenAI 兼容接口）        |
| 编排     | GitHub Actions（cron: 0 22 * * * UTC） |
| 托管     | Cloudflare Pages                       |
| 数据存储 | Git-based Markdown（无数据库）         |

## API Key 管理

| 用途         | 环境变量                             | 存储位置                                  |
| ------------ | ------------------------------------ | ----------------------------------------- |
| DeepSeek API | `DEEPSEEK_API_KEY`                 | GitHub Secrets +`pipeline/.env`（本地） |
| Cloudflare   | `CF_API_TOKEN` + `CF_ACCOUNT_ID` | GitHub Secrets                            |

## 重要约定

### 文件命名

- Pipeline 生成的 .md：`{date}-{slug}.md`（slug 仅英文+数字）
- 文章 frontmatter 必须包含：`title`, `date`, `slug`, `aigc`, `summary`

### 代码规范

- Python 使用类型注解（Pydantic models）
- 所有 LLM 调用走 `_llm_call()` 封装，不直接调用 API
- 日志用 `logging` 模块，格式 `[INFO/ERROR/WARN]`
- 适配器实现 `BaseAdapter` 接口，发布器独立封装

### 平台适配器模式

```
adapt/base.py (AdaptedContent 接口)
├── adapt/blog_adapter.py     → Hugo frontmatter + .md (Phase 1)
├── adapt/wechat_adapter.py   → 微信内联 HTML       (Phase 2 - 待实现)
└── adapt/douyin_adapter.py   → 视频脚本 + TTS      (Phase 3 - 待实现)
```

## 本地开发

```bash
# Hugo 博客预览
cd blog
npm ci
hugo server --buildDrafts
# → http://localhost:1313

# Pipeline 测试
cd pipeline
.venv/Scripts/python -m src.main --dry-run
# → 只采集+过滤，不调用 LLM 摘要

# Pipeline 全量运行
.venv/Scripts/python -m src.main
# → 需要 .env 中有 DEEPSEEK_API_KEY
```

## 关键文件速查

| 文件                                  | 说明                                                        |
| ------------------------------------- | ----------------------------------------------------------- |
| `pipeline/src/main.py`              | 管道编排入口，理解全局流程                                  |
| `pipeline/src/models.py`            | 数据模型定义（RawArticle / ProcessedArticle / DailyDigest） |
| `pipeline/config.yaml`              | 新闻源配置 + 管道参数                                       |
| `blog/layouts/_default/baseof.html` | 全站骨架模板                                                |
| `blog/layouts/_default/single.html` | 文章详情页模板                                              |
| `blog/config/_default/hugo.toml`    | 站点配置                                                    |
| `blog/config/_default/params.toml`  | 自定义参数                                                  |

## 已知问题

- 部分 RSS 源返回 0 条（google-ai, meta-ai, anthropic, mit-news, theverge-ai）
- 中文源爬虫未生效（量子位、机器之心的 CSS 选择器需更新）
- Pipeline 日期使用北京时间（UTC+8），已在 cron 和 date_str 中处理
- Embedding QA 对英文→中文跨语言摘要跳过校验
- Cloudflare Pages 的自动构建 token 已过期：当前仅通过 GitHub Actions + Wrangler CLI 部署
