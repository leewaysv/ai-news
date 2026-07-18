# AI News 早报平台

每日精选 AI 新闻 → 自动生成中文早报 → 多平台发布。

🌐 [ai-news-2li.pages.dev](https://ai-news-2li.pages.dev)

## 架构

```
采集 (RSS/API/爬虫) → 过滤 (关键词+LLM) → 摘要 (DeepSeek) → QA → 适配 → 发布
```

| 平台 | 输出 | 发布方式 | 状态 |
|------|------|---------|------|
| 📄 Blog | Markdown 文件 | Hugo → Cloudflare Pages | ✅ 每日自动发布 |
| 💬 微信 | 富文本 HTML | Playwright 浏览器自动化 | ✅ 个人订阅号适用 |
| 🎬 抖音 | 口播脚本 + .srt 字幕 | edge-tts → Pexels → FFmpeg | ✅ 本地渲染 |
| 📢 飞书 | 富文本消息 | Webhook 推送到群聊 | ✅ 已启用 |

## 技术栈

| 组件 | 技术 |
|------|------|
| 博客框架 | Hugo 0.145（Go 模板） |
| 样式 | Tailwind CSS v4 |
| 管道 | Python 3.12 / Pydantic / httpx |
| LLM | DeepSeek API（OpenAI 兼容） |
| 编排 | GitHub Actions（UTC 22:00 = 北京时间 06:00） |
| 托管 | Cloudflare Pages |
| 数据 | Git-based Markdown（无数据库） |
| 测试 | pytest / pytest-asyncio（106 项） |

## 快速开始

```bash
# 1. 安装依赖
cd pipeline
python -m venv .venv && source .venv/bin/activate
pip install -e .

# 2. 配置 API Key
echo "DEEPSEEK_API_KEY=sk-xxx" > .env

# 3. 测试采集
python -m src.main --dry-run

# 4. 全量运行
python -m src.main
```

## 项目结构

```
ai-news/
├── pipeline/               # Python 新闻处理管道
│   ├── src/
│   │   ├── gather/         # 采集器 (RSS/API/Scrape)
│   │   ├── filter/         # 关键词过滤 + LLM 精判
│   │   ├── summarize/      # DeepSeek 摘要 + 详细分析
│   │   ├── qa/             # Embedding 质量校验
│   │   ├── adapt/          # 多平台适配器
│   │   │   ├── blog_adapter.py     # Hugo Markdown
│   │   │   ├── wechat_adapter.py   # 微信 HTML
│   │   │   └── douyin_adapter.py   # 脚本 + 字幕
│   │   └── publish/        # 多平台发布器
│   │       ├── blog_publisher.py     # 文件写入
│   │       ├── wechat_publisher.py   # API 发布
│   │       ├── wechat_playwright.py  # 浏览器自动化
│   │       ├── douyin_video.py       # 视频渲染
│   │       └── feishu_publisher.py   # Webhook 推送
│   ├── tests/              # 106 项单元测试
│   └── config.yaml         # 新闻源 + 平台配置
├── blog/                   # Hugo 静态站点
│   ├── content/articles/   # Pipeline 输出的 .md
│   ├── layouts/            # Go HTML 模板
│   └── assets/             # Tailwind CSS
└── .github/workflows/      # CI/CD
    ├── daily-digest.yml    # 每日 06:00 运行
    └── deploy-blog.yml     # Hugo 构建 + 部署
```

## 配置

编辑 `pipeline/config.yaml`：

```yaml
platforms:
  blog:    { enabled: true }
  wechat:  { enabled: false, method: playwright }  # 需 WECHAT_APP_ID/SECRET
  douyin:  { enabled: false }                       # 需 PEXELS_API_KEY + FFmpeg
  feishu:  { enabled: true }                        # 需 FEISHU_WEBHOOK_URL
```

## 测试

```bash
cd pipeline
.venv/Scripts/python -m pytest tests/ -v
# 106 passed
```

## 开发理念

- **成本敏感** — 优先使用免费服务，API Key 零成本或低成本
- **适配器模式** — 每个平台独立 Adapter + Publisher，新增平台只需注册
- **TDD** — 核心逻辑通过测试驱动开发，三轮红绿循环
- **降级优先** — API 不可用时自动降级到浏览器自动化

## 已知问题

- 部分 RSS 源返回 0 条（google-ai, meta-ai, anthropic, mit-news）
- 中文源爬虫 CSS 选择器需站点改版后更新
- Embedding QA 对英→中跨语言摘要跳过校验
- 抖音视频渲染需本地 FFmpeg，GitHub Actions 不支持 GPU 加速

## 许可

MIT
