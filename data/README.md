# 数据文件

| 文件 | 用途 |
|---|---|
| [catalog.json](catalog.json) | 产品、套餐与功能数据 |
| [catalog.schema.json](catalog.schema.json) | 数据格式 |
| [browser-plans.csv](browser-plans.csv) | 套餐 CSV 导出 |
| [browser-plans.json](browser-plans.json) | 套餐 JSON 导出 |
| [page-metadata.json](page-metadata.json) | 页面标题与摘要 |

`site`、币种与付款周期用于区分价格记录；`checked_at` 保存资料日期。API、RPA 与同步器权限使用 `true`、`false` 或 `null`，人员字段保留员工与席位的区别。

生成和校验方式见[更新说明](../CONTRIBUTING.md)。
