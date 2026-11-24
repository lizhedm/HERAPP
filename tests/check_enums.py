#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""校验代码中的枚举成员与需求文档 14 章一致。

技术方案 6.3 把「新增枚举值遗漏分支」列为功能增长期的四个混乱根因之一，
对策是让需求文档 14 章成为枚举的唯一事实来源，代码偏离即构建失败。

本脚本解析 14 章的 28 个枚举，与 packages/ling_core/lib/src/enums.dart 的
定义逐一对照。文档新增成员而代码未跟进、代码新增成员而文档未记录，
两个方向都会报错，使文档与代码无法单边漂移。

enums.dart 尚未实现时只输出文档侧清单并通过，使本检查可在开发第一天接入 CI，
随 enums.dart 落地自动转为双向对照。

只依赖标准库，Python 3.9 可运行。
"""

from __future__ import annotations

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
REQ_DOC = os.path.join(ROOT, "需求文档V1.1.md")
ENUMS_DART = os.path.join(ROOT, "packages", "ling_core", "lib", "src", "enums.dart")
SNAPSHOT = os.path.join(HERE, "enum_snapshot.json")

# 14 章的枚举节标题格式为「### 14.n 中文名 EnglishName」，成员列于其后第一段的首句。
SECTION = re.compile(r"^### (14\.\d+) (\S+) (\w+)\n\n(.+?)(?=\n\n)", re.M | re.S)
DART_ENUM = re.compile(r"enum\s+(\w+)\s*\{(.*?)\}", re.S)

errors: list = []


def dedupe(items: list) -> list:
    out = []
    for item in items:
        if item not in out:
            out.append(item)
    return out


def parse_requirements() -> dict:
    """解析 14 章。成员以反引号标识时取反引号内容，否则按顿号切分中文枚举。"""
    text = open(REQ_DOC, encoding="utf-8").read()
    enums = {}
    for section, cn_name, en_name, body in SECTION.findall(text):
        head = body.split("。")[0]
        ticked = dedupe(re.findall(r"`([^`]+)`", head))
        if ticked:
            members = ticked
        else:
            members = [p.strip() for p in head.replace("内置：", "").split("、") if p.strip()]
        enums[en_name] = {"section": section, "cnName": cn_name, "members": members}
    return enums


def parse_dart() -> dict:
    """解析 enums.dart。只取成员名，忽略注释、尾随逗号与成员上的构造参数。"""
    text = open(ENUMS_DART, encoding="utf-8").read()
    text = re.sub(r"//[^\n]*", "", text)
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    enums = {}
    for name, body in DART_ENUM.findall(text):
        # 成员区止于第一个分号，分号之后是方法与字段。
        members = []
        for raw in body.split(";")[0].split(","):
            token = raw.strip()
            if not token:
                continue
            members.append(token.split("(")[0].strip())
        enums[name] = members
    return enums


def compare(doc: dict, code: dict) -> None:
    for name in sorted(set(doc) | set(code)):
        if name not in code:
            errors.append(f"枚举 {name}（需求 {doc[name]['section']}）在 enums.dart 中缺失")
            continue
        if name not in doc:
            errors.append(f"枚举 {name} 在 enums.dart 中定义，需求 14 章无对应条目")
            continue
        expected = doc[name]["members"]
        actual = code[name]
        # 中文成员的枚举在代码中以 ASCII 标识符表达，成员数一致即可，逐名对照留给该枚举自身的单测。
        ascii_doc = all(re.fullmatch(r"[A-Za-z0-9_+\-]+", m) for m in expected)
        if ascii_doc:
            missing = [m for m in expected if m not in actual]
            extra = [m for m in actual if m not in expected]
            if missing:
                errors.append(f"枚举 {name} 缺少成员 {', '.join(missing)}（需求 {doc[name]['section']}）")
            if extra:
                errors.append(f"枚举 {name} 多出成员 {', '.join(extra)}，需求 {doc[name]['section']} 未记录")
        elif len(expected) != len(actual):
            errors.append(
                f"枚举 {name} 成员数为 {len(actual)}，需求 {doc[name]['section']} 为 {len(expected)}"
            )


def main() -> int:
    doc = parse_requirements()
    if len(doc) != 28:
        errors.append(f"需求 14 章解析出 {len(doc)} 个枚举，应为 28 个")

    total = sum(len(v["members"]) for v in doc.values())
    print(f"  需求 14 章 {len(doc)} 个枚举，{total} 个成员")

    if os.path.exists(ENUMS_DART):
        compare(doc, parse_dart())
        print(f"  与 {os.path.relpath(ENUMS_DART, ROOT)} 双向对照")
    else:
        print(f"  {os.path.relpath(ENUMS_DART, ROOT)} 尚未实现，本次只校验文档侧")

    # 快照供 ling_core 的枚举测试读取，使 Dart 侧断言与本检查同源。
    snapshot = {
        "$comment": "由 tests/check_enums.py 从需求文档 14 章生成。"
                    "ling_core 的枚举测试读取本文件断言成员集合。",
        "enums": doc,
    }
    open(SNAPSHOT, "w", encoding="utf-8").write(
        json.dumps(snapshot, ensure_ascii=False, indent=1) + "\n"
    )

    if errors:
        print("\n枚举一致性校验失败:")
        for item in errors:
            print(f"  - {item}")
        return 1
    print("\n枚举一致性校验通过。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
