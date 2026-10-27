# Dolphin Anty 免费版有几个环境？3 个与 5 个的资料差异

如果你在搜索 Dolphin Anty 的免费版额度，很可能会在官方渠道看到两个互相冲突的数字：有的页面写免费 3 个环境，有的表格却写着 5 个。截至 2026-10-27 核验时，官方套餐帮助与价格页部分表格的记载确实不同。

同时，官方资料中还有一项“每月 20 次重建（Recreations）”的限制，经常被初次接触的读者误当成“可保存 20 个环境”或“每天能建 20 个”。下面分别说明免费名额、重建次数和付费档位，其他产品见[对比总览](../README.md)。

## 为什么官方资料里同时出现 3 个和 5 个免费环境？

套餐帮助与价格页对免费名额的记载如下：

| 官方资料位置 | 免费版环境数量记载 | 附加额度记载 | 核验日期与采用建议 |
|---|---|---|---|
| [官方套餐帮助文档（Plans in Dolphin Anty）](https://docs.dolphin-anty.com/en/personal-cabinet/plans-in-dolphin-anty) 及官网页尾 | **3 个浏览器环境** | 每月 20 次重建额度 | 2026-10-27 核验；说明更具体，本目录以此作为基准规划值 |
| [官方环境限制帮助文档](https://docs.dolphin-anty.com/en/working-with-profiles/restrictions-on-working-with-profiles-in-dolphin-anty) | 配合免费配额说明重建规则 | 每月 20 次重建额度 | 2026-10-27 核验；解释删除与重建的触发关系 |
| [官网价格页（Tarifs）部分功能表](https://dolphin-anty.com/tarifs/) | 部分功能对比表仍显示 **5 个环境** | 页尾及帮助页为 3 个 | 2026-10-27 核验；与套餐帮助和页尾的记载不同 |

面对这种官方页面内部的冲突，最稳妥的选型原则是：**按更严格的最新套餐帮助文档（3 个环境）来做业务规划**。

- 如果你的日常任务只需要 1～3 个固定环境，那么无论实际后台按 3 个还是 5 个执行，你都能稳妥控制在免费范围内。
- 如果你恰好需要 4～5 个长期环境，应先核对当前账号的实际配额。已有账号可在客户端个人中心（Personal Cabinet）的套餐界面查看配额，或者参考 [免费额度口径说明](../guides/best-free-fingerprint-browsers.md) 挑选名额明确在 5 个及以上的产品。

## 每月 20 次“重建额度（Recreations）”到底限制什么？

在[Dolphin Anty 套餐帮助](https://docs.dolphin-anty.com/en/personal-cabinet/plans-in-dolphin-anty)与[环境限制说明文档](https://docs.dolphin-anty.com/en/working-with-profiles/restrictions-on-working-with-profiles-in-dolphin-anty)中，免费版除了同时保存 3 个环境的上限外，还规定了 **每自然月 20 次重建额度**。理解这个指标要避开三个常见误区：

1. **重建次数 ≠ 可同时保存的环境总数**：哪怕你当月还有 20 次重建额度，你列表里同时留存的环境最多也只有 3 个（按帮助文档口径）。
2. **重建次数 ≠ 每日新建额度**：20 次是按月（每自然月）统计的配额，不是每天 20 次。
3. **单纯“删除动作”本身不等于一次重建**：根据[环境限制文档](https://docs.dolphin-anty.com/en/working-with-profiles/restrictions-on-working-with-profiles-in-dolphin-anty)，当你把免费名额用满后，删掉旧环境并再次创建新环境的循环替换过程会消耗当月的重建额度。一旦当月 20 次重建配额用尽，即使你把现有环境删掉，在该月剩余时间内也无法再创建新环境来填补空位。

换句话说，Dolphin Anty 的免费版允许你每个月对这 3 个环境位置进行最多 20 次的“删旧建新”轮换，适合偶尔更换测试配置的用户，但不适合每天都要批量销毁并新建几十个临时环境的场景。

## Cookie 导出、云同步、自动化与付费档位价格

除了环境数量限制，免费版在数据导出与团队协作上也有功能边界。根据[官方套餐帮助文档](https://docs.dolphin-anty.com/en/personal-cabinet/plans-in-dolphin-anty)与[官网价格页](https://dolphin-anty.com/tarifs/)，升级付费档位主要带来以下能力与容量变化：

- **Starter 档（20～60 个环境）**：[套餐帮助文档](https://docs.dolphin-anty.com/en/personal-cabinet/plans-in-dolphin-anty)介绍了包含 20 至 60 个环境的 Starter 档位，并明确指出升级后将增加 **Cookie 导出**、**云同步** 等在免费档受限的能力。套餐帮助同时列出 **Starter 20 为 10 美元/月起**，更高环境数量按所选档位核价。
- **Base 档（100 个环境，89 美元/月）**：根据[官网价格页](https://dolphin-anty.com/tarifs/)，Base 档公开月付标价为 **89 美元/月**，包含 100 个浏览器环境；如需添加额外团队成员，需按人数配置另行核算费用。
- **Team 档（300 个环境，159 美元/月）**：公开月付标价为 **159 美元/月**，包含 300 个浏览器环境，适合较大规模的多人团队（额外成员同样按配置核算）。
- **基础自动化接口**：官方提供了[Dolphin Anty 基础自动化文档（Basic Automation）](https://docs.dolphin-anty.com/en/api/basic-automation-dolphin-anty)，说明如何通过本地端口启动环境并对接自动化工具。依赖脚本时，需要把接口权限与环境数量一起核对，不能仅按保存名额决定方案。

## Dolphin Anty 适合哪些使用量？

- **适合用免费版试水**：个人维护 1～3 个浏览器环境，每月更换重建环境的次数在 20 次以内，且暂时不需要导出 Cookie 或多人共享。
- **适合考虑 Starter / Base / Team 付费档**：习惯 Dolphin Anty 的界面与环境管理逻辑，业务规模达到 20～300 个环境，且明确需要云同步、Cookie 导出或接入[官方基础自动化接口](https://docs.dolphin-anty.com/en/api/basic-automation-dolphin-anty)。
- **如果觉得 89 美元/月（100 环境）超出预算**：可以返回 [8 产品比较](../README.md)，对比同样在 50～100 个环境规模下月费在几十元人民币或 10～30 美元区间的其他商业方案。

---

[返回产品对比总览](../README.md) · [官方来源](../SOURCES.md)
