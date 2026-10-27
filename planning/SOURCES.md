# 产品数据来源与本轮核验记录

核验日期：2026-10-27。这里保留会影响选型的公开条件与对应入口；内容更新时，先修改同一条记录，再同步总览、详情页和 CSV。

## 免费额度与价格

| 产品 | 来源 | 本轮采用的条件 |
|---|---|---|
| 比特浏览器 | [国际站价格卡](https://www.bitbrowser.net/price) | 免费 10 个环境、成员上限 1；每日打开 50 次、创建 20 个；免费卡列有同步器、Local API、RPA |
| 比特浏览器 | [中国站价格](https://www.bitbrowser.cn/price) | 人民币月付方案：50 窗口/2 员工 50 元；100/4 为 75 元；200/8 为 125 元 |
| AdsPower | [价格页](https://www.adspower.com/pricing) | 长期免费 2 环境、0 额外成员，含 1 超级管理员；另有 7 天完整功能试用；付费按数量、成员和周期配置 |
| GoLogin | [价格页](https://gologin.com/pricing/) | 免费 3 环境；Professional 月付 9 美元起；使用专业版入门价，不引用有冲突的高级档报价 |
| GoLogin | [套餐帮助](https://support.gologin.com/en/articles/14617029-pricing) | 免费档每自然月创建 25 次；Cookie 导出、API、云端启动和团队等限制；新价格适用账号条件 |
| MoreLogin | [价格与功能页](https://www.morelogin.com/pricing) | 免费 2 环境、2 用户；列有同步器、Local API 和 Selenium/Puppeteer；Pro 9 美元与年付折扣展示分别记录 |
| ixBrowser | [价格表](https://ixbrowser.com/pricing) | 免费环境不限；2 席位，每日创建 10 次、打开 100 次；付费频次和成员规模分层 |
| Incogniton | [价格与功能表](https://incogniton.com/pricing/) | 免费前两个月 10 环境，之后 3；付费环境数、月付标价及自动化权限分层 |
| Dolphin Anty | [套餐帮助](https://docs.dolphin-anty.com/en/personal-cabinet/plans-in-dolphin-anty) | 免费 3 环境、每月重建 20 次；Starter 20～60 环境，增加导出与云同步等能力 |
| Dolphin Anty | [价格页](https://dolphin-anty.com/tarifs/) | Base 100 环境 89 美元/月，Team 300 环境 159 美元/月；免费额度页面内有冲突，见下节 |
| Multilogin | [价格与 FAQ](https://multilogin.com/pricing/) | Free 为 5 个云手机与浏览器配置名额；代理流量与移动分钟为一次性赠送；Pro 月付与年付分别记录 |

## 操作与功能入口

| 资料 | 本目录使用范围 |
|---|---|
| [比特下载页](https://www.bitbrowser.cn/download) | Windows、macOS 客户端入口 |
| [比特代理设置](https://www.bitbrowser.cn/proxy-setting) | 代理配置与连接检测 |
| [比特 Local API](https://www.bitbrowser.cn/local-api) | 环境程序化管理与自动化框架接入 |
| [比特 MCP 教程](https://www.bitbrowser.cn/news/how-to-configure-bitbrowser-mcp) | Local API 鉴权、MCP 配置与工具连接 |
| [比特窗口迁移教程](https://www.bitbrowser.cn/blog/how-to-migrate-browser-profiles-to-bitbrowser) | 原窗口资料、Cookie、代理整理与批量导入 |
| [AdsPower API](https://help.adspower.com/docs/api) | Local API 入口、超级管理员与成员授权 |
| [AdsPower RPA](https://help.adspower.com/docs/rpa) | 流程编辑、错误处理、分组和模板分享 |
| [GoLogin 系统与安装](https://support.gologin.com/en/articles/3452486-supported-platforms-installation) | 桌面与移动端支持范围 |
| [GoLogin API Quickstart](https://gologin.com/docs/api-reference/introduction/quickstart) | API key 入口、客户端与调用示例 |
| [MoreLogin 产品页](https://www.morelogin.com/) | 本地与云端环境、Android 云手机、同步操作 |
| [ixBrowser 产品页](https://ixbrowser.com/en) | 产品定位与环境管理 |
| [Dolphin 环境限制](https://docs.dolphin-anty.com/en/working-with-profiles/restrictions-on-working-with-profiles-in-dolphin-anty) | 环境名额与重新创建额度 |
| [Dolphin 自动化](https://docs.dolphin-anty.com/en/api/basic-automation-dolphin-anty) | 启动环境与自动化接口说明 |
| [Multilogin 系统要求](https://multilogin.com/help/en_US/minimum-system-requirements) | Windows、macOS 和 Ubuntu 版本条件 |
| [fingerprint-chromium](https://github.com/adryfish/fingerprint-chromium) | 开源浏览器项目的类型说明 |
| [Camoufox](https://github.com/daijro/camoufox) | 开源反检测与自动化项目的类型说明 |

## 本轮发现的口径差异

**Dolphin 免费额度：** 套餐帮助文档和官网页尾写 3 个，价格页部分功能表仍写 5 个。本轮事实包与 CSV 采用套餐文档的 3 个，并同时保留两个来源；已有账号以其套餐界面显示的配额核对。

**GoLogin 报价与免费权限：** 价格页和帮助页在高级档报价、部分免费功能概括上存在差异。本轮不发布高级档的统一金额；免费 API、云端启动、分享及导出等条件采用列项更具体的套餐帮助页。年付帮助页还有示例数字不一致，正文不据此自行补出一套年付价格。

**Multilogin 的免费资源：** 价格页的 5 个配置覆盖云手机与浏览器；一次性代理流量和移动分钟没有按每月赠送登记。页面对 API 与团队权限的呈现不够一致，自动化任务按对应付费档进一步选择，CSV 不给免费档补上 API 权限。

**动态价格与图标：** 数量选择器未固定的金额，不记为唯一成交价；功能表中只有图标、缺少可识别权限文字的项目，留空而不推断免费包含。

## 记录范围

本轮完成公开页面与链接核验，没有登录上述产品账号进行并发、稳定性、封号率或客服响应测试。规划中的工作量例子属于套餐数字的计算示例。

[使用说明](START_HERE.md) · [查看套餐 CSV](data/browser-plans.csv) · [结构化事实包](data/product-facts.json)

## 结构与搜索研究来源

- S01：[BitBrowser 国际站价格](https://www.bitbrowser.net/price)，核验快照 2026-10-27。
- S02：[BitBrowser 中国站价格](https://www.bitbrowser.cn/price)，核验快照 2026-10-27。
- S03：[BitBrowser 下载](https://www.bitbrowser.cn/download)，核验快照 2026-10-27。
- S04：[BitBrowser 代理设置](https://www.bitbrowser.cn/proxy-setting)，核验快照 2026-10-27。
- S05：[BitBrowser Local API](https://www.bitbrowser.cn/local-api)，核验快照 2026-10-27。
- S06：[BitBrowser MCP 教程](https://www.bitbrowser.cn/news/how-to-configure-bitbrowser-mcp)，核验快照 2026-10-27。
- S07：[AdsPower 价格](https://www.adspower.com/pricing)，核验快照 2026-10-27。
- S08：[AdsPower Local API](https://help.adspower.com/docs/api)，核验快照 2026-10-27。
- S09：[AdsPower RPA](https://help.adspower.com/docs/rpa)，核验快照 2026-10-27。
- S10：[GoLogin 价格](https://gologin.com/pricing/)，核验快照 2026-10-27。
- S11：[GoLogin 套餐帮助](https://support.gologin.com/en/articles/14617029-pricing)，核验快照 2026-10-27。
- S12：[GoLogin 安装与系统](https://support.gologin.com/en/articles/3452486-supported-platforms-installation)，核验快照 2026-10-27。
- S13：[GoLogin API](https://gologin.com/docs/api-reference/introduction/quickstart)，核验快照 2026-10-27。
- S14：[MoreLogin 价格](https://www.morelogin.com/pricing)，核验快照 2026-10-27。
- S15：[MoreLogin 产品](https://www.morelogin.com/)，核验快照 2026-10-27。
- S16：[ixBrowser 价格](https://ixbrowser.com/pricing)，核验快照 2026-10-27。
- S17：[ixBrowser 产品](https://ixbrowser.com/en)，核验快照 2026-10-27。
- S18：[Incogniton 价格](https://incogniton.com/pricing/)，核验快照 2026-10-27。
- S19：[Dolphin Anty 套餐帮助](https://docs.dolphin-anty.com/en/personal-cabinet/plans-in-dolphin-anty)，核验快照 2026-10-27。
- S20：[Dolphin Anty 价格](https://dolphin-anty.com/tarifs/)，核验快照 2026-10-27。
- S21：[Dolphin Anty 环境限制](https://docs.dolphin-anty.com/en/working-with-profiles/restrictions-on-working-with-profiles-in-dolphin-anty)，核验快照 2026-10-27。
- S22：[Dolphin Anty 自动化](https://docs.dolphin-anty.com/en/api/basic-automation-dolphin-anty)，核验快照 2026-10-27。
- S23：[Multilogin 价格与 FAQ](https://multilogin.com/pricing/)，核验快照 2026-10-27。
- S24：[Multilogin 系统要求](https://multilogin.com/help/en_US/minimum-system-requirements)，核验快照 2026-10-27。

- [Google 高质量评测建议](https://developers.google.com/search/docs/specialty/ecommerce/write-high-quality-reviews)
- [Google 链接建议](https://developers.google.com/search/docs/crawling-indexing/links-crawlable)
- [最初参考仓库](https://github.com/pukaranda1/zhiwenliulanqi)
- [资源型仓库](https://github.com/zhaotoday/fingerprint-browser)
- [目录型仓库](https://github.com/fingerprint-browser-guide/fingerprint-browser)
- [厂商比较内容样本](https://www.adspower.net/blog/fingerprint-browser-comparison)
- [免费目录内容样本](https://fingerbrowser.com/zh/browsers/free)
