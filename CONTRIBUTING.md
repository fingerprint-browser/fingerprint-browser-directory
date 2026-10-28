# 更新资料

欢迎通过 Issues 提交价格、免费数量和功能变化。请提供产品名称、变更内容、官方页面和查看日期。

修改套餐时，更新 `data/catalog.json`，然后运行：

```bash
python -m pip install -r requirements-dev.txt
python scripts/build.py
python scripts/build.py --check
python -m unittest discover -s tests
```

生成表格位于 `BEGIN GENERATED` / `END GENERATED` 注释之间，正文介绍可以直接编辑。价格和额度变化后，一并检查相关正文。

接口权限为 `null` 时表示资料尚未填写，保留空值，避免与明确不支持混淆。

[返回总览](README.md)
