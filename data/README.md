# 数据文件

| 文件 | 用途 |
|---|---|
| [catalog.json](catalog.json) | 套餐、免费权限与资料来源的维护入口 |
| [catalog.schema.json](catalog.schema.json) | JSON Schema 2020-12 数据格式 |
| [browser-plans.csv](browser-plans.csv) | 由数据源生成的完整套餐表 |
| [browser-plans.json](browser-plans.json) | 与 CSV 对应的结构化导出 |
| [page-metadata.json](page-metadata.json) | 页面标题与摘要，供后续静态站部署使用 |

`site` 区分中国站与国际资料，`amount` / `currency` / `billing_period` 保留原币种与付款周期。动态报价的金额为 `null`，年付金额记录整年账单。

`api`、`rpa`、`sync` 分别取 `true`（包含）、`false`（明确不含）或 `null`（未核实）。成员字段保留“员工”“团队席位”“总用户”等原始口径。

`checked_at` 是资料日期，导出中的 `next_review_at` 按 45 天复核间隔计算。`confidence` 为资料状态，`conflict_note` 保存官方页面之间的差异，不是产品质量评分。

来源记录包含官网入口和文档名称。每次数据提交保留在 Git 历史中，可比较前后版本；这些导出文件是结构化摘录。

运行方式见[贡献说明](../CONTRIBUTING.md)。
