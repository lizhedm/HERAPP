# -*- coding: utf-8 -*-
"""本文件由 tests/generate.py 从 tests/registry/ 生成，测试函数与用例 ID 一一对应。

用例的 given / when / then 见各函数注释，断言在此实现。
实现一条用例时删除该条的 skip 标记。
"""

import pytest

@pytest.mark.skip(reason="SYS-BACKEND-010 待实现")
def test_sys_backend_010():
    """脱敏不落盘"""
    # SYS-BACKEND-010 [P0] 脱敏在内存副本上执行，本地存储与对话流保留原文
    # 需求 REQ-16-36 / 章节 6.5
    # 屏幕 D1
    # given: 某日消息含手机号与邮箱
    # when: 该日完成 AI 评估后查看对话流
    # then: 送 AI 的文本为脱敏后内容
    # then: 本地数据库与对话流展示保留原文
    # then: 字数统计以原文为准，脱敏引起的长度变化不影响统计
    # 实现 SYS-BACKEND-010 的断言

@pytest.mark.skip(reason="SYS-BACKEND-011 待实现")
def test_sys_backend_011():
    """姓名昵称保留"""
    # SYS-BACKEND-011 [P1] 姓名与昵称保留原文，供亲密度判定使用
    # 需求 REQ-16-36 / 章节 6.5
    # given: 含双方姓名与昵称的文本
    # when: 执行脱敏
    # then: 姓名与昵称保留原文
    # then: 称呼本身是亲密度判定的依据，替换会改变评估结果
    # then: 聊天正文的其余内容同样保留原文
    # oracle: mask，期望值取自 tests/oracle_fixtures.json
    # 实现 SYS-BACKEND-011 的断言

@pytest.mark.skip(reason="SYS-RULE-050 待实现")
def test_sys_rule_050():
    """六类敏感信息替换"""
    # SYS-RULE-050 [P0] 脱敏按固定顺序替换 6 类结构化敏感信息
    # 需求 REQ-16-36 / 章节 6.5
    # given: 含手机号、身份证号、银行卡号、邮箱、详细地址与验证码的文本
    # when: 执行送 AI 前的脱敏
    # then: 6 类对象各替换为对应占位符
    # then: 邮箱先行替换，整个邮箱作为一个整体被替换
    # then: 身份证先于银行卡，18 位纯数字判为身份证号
    # then: 身份证末位的 X 大小写均识别
    # oracle: mask，期望值取自 tests/oracle_fixtures.json
    # 实现 SYS-RULE-050 的断言

@pytest.mark.skip(reason="SYS-RULE-051 待实现")
def test_sys_rule_051():
    """验证码上下文识别"""
    # SYS-RULE-051 [P0] 验证码只替换与验证码字样相邻的数字，普通数字保留原文
    # 需求 REQ-16-36 / 章节 6.5
    # given: 含验证码数字与普通数字的文本
    # when: 执行脱敏
    # then: 与「验证码」「码」相邻的 4-8 位数字替换为占位符，字样本身保留
    # then: 冒号、空格、「是」「为」作为分隔符时同样识别
    # then: 订单号、价格、年份等普通数字保留原文，供 AI 判断语义
    # oracle: mask，期望值取自 tests/oracle_fixtures.json
    # 实现 SYS-RULE-051 的断言

@pytest.mark.skip(reason="SYS-RULE-052 待实现")
def test_sys_rule_052():
    """详细地址识别"""
    # SYS-RULE-052 [P1] 详细地址识别省市区与门牌号组合
    # 需求 REQ-16-36 / 章节 6.5
    # given: 含省市区与门牌号的地址串，以及仅含城市名的普通文本
    # when: 执行脱敏
    # then: 完整地址串替换为地址占位符
    # then: 仅提及城市名而无门牌号的文本保留原文，城市话题是情绪判定的依据
    # then: 识别偏保守方向，地址串前缀一并替换不影响 AI 判断
    # oracle: mask，期望值取自 tests/oracle_fixtures.json
    # 实现 SYS-RULE-052 的断言
