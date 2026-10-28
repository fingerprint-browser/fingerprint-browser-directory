# Octo Browser 怎么选套餐？Lite、Base、API 与团队环境

<!-- BEGIN GENERATED:quick:octo-browser -->
> **免费版**：无长期免费版
>
> **付费起价**：10 欧元/月
>
> **常用功能**：标签、代理与 Cookie 管理；API 从 Base 档开放
<!-- END GENERATED:quick:octo-browser -->

Octo Browser 将浏览器环境、代理、Cookie、标签与文件夹集中管理。它按订阅提供环境资源，Lite 适合少量手动操作；需要 API 时，从 Base 档开始比较。

## Lite 与 Base 的区别

<!-- BEGIN GENERATED:plans:octo-browser -->
| 套餐 | 环境数量 | 人员 | 价格 |
|---|---|---|---|
| Lite | 3 个环境 | 1 人 | 10 欧元/月 |
| Base | 100 个环境 | 1 人 | 79 欧元/月 |
<!-- END GENERATED:plans:octo-browser -->

Lite 提供 3 个环境，不包含 API 和跨账号环境转移。Base 基础资源为 100 个环境，开放 API 和环境转移，可以另购环境数量。先确定是否要接入脚本，再选择档位，会比只按最少环境数选择更直接。

订阅使用账户代币结算：充值时 1 token 对应 1 欧元，Lite 为 10 tokens，Base 为 79 tokens，每个订阅周期为 30 天。表中按对应欧元金额列出，额外环境和成员另购。

## API 怎样接入已有脚本？

API 可以管理环境、代理、标签和文件夹，启动环境后接入 Playwright、Puppeteer、Selenium 或 CDP。Base 的限额为每分钟 50 次、每小时 500 次请求；创建与关闭环境的管理请求也要纳入工作流程。

一次性环境适合无需长期保存状态的任务。长期登录环境则继续复用原配置，脚本结束后关闭窗口，保留后续需要的数据。接口入口见[官方 API 文档](https://docs.octobrowser.net/en/api/start-api/)。

## 系统和环境整理

客户端支持 Windows、macOS 和 Linux，系统要求见[官方说明](https://docs.octobrowser.net/en/start/system-requirements/)。多人维护时，标签用于标注项目，文件夹用于组织环境，再结合成员权限安排访问范围。

如果主要是 Windows 或 Mac 上的个人多窗口操作，希望先免费使用 API、RPA 和同步器，可以比较[比特浏览器](bitbrowser.md)；需要 Octo 的环境组织与既有脚本接口时，则按 Base 和团队资源选择。

[Octo Browser 官网](https://octobrowser.net/) · [套餐资源](https://docs.octobrowser.net/en/payments/subscriptions/) · [代币与支付](https://docs.octobrowser.net/en/start/account-settings/)


[首页](../README.md) · [产品目录](../browsers/README.md) · [全部对比](../comparisons/README.md) · [入门与配置](../guides/README.md)
