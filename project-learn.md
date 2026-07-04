# AI-News

AI新闻早报，目前已经实现博客平台，后续推广到微信公众号、抖音短视频等平台

项目主要由三大模块组成：Pipeline、Blog、Infrastructure

**数据流：**

1、Pipeline：

* RSS/API/爬虫获取热点新闻
* 对新闻进行预过滤
* 启动LLM对咨询进行摘要处理
* 将摘要和原文做QA校验，判断是否符合原文语义

2、Blog

* 摘要文件按md格式存储
* 将md文件更新到Hugo系统
* 每个md文件单独作为一条内容，调整网页HTML和CSS，得到完整的一个新闻网页

3、Infrastructure

* 通过Github Actions实现CI/CD效果
* **Hugo Build**
* **Cloudflare Pages**

4、用户正常浏览网页

## Pipeline

> 负责搜集新闻、筛选、摘要

| 模块         | 做什么                         | 关键文件             |
| :----------- | :----------------------------- | :------------------- |
| `gather/`    | 从 RSS、API、网页爬取新闻      | `rss_collector.py`   |
| `filter/`    | 判断文章是否和 AI 相关         | `classifier.py`      |
| `summarize/` | 调用 DeepSeek API 生成中文摘要 | `summarizer.py`      |
| `qa/`        | 检查摘要质量                   | `embedding_check.py` |
| `adapt/`     | 转成 Hugo 认识的 .md 格式      | `blog_adapter.py`    |

**gather/ 三种新闻采集方式：**

| 采集方式           | 如何理解                                                     | 对应源                                 | 举例                                                         |
| :----------------- | ------------------------------------------------------------ | :------------------------------------- | :----------------------------------------------------------- |
| **RSS**            | 订阅站点推送内容                                             | OpenAI Blog、Google AI 等有 RSS 的站点 | https://www.theverge.com/ai-artificial-intelligence/rss      |
| **API**            | 调用网站提供的API获取内容                                    | HackerNews、GitHub Trending            | https://api.github.com/search/repositories?q=topic:ai+sort:stars&per_page=20 |
| **Scrape（爬虫）** | 若网站不支持RSS和API，只能通过爬取源码来获取内容，爬取操作必须符合网页要求 | 机器之心、量子位（无 RSS）             | https://www.jiqizhixin.com/                                  |

注意：API和Scrape方法需要 **async** 关键字修饰，是为了异步的效果；RSS 采集器用的 feedparser 没有 async 版本，所以只能实现成同步的

> RSS认知加深：很多网站都支持RSS订阅功能，实际上就是网站会自主维护一个XML文件，文件内容和网站内容同步更新，通过程序调用RSS的url即可获取到这个XML文件从而获取到网站的最新内容。注意，XML的标签和HTML标签并不相同，可以将XML文件放到RSS阅读器上进行渲染即可阅读

**filter/ 筛选机制：**

从获取的几百条新闻中挑出 AI 相关的内容，通过一层去重+两层过滤机制实现：

* dedup（免费）

  同一篇新闻可能被多个源报道（比如 OpenAI 自己的 Blog + TechCrunch 的报道），用 URL 和 hash 去重，避免重复内容

- 关键词过滤（免费）

  用 `AI_KEYWORDS` 列表检查标题和正文。命中关键词越多得分越高。得分低于阈值直接扔。这一步会砍掉 60-70% 的无关内容（体育、娱乐、纯财经等）。

- LLM 精判（花钱）

  通过第一层的文章（每天约 30-40 篇），每 10 篇一批递给 LLM，判断哪些"与 AI 行业高度相关"。这一步会进一步筛选到 10-15 篇。

**summarize/ 摘要：**

通过提示词模板要求 LLM 输出严格的 JSON 格式的摘要内容：

1. 单篇摘要：对每篇文章调用 LLM，要求输出中文标题、1-2 句摘要、关键要点、分类标签
2. 早报标题：全部摘要完成后，再把文章列表汇总给 LLM，让它为今天的早报想一个总标题

**qa/ 质量评估：**

验证 LLM 生成的摘要"没乱说"。两种机制：

- **Embedding 相似度**：用 `sentence-transformers` 把原文和摘要都转成向量，算余弦相似度。低于阈值说明摘要可能偏离原文，丢弃。
- **兜底策略**：如果当天通过 QA 的文章不足 3 篇，跳过发布，不发"没什么好说的"那种早报。

注意：目前新闻源主要是英文，但摘要是中文。英文原文和中文摘要的 embedding 相似度天然偏低，所以 QA 模块对英文源跳过了校验，后续可以继续优化调整。

 **adapt/ 适配：**

把 Json 格式的新闻内容转为 Hugo 能识别的 Markdown 格式。具体工作：

- 生成 YAML frontmatter（标题、日期、分类、标签等）
- 把摘要和 key_points 排版成 Markdown 正文
- 生成文件名（如 `2026-07-04-en-openai-gpt-56-sol.md`）

适配器使用**策略模式（base_adater)**——以后如果添加微信或抖音的适配器，只需要新增一个类，不侵入已有代码。

**publish/ 发布：**

把适配器生成的符合markdown格式的字符串写入文件中，生成markdown文件。

## Blog

> 负责将稿件排版成网页

注意：Hugo是一个静态站点生成器，而不是类似Helo和Hexo的“博客后台管理界面”通过提供文章编辑界面来编辑文章再发布

Hugo工作方式：

1、在项目 content/ 目录存储文章md文件

2、在项目 layout/ 目录预备HTML的模板

3、执行hugo构建命令：hugo --gc --minify

4、Hugo系统将md文件中的内容和HTML模板合并成网页

## Infrastructure

> 负责定时发布

| **GitHub Actions**   | 每天早上 06:00 自动运行 Pipeline |
| -------------------- | -------------------------------- |
| **Git**              | 存储所有代码和文章 .md 文件      |
| **Cloudflare Pages** | 把 Hugo 构建的 HTML 放到网上     |

> ① 06:00 daily-digest 跑完 → ② 它 commit .md 文件并 push → ③ push 事件触发 deploy-blog → ④ Hugo 构建 → ⑤ Cloudflare 部署上线。

Cloudflare Pages 是一个**静态站点托管服务**。它从你的 GitHub 仓库拉代码，自动构建 Hugo，然后把生成的 HTML 部署到全球 CDN 节点上。

Github Actions详细资料请看 C://user/13682/desktop/github_actions.md