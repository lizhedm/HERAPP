#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""扫描表现层与后端中的规则字面量，强制规则只在 ling_core 实现一次。

技术方案 6.1 要求全部确定性映射收敛到 ling_core，表现层与后端不得出现
天气区间、封面区间、情绪色值、权重系数的字面量。规则散落多处实现是
功能增长期混乱的首要根因：同一规则改两处、漏一处，偏差在发布后才暴露。

判定方式按「组合命中」而非「单值命中」。`0.5` 这类裸小数在布局、动画、
透明度中正常出现，单值命中会产生大量误报，误报会让开发者学会忽略本检查。
因此只在同一文件中同时出现一组规则特征时报错，例如权重 0.6 与 0.4 同现、
或三个以上天气区间端点同现。这样做放过了单独写死一个系数的情形，
该情形由评审清单的「规则归属」一项覆盖。

扫描范围按技术方案 6.1 限定：
  packages/ling_app/lib/presentation/   表现层
  backend/app/                          后端

只依赖标准库，Python 3.9 可运行。
"""

from __future__ import annotations

import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

SCAN_DIRS = [
    os.path.join("packages", "ling_app", "lib", "presentation"),
    os.path.join("backend", "app"),
]
SCAN_EXT = (".dart", ".py")

# 每条规则给出特征表达式集合与触发阈值。同一文件命中数达到阈值即报错。
#
# 特征按「运算形状」而非「数值出现」来写。权重的形状是乘法 `× 0.6`，
# 区间端点的形状是比较 `>= 85`，档位中值的形状是减法或映射表项。
# 布局里的 `padding: 0.6`、`width: 85` 不具备这些形状，因此不会误伤。
# 这是本检查可用的前提：误报会让开发者学会忽略它，机制随之失效。
RULES = [
    {
        "name": "天气综合分权重",
        "section": "需求 7.1",
        "hint": "改为调用 ling_core 的 WeatherService.compositeScore",
        "values": [r"[*×]\s*0\.4\b", r"[*×]\s*0\.25\b", r"[*×]\s*0\.15\b", r"[*×]\s*0\.2\b",
                   r"0\.4\s*[*×]", r"0\.25\s*[*×]", r"0\.15\s*[*×]", r"0\.2\s*[*×]"],
        "threshold": 3,
    },
    {
        "name": "沟通比分项权重与对等度公式",
        "section": "需求 6.4",
        "hint": "改为调用 ling_core 的 BalanceService.communicationBalance",
        "values": [r"[*×]\s*0\.30?\b", r"[*×]\s*0\.25\b", r"[*×]\s*0\.20?\b",
                   r"2\s*[*×]\s*min", r"\bminOf\b"],
        "threshold": 3,
    },
    {
        "name": "封面综合关系分权重",
        "section": "需求 5.1",
        "hint": "改为调用 ling_core 的 CoverService.compositeScore",
        "values": [r"[*×]\s*0\.6\b", r"[*×]\s*0\.4\b",
                   r"0\.6\s*[*×]", r"0\.4\s*[*×]"],
        "threshold": 2,
    },
    {
        "name": "天气区间端点",
        "section": "需求 7.2",
        "hint": "改为调用 ling_core 的 WeatherService.byBand",
        "values": [r"[><]=?\s*95\b", r"[><]=?\s*85\b", r"[><]=?\s*75\b",
                   r"[><]=?\s*65\b", r"[><]=?\s*55\b", r"[><]=?\s*45\b",
                   r"[><]=?\s*35\b", r"[><]=?\s*25\b"],
        "threshold": 3,
    },
    {
        "name": "封面等级区间端点",
        "section": "需求 5.1",
        "hint": "改为调用 ling_core 的 CoverService.levelOf",
        "values": [r"[><]=?\s*21\b", r"[><]=?\s*41\b",
                   r"[><]=?\s*61\b", r"[><]=?\s*81\b",
                   r"[><]=?\s*20\b", r"[><]=?\s*40\b",
                   r"[><]=?\s*60\b", r"[><]=?\s*80\b"],
        "threshold": 3,
    },
    {
        "name": "档位中值",
        "section": "需求 5.2",
        "hint": "改为调用 ling_core 的 CoverService.variantOf",
        "values": [r"\b13\b", r"\b38\b", r"\b63\b", r"\b88\b"],
        "threshold": 3,
    },
    {
        "name": "天气枚举与分数同现",
        "section": "需求 7.2",
        "hint": "天气判定应由 ling_core 返回，表现层只做图标与文案映射",
        "values": [r"RAINBOW", r"THUNDERSTORM", r"[><]=?\s*\d{2}\b"],
        "threshold": 3,
    },
    {
        "name": "情绪色系色值",
        "section": "需求 9.4",
        "hint": "改为调用 ling_core 的情绪色系映射并由主题取色",
        "values": [r"0x[fF][fF][0-9a-fA-F]{6}", r"#[0-9a-fA-F]{6}\b",
                   r"Color\(0x", r"WARM_YELLOW", r"GRAY_BROWN"],
        "threshold": 4,
    },
]

# 常量定义文件与测试文件允许出现字面量：前者是规则的实现处，后者是规则的断言处。
ALLOW_PATH = re.compile(r"(^|/)(test|tests|fixtures)(/|$)|_test\.|constants?\.|theme")

errors: list = []


def strip_comments(text: str, path: str) -> str:
    """去掉注释，避免注释中的说明文字触发误报。"""
    if path.endswith(".dart"):
        text = re.sub(r"//[^\n]*", "", text)
        text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    else:
        text = re.sub(r"#[^\n]*", "", text)
        text = re.sub(r'"""".*?""""', "", text, flags=re.S)
        text = re.sub(r'""".*?"""', "", text, flags=re.S)
    return text


def scan_file(path: str, rel: str) -> None:
    """命中时报出行号与原文，使开发者直接定位到要改的那几行。"""
    lines = strip_comments(open(path, encoding="utf-8").read(), path).splitlines()
    for rule in RULES:
        matched = {}
        for lineno, line in enumerate(lines, 1):
            for pattern in rule["values"]:
                if pattern not in matched and re.search(pattern, line):
                    matched[pattern] = (lineno, line.strip())
        if len(matched) >= rule["threshold"]:
            # 同一行可能命中多个特征，按行去重后展示。
            spots = sorted(set(matched.values()))
            detail = "".join(f"\n      第 {no} 行: {text}" for no, text in spots)
            errors.append(
                f"{rel} 命中{rule['name']}（{rule['section']}）{len(matched)} 处{detail}\n"
                f"      {rule['hint']}"
            )


def main() -> int:
    scanned = 0
    for rel_dir in SCAN_DIRS:
        base = os.path.join(ROOT, rel_dir)
        if not os.path.isdir(base):
            print(f"  {rel_dir} 尚未创建，跳过")
            continue
        for dirpath, _, filenames in os.walk(base):
            for filename in sorted(filenames):
                if not filename.endswith(SCAN_EXT):
                    continue
                path = os.path.join(dirpath, filename)
                rel = os.path.relpath(path, ROOT)
                if ALLOW_PATH.search(rel):
                    continue
                scan_file(path, rel)
                scanned += 1
        print(f"  扫描 {rel_dir}")

    print(f"  共 {scanned} 个文件，{len(RULES)} 条规则特征")

    if errors:
        print("\n规则字面量扫描失败，规则应只在 ling_core 实现一次:")
        for item in errors:
            print(f"  - {item}")
        return 1
    print("\n规则字面量扫描通过。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
