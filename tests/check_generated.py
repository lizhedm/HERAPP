#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""检查派生产物与用例清单一致。

追溯矩阵与 oracle 固定数据由 generate.py 派生。改了用例清单却忘记重新生成时，
提交中的追溯矩阵会落后于清单，评审看到的覆盖情况与实际不符。本脚本调用
generate 的渲染函数重算一遍并与磁盘内容比对，不一致即失败并提示重新生成。

测试骨架不参与内容比对：骨架在生成后由开发者填入断言，内容必然与初始骨架不同。
骨架的完整性以存在性保证，即清单中每个 testId 指向的文件都存在。

只依赖标准库，Python 3.9 可运行。
"""

from __future__ import annotations

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import generate  # noqa: E402

errors = []


def compare(path: str, expected: str, label: str) -> None:
    rel = os.path.relpath(path, ROOT)
    if not os.path.exists(path):
        errors.append(f"{label} 缺失: {rel}")
        return
    if open(path, encoding="utf-8").read() != expected:
        errors.append(f"{label} 与用例清单不一致: {rel}")


def main() -> int:
    cases = generate.load_cases()

    compare(generate.TRACE_DOC, generate.render_trace(cases), "追溯矩阵")
    compare(generate.FIXTURES, generate.render_fixtures(cases), "oracle 固定数据")

    files = sorted({c["testId"].partition("::")[0] for c in cases})
    missing = [p for p in files if not os.path.exists(os.path.join(ROOT, p))]
    if missing:
        errors.append(f"{len(missing)} 个测试文件不存在，首个为 {missing[0]}")

    if errors:
        print("  产物检查失败:")
        for err in errors:
            print(f"  - {err}")
        print("\n  执行 python3 tests/generate.py 重新生成后提交。")
        return 1

    print(f"  追溯矩阵与 oracle 固定数据同步，{len(files)} 个测试文件齐全")
    return 0


if __name__ == "__main__":
    sys.exit(main())
