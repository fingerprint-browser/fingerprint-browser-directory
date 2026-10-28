# 更新数据与提交更正

欢迎补充官方价格变动、免费额度和功能权限。请提供具体官方页面及资料日期；界面截图如含账户资料，请先遮挡。

## 修改套餐数据

1. 修改 `data/catalog.json` 中对应产品、套餐与来源记录。
2. 安装校验依赖：`python -m pip install -r requirements-dev.txt`。
3. 运行 `python scripts/build.py` 同步生成表格和导出文件。
4. 运行 `python scripts/build.py --check` 与 `python -m unittest discover -s tests`。

生成区块由 `BEGIN GENERATED` / `END GENERATED` 注释标记。产品介绍、比较判断和使用步骤直接编辑正文；价格或额度改变时，一并检查引用该数据的叙述。

## 核对来源

优先使用官网价格页、功能表与帮助中心；动态报价应给出环境数、成员数和付款周期。`null` 表示未核实，不能改成 `false` 来代表不支持。

比特外部链接统一使用已登记的推广入口，付费套餐仅展示中国站 50 窗口档。收录与推荐方式见 [METHODOLOGY.md](METHODOLOGY.md)。

提交价格更正可使用仓库 Issues 的“价格或额度更正”表单；新增产品请说明免费条件和对应官方资料。

[返回总览](README.md)
