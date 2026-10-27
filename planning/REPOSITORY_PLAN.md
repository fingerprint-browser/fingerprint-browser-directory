# 仓库与页面规划

建议仓库名：`fingerprint-browser-directory`。受众是使用简体中文、正在比较商业指纹浏览器的读者。内容以 Google 可见性为目标，首批 12 页；发布前不承诺排名或流量。

## 交付与文案分工

研究方提供选题、官方事实、来源、页面边界、内链和 Gemini 提示词。Gemini 生成最终 Markdown。用户确认稿件后再用于发布。当前 README 是项目说明，不是最终推荐文章。

## 当前资料目录

- `planning/START_HERE.md`：使用方法与任务顺序。
- `planning/RESEARCH_FINDINGS.md`：机会、竞品结构和证据范围。
- `planning/data/product-facts.json`、`browser-plans.csv`：事实与套餐快照。
- `planning/data/page-map.csv`、`page-briefs.json`：页面与关键词分工。
- `planning/briefs/P00.md` 至 `P11.md`：单页简报。
- `planning/prompts/P00.md` 至 `P11.md`：可独立复制给 Gemini 的完整任务。
- 总写作提示词、复核提示词与验收表各一份。

## 最终公开页面

下表是目标文件，不代表文章已经生成。Gemini 应按这些相对路径输出；先写正文，首页最后写。

| ID | 目标文件 | 建议标题 | 主要查询 | 分工 |
|---|---|---|---|---|
| P00 | `README.md` | 指纹浏览器对比：8 款产品的价格、团队与自动化选择 | 指纹浏览器对比 | P0 |
| P01 | `browsers/bitbrowser.md` | 比特浏览器怎么样？免费环境、价格、代理与自动化 | 比特浏览器怎么样 | P0 |
| P02 | `browsers/adspower.md` | AdsPower 免费版够用吗？环境数量、试用与自动化 | AdsPower 免费版 | P0 |
| P03 | `browsers/gologin.md` | GoLogin 免费版有哪些限制？3 个环境、创建次数与云端功能 | GoLogin 免费版限制 | P0 |
| P04 | `browsers/morelogin.md` | MoreLogin 免费版适合两个人用吗？环境、用户与自动化 | MoreLogin 免费版 | P1 |
| P05 | `browsers/ixbrowser.md` | ixBrowser 真的不限环境吗？免费日次数与付费方式 | ixBrowser 免费版 | P1 |
| P06 | `browsers/incogniton.md` | Incogniton 免费多久？前两个月额度与自动化套餐 | Incogniton 免费版 | P1 |
| P07 | `browsers/dolphin-anty.md` | Dolphin Anty 免费版有几个环境？3 个与 5 个的资料差异 | Dolphin Anty 免费版 | P1 |
| P08 | `browsers/multilogin.md` | Multilogin 免费版是什么？配置名额、代理与云手机时长 | Multilogin 免费版 | P1 |
| P09 | `comparisons/bitbrowser-vs-adspower.md` | 比特浏览器和 AdsPower 怎么选？免费额度、自动化与团队成本 | 比特浏览器和 AdsPower 哪个好 | P0 |
| P10 | `comparisons/bitbrowser-vs-gologin.md` | 比特浏览器和 GoLogin 怎么选？免费名额、云端运行与价格 | 比特浏览器和 GoLogin 对比 | P0 |
| P11 | `guides/best-free-fingerprint-browsers.md` | 免费指纹浏览器有哪些？8 款免费版额度与限制 | 免费指纹浏览器哪个好 | P0 |

## 页面之间怎么链接

总览连接 8 个品牌、2 个对比和免费指南。品牌详情返回总览；比特、AdsPower、GoLogin 连接对应比较；涉及免费条件的页面连接免费指南。比较页连接双方详情。免费指南连接各品牌的完整限制。

链接用 Markdown 相对路径。单页简报已给出相对路径，Gemini 不需要自行猜地址。目标稿全部完成后统一检查链接；不创建空白占位页来凑数量。

## 关键词与重叠控制

首页主抓“指纹浏览器对比”，免费指南主抓“免费指纹浏览器哪个好/有哪些”。品牌详情解释其自己的价格和免费条件；比较页主抓明确的两个品牌组合。相同数字可以出现在不同页，但段落、判断和主要问题不能整段重复。

同一品牌先保留一个完整详情页。之后只有在出现独立问题且来源足够时，才拆出 API、代理、迁移等子页。不要一开始就生成所有品牌的价格页、下载页、免费页和年度换皮页。

## GitHub 发布范围

当前只准备 Markdown 仓库，不创建 GitHub Pages、域名或网页部署。Gemini 输出的 SEO Title/Meta Description 是后续网页项目可复用的编辑资料，不会自动成为 GitHub 的 HTML 元标签。

只有经过确认的文章才替换首页并加入目标目录。原始研究与事实变化继续留在 planning 中维护。若后续转独立网站，再另行规划 HTML 标题、canonical、sitemap 和收录检查，不在 Markdown 正文粘贴无效标签。

## 更新规则

价格、名额、计数与权限变化时，先更新事实包及 CSV，再检查引用该产品的首页、详情、比较和免费指南。保留实际核验日期。没有发生核验就不刷新日期，也不把表内空值解释为额度为零。
