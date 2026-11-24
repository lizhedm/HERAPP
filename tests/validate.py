#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""系统测试用例清单的校验器。

校验分五组，任一失败即以非零码退出，供 CI 阻断合并：

1. 结构：必填字段齐全、取值在约定集合内、用例 ID 全局唯一且格式正确。
2. 需求覆盖：需求文档 16 章的每条 REQ-16-nn 至少被一条用例覆盖，且用例引用的编号都真实存在。
3. 屏幕覆盖：线框图的每个屏幕 ID 至少被一条用例覆盖，且用例引用的屏幕 ID 都真实存在。
4. 断言可执行：带 oracle 的用例逐例执行参考实现，期望值与实际结果一致。
5. 测试标识：testId 格式正确、路径与层相符且不重复，保证一个用例对应一个可定位的测试。

只依赖标准库，Python 3.9 可运行。
"""

from __future__ import annotations

import glob
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
REGISTRY = os.path.join(HERE, "registry")
REQ_DOC = os.path.join(ROOT, "需求文档V1.1.md")
WIREFRAME = os.path.join(ROOT, "低保真线框图-LingLing-V1.1.html")

sys.path.insert(0, os.path.join(HERE, "lib"))
import rules  # noqa: E402

REQUIRED_FIELDS = ["id", "title", "req", "reqSection", "screens", "layer", "priority", "given", "when", "then", "testId"]
LIST_FIELDS = ["req", "reqSection", "screens", "given", "when", "then"]
LAYERS = {"rule", "service", "dao", "widget", "golden", "integration", "backend", "contract", "perf"}
PRIORITIES = {"P0", "P1", "P2"}
ID_PATTERN = re.compile(r"^SYS-(?:[A-H]|RULE|BACKEND|PERF|COVER|MIGRATE)-\d{3}$")
TEST_ID_PATTERN = re.compile(r"^[\w./]+\.(?:dart|py)::.+$")

# 测试标识的路径前缀由层决定，与技术方案 2.3 的仓库结构一致。
LAYER_ROOTS = {
    "rule": ["packages/ling_core/test/"],
    "service": ["packages/ling_app/test/"],
    "dao": ["packages/ling_app/test/"],
    "widget": ["packages/ling_app/test/"],
    "golden": ["packages/ling_app/test/golden/"],
    "perf": ["packages/ling_app/test/perf/"],
    "integration": ["packages/ling_app/integration_test/"],
    "backend": ["backend/tests/"],
    "contract": ["backend/tests/"],
}

errors = []
notes = []


def fail(msg: str) -> None:
    errors.append(msg)


def load_cases() -> list:
    cases = []
    for path in sorted(glob.glob(os.path.join(REGISTRY, "*.json"))):
        name = os.path.basename(path)
        if name.startswith("_"):
            continue
        try:
            data = json.load(open(path, encoding="utf-8"))
        except json.JSONDecodeError as exc:
            fail(f"{name} 不是合法 JSON: {exc}")
            continue
        if not isinstance(data, list):
            fail(f"{name} 顶层应为用例数组")
            continue
        for case in data:
            case["_file"] = name
            cases.append(case)
    return cases


def check_structure(cases: list) -> None:
    seen_ids = {}
    seen_dart = {}
    for case in cases:
        cid = case.get("id", "<缺少 id>")
        where = f"{case['_file']} / {cid}"
        for field in REQUIRED_FIELDS:
            if field not in case:
                fail(f"{where} 缺少必填字段 {field}")
        for field in LIST_FIELDS:
            if field in case and not isinstance(case[field], list):
                fail(f"{where} 字段 {field} 应为数组")
        for field in ["given", "when", "then"]:
            if isinstance(case.get(field), list) and not case[field]:
                fail(f"{where} 字段 {field} 不可为空数组")
        if "id" in case and not ID_PATTERN.match(case["id"]):
            fail(f"{where} ID 格式不符合 SYS-<区>-<三位序号>")
        if case.get("layer") not in LAYERS:
            fail(f"{where} layer 取值 {case.get('layer')!r} 不在约定集合内")
        if case.get("priority") not in PRIORITIES:
            fail(f"{where} priority 取值 {case.get('priority')!r} 不在 P0/P1/P2 内")
        if not case.get("req") and not case.get("reqSection"):
            fail(f"{where} req 与 reqSection 不可同时为空")
        if "id" in case:
            if case["id"] in seen_ids:
                fail(f"用例 ID {case['id']} 重复，出现在 {seen_ids[case['id']]} 与 {case['_file']}")
            seen_ids[case["id"]] = case["_file"]
        test_id = case.get("testId")
        if test_id:
            if not TEST_ID_PATTERN.match(test_id):
                fail(f"{where} testId 格式应为 <文件路径>::<测试名>，实际 {test_id!r}")
            if test_id in seen_dart:
                fail(f"testId {test_id} 重复，出现在 {seen_dart[test_id]} 与 {cid}")
            seen_dart[test_id] = cid
            roots = LAYER_ROOTS.get(case.get("layer"), [])
            if roots and not any(test_id.startswith(r) for r in roots):
                fail(f"{where} layer {case['layer']} 的测试应位于 {' 或 '.join(roots)}，实际 {test_id!r}")
    notes.append(f"结构校验覆盖 {len(cases)} 条用例，{len(seen_dart)} 个测试标识")


def doc_req_ids() -> set:
    text = open(REQ_DOC, encoding="utf-8").read()
    return set(re.findall(r"REQ-16-\d{2}", text))


def check_req_coverage(cases: list) -> None:
    declared = doc_req_ids()
    if not declared:
        fail("需求文档中未找到任何 REQ-16-nn 编号")
        return
    used = set()
    for case in cases:
        for rid in case.get("req", []):
            used.add(rid)
            if rid not in declared:
                fail(f"{case['_file']} / {case['id']} 引用了不存在的需求编号 {rid}")
    uncovered = sorted(declared - used)
    if uncovered:
        fail(f"以下需求验收标准没有对应用例: {', '.join(uncovered)}")
    notes.append(f"需求覆盖 {len(used & declared)} / {len(declared)} 条验收标准")


def wireframe_screen_ids() -> set:
    if not os.path.exists(WIREFRAME):
        fail(f"线框图文件缺失: {os.path.basename(WIREFRAME)}")
        return set()
    html = open(WIREFRAME, encoding="utf-8").read()
    return set(re.findall(r'<span class="sid">([A-H]\d+[a-z]?)</span>', html))


def check_screen_coverage(cases: list) -> None:
    declared = wireframe_screen_ids()
    if not declared:
        return
    used = set()
    for case in cases:
        for sid in case.get("screens", []):
            used.add(sid)
            if sid not in declared:
                fail(f"{case['_file']} / {case['id']} 引用了线框图中不存在的屏幕 {sid}")
    uncovered = sorted(declared - used)
    if uncovered:
        fail(f"以下屏幕没有对应用例: {', '.join(uncovered)}")
    notes.append(f"屏幕覆盖 {len(used & declared)} / {len(declared)} 个屏幕")


def check_oracles(cases: list) -> None:
    executed = 0
    assertions = 0
    for case in cases:
        oracle = case.get("oracle")
        if not oracle:
            continue
        where = f"{case['_file']} / {case['id']}"
        fn_name = oracle.get("fn")
        fn = getattr(rules, fn_name, None)
        if fn is None:
            fail(f"{where} oracle 引用了不存在的函数 {fn_name}")
            continue
        executed += 1
        exhaustive = oracle.get("exhaustive")
        if exhaustive == "cover_reachability":
            found = rules.reachable_subpools()
            all_pools = {(lv, vr) for lv in ["L1", "L2", "L3", "L4", "L5"] for vr in ["V1", "V2", "V3", "V4"]}
            if len(found) != 18:
                fail(f"{where} 可达子池数为 {len(found)}，期望 18")
            if all_pools - found != rules.UNREACHABLE_SUBPOOLS:
                fail(f"{where} 不可达子池为 {sorted(all_pools - found)}，期望 {sorted(rules.UNREACHABLE_SUBPOOLS)}")
            assertions += 2
            continue
        for idx, item in enumerate(oracle.get("cases", [])):
            args = item.get("args", [])
            kwargs = item.get("kwargs", {})
            try:
                actual = fn(*args, **kwargs)
            except Exception as exc:  # 参考实现抛错即用例定义有问题
                fail(f"{where} 第 {idx + 1} 例执行 {fn_name} 抛出 {type(exc).__name__}: {exc}")
                continue
            expect = item["expect"]
            if isinstance(actual, set):
                actual = sorted(actual)
            if actual != expect:
                fail(f"{where} 第 {idx + 1} 例 {fn_name}(args={args}, kwargs={kwargs}) 得 {actual!r}，期望 {expect!r}")
            assertions += 1
    notes.append(f"断言执行 {executed} 个 oracle，{assertions} 条输入输出对")


def check_rule_version() -> None:
    plan = os.path.join(ROOT, "技术方案V1.0.md")
    if not os.path.exists(plan):
        fail("技术方案文件缺失")
        return
    text = open(plan, encoding="utf-8").read()
    for axis in ["schemaVersion", "promptVersion", "ruleVersion", "appVersion", "coverPoolVersion"]:
        if axis not in text:
            fail(f"技术方案缺少版本轴 {axis}")
    notes.append("版本轴校验通过，5 条版本轴均在技术方案中声明")


def main() -> int:
    cases = load_cases()
    if not cases:
        fail("registry 下没有读到任何用例")
    check_structure(cases)
    check_req_coverage(cases)
    check_screen_coverage(cases)
    check_oracles(cases)
    check_rule_version()

    for note in notes:
        print(f"  {note}")
    if errors:
        print(f"\n校验失败，共 {len(errors)} 项:")
        for err in errors:
            print(f"  - {err}")
        return 1
    print(f"\n校验通过，{len(cases)} 条用例全部合规。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
