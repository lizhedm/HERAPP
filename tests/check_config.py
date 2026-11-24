#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""校验配置项清单与代码结构的键名集合一致。

技术方案 6.4 把「配置项散落在代码里」列为功能增长期的四个混乱根因之一，
对策是全部可配置项集中在 AppConfig 与 UserPreference，清单维护在
docs/config-reference.md。清单落后于代码时，排查问题的人会按清单去找
不存在的配置项，或漏掉实际生效的配置项，两种情形都会浪费排查时间。

本脚本解析清单表格，与两个结构的 Dart 定义逐一对照。清单新增而代码未跟进、
代码新增而清单未记录，两个方向都会报错。

结构文件尚未实现时只校验清单自身的完整性并通过，使本检查可在开发第一天接入 CI。
清单自身的校验包含：键名唯一、五列齐备、生效时机取值合法、需求章节已填。

只依赖标准库，Python 3.9 可运行。
"""

from __future__ import annotations

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DOC = os.path.join(ROOT, "docs", "config-reference.md")
SNAPSHOT = os.path.join(HERE, "config_snapshot.json")

# 两个结构的 Dart 定义位置。字段以 `final <类型> <名称>;` 声明。
STRUCTS = {
    "AppConfig": os.path.join(ROOT, "packages", "ling_app", "lib", "data", "config", "app_config.dart"),
    "UserPreference": os.path.join(ROOT, "packages", "ling_app", "lib", "data", "config", "user_preference.dart"),
}

VALID_TIMING = {"启动", "即时", "下次同步", "下次进入月视图", "下次进入趋势页", "下次进入日详情"}

errors: list = []


def parse_doc() -> dict:
    """解析清单中的表格行。表格行格式为 | `键名` | 类型 | 默认值 | 取值范围 | 生效时机 | 需求 |"""
    entries = {}
    section = ""
    for lineno, line in enumerate(open(DOC, encoding="utf-8"), 1):
        line = line.rstrip("\n")
        if line.startswith("##"):
            section = line.lstrip("# ").strip()
            continue
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) != 6 or cells[0] in ("键名", "---") or set(cells[0]) == {"-"}:
            continue
        key = cells[0].strip("`")
        if not key:
            continue
        if key in entries:
            errors.append(f"清单第 {lineno} 行 键名 {key} 重复")
            continue
        entry = {
            "section": section,
            "type": cells[1],
            "default": cells[2],
            "range": cells[3],
            "timing": cells[4],
            "requirement": cells[5],
        }
        for field in ("type", "default", "timing", "requirement"):
            if not entry[field] or entry[field] == "—":
                errors.append(f"清单第 {lineno} 行 {key} 的「{field}」为空")
        if entry["timing"] not in VALID_TIMING:
            errors.append(
                f"清单第 {lineno} 行 {key} 的生效时机 {entry['timing']!r} 不在允许取值内"
            )
        entries[key] = entry
    return entries


def parse_struct(path: str) -> list:
    """取 Dart 类中的 final 字段名。"""
    text = open(path, encoding="utf-8").read()
    text = re.sub(r"//[^\n]*", "", text)
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    return re.findall(r"final\s+[\w<>?,\s]+?\s+(\w+)\s*;", text)


def compare(doc_keys: set, struct: str, path: str, prefix: str) -> None:
    actual = set(parse_struct(path))
    expected = {k[len(prefix):] if prefix and k.startswith(prefix) else k for k in doc_keys}
    for name in sorted(expected - actual):
        errors.append(f"{struct} 缺少字段 {name}，docs/config-reference.md 已记录")
    for name in sorted(actual - expected):
        errors.append(f"{struct} 的字段 {name} 未记录在 docs/config-reference.md")


def main() -> int:
    if not os.path.exists(DOC):
        print(f"配置项清单缺失: {os.path.relpath(DOC, ROOT)}")
        return 1

    entries = parse_doc()
    groups = {}
    for key in entries:
        groups.setdefault(key.split(".")[0] if "." in key else "UserPreference", []).append(key)

    print(f"  配置项清单 {len(entries)} 项，{len(groups)} 个分组")
    for group in sorted(groups):
        print(f"    {group} {len(groups[group])} 项")

    for struct, path in STRUCTS.items():
        if not os.path.exists(path):
            print(f"  {os.path.relpath(path, ROOT)} 尚未实现，跳过该结构的对照")
            continue
        if struct == "AppConfig":
            # AppConfig 的键名带分组前缀，嵌套结构的字段名取分组名。
            compare(set(groups), struct, path, "")
        else:
            compare(set(groups.get("UserPreference", [])), struct, path, "")

    if errors:
        print("\n配置项校验失败:")
        for item in errors:
            print(f"  - {item}")
        return 1

    snapshot = {
        "$comment": "由 tests/check_config.py 从 docs/config-reference.md 生成。"
                    "断言默认值的测试读取本文件，使默认值有单一出处。",
        "entries": entries,
    }
    open(SNAPSHOT, "w", encoding="utf-8").write(
        json.dumps(snapshot, ensure_ascii=False, indent=1) + "\n"
    )
    print("\n配置项校验通过。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
