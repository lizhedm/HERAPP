# -*- coding: utf-8 -*-
"""本文件由 tests/generate.py 从 tests/registry/ 生成，测试函数与用例 ID 一一对应。

用例的 given / when / then 见各函数注释，断言在此实现。
实现一条用例时删除该条的 skip 标记。
"""

import pytest

@pytest.mark.skip(reason="SYS-BACKEND-012 待实现")
def test_sys_backend_012():
    """非文本占位符"""
    # SYS-BACKEND-012 [P1] 非文本消息以类型占位符送入提示词，条数照常计入
    # 需求 REQ-16-36 / 章节 6.6
    # 屏幕 D1
    # given: 某日消息含图片、语音、视频、红包、转账、通话记录
    # when: 构建 AI 提示词的消息序列
    # then: 文本类型传脱敏后文本，其余类型传对应的类型占位符
    # then: 各类型消息条数照常计入互动统计，字数计 0
    # then: 提示词仅要求输出 JSON 本体
    # 实现 SYS-BACKEND-012 的断言
