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

| 模块           | 做什么                         | 关键文件               |
| :------------- | :----------------------------- | :--------------------- |
| `gather/`    | 从 RSS、API、网页爬取新闻      | `rss_collector.py`   |
| `filter/`    | 判断文章是否和 AI 相关         | `classifier.py`      |
| `summarize/` | 调用 DeepSeek API 生成中文摘要 | `summarizer.py`      |
| `qa/`        | 检查摘要质量                   | `embedding_check.py` |
| `adapt/`     | 转成 Hugo 认识的 .md 格式      | `blog_adapter.py`    |

**gather/ 三种新闻采集方式：**

| 采集方式                 | 如何理解                                                                   | 对应源                                 | 举例                                                                         |
| :----------------------- | -------------------------------------------------------------------------- | :------------------------------------- | :--------------------------------------------------------------------------- |
| **RSS**            | 订阅站点推送内容                                                           | OpenAI Blog、Google AI 等有 RSS 的站点 | https://www.theverge.com/ai-artificial-intelligence/rss                      |
| **API**            | 调用网站提供的API获取内容                                                  | HackerNews、GitHub Trending            | https://api.github.com/search/repositories?q=topic:ai+sort:stars&per_page=20 |
| **Scrape（爬虫）** | 若网站不支持RSS和API，只能通过爬取源码来获取内容，爬取操作必须符合网页要求 | 机器之心、量子位（无 RSS）             | https://www.jiqizhixin.com/                                                  |

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
| -------------------------- | -------------------------------- |
| **Git**              | 存储所有代码和文章 .md 文件      |
| **Cloudflare Pages** | 把 Hugo 构建的 HTML 放到网上     |

> ① 06:00 daily-digest 跑完 或手动触发Blog Deploy → ② 它 commit .md 文件并 push → ③ push 事件触发 deploy-blog → ④ Hugo 构建 → ⑤ Cloudflare 部署上线。

Cloudflare Pages 是一个**静态站点托管服务**。它从你的 GitHub 仓库拉代码，自动构建 Hugo，然后把生成的 HTML 部署到全球 CDN 节点上。

注意：由GithubActions触发的git commit生成的md新闻文件，存储在云虚拟机上，不会同步到本地环境

Github Actions详细资料请看 C://user/13682/desktop/github_actions.md

## 扩展：如何将博客部署到公网

将博客部署到公网有两种思路：

| 方式                 | 怎么做                                                                                                   | 典型服务                                        | 类比                                   |
| :------------------- | :------------------------------------------------------------------------------------------------------- | :---------------------------------------------- | -------------------------------------- |
| **静态托管**   | 将用户上传的 / 自动生成的 HTML 文件上传到 CDN 服务器，服务器不需要运行任何程序，只需要将HTML文件进行分发 | Cloudflare Pages、Vercel、Netlify、GitHub Pages | 印刷厂打印报纸后让快递员配送到每家每户 |
| **服务器托管** | 租一台云服务器，自己装 Web 服务软件，需要在服务器运行程序、连接数据库等                                  | 阿里云、腾讯云、AWS EC2、VPS                    | 每家每户自己用打印机打印每天的报纸     |

> 什么是静态网页：页面文件提前做好，直接发给用户，无后端运算
>
> 什么是动态网页：用户访问域名时，服务器运行后端代码，实时查询数据库、拼接 HTML，再把拼接好的页面发给浏览器。

> 什么是CDN：Content Delivery Network，内容分发网络。Cloudflare提供 CDN 加速，让全球读者都能快速访问

### 静态托管

**四大静态托管平台对比**

|                      | Cloudflare Pages        | Vercel                | Netlify                | GitHub Pages         |
| :------------------- | :---------------------- | :-------------------- | :--------------------- | :------------------- |
| **免费额度**   | 无限带宽                | 100GB/月              | 100GB/月               | 1GB 存储             |
| **构建次数**   | 500次/月                | 6000分钟/月           | 300分钟/月             | 10次/小时            |
| **Hugo 支持**  | ✅ 原生                 | ✅ 需配置             | ✅ 需配置              | ✅ 原生              |
| **自定义域名** | ✅ 免费                 | ✅ 免费               | ✅ 免费                | ✅（需自己管理 DNS） |
| **Git 集成**   | ✅                      | ✅                    | ✅                     | ✅（仅 GitHub）      |
| **部署方式**   | Git 推送 / Wrangler CLI | Git 推送 / Vercel CLI | Git 推送 / Netlify CLI | Git 推送             |

> 四种平台本质上做的是同一件事：你 git push → 它们自动拉代码、构建、部署。区别只有免费额度、界面交互和附加功能。

> Cloudflare Pages 和 GitHub Pages不是上下游关系，Cloudflare Pages和 Github Actions才是

**静态托管的两种部署方式**

pull：授权静态托管平台访问你的Github仓库，平台实现 检测更新-拉取代码-运行pipeline-执行构建命令-将命令输出文件部署上线 （本项目第一次尝试的就是这个方法，但是配置信息没完成导致失败）

push：在GithubActions中运行pipeline再完成构建命令，再将产物推送给静态托管平台进行部署上线（本项目采取的方法）

**我的域名**

静态托管的域名一般是自动分配，本项目公网域名为https://ai-news-2li.pages.dev/，也可以在托管平台上绑定自定义域名：

1. 在域名注册商（如 Namesilo、GoDaddy、阿里云）买一个域名（如 `ainews.com`）
2. 在托管平台添加域名，获得 DNS 记录（通常是 CNAME 或 A 记录）
3. 去域名注册商的管理面板添加这些 DNS 记录
4. 等待 DNS 生效（几分钟到 48 小时）
5. 自动获得免费的 HTTPS 证书

域名也可以托管在 Cloudflare，绑定过程更加简单：Cloudflare 能自动检测到托管的域名实现自动绑定。所以常见组合是"在 Namesilo 买域名，DNS 托管到 Cloudflare（免费），然后绑定到 Cloudflare Pages"

### 服务器托管

**三种服务器类型：**

| 类型                            | 白话解释                                                               | 典型价格    |
| :------------------------------ | :--------------------------------------------------------------------- | :---------- |
| **VPS（虚拟专用服务器）** | 一台物理机用虚拟化切分多份，多人共用同一台硬件，资源互相争抢。         | $3-10/月    |
| **云服务器**              | 基于分布式集群虚拟化，底层多台物理机做资源池，故障自动迁移，弹性扩容。 | ¥50-200/月 |
| **独立服务器**            | 一整台服务器物理机归你使用                                             | $50-200/月  |

**国内外常见服务商：**

| 服务商                            | 最低配置  | 月费     | 特点                       |
| :-------------------------------- | :-------- | :------- | :------------------------- |
| **BandwagonHOST（搬瓦工）** | 1核/512MB | $5-10    | 老牌 VPS，对中文用户友好   |
| **Vultr**                   | 1核/512MB | $6       | 按时计费，全球机房多       |
| **阿里云 ESC**              | 1核/1GB   | ¥50-100 | 国内访问快，需备案         |
| **腾讯云 Lighthouse**       | 1核/1GB   | ¥40-80  | 轻量服务器，国内快，需备案 |
| **Azure / AWS Lightsail**   | 1核/512MB | $5-10    | 国际大厂，稳定             |

> 如果用阿里云、腾讯云等国内服务商，域名必须**备案**——即向工信部登记网站信息。备案流程 1-2 周。如果用国外 VPS（Vultr、搬瓦工等），不需要备案，但国内用户访问速度慢一点。

空白云服务器的配置内容：

1、若仅用来部署静态网页（前端）：Ubuntu 22.04 / CentOS7/9 作为底层操作系统，配置Nginx 即可

2、若用来部署完整的JavaWeb（前端+后端）：Ubuntu 22.04 / CentOS7/9 作为底层操作系统，配置 Java 、Maven 、 SpringBoot 、 MySQL 、Redis、 Nginx 、 防火墙 等内容

### 内网穿透

如果你的博客只在本地跑，只有你电脑自己能访问。但有时候你想让**别人临时看看效果**——比如给朋友验证、用手机测试、或者给甲方演示——又不想正式部署到公网。

这时候就需要**内网穿透**：把你本机的端口（如 `localhost:1313`）通过一个中间服务器暴露到公网上。只需要在终端跑一行命令，穿透服务会给你一个公网 URL（如 `https://abc123.ngrok.io`），任何人打开这个 URL 就能看到你本机的网页。你的博客一直都在你自己电脑上，穿透服务**只负责"转发"流量，不存储内容。**

> 注意不是将本机的网页文件发送给穿透服务器，而是穿透服务器将访客的流量转发到本地，本地做出访问响应后，穿透服务器再返回给访客

**常见的穿透工具**

| 工具                       | 免费额度               | 命令示例                          | 特点                                |
| :------------------------- | :--------------------- | :-------------------------------- | :---------------------------------- |
| **ngrok**            | 1 个隧道，40 连接/分钟 | `ngrok http 1313`               | 最知名，速度稳定，有 Web 调试界面   |
| **frp**              | 需自建服务器           | `./frpc -c frpc.toml`           | 开源，功能强，可自建中转服务        |
| **Tailscale Funnel** | 免费（3 用户）         | `tailscale funnel 1313`         | 基于 WireGuard，需要 Tailscale 网络 |
| **Localtunnel**      | 免费                   | `lt --port 1313`                | 无需注册，npm 安装即用              |
| **bore**             | 免费                   | `bore local 1313 --to bore.pub` | Rust 写的，极简                     |

最简操作示例：

1. **下载 ngrok** — https://ngrok.com/download （Windows 下载 exe 放到任意目录）
2. **启动 Hugo** — `cd blog && hugo server`
3. **启动隧道** — 新开一个终端，`ngrok http 1313`

终端会显示一个公网 URL：

```
Forwarding   https://a1b2c3d4.ngrok.io → http://localhost:1313
```

## 扩展：常见的几种网络请求

**Headers：**

HTTP 请求可以带一些"元信息"。最关键的是 **User-Agent**——告诉服务器"我是谁"：

```
# 反面教材：不设 User-Agent（服务器一眼识别是爬虫）
async with httpx.AsyncClient() as client:
    resp = await client.get(url)    # ❌ 容易被封

# 正确模仿：伪装成浏览器
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36"
}
async with httpx.AsyncClient(headers=headers) as client:
    resp = await client.get(url)    # ✅ 像真人浏览器
```

UA中最主要的字段：

```
Windows NT 10.0; Win64; x64 # 操作系统：Windows 10 64 位
Chrome/120.0.0.0 # 浏览器：Chrome 120 版本
```

> 其余的 `Mozilla/AppleWebKit/Safari` 都是历史兼容遗留字段，现代网站只看 Chrome 版本

**几种网络请求的模板代码：**

1、RSS

```
import feedparser

feed = feedparser.parse("https://example.com/rss.xml")
for entry in feed.entries:
    title = entry.get("title")
    link  = entry.get("link")
    # 正文大概率在 entry.content 或 entry.summary 里
```

整个采集就两步：parse → 遍历 entries。不需要处理 JSON、不需要解析 HTML、不需要关心反爬

2、API

```
import httpx

async with httpx.AsyncClient() as client:
    resp = await client.get(
        "https://api.example.com/data",
        headers={"Authorization": "Bearer YOUR_TOKEN"},
        params={"page": 1, "limit": 20}
    )
    resp.raise_for_status()      # 检查状态码
    data = resp.json()            # 自动解析 JSON
    for item in data["items"]:
        print(item["title"])
```

3、scrapy

```
import httpx
from bs4 import BeautifulSoup

# 1. 下载网页
resp = httpx.get("https://example.com", headers=headers)
soup = BeautifulSoup(resp.text, "lxml")

# 2. 通过CSS选择器提取信息
for item in soup.select(".article-title a"):
    title = item.get_text(strip=True)   # 提取文本
    url   = item.get("href")            # 提取链接属性
```

CSS 选择器示例：

| 选择器                  | 含义                             |
| :---------------------- | :------------------------------- |
| `h2`                  | 所有 元素                        |
| `.title`              | 所有 class="title" 的元素        |
| `h2 a`                |  内部的 <a></a>                  |
| `h2 > a`              |  的直接子 <a></a>                |
| `.entry-title a`      | class 为 entry-title 内的<a></a> |
| `a[href*='/article']` | href 包含 "/article" 的<a></a>   |

爬虫的编写思路：在浏览器打开目标网站  → 检查（F12）→ 找到一篇文章 → 看它的 HTML 结构 → 写选择器匹配所有文章 → 再获取文章中的任意元素

反爬机制和反反爬手段：**(大多数网站只需要 User-Agent 伪装就够了)**

| 级别      | 反爬类型              | 特征描述                                                                                | 应对策略                                                                               | 代码示例/关键点                                                                                  | 实施难度 | 绕过成功率 |
| :-------- | :-------------------- | :-------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------- | :------- | :--------- |
| 🔵 基础级 | Referer来源校验       | 拦截跨站请求，拒绝返回数据，提示“非法请求来源”。                                      | 在请求头中补充合法的`Referer`字段，模拟从搜索引擎或网站内部的跳转。                  | `headers["Referer"] = "https://www.google.com/"` 或目标网站域名。                              | 低       | 80%        |
| 🔵 基础级 | 基础IP访问频率限制    | 高频请求返回`429 Too Many Requests`状态码，并临时封禁IP。                             | 1. 在请求间增加固定延时。2. 控制并发请求数量在3-5个以内。                              | (1)`await asyncio.sleep(2)`  使用 `asyncio.Semaphore(3)` 控制并发。                          | 中       | 90%        |
| 🔵 基础级 | 静态资源防盗链        | 文章内的图片无法加载，显示403占位图（例如在自己的博客中填入其他网站的图片资源地址）     | 在图片资源的请求头中补充`Referer`为目标网站域名。                                    | `headers["Referer"] = "https://www.qbitai.com/"`                                               | 低       | 70%        |
| 🟡 进阶级 | Cloudflare JS人机验证 | 访问时弹出中转验证页面（如滑块、点选），需验证后才能获取源码。                          | 1. 使用`cloudscraper`库自动完成基础验证。2. 对接Cloudflare Turnstile验证服务。       | `scraper = cloudscraper.create_scraper(browser={'browser': 'chrome', 'platform': 'windows'})`  | 中高     | 60%        |
| 🟡 进阶级 | JS动态渲染页面        | 原始HTML不包含文章数据，内容由JavaScript异步加载，导致解析不到内容。                    | 使用Playwright、Selenium等无头浏览器模拟完整页面加载，等待JS执行完毕后获取HTML。       | `await page.wait_for_selector("article h2 a")`  `html = await page.content()`                | 高       | 50%        |
| 🟡 进阶级 | 图形/滑块验证码       | 频繁访问时弹出验证码，需手动验证才能继续。                                              | 1. 对接第三方打码平台（如超级鹰）。2. 使用Playwright结合OCR自动识别和操作。            | `await slider.drag_to(page.locator(".slider-target"), steps=20)`                               | 高       | 40%        |
| 🟡 进阶级 | 字体反爬              | 页面数字或文字显示乱码，HTML源码为特殊Unicode编码，无法直接提取。                       | 1. 下载并解析自定义字体文件（如`.woff`），映射字符对应关系。2. 使用OCR识别文字内容。 | `font = TTFont("custom_font.woff")`  `glyph_map = font.getBestCmap()`                        | 高       | 30%        |
| 🟡 进阶级 | 请求参数签名校验      | 接口URL或Headers携带加密参数（如`timestamp`、`nonce`、`sign`），参数错误返回403。 | 逆向JavaScript加密逻辑，使用Python复现签名生成算法。                                   | `sign = hashlib.md5(f"{timestamp}{nonce}{secret_key}".encode()).hexdigest()`                   | 高       | 40%        |
| 🔴 高阶   | 设备/浏览器指纹识别   | 检测Canvas、WebGL、WebRTC等指纹，识别自动化浏览器并封禁。                               | 使用Playwright并配置启动参数，禁用自动化控制特征，模拟真实指纹。                       | `args=["--disable-blink-features=AutomationControlled"]`  配置`viewport`和`user_agent`。   | 极高     | 30%        |
| 🔴 高阶   | 行为轨迹反爬          | 检测鼠标移动、滚动、点击等轨迹，识别非人类行为。                                        | 使用Playwright模拟更真实的用户操作，如带步骤的移动、随机停顿、模拟滚动等。             | `await page.mouse.move(100, 200, steps=10)`  `await asyncio.sleep(random.uniform(0.5, 1.5))` | 极高     | 25%        |
| 🔴 高阶   | 账号登录权限校验      | 未登录状态无法查看正文，部分内容仅对登录用户开放。                                      | 1. 持久化登录后的Cookie，在后续请求中复用会话。2. 优先探索官方API。                    | `cookies = await context.cookies()`  `context = await browser.new_context(cookies=cookies)`  | 高       | 35%        |
| 🔴 高阶   | 蜜罐陷阱              | 页面中隐藏不可见链接（蜜罐），爬虫一旦访问则触发封禁。                                  | 解析页面时，过滤掉CSS样式为`display:none`或`visibility:hidden`等隐藏元素。         | `soup.select('a[style*="display:none"]')`  使用`decompose()`移除。                           | 中       | 20%        |
| 🔴 高阶   | 代理IP检测            | 通过请求头（如`X-Forwarded-For`）检测并封禁代理IP。                                   | 1. 使用高匿代理IP。2. 在请求前移除或禁用代理相关的请求头。                             | `headers.pop("X-Forwarded-For", None)`  配置高匿代理。                                         | 高       | 20%        |

> 无头浏览器：启动浏览器内核，但不弹出可视化窗口，没有窗口界面，后台静默运行。对比普通浏览器和http request的优点是无头浏览器会等待页面js代码执行完成、DOM元素渲染完成之后才会返回网页源码，这就避免了在http request中不等待完全渲染就立刻返回网页源码，导致在处理JS动态异步渲染的网页时无法返回包含完整内容的源码

> 设备/浏览器指纹：访客在访问网站时，网站的服务器会主动通过JS来采集访客的设备/浏览器指纹，以此来判定访客是否是机器人/爬虫脚本还是真实用户。所谓的指纹就是访客的特征，例如设备指纹有CPU型号、GPU信息、硬件序列号等，浏览器指纹有浏览器版本、浏览器使用的插件、使用的字体、屏幕的分辨率等

> 采集鼠标行为轨迹：前端在JS监听mouse move和mouse click等事件，每隔一定事件采样鼠标坐标和时间戳，攒够数据就带着session id发给后端。后端拿到数据，可以计算鼠标轨迹的线性度（爬虫的直线轨迹线性度接近1，真人的则会较低）、鼠标移动的速度变化（爬虫大多匀速，真人则是先加速后减速）等等。后端还可以将这些数据都交给大模型进行进一步的研判

4、其他网络请求方式（省略）

| 方式                       | 传输方向           | 数据格式           | 典型场景                                | Python 库                 |
| :------------------------- | :----------------- | :----------------- | :-------------------------------------- | :------------------------ |
| **WebSocket**        | 双向实时           | 任意（常见 JSON）  | 聊天、股票行情、实时通知                | `websockets`            |
| **GraphQL**          | 客户端查询         | JSON               | 灵活的数据查询（GitHub API 新版）       | `gql` / httpx           |
| **gRPC**             | 双向（支持流）     | Protobuf（二进制） | 微服务内部通信、高性能场景              | `grpcio`                |
| **SSE**              | 服务端→客户端     | 文本流             | AI 流式输出（如 DeepSeek 的 streaming） | httpx /`sse-starlette`  |
| **Webhook**          | 服务端→你的服务器 | JSON（常见）       | GitHub push 通知、支付回调              | Flask / FastAPI（接收端） |
| **FTP / SFTP**       | 文件传输           | 文件               | 旧系统对接、批量文件交换                | `ftplib` / `paramiko` |
| **TCP / UDP 裸连接** | 双向               | 二进制             | 游戏、视频流、自定义协议                | `socket`                |

## 扩展：什么是跨站请求

跨站请求=跨域请求=跨站访问=跨域

**判断是否跨站三要素（有一个不同即跨站）：**

1. 协议：`http` / `https`
2. 主域名：`qbitai.com` / `baidu.com`
3. 端口：`80` / `8080` / `3000`

**为什么会有跨域限制：浏览器原生的同源策略**

> 同站：页面来自 `https://www.qbitai.com`，请求 `https://www.qbitai.com/news`
>
> 跨站：页面来自 `https://google.com`，请求 `https://www.qbitai.com`

**网站通过 请求头中的`Referer` 字段判断访问来源：**

- `Referer`：告诉服务器「当前请求是从哪个页面跳转过来的」
- 如果请求里没有 Referer，或者 Referer 是别的域名（跨站），网站判定为盗链 / 爬虫，直接返回 403

**两种典型拦截场景：**

1. 图片防盗链

   你在自己博客直接嵌入量子位图片 `<img src="https://qbitai.com/xxx.jpg">`

   浏览器请求图片时 Referer 是你的域名，属于跨站，服务器拒绝返回图片。
2. 接口防爬虫

   爬虫不带 Referer，服务器识别是外部跨站请求，直接拦截。

注意：拦截请求的主体是访客的浏览器，而不是网页的服务器

## 项目源码阅读
