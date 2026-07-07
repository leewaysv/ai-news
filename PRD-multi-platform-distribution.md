# PRD：AI 早报多平台发布（微信公众号 + 抖音短视频）

## Problem Statement

目前 AI 早报仅在 Hugo 博客上发布，覆盖范围有限。大量目标读者活跃在微信公众号和抖音上。每次手动将博客内容适配到不同平台费时费力，且容易出错。需要一套自动化多平台发布系统，让同一份内容在多个渠道同时触达读者。

## Solution

扩展 Pipeline 的适配器层和发布器层，利用已定义的 `BaseAdapter` 接口，新增微信公众号和抖音两个平台的适配器与发布器。Pipeline 每日运行后，除了写入 Hugo Markdown，还自动生成各平台格式的内容并发布。博客作为内容原创性锚点，微信做深度阅读和私域转化，抖音做公域引流。

## User Stories

1. 作为早报运营者，我希望 Pipeline 完成新闻摘要后自动生成微信公众号格式的图文，以便每日定时推送。
2. 作为早报运营者，我希望 Pipeline 自动将新闻摘要转换为抖音短视频脚本，以便在短视频平台传播。
3. 作为早报运营者，我希望微信发布的文章带有合规的 AIGC 标注，以避免违反平台规定。
4. 作为早报运营者，我希望微信文章的标题不超过 32 个字符（微信限制），标题能传达核心信息。
5. 作为早报运营者，我希望微信文章正文中的图片能自动上传到微信 CDN，以避免图片无法显示。
6. 作为早报运营者，我希望一天内的多篇文章能合并为一次微信推文推送（微信限制：每天 1 次，最多 8 篇）。
7. 作为早报运营者，我希望系统支持微信 API 的 access_token 自动刷新（两小时有效期），以避免发布失败。
8. 作为早报运营者，我希望抖音视频自动生成带字幕的竖屏短视频，以适应抖音的推荐算法。
9. 作为早报运营者，我希望抖音视频包含 AI 内容标注，以符合 2025 年 9 月生效的 AIGC 法规。
10. 作为早报运营者，我希望 Pipeline 发布失败时能自动重试并记录日志，以便排查问题。
11. 作为早报运营者，我希望 Pipeline 在微信 API 不可用时能够降级（跳过微信发布不影响博客上线），以避免互相影响。
12. 作为早报运营者，我希望系统以配置驱动的方式控制哪个平台启用/禁用，以便灵活调整发布策略。
13. 作为早报运营者，我希望微信公众号发布前可预览草稿，以便人工确认格式正确。
14. 作为早报运营者，我希望抖音视频脚本可以先保存到本地审查，确认后再发布，以便避免 AI 生成内容违规。
15. 作为早报运营者，我希望 Pipeline 中各平台的发布状态和错误信息能记录到日志，以便监控和排查。

## Implementation Decisions

### 架构决策

- **适配器模式**：复用 `pipeline/src/adapt/base.py` 中已定义的 `BaseAdapter` 接口。新增 `WeChatAdapter` 和 `DouyinAdapter`，各自实现 `adapt(digest) -> list[AdaptedContent]` 方法。已有 `BlogAdapter` 作为参考实现。
- **发布器模式**：新增 `WeChatPublisher` 和 `DouyinPublisher`，各自封装对应平台的 API 调用逻辑。`BlogPublisher`（文件写入）作为参考。
- **Pipeline 编排**：在 `main.py` 的 `run()` 方法中，适配和发布步骤改为遍历启用中的平台列表，依次执行适配→发布。
- **配置驱动**：在 `config.yaml` 中新增 `platforms` 配置段，控制各平台启用/禁用，以及平台特定的参数（如微信的 app_id、抖音的视频时长等）。

### 模块修改/新增

| 模块 | 动作 | 职责 |
|------|------|------|
| `adapt/wechat_adapter.py` | 新增 | `DailyDigest` → 微信兼容的内联 HTML |
| `adapt/douyin_adapter.py` | 新增 | `DailyDigest` → 视频脚本 + TTS 配置 + 字幕 |
| `publish/wechat_publisher.py` | 新增 | 调用微信发布 API |
| `publish/douyin_publisher.py` | 新增 | 视频生成 + 上传到抖音 |
| `config.py` | 修改 | 新增 `PlatformConfig` 模型，解析平台配置 |
| `main.py` | 修改 | 适配/发布步骤改为平台循环 |
| `config.yaml` | 修改 | 新增 `platforms` 配置段 |

### WeChatAdapter 关键决策

- 标题截断：超过 32 字符自动截断并加 `…`
- 正文转换：Markdown → 微信支持的 HTML 子集（div, p, section, h1-h6, img, strong, blockquote, a, ul/ol/li）
- 图片处理：正文图片通过微信 `uploadimg` API 上传，获取永久 URL 后嵌入 HTML
- 封面图：第一条新闻的标题图自动作为推文封面，通过 `add_material` API 上传
- AIGC 合规：每篇文章底部追加 AI 辅助生成声明（与博客对齐）
- 合并推送：当日早报的 N 篇文章合并为一次微信推文（最多 8 篇）

### DouyinAdapter 关键决策

- 脚本生成：每篇文章提炼 15-60 秒口播脚本（hook → 问题 → 结论 → CTA）
- TTS 方案：集成 `edge-tts`（免费，中文音质可接受），后续可升级 CosyVoice
- 字幕生成：自动生成 .srt 字幕文件，嵌入视频
- 素材选择：用关键词搜索 Pexels/Pixabay 作为背景视频素材
- 视频合成：`MoneyPrinterTurbo` 或 FFmpeg + moviepy 流水线
- AI 标注：在视频结尾叠加"AI 辅助生成"水印

### 微信 API 集成决策

- API 版本：使用微信公众平台最新 REST API
- 认证要求：2025 年 7 月起仅认证公众号可用 API。如果账号未认证，降级为 Playwright 自动化（通过 social-auto-upload 操作后台）
- Token 管理：全局缓存 `access_token`，首次获取后定时刷新（有效期 7200s）
- 发布流程：上传图片 → 创建草稿 → 提交发布 → 轮询发布状态
- IP 白名单：服务器 IP 需要在微信后台加入白名单（GitHub Actions 的 IP 不固定，可改用固定代理或自建中转服务器）
- 降级策略：API 调用失败时自动跳过微信发布，不影响博客和其他平台

### 抖音视频生成集成决策

- 优先方案：`MoneyPrinterTurbo` 开源项目（47K+ Stars），支持 LLM 脚本 + TTS + 字幕 + BGM 全流程
- 视频规格：竖屏 9:16，720p，MP4，15-60 秒
- 发布方案：Playwright 自动化（`social-auto-upload`，11K Stars），因抖音开放平台 API 门槛过高（注册资本 ≥50 万元）
- GPU 需求：视频渲染需 GPU 加速（NVIDIA NVENC），GitHub Actions 不支持 GPU，可在本地或自建 runner 上运行
- 生成本地优先：视频脚本和字幕生成本地完成，视频渲染在有 GPU 的环境中运行

### 配置格式（config.yaml 扩展）

```yaml
platforms:
  blog:
    enabled: true
    output_dir: "../blog/content/articles"
  wechat:
    enabled: false        # 默认关闭，认证后开启
    app_id: ""
    app_secret: ""
    max_articles_per_push: 8
  douyin:
    enabled: false        # 默认关闭，需 GPU 环境
    video_duration: 45    # 秒
    tts_provider: "edge-tts"
    watermark: true
```

## Testing Decisions

### 测试原则

- 只测外部行为，不测实现细节
- Adapter 测试是最佳 seam——给定相同的 `DailyDigest`，验证输出格式是否正确
- Publisher 测试通过 mock API 响应来验证请求构造和错误处理

### 测试内容

| 测试 | 层级 | 方法 |
|------|------|------|
| WeChatAdapter 标题截断 | Adapter | 输入超长标题，验证输出 HTML 标题 ≤32 字 |
| WeChatAdapter HTML 合规性 | Adapter | 验证输出的 HTML 不含微信禁止的标签 |
| WeChatAdapter AIGC 标注 | Adapter | 验证每篇文章底部有 AI 生成声明 |
| DouyinAdapter 脚本长度 | Adapter | 验证脚本时长在 15-60 秒范围 |
| DouyinAdapter 字幕格式 | Adapter | 验证输出的 .srt 文件格式正确 |
| DouyinAdapter 关键词提取 | Adapter | 验证素材搜索关键词从摘要提取 |
| WeChatPublisher Token 刷新 | Publisher | mock API，验证 token 过期后自动刷新 |
| WeChatPublisher 发布流程 | Publisher | mock API，验证 uploadimg→draft→submit 完整链路 |
| WeChatPublisher 降级 | Publisher | mock API 返回错误，验证不影响博客发布 |
| 配置解析 | Config | 验证 platforms 配置正确加载 |

### 已有参考

- `BlogAdapter` 的适配逻辑作为 `WeChatAdapter`/`DouyinAdapter` 的测试模板

## Out of Scope

- **抖音开放平台官方 API 集成**：由于注册资本门槛过高（≥50 万元），Phase 3 使用 Playwright 自动化代替。如未来条件满足，可替换。
- **微信订阅通知**：仅做公众号内容发布，不包括模板消息或客服消息。
- **跨平台数据统计**：不追踪各平台的阅读量/播放量，仅做发布。
- **抖音直播**：不做直播功能，仅做短视频发布。
- **自定义域名配置**：博客的自定义域名绑定，非本 PRD 范围。

## Further Notes

- **微信 API 策略变更频繁**：2025 年 7 月的个人/未认证账号 API 回收政策表明微信在收紧自动化。建议先将微信发布标记为"试用"状态，持续关注政策变化。
- **Phase 3 依赖 GPU**：短视频渲染需要 GPU，在 GitHub Actions 免费 runner 上无法完成。方案：① 本地运行（每周批量生成一次）；② 自建 GPU runner；③ 使用云 GPU 服务（如 RunPod、Banana.dev）。
- **中国 AIGC 法规**：2025 年 9 月《人工智能生成合成内容标识方法》生效，所有 AI 生成/辅助内容必须标注。两平台的适配器都必须实现合规标注。
- **Playwright 维护成本**：`social-auto-upload` 依赖浏览器自动化，网站改版可能导致脚本失效，需要持续维护。
