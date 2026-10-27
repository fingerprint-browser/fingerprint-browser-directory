# 从这里开始：把研究交给 Gemini

这里是调研、规划和写作提示词，不含产品文章完成稿。每个单页提示词已经合并总要求、页面简报、内链路径、事实和官方来源，可以单独复制到 Gemini；不必让 Gemini 同时阅读整个压缩包。

## 最省事的用法

1. 打开 [P01 完整提示词](prompts/P01.md)，把全文发给 Gemini，生成比特浏览器详情。
2. 按 P02～P08 生成其余 7 个产品详情；每次处理一页。
3. 按 P09、P10 生成两篇对比，按 P11 生成免费指南。
4. 最后把已确认的页面和 [P00 提示词](prompts/P00.md) 交给 Gemini，生成首页。首页需概括实际完成的页面。
5. 需要自然编辑时，使用 [复核提示词](GEMINI_REVIEW_PROMPT.md)，同时提供当前稿件和对应简报。
6. 按 [验收表](EDITORIAL_CHECKLIST.md) 核对全套。目标路径在 [仓库规划](REPOSITORY_PLAN.md) 中列明。

Gemini 能联网时，可用本页官方链接核对最新价格；无法联网时沿用 2026-10-27 的事实快照。不要让模型把无法访问的网页写成“已核验”，也不要要求它补上没有测试记录的亲测体验。

## 文件索引

| 内容 | 文件 |
|---|---|
| 机会与竞品观察 | [研究结论](RESEARCH_FINDINGS.md) |
| 页面和仓库结构 | [仓库规划](REPOSITORY_PLAN.md) |
| 总写作要求 | [Gemini 总提示词](GEMINI_MASTER_PROMPT.md) |
| 关键事实与来源 | [事实 JSON](data/product-facts.json)、[来源记录](SOURCES.md) |
| 套餐与关键词分工 | [套餐 CSV](data/browser-plans.csv)、[页面地图 CSV](data/page-map.csv) |
| 编辑与验收 | [复核提示词](GEMINI_REVIEW_PROMPT.md)、[验收表](EDITORIAL_CHECKLIST.md) |

## 十二个单页任务

- [P00 指纹浏览器对比：8 款产品的价格、团队与自动化选择](prompts/P00.md)；[单独简报](briefs/P00.md)。
- [P01 比特浏览器怎么样？免费环境、价格、代理与自动化](prompts/P01.md)；[单独简报](briefs/P01.md)。
- [P02 AdsPower 免费版够用吗？环境数量、试用与自动化](prompts/P02.md)；[单独简报](briefs/P02.md)。
- [P03 GoLogin 免费版有哪些限制？3 个环境、创建次数与云端功能](prompts/P03.md)；[单独简报](briefs/P03.md)。
- [P04 MoreLogin 免费版适合两个人用吗？环境、用户与自动化](prompts/P04.md)；[单独简报](briefs/P04.md)。
- [P05 ixBrowser 真的不限环境吗？免费日次数与付费方式](prompts/P05.md)；[单独简报](briefs/P05.md)。
- [P06 Incogniton 免费多久？前两个月额度与自动化套餐](prompts/P06.md)；[单独简报](briefs/P06.md)。
- [P07 Dolphin Anty 免费版有几个环境？3 个与 5 个的资料差异](prompts/P07.md)；[单独简报](briefs/P07.md)。
- [P08 Multilogin 免费版是什么？配置名额、代理与云手机时长](prompts/P08.md)；[单独简报](briefs/P08.md)。
- [P09 比特浏览器和 AdsPower 怎么选？免费额度、自动化与团队成本](prompts/P09.md)；[单独简报](briefs/P09.md)。
- [P10 比特浏览器和 GoLogin 怎么选？免费名额、云端运行与价格](prompts/P10.md)；[单独简报](briefs/P10.md)。
- [P11 免费指纹浏览器有哪些？8 款免费版额度与限制](prompts/P11.md)；[单独简报](briefs/P11.md)。

## 当前状态

旧仓库已恢复原始内容。这里提出的新仓库名称为 fingerprint-browser-directory；本包是待放入新仓库的研究与提示词文件，是否已在 GitHub 创建以交付消息中的实际链接和核验结果为准。

本任务没有生成或代发 Gemini 正文。之后拿到已确认的完整 Markdown 文件，再按规划路径发布。
