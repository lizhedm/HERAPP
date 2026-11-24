#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""由用例清单生成测试骨架与追溯矩阵。

用例清单是唯一事实来源，以下产物都由它派生，不手工维护：

1. 测试骨架：按 testId 的文件路径分组，每条用例生成一个带 given / when / then
   注释的测试占位。路径前缀由 layer 决定，与技术方案 2.3 的仓库结构一致，
   Dart 侧落在 packages/，后端侧落在 backend/tests/。
   未实现的占位标记为跳过而非失败，使 CI 在开发期保持可用，
   跳过数即待实现用例数，是可读的进度指标。
   已存在的文件默认保留，避免冲掉已实现的测试体；--force 用于重建骨架。
2. docs/traceability.md：需求编号、用例、屏幕、测试标识的四向追溯表，
   供评审与验收时核对覆盖。
3. tests/oracle_fixtures.json：规则层 oracle 的输入输出对，Dart 与后端读取
   同一份数据做跨语言对照，保证两侧对同一输入得出相同结果。

只依赖标准库，Python 3.9 可运行。
"""

from __future__ import annotations

import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
REGISTRY = os.path.join(HERE, "registry")
TRACE_DOC = os.path.join(ROOT, "docs", "traceability.md")
FIXTURES = os.path.join(HERE, "oracle_fixtures.json")

FORCE = "--force" in sys.argv


def load_cases() -> list:
    cases = []
    for path in sorted(glob.glob(os.path.join(REGISTRY, "*.json"))):
        if os.path.basename(path).startswith("_"):
            continue
        cases.extend(json.load(open(path, encoding="utf-8")))
    return sorted(cases, key=lambda c: c["id"])


def group_by_file(cases: list) -> dict:
    groups = {}
    for case in cases:
        path, _, name = case["testId"].partition("::")
        groups.setdefault(path, []).append((name, case))
    return groups


def case_comment(case: dict, prefix: str) -> list:
    lines = [
        f"{prefix} {case['id']} [{case['priority']}] {case['title']}",
        f"{prefix} 需求 {', '.join(case['req']) or '—'} / 章节 {', '.join(case['reqSection'])}",
    ]
    if case["screens"]:
        lines.append(f"{prefix} 屏幕 {', '.join(case['screens'])}")
    for label in ("given", "when", "then"):
        for item in case[label]:
            lines.append(f"{prefix} {label}: {item}")
    if case.get("oracle"):
        lines.append(f"{prefix} oracle: {case['oracle']['fn']}，期望值取自 tests/oracle_fixtures.json")
    return lines


def dart_escape(text: str) -> str:
    return text.replace("\\", "\\\\").replace("'", "\\'").replace("$", "\\$")


def render_dart(path: str, items: list) -> str:
    is_integration = "/integration_test/" in path
    is_core = path.startswith("packages/ling_core/")

    lines = [
        "// 本文件由 tests/generate.py 从 tests/registry/ 生成，测试名与用例 ID 一一对应。",
        "// 用例的 given / when / then 见注释，断言在此实现。",
        "// 实现一条用例时删除该条的 skip 参数。",
        "",
    ]
    if is_integration:
        lines.append("import 'package:integration_test/integration_test.dart';")
    lines.append("import 'package:test/test.dart';" if is_core else "import 'package:flutter_test/flutter_test.dart';")
    lines.append("")
    lines.append("void main() {")
    if is_integration:
        lines.append("  IntegrationTestWidgetsFlutterBinding.ensureInitialized();")
        lines.append("")

    for name, case in items:
        lines.extend("  " + line for line in case_comment(case, "//"))
        widget_style = case["layer"] in ("widget", "golden", "integration")
        fn = "testWidgets" if widget_style else "test"
        sig = "(tester) async {" if widget_style else "() {"
        lines.append(f"  {fn}('{dart_escape(name)}', {sig}")
        lines.append(f"    // 实现 {case['id']} 的断言")
        lines.append(f"  }}, skip: '{case['id']} 待实现');")
        lines.append("")

    lines.append("}")
    return "\n".join(lines) + "\n"


def py_escape(text: str) -> str:
    return text.replace("\\", "\\\\").replace('"', '\\"')


def py_ident(name: str, case_id: str) -> str:
    """pytest 函数名用 ASCII，中文测试名放进 docstring，保持可读与可定位。"""
    return "test_" + case_id.lower().replace("-", "_")


def render_python(path: str, items: list) -> str:
    lines = [
        "# -*- coding: utf-8 -*-",
        '"""本文件由 tests/generate.py 从 tests/registry/ 生成，测试函数与用例 ID 一一对应。',
        "",
        "用例的 given / when / then 见各函数注释，断言在此实现。",
        "实现一条用例时删除该条的 skip 标记。",
        '"""',
        "",
        "import pytest",
        "",
    ]
    for name, case in items:
        lines.append(f'@pytest.mark.skip(reason="{case["id"]} 待实现")')
        lines.append(f"def {py_ident(name, case['id'])}():")
        lines.append(f'    """{py_escape(name)}"""')
        lines.extend("    " + line for line in case_comment(case, "#"))
        lines.append(f"    # 实现 {case['id']} 的断言")
        lines.append("")
    return "\n".join(lines)


def write_skeletons(cases: list) -> tuple:
    created = skipped = 0
    for path, items in sorted(group_by_file(cases).items()):
        target = os.path.join(ROOT, path)
        os.makedirs(os.path.dirname(target), exist_ok=True)
        if os.path.exists(target) and not FORCE:
            skipped += 1
            continue
        body = render_python(path, items) if path.endswith(".py") else render_dart(path, items)
        open(target, "w", encoding="utf-8").write(body)
        created += 1
    return created, skipped


def screen_sort_key(sid: str) -> tuple:
    digits = "".join(ch for ch in sid if ch.isdigit())
    return (sid[0], int(digits) if digits else 0, sid)


def render_trace(cases: list) -> str:
    by_req = {}
    for case in cases:
        for rid in case["req"]:
            by_req.setdefault(rid, []).append(case)

    out = [
        "# LingLing 需求追溯矩阵",
        "",
        "本文件由 `tests/generate.py` 从 `tests/registry/` 生成，改动用例清单后重新生成。",
        "每条需求验收标准至少对应一条用例，每条用例对应一个可定位的测试标识。",
        "`tests/validate.py` 在 CI 中强制这两条性质，覆盖缺口会阻断合并。",
        "",
        f"需求验收标准 {len(by_req)} 条，用例 {len(cases)} 条，测试标识 {len({c['testId'] for c in cases})} 个。",
        "",
        "## 需求 → 用例 → 屏幕 → 测试",
        "",
        "| 需求编号 | 用例 ID | 优先级 | 层 | 屏幕 | 用例标题 | 测试标识 |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for rid in sorted(by_req):
        for case in sorted(by_req[rid], key=lambda c: c["id"]):
            screens = ", ".join(case["screens"]) if case["screens"] else "—"
            out.append(
                f"| {rid} | {case['id']} | {case['priority']} | {case['layer']} | "
                f"{screens} | {case['title']} | `{case['testId']}` |"
            )
    out.append("")

    by_screen = {}
    for case in cases:
        for sid in case["screens"]:
            by_screen.setdefault(sid, []).append(case["id"])
    out += ["## 屏幕 → 用例", "", "| 屏幕 | 用例 ID |", "| --- | --- |"]
    for sid in sorted(by_screen, key=screen_sort_key):
        out.append(f"| {sid} | {', '.join(sorted(by_screen[sid]))} |")
    out.append("")

    by_layer = {}
    for case in cases:
        by_layer.setdefault(case["layer"], []).append(case)
    out += ["## 分层统计", "", "| 层 | 用例数 | P0 | P1 | P2 |", "| --- | --- | --- | --- | --- |"]
    for layer in sorted(by_layer, key=lambda l: -len(by_layer[l])):
        group = by_layer[layer]
        counts = [sum(1 for c in group if c["priority"] == p) for p in ("P0", "P1", "P2")]
        out.append(f"| {layer} | {len(group)} | {counts[0]} | {counts[1]} | {counts[2]} |")
    total = [sum(1 for c in cases if c["priority"] == p) for p in ("P0", "P1", "P2")]
    out.append(f"| **合计** | **{len(cases)}** | **{total[0]}** | **{total[1]}** | **{total[2]}** |")
    out.append("")

    return "\n".join(out)


def render_fixtures(cases: list) -> str:
    fixtures = {}
    for case in cases:
        oracle = case.get("oracle")
        if not oracle:
            continue
        fixtures[case["id"]] = {
            "fn": oracle["fn"],
            "title": case["title"],
            "testId": case["testId"],
            "exhaustive": oracle.get("exhaustive"),
            "cases": oracle.get("cases", []),
        }
    header = {
        "$comment": "由 tests/generate.py 从 tests/registry/ 生成。"
                    "Dart 与后端读取同一份期望值，保证跨语言一致。",
        "ruleVersion": 2,
        "oracles": fixtures,
    }
    return json.dumps(header, ensure_ascii=False, indent=1) + "\n"


def write(path: str, content: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w", encoding="utf-8").write(content)


def main() -> int:
    cases = load_cases()
    created, skipped = write_skeletons(cases)
    write(TRACE_DOC, render_trace(cases))
    write(FIXTURES, render_fixtures(cases))
    oracle_count = sum(1 for c in cases if c.get("oracle"))

    print(f"  用例 {len(cases)} 条")
    print(f"  测试骨架 新建 {created} 个文件，保留已存在 {skipped} 个（--force 重建）")
    print(f"  追溯矩阵 {os.path.relpath(TRACE_DOC, ROOT)}")
    print(f"  oracle 固定数据 {oracle_count} 组 → {os.path.relpath(FIXTURES, ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
