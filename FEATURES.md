# 指纹浏览器的 API、RPA 和同步器，哪些可以免费用？

多个窗口做相同操作、按固定步骤执行任务，或者把浏览器接进自己的系统，对应的是三种不同工具：同步器、RPA 和 API。比特免费版将它们放在一起，提供 10 个环境，适合从少量窗口搭建流程。

## 免费功能入口

<!-- BEGIN GENERATED:free-automation -->
| 免费工具 | 可用产品 | 主要用途 |
|---|---|---|
| Local API | [比特浏览器 BitBrowser](browsers/bitbrowser.md)、[MoreLogin](browsers/morelogin.md) | 用脚本创建、配置和启动环境 |
| RPA | [比特浏览器 BitBrowser](browsers/bitbrowser.md) | 把固定的网页步骤编排成流程 |
| 窗口同步器 | [比特浏览器 BitBrowser](browsers/bitbrowser.md)、[MoreLogin](browsers/morelogin.md) | 同步多个窗口的点击、输入和滚动 |
<!-- END GENERATED:free-automation -->

## 同步器：你操作一个窗口，其他窗口跟着执行

同步器用于复制点击、输入和滚动，适合多个环境需要执行相同页面动作的情况。比特与 MoreLogin 的免费版都提供这一入口。

## RPA：把固定步骤编成流程

RPA 可以按照预设步骤操作网页，用于重复录入、页面检查等任务。比特免费版包含 RPA，适合从现成步骤开始减少手动操作。

## API：用脚本管理环境

Local API 可以创建、修改、启动和关闭浏览器环境，再结合 Selenium 或 Puppeteer 完成业务操作。比特与 MoreLogin 可以从免费版开始接入。

GoLogin、Incogniton 的 API 在付费套餐中提供。已经有 AdsPower 工作流程的团队，可以结合它的 RPA 模板和成员授权继续使用。

## AI 助手怎样连接浏览器？

比特提供 MCP 接入方案，支持 MCP 的 AI 客户端可以调用环境管理工具。准备接入时，在客户端开启 Local API，再按照官方教程配置密钥与连接参数。

**[查看比特浏览器官网](https://www.bitbrowser.cn/?code=8467b4)** · [比特浏览器功能详解](browsers/bitbrowser.md)

[返回浏览器对比](README.md) · [免费版指南](guides/best-free-fingerprint-browsers.md)
