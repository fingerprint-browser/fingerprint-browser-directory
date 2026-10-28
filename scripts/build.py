#!/usr/bin/env python3
"""Validate the catalog and update the directory's generated data blocks."""

from __future__ import annotations

import argparse
import csv
from datetime import date, timedelta
import io
import json
from pathlib import Path
import re
import sys
from urllib.parse import urlparse

from jsonschema import Draft202012Validator, FormatChecker, ValidationError

ROOT = Path(__file__).resolve().parents[1]
REFERRAL = "https://www.bitbrowser.cn/?code=8467b4"


def load_catalog(root: Path) -> dict:
    data = json.loads((root / "data/catalog.json").read_text(encoding="utf-8"))
    schema = json.loads((root / "data/catalog.schema.json").read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema, format_checker=FormatChecker()).validate(data)
    validate_catalog(data, root)
    return data


def validate_catalog(data: dict, root: Path) -> None:
    products = data["products"]
    ids = [p["id"] for p in products]
    if len(ids) != len(set(ids)) or data["preferred_product"] not in ids:
        raise ValueError("Product IDs must be unique and include the preferred product")
    if data["affiliate_url"] != REFERRAL:
        raise ValueError("Unexpected BitBrowser referral URL")
    for product in products:
        detail = (root / product["detail_path"]).resolve()
        if not detail.is_relative_to(root.resolve()) or not detail.is_file():
            raise ValueError(f"Missing product detail: {product['detail_path']}")
        plans = product["plans"]
        plan_ids = [p["id"] for p in plans]
        if len(plan_ids) != len(set(plan_ids)) or product["featured_plan"] not in plan_ids:
            raise ValueError(f"Invalid plan IDs for {product['id']}")
        free = [p for p in plans if p["price_type"] == "free"]
        if len(free) != 1:
            raise ValueError(f"Expected one long-term free record for {product['id']}")
        sources = product["sources"]
        source_ids = [s["id"] for s in sources]
        if len(source_ids) != len(set(source_ids)):
            raise ValueError(f"Duplicate source IDs for {product['id']}")
        for plan in plans:
            if not set(plan["source_ids"]).issubset(source_ids):
                raise ValueError(f"Unknown source for {product['id']}/{plan['id']}")
            if plan["price_type"] == "free":
                if plan["amount"] != 0 or plan["billing_period"] != "free":
                    raise ValueError("Free plans must have zero amount and free billing")
            elif plan["price_type"] == "dynamic":
                if plan["amount"] is not None:
                    raise ValueError("Dynamic prices must not invent a fixed amount")
            elif plan["amount"] is None or plan["amount"] <= 0 or plan["currency"] is None:
                raise ValueError("Fixed or starting prices need a positive amount and currency")
            if (plan["create_limit"] is None) != (plan["create_period"] is None):
                raise ValueError("Creation quota and period must be recorded together")
            if plan["confidence"] == "source_conflict" and not plan["conflict_note"]:
                raise ValueError("Source conflicts need a note")
            date.fromisoformat(plan["checked_at"])
        if product["id"] == "bitbrowser":
            paid = [p for p in plans if p["price_type"] != "free"]
            if len(paid) != 1 or paid[0]["site"] != "cn":
                raise ValueError("BitBrowser displays one Chinese-site paid plan")
            for url in [product["official_url"], *[s["official_url"] for s in sources]]:
                if url != REFERRAL:
                    raise ValueError("All external BitBrowser entries must use the referral URL")


def cell(value: str) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def table(headers: list[str], rows: list[list[str]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "|" + "|".join(["---"] * len(headers)) + "|"]
    lines.extend("| " + " | ".join(cell(v) for v in row) + " |" for row in rows)
    return "\n".join(lines)


def ordered_products(data: dict) -> list[dict]:
    preferred = data["preferred_product"]
    return sorted(data["products"], key=lambda p: p["id"] != preferred)


def get_free(product: dict) -> dict:
    return next(p for p in product["plans"] if p["price_type"] == "free")


def profiles(plan: dict) -> str:
    if plan["profiles"] == "unlimited":
        return "保存环境不限"
    if plan["profiles"] is None:
        return "按配置选择"
    if plan["intro_profiles"] is not None:
        return f"前 {plan['intro_months']} 个月 {plan['intro_profiles']} 个，之后 {plan['profiles']} 个"
    suffix = "个配置" if plan["profile_scope"] == "cloud_mobile_and_browser" else "个环境"
    return f"{plan['profiles']} {suffix}"


def price(plan: dict) -> str:
    if plan["price_type"] == "free":
        return "免费"
    if plan["price_type"] == "dynamic":
        return "按环境、成员和周期报价"
    currency = {"CNY": "元", "USD": "美元"}[plan["currency"]]
    period = {"month": "月", "year": "年"}[plan["billing_period"]]
    text = f"{plan['amount']:g} {currency}/{period}"
    if plan["price_type"] == "starting":
        text += "起"
    return text


def resources(plan: dict) -> str:
    values = []
    if plan["proxy_mb_once"] is not None:
        values.append(f"一次性 {plan['proxy_mb_once']}MB 代理流量")
    if plan["mobile_minutes_once"] is not None:
        values.append(f"{plan['mobile_profiles_once']} 个云手机配置赠 {plan['mobile_minutes_once']} 分钟")
    return "；".join(values)


def replace_block(text: str, key: str, content: str) -> str:
    begin, end = f"<!-- BEGIN GENERATED:{key} -->", f"<!-- END GENERATED:{key} -->"
    if text.count(begin) != 1 or text.count(end) != 1:
        raise ValueError(f"Expected one pair of generated markers: {key}")
    start = text.index(begin) + len(begin)
    finish = text.index(end)
    if finish < start:
        raise ValueError(f"Reversed generated markers: {key}")
    return text[:start] + "\n" + content + "\n" + text[finish:]


def next_review(data: dict, checked_at: str) -> str:
    return (date.fromisoformat(checked_at) + timedelta(days=data["review_after_days"])).isoformat()


def readable_users(plan: dict) -> str:
    label = plan['users_label'].strip()
    return '' if label in {'未登记', '未公开', '待核对', '—'} else label


def short_quota(plan: dict) -> str:
    if plan['create_period'] == 'day' and plan['open_limit'] is not None:
        return f"每日新建 {plan['create_limit']:,} 个、打开 {plan['open_limit']:,} 次"
    if plan['create_period'] == 'calendar_month':
        return f"每月新建 {plan['create_limit']:,} 次"
    if plan['open_limit'] is not None:
        return f"每日打开 {plan['open_limit']:,} 次"
    if plan['create_limit'] is not None:
        return f"每日新建 {plan['create_limit']:,} 个"
    return ''


def included_tools(plan: dict) -> str:
    return '、'.join(name for key, name in [('api','API'),('rpa','RPA'),('sync','同步器')] if plan[key] is True)


def free_usage(plan: dict) -> str:
    if short_quota(plan):
        return short_quota(plan)
    if resources(plan):
        return resources(plan)
    if plan['intro_months']:
        return f"第 {plan['intro_months']+1} 个月起保留 {plan['profiles']} 个环境"
    if included_tools(plan):
        return '支持 ' + included_tools(plan)
    if plan['trial_days']:
        return f"另有 {plan['trial_days']} 天完整功能试用"
    return '适合少量固定账号'


def plan_table(product: dict) -> str:
    has_users = any(readable_users(p) for p in product['plans'])
    has_daily = all(p['create_period']=='day' and p['open_limit'] is not None for p in product['plans'])
    headers = ['套餐','环境数量']
    if has_users:
        headers.append('人员')
    headers.append('价格')
    if has_daily:
        headers.append('每日新建 / 打开')
    rows = []
    for plan in product['plans']:
        row = [plan['name'], profiles(plan)]
        if has_users:
            row.append(readable_users(plan))
        row.append(price(plan))
        if has_daily:
            row.append(f"{plan['create_limit']:,} / {plan['open_limit']:,} 次")
        rows.append(row)
    return table(headers, rows)


def render_outputs(data: dict, root: Path) -> dict[str, str]:
    products = ordered_products(data)
    outputs, overview, free_rows, records = {}, [], [], []
    for product in products:
        free = get_free(product)
        featured = next(p for p in product['plans'] if p['id']==product['featured_plan'])
        paid_price = price(featured)
        if product['price_note']:
            paid_price += f"（{product['price_note']}）"
        overview.append([f"[{product['name']}]({product['detail_path']})", profiles(free), paid_price, product['summary']])
        free_rows.append([f"[{product['name']}](../{product['detail_path']})", profiles(free), readable_users(free), free_usage(free)])
        member = f"，{readable_users(free)}" if readable_users(free) else ''
        card = f"> **免费版**：{profiles(free)}{member}\n>\n> **付费起价**：{paid_price}\n>\n> **常用功能**：{product['summary']}"
        detail = (root/product['detail_path']).read_text(encoding='utf-8')
        detail = replace_block(detail, 'quick:'+product['id'], card)
        outputs[product['detail_path']] = replace_block(detail, 'plans:'+product['id'], plan_table(product))
        for plan in product['plans']:
            sources = [s for s in product['sources'] if s['id'] in plan['source_ids']]
            record = dict(product_id=product['id'], product=product['name'], **plan)
            record['official_url'] = product['official_url']
            record['source_documents'] = '；'.join(s['document'] for s in sources)
            record['next_review_at'] = next_review(data,plan['checked_at'])
            records.append(record)
    outputs['README.md'] = replace_block((root/'README.md').read_text(encoding='utf-8'),'overview',table(['产品详情','长期免费环境','付费起价','常用功能'],overview))
    guide='guides/best-free-fingerprint-browsers.md'
    outputs[guide] = replace_block((root/guide).read_text(encoding='utf-8'),'free-comparison',table(['产品详情','免费环境','人数','日常使用'],free_rows))
    automation=[]
    use_cases={'api':'用脚本创建、配置和启动环境','rpa':'把固定的网页步骤编排成流程','sync':'同步多个窗口的点击、输入和滚动'}
    for key,name in [('api','Local API'),('rpa','RPA'),('sync','窗口同步器')]:
        names=[f"[{p['name']}]({p['detail_path']})" for p in products if get_free(p)[key] is True]
        if names:
            automation.append([name,'、'.join(names),use_cases[key]])
    outputs['FEATURES.md']=replace_block((root/'FEATURES.md').read_text(encoding='utf-8'),'free-automation',table(['免费工具','可用产品','主要用途'],automation))
    by_id={p['id']:p for p in products}
    bit=by_id['bitbrowser']; bit_free=get_free(bit)
    bit_paid=next(p for p in bit['plans'] if p['id']==bit['featured_plan'])
    for rival_id in ['adspower','gologin']:
        rival=by_id[rival_id]; free=get_free(rival)
        paid=next(p for p in rival['plans'] if p['id']==rival['featured_plan'])
        path=f'comparisons/bitbrowser-vs-{rival_id}.md'
        text=(root/path).read_text(encoding='utf-8')
        if rival_id=='adspower':
            rows=[['长期免费环境',profiles(bit_free),profiles(free)],['免费使用人数',readable_users(bit_free),readable_users(free)],['付费入门',price(bit_paid),price(paid)],['员工或成员',readable_users(bit_paid),readable_users(paid)]]
            text=replace_block(text,'compare:adspower',table(['对比项','比特浏览器','AdsPower'],rows))
        else:
            api_label={True:'支持',False:'需付费',None:''}
            rows=[['长期免费环境',profiles(bit_free),profiles(free)],['使用人数',readable_users(bit_free),readable_users(free)],['操作次数',short_quota(bit_free),short_quota(free)],['免费 API',api_label[bit_free['api']],api_label[free['api']]]]
            text=replace_block(text,'compare:gologin:free',table(['免费版','比特浏览器','GoLogin'],rows))
            rows=[['月费',price(bit_paid),price(paid)],['环境数量',profiles(bit_paid),profiles(paid)],['员工或成员',readable_users(bit_paid),readable_users(paid)]]
            text=replace_block(text,'compare:gologin:paid',table(['入门付费套餐','比特浏览器','GoLogin Professional 10'],rows))
        outputs[path]=text
    source_rows=[[p['name'],f"[官网与价格]({p['official_url']})"] for p in products]
    outputs['SOURCES.md']='# 产品官网与价格入口\n\n'+table(['产品','官方入口'],source_rows)+'\n\n价格与免费额度以各产品官网为准。比特浏览器链接含推广参数。\n\n[返回浏览器对比](README.md)\n'
    outputs['data/browser-plans.json']=json.dumps(dict(schema_version=data['schema_version'],checked_at=data['checked_at'],plans=records),ensure_ascii=False,indent=2)+'\n'
    columns=['product_id','product','id','name','site','price_type','profiles','profile_scope','users_count','users_label','amount','currency','billing_period','trial_days','intro_profiles','intro_months','create_limit','create_period','open_limit','recreation_limit','monthly_additional_create','monthly_additional_open','api','rpa','sync','proxy_mb_once','mobile_minutes_once','mobile_profiles_once','conditions','confidence','conflict_note','official_url','source_documents','checked_at','next_review_at']
    stream=io.StringIO(newline='')
    writer=csv.DictWriter(stream,fieldnames=columns,lineterminator='\n',extrasaction='ignore');writer.writeheader()
    for record in records:
        row={key:record[key] for key in columns}
        for key in ['api','rpa','sync']:
            row[key]={True:'true',False:'false',None:'unknown'}[row[key]]
        writer.writerow(row)
    outputs['data/browser-plans.csv']=stream.getvalue()
    return outputs


def validate_links(root: Path) -> None:
    for path in root.rglob("*.md"):
        for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", path.read_text(encoding="utf-8")):
            if target.startswith(("http://", "https://", "mailto:", "#")):
                if target.startswith(("http://", "https://")):
                    host = urlparse(target).hostname or ""
                    if (host.endswith(".bitbrowser.cn") or host.endswith(".bitbrowser.net") or host in {"bitbrowser.cn", "bitbrowser.net"}) and target != REFERRAL:
                        raise ValueError(f"Unexpected BitBrowser link in {path.relative_to(root)}")
                continue
            resolved = (path.parent / target.split("#", 1)[0]).resolve()
            if not resolved.is_relative_to(root.resolve()) or not resolved.is_file():
                raise ValueError(f"Broken internal link: {path.relative_to(root)} -> {target}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Report generated files that need updating")
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    root = args.root.resolve()
    try:
        data = load_catalog(root)
        expected = render_outputs(data, root)
        changed = [name for name, text in expected.items() if not (root / name).exists() or (root / name).read_text(encoding="utf-8") != text]
        if args.check and changed:
            print("Generated files need updating: " + ", ".join(changed), file=sys.stderr)
            return 1
        if not args.check:
            for name, text in expected.items():
                (root / name).write_text(text, encoding="utf-8")
        validate_links(root)
        stale = [p["id"] for product in data["products"] for p in product["plans"] if date.today() > date.fromisoformat(next_review(data, p["checked_at"]))]
        if stale:
            print(f"Warning: {len(stale)} plan records are due for review", file=sys.stderr)
        count = sum(len(p["plans"]) for p in data["products"])
        print(f"Validated {len(data['products'])} products, {count} plans and all internal links; generated files {'match' if args.check else 'updated'}.")
        return 0
    except (ValueError, KeyError, OSError, ValidationError) as error:
        print(str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
