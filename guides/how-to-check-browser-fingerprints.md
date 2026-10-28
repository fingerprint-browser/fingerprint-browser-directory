# 浏览器指纹怎么检测？6 个工具与结果阅读方法

新建环境或换代理后，先检查网站实际收到的 IP 和浏览器参数，再保存为日常工作环境。建议在需要检查的浏览器环境里直接打开检测页，这样结果才能对应当前环境。

## 6 个检测工具分别看什么？

| 工具 | 适合查看 | 入口 |
|---|---|---|
| BrowserLeaks | IP、WebRTC、Canvas、WebGL、字体与请求信息 | [BrowserLeaks](https://browserleaks.com/) |
| ToDetect | IP、DNS/WebRTC 泄漏、Canvas、WebGL、时区与语言 | [ToDetect](https://www.todetect.net/) |
| CreepJS | 浏览器特征、参数一致性与 JavaScript 修改痕迹 | [官方检测页](https://abrahamjuliot.github.io/creepjs/) |
| Pixelscan | 通过交互页面查看浏览器与网络检测结果 | [Pixelscan](https://pixelscan.net/) |
| AmIUnique | 当前指纹在其样本中的特征分布与独特程度 | [AmIUnique](https://amiunique.org/) |
| Cover Your Tracks | 浏览器追踪保护与指纹识别相关表现 | [EFF 检测页](https://coveryourtracks.eff.org/) |

ToDetect 适合在同一页面集中查看网络出口与浏览器特征。打开首页后，可以继续进入 DNS、WebRTC、Canvas 等检测模块，核对代理、时区、语言和图形信息。

## 第一步：确认网络出口

打开 [BrowserLeaks IP 页面](https://browserleaks.com/ip)，查看 IP、国家或地区、运营商以及请求头。把结果与代理服务提供的出口信息相互对应。城市定位数据库可能有差异，首先核对实际 IP 和预期地区。

如果结果仍是原来的网络出口，回到客户端查看当前环境绑定的代理，再确认启动的是修改后的环境。代理用户名、端口或白名单有变化时，也要先保存后重新打开。

## 第二步：单独查看 WebRTC

打开 [WebRTC 页面](https://browserleaks.com/webrtc)，重点看公网候选地址是否出现额外的真实网络出口。以 192.168、10 等开头的局域网地址与真实公网 IP 含义不同，浏览器还可能使用 mDNS 名称代替本地地址。

遇到额外公网出口时，回到该环境的 WebRTC 设置调整网络策略，再重开环境复查。不同客户端的模式名称不同，可以在详情或帮助页中查找对应设置。

## 第三步：核对系统、语言和渲染信息

在 BrowserLeaks、CreepJS 或 ToDetect 中查看系统、浏览器、时区、语言、屏幕、Canvas 和 WebGL。先确认系统类型、浏览器类型与自己的环境配置对应，再检查是否存在明显的参数错配。

Canvas 哈希值用于概括该页面的绘制结果，单个哈希没有统一的“安全值”。检查时更有用的是保留当前环境的配置，关闭再重开后比较结果，以及确认不同环境的 Cookie 和代理没有串用。

## 唯一性、一致性和泄漏分别代表什么？

| 结果 | 应怎样阅读 |
|---|---|
| Unique / 唯一性 | 与该工具已有样本进行比较，反映特征组合的独特程度 |
| 参数一致性 | 浏览器、系统、图形与语言等信息是否出现明显矛盾 |
| WebRTC / IP 泄漏 | 网络检查是否看见了预期代理以外的公网出口 |
| 登录状态保存 | 关闭再打开环境后，站点会话是否继续保留 |

这些结果回答的是不同问题。整理环境时，可以记录环境名称、检查时间、出口 IP 和需要调整的项目，方便以后更换代理或迁移电脑时复查。截图中的账号、代理密码和 API 密钥应隐藏后再分享。

## 怎样用于日常环境管理？

在比特浏览器中，先给环境配置代理，再从对应窗口打开上述工具；检查后继续使用同一环境保存账号状态。需要多窗口重复操作时，再接入[同步器、RPA 或 API](../FEATURES.md)。代理连接本身有问题，可先看[代理配置与排查](how-to-configure-proxy.md)。

相关说明：[BrowserLeaks 工具介绍](https://browserleaks.com/) · [CreepJS 项目](https://github.com/abrahamjuliot/creepjs) · [EFF 追踪原理](https://coveryourtracks.eff.org/learn)


[首页](../README.md) · [产品目录](../browsers/README.md) · [全部对比](../comparisons/README.md) · [入门与配置](../guides/README.md)
