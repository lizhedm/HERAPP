# -*- coding: utf-8 -*-
"""本文件由 tests/generate.py 从 tests/registry/ 生成，测试函数与用例 ID 一一对应。

用例的 given / when / then 见各函数注释，断言在此实现。
实现一条用例时删除该条的 skip 标记。
"""

import pytest

@pytest.mark.skip(reason="SYS-BACKEND-015 待实现")
def test_sys_backend_015():
    """多端编辑按更新时刻取较新"""
    # SYS-BACKEND-015 [P0] 同一条记录被多端编辑时后端按更新时刻保留较新者
    # 需求 REQ-16-50 / 章节 3.11
    # given: 两个客户端对同一条记录分别提交编辑，更新时刻一前一后
    # when: 后端按到达顺序与逆序各处理一遍
    # then: 两种到达顺序下后端均保留更新时刻较新的版本
    # then: 较旧的提交被判定为过期，不覆盖较新版本
    # then: 任一端的编辑在其他端下一次同步后可见
    # 实现 SYS-BACKEND-015 的断言
