// 本文件由 tests/generate.py 从 tests/registry/ 生成，测试名与用例 ID 一一对应。
// 用例的 given / when / then 见注释，断言在此实现。
// 实现一条用例时删除该条的 skip 参数。

import 'package:flutter_test/flutter_test.dart';

void main() {
  // SYS-F-004 [P0] 内置分类为固定 26 项，编辑与删除只对自定义分类开放
  // 需求 REQ-16-21 / 章节 10.4
  // 屏幕 F3
  // given: 进入分类管理页
  // when: 分别对内置分类与自定义分类尝试编辑与删除
  // then: 内置分类共 26 项，均可选择
  // then: 内置分类不提供编辑与删除操作
  // then: 自定义分类可编辑名称、可删除
  // then: 分类选择器底部提供新增分类入口
  testWidgets('内置与自定义分类权限', (tester) async {
    // 实现 SYS-F-004 的断言
  }, skip: 'SYS-F-004 待实现');

}
