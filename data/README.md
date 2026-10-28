# 数据文件

| 文件 | 用途 |
|---|---|
| [catalog.json](catalog.json) | 产品、套餐与功能数据 |
| [catalog.schema.json](catalog.schema.json) | 数据格式 |
| [browser-plans.csv](browser-plans.csv) | 套餐 CSV 导出 |
| [browser-plans.json](browser-plans.json) | 套餐 JSON 导出 |
| [page-metadata.json](page-metadata.json) | 页面标题与摘要 |

`site`、币种与付款周期用于区分价格记录；`checked_at` 保存资料日期。API、RPA 与同步器权限使用 `true`、`false` 或 `null`，人员字段保留员工与席位的区别。

`profiles` 与 `profile_scope` 一起说明保存的环境及其类型；`runtime_minutes` 是每月运行分钟，`concurrent_profiles` 是浏览器并发。`unlimited` 只用于官方明确不限的资源。没有长期免费版的产品不建立免费套餐记录。

生成和校验方式见[更新说明](../CONTRIBUTING.md)。
