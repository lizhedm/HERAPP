# -*- coding: utf-8 -*-
"""本文件由 tests/generate.py 从 tests/registry/ 生成，测试函数与用例 ID 一一对应。

用例的 given / when / then 见各函数注释，断言在此实现。
实现一条用例时删除该条的 skip 标记。
"""

import pytest

@pytest.mark.skip(reason="SYS-BACKEND-005 待实现")
def test_sys_backend_005():
    """JSON 解析失败处理"""
    # SYS-BACKEND-005 [P0] AI 输出 JSON 解析失败记录失败状态并保留重试入口
    # 需求 REQ-16-13 / 章节 6.2
    # 屏幕 D4
    # given: AI 返回非 JSON 或字段缺失的响应
    # when: 解析评估结果
    # then: 评估状态置为失败，不写入部分结果
    # then: 日详情展示评估失败状态与重试入口
    # then: 同步与对话流继续可用
    # 实现 SYS-BACKEND-005 的断言
