# -*- coding: utf-8 -*-
"""本文件由 tests/generate.py 从 tests/registry/ 生成，测试函数与用例 ID 一一对应。

用例的 given / when / then 见各函数注释，断言在此实现。
实现一条用例时删除该条的 skip 标记。
"""

import pytest

@pytest.mark.skip(reason="SYS-F-015 待实现")
def test_sys_f_015():
    """引用解除与无引用清理"""
    # SYS-F-015 [P1] 删除条目图片后解除引用，无引用图片由后端清理
    # 需求 REQ-16-51 / 章节 3.12
    # 屏幕 F2, F9
    # given: 某张图片被一个喜好条目引用
    # when: 用户删除该条目图片或重新选择另一张图片
    # then: 后端解除该条目与原图片的引用关系
    # then: 重新选择即替换，替换后旧图片解除引用
    # then: 图片不再被任何条目引用时由后端清理
    # 实现 SYS-F-015 的断言
