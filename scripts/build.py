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
    suffix = "个混合配置" if plan["profile_scope"] == "cloud_mobile_and_browser" else "个环境"
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


def quotas(plan: dict) -> str:
    values = []
    if plan["create_limit"] is not None:
        prefix = "每日" if plan["create_period"] == "day" else "每自然月"
        values.append(f"{prefix}创建 {plan['create_limit']:,} 个")
    if plan["open_limit"] is not None:
        values.append(f"每日打开 {plan['open_limit']:,} 次")
    if plan["recreation_limit"] is not None:
        values.append(f"每自然月重建 {plan['recreation_limit']:,} 次")
    if plan["monthly_additional_create"] is not None:
        values.append(f"月追加创建/打开 {plan['monthly_additional_create']:,}/{plan['monthly_additional_open']:,} 次")
    return "；".join(values)


def permissions(plan: dict) -> str:
    included = [name for key, name in [("api", "API"), ("rpa", "RPA"), ("sync", "同步器")] if plan[key] is True]
    excluded = [name for key, name in [("api", "API"), ("rpa", "RPA"), ("sync", "同步器")] if plan[key] is False]
    text = []
    if included:
        text.append("含 " + "、".join(included))
    if excluded:
        text.append("不含 " + "、".join(excluded))
    return "；".join(text)


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


def render_outputs(data: dict, root: Path) -> dict[str, str]:
    products = ordered_products(data)
    outputs = {}
    overview, free_rows, automation = [], [], []
    records = []
    for product in products:
        free = get_free(product)
        featured = next(p for p in product["plans"] if p["id"] == product["featured_plan"])
        link = f"[{product['name']}]({product['detail_path']})"
        member_label = free["users_label"] if free["users_label"] != "未登记" else ""
        free_summary = "；".join(filter(None, [profiles(free), quotas(free), member_label, resources(free)]))
        if free["trial_days"]:
            free_summary += f"；另有 {free['trial_days']} 天试用"
        paid_summary = "中国站 " if featured["site"] == "cn" else ""
        paid_summary += f"{featured['name']}：{price(featured)}"
        if product["price_note"]:
            paid_summary += f"（{product['price_note']}）"
        if product["id"] == data["preferred_product"]:
            link = f"**{link}**"
            paid_summary = f"**{paid_summary}**"
        overview.append([link, free_summary, paid_summary, product["summary"]])
        guide_link = f"[{product['name']}](../{product['detail_path']})"
        free_rows.append([guide_link, profiles(free), quotas(free) or "官方未单列", free["users_label"], permissions(free) or "权限未登记"])
        labels = {True: "包含", False: "不含", None: "未登记"}
        automation.append([f"[{product['name']}]({product['detail_path']})", profiles(free), labels[free["api"]], labels[free["rpa"]], labels[free["sync"]]])
        plan_rows = []
        for plan in product["plans"]:
            trial = f"另有 {plan['trial_days']} 天试用" if plan["trial_days"] else ""
            notes = "；".join(filter(None, [quotas(plan), permissions(plan), resources(plan), trial, plan["conditions"], plan["conflict_note"]])) or "—"
            site = "中国站" if plan["site"] == "cn" else "国际资料"
            plan_rows.append([plan["name"], profiles(plan), plan["users_label"], f"{price(plan)}（{site}）", notes])
            sources = [s for s in product["sources"] if s["id"] in plan["source_ids"]]
            record = dict(product_id=product["id"], product=product["name"], **plan)
            record["official_url"] = product["official_url"]
            record["source_documents"] = "；".join(s["document"] for s in sources)
            record["next_review_at"] = next_review(data, plan["checked_at"])
            records.append(record)
        detail_path = product["detail_path"]
        detail = (root / detail_path).read_text(encoding="utf-8")
        plan_table = table(["套餐", "保存环境数", "成员或员工", "价格与付款周期", "额度与功能说明"], plan_rows)
        outputs[detail_path] = replace_block(detail, f"plans:{product['id']}", plan_table)
    outputs["README.md"] = replace_block((root / "README.md").read_text(encoding="utf-8"), "overview", table(["产品详情", "长期免费额度", "付费方案参考（原币种）", "主要功能与特点"], overview))
    guide = "guides/best-free-fingerprint-browsers.md"
    outputs[guide] = replace_block((root / guide).read_text(encoding="utf-8"), "free-comparison", table(["产品详情", "免费保存数量", "操作次数", "成员或席位", "免费自动化入口"], free_rows))
    outputs["FEATURES.md"] = replace_block((root / "FEATURES.md").read_text(encoding="utf-8"), "free-automation", table(["产品详情", "长期免费环境", "API", "RPA", "同步器"], automation))
    by_id = {product["id"]: product for product in products}
    bit = by_id["bitbrowser"]
    bit_free = get_free(bit)
    bit_paid = next(p for p in bit["plans"] if p["id"] == bit["featured_plan"])
    for rival_id in ["adspower", "gologin"]:
        rival = by_id[rival_id]
        rival_free = get_free(rival)
        rival_paid = next(p for p in rival["plans"] if p["id"] == rival["featured_plan"])
        rows = [
            ["长期免费环境", profiles(bit_free), profiles(rival_free)],
            ["免费操作额度", quotas(bit_free), quotas(rival_free) or "官方未单列日操作上限"],
            ["免费成员", bit_free["users_label"], rival_free["users_label"]],
            ["免费自动化入口", permissions(bit_free), permissions(rival_free) or "按当前套餐核对"],
        ]
        path = f"comparisons/bitbrowser-vs-{rival_id}.md"
        text = (root / path).read_text(encoding="utf-8")
        if rival_id == "adspower":
            rows.append(["付费入门", f"中国站 {price(bit_paid)}，{profiles(bit_paid)}、{bit_paid['users_label']}", price(rival_paid)])
            rows.append(["限时试用", "本文比较长期免费档", f"另有 {rival_free['trial_days']} 天完整功能试用"])
            text = replace_block(text, "compare:adspower", table(["对比项", "比特浏览器", rival["name"]], rows))
        else:
            text = replace_block(text, "compare:gologin:free", table(["免费档对比", "比特浏览器", rival["name"]], rows))
            paid_rows = [
                ["标价与付款周期", f"中国站 {price(bit_paid)}", price(rival_paid)],
                ["保存环境", profiles(bit_paid), profiles(rival_paid)],
                ["成员或员工", bit_paid["users_label"], rival_paid["users_label"]],
                ["自动化入口", permissions(bit_paid), permissions(rival_paid)],
                ["其他条件", bit_paid["conditions"], rival_paid["conditions"]],
            ]
            text = replace_block(text, "compare:gologin:paid", table(["付费入门档", "比特浏览器 50 窗口档", "GoLogin Professional 10"], paid_rows))
        outputs[path] = text
    source_rows = []
    for product in products:
        for source in product["sources"]:
            plans = [p for p in product["plans"] if source["id"] in p["source_ids"]]
            facts = []
            for plan in plans:
                text = f"{plan['name']}：{profiles(plan)}，{price(plan)}，{plan['users_label']}"
                if quotas(plan):
                    text += "，" + quotas(plan)
                if plan["conflict_note"]:
                    text += "；" + plan["conflict_note"]
                facts.append(text)
            entry = f"[官方入口]({source['official_url']}) · {source['document']}"
            source_rows.append([product["name"], entry, "；".join(facts), source["checked_at"]])
    outputs["SOURCES.md"] = ("# 产品资料与官方入口\n\n" + table(["产品", "官方资料", "已登记套餐与额度", "资料日期"], source_rows)
        + f"\n\n建议下次复核：{next_review(data, data['checked_at'])}。\n\n[收录与推广说明](METHODOLOGY.md) · [结构化数据](data/catalog.json) · [套餐 CSV](data/browser-plans.csv) · [返回总览](README.md)\n")
    outputs["data/browser-plans.json"] = json.dumps(dict(schema_version=data["schema_version"], checked_at=data["checked_at"], plans=records), ensure_ascii=False, indent=2) + "\n"
    columns = ["product_id", "product", "id", "name", "site", "price_type", "profiles", "profile_scope", "users_count", "users_label", "amount", "currency", "billing_period", "trial_days", "intro_profiles", "intro_months", "create_limit", "create_period", "open_limit", "recreation_limit", "monthly_additional_create", "monthly_additional_open", "api", "rpa", "sync", "proxy_mb_once", "mobile_minutes_once", "mobile_profiles_once", "conditions", "confidence", "conflict_note", "official_url", "source_documents", "checked_at", "next_review_at"]
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=columns, lineterminator="\n", extrasaction="ignore")
    writer.writeheader()
    for record in records:
        row = {key: record[key] for key in columns}
        for key in ["api", "rpa", "sync"]:
            row[key] = {True: "true", False: "false", None: "unknown"}[row[key]]
        writer.writerow(row)
    outputs["data/browser-plans.csv"] = stream.getvalue()
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
