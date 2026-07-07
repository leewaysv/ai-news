---
title: "抖音视频渲染 + 上传"
labels: ["ready-for-agent"]
---

## Parent

Parent issue: #1 (7-6 prd)

## What to build

将 DouyinAdapter 生成的脚本和字幕渲染为实际视频，并自动上传到抖音：

- 视频渲染：集成 FFmpeg + moviepy 流水线，或利用 MoneyPrinterTurbo
- 背景素材：用 Pexels/Pixabay API 搜索免费商用素材
- TTS 语音合成：集成 edge-tts（免费/本地，中文音质良好）
- 字幕嵌入：将 .srt 字幕烧录到视频中
- BGM 添加：可选背景音乐
- AI 水印：视频结尾叠加"AI 辅助生成"水印
- 上传：集成 social-auto-upload（Playwright 自动化），自动登录抖音创作者平台并上传视频
- 发布状态记录：上传成功后记录视频 ID 和发布状态

## Acceptance criteria

- [ ] 从脚本生成 15-60 秒竖屏视频（9:16, 720p, MP4）
- [ ] TTS 语音和字幕同步
- [ ] 视频结尾包含 AI 辅助生成水印
- [ ] 视频可成功上传到抖音
- [ ] 上传状态记录到日志
- [ ] 失败时自动重试并记录错误

## Blocked by

- 抖音脚本生成（DouyinAdapter）

## Notes

- 视频渲染需要 GPU 加速（NVIDIA NVENC），GitHub Actions 不支持
- 可在本地开发机、自建 GPU runner 或云 GPU（RunPod/Banana.dev）上运行
- 首次实现以本地执行为主，后续优化到 CI
