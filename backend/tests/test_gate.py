# -*- coding: utf-8 -*-
"""本文件由 tests/generate.py 从 tests/registry/ 生成，测试函数与用例 ID 一一对应。

用例的 given / when / then 见各函数注释，断言在此实现。
实现一条用例时删除该条的 skip 标记。
"""

import pytest

@pytest.mark.skip(reason="SYS-BACKEND-016 待实现")
def test_sys_backend_016():
    """密码哈希下发与改密脚本"""
    # SYS-BACKEND-016 [P0] 访问密码只下发加盐哈希，改密码脚本刷新哈希与盐值
    # 需求 REQ-16-43 / 章节 3.10
    # given: 后端配置项 gate.password 为默认值
    # when: 调用改密码脚本设置新密码，再请求门禁凭据接口
    # then: 接口返回加盐哈希与盐值，响应体不含明文密码
    # then: 改密码脚本写入新的哈希与新盐值，旧哈希不再校验通过
    # then: 同一密码在两次改密后得到不同盐值与不同哈希
    # 实现 SYS-BACKEND-016 的断言
