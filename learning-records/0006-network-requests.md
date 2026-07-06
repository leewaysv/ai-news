# 网络请求三种方式与爬虫技术细节

理解了 RSS（标准化 XML 解析）、API（结构化 JSON 接口）、爬虫（HTML 解析 + CSS 选择器）三种数据获取方式的本质区别和各自适用场景。掌握了 HTTP 基础知识（状态码、headers、User-Agent 伪装）、爬虫通用思维模式（分析→选择器→提取）、以及从 User-Agent 伪装到 Playwright 浏览器自动化的反爬对抗阶梯。能对照 pipeline 的 gather 模块代码理解每种采集器的实现模式。

**Evidence:** 用户主动要求系统学习网络请求方式，特别提到了爬虫模板思路、反爬对策，以及对照 pipeline 中三种 gather 方法。用户打开了 api_collector.py 表明对代码实现有具体兴趣。

**Implications:** 后续可以深入到数据清洗和处理、或更多实战抓取练习。
