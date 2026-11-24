// 本文件由 tests/generate.py 从 tests/registry/ 生成，测试名与用例 ID 一一对应。
// 用例的 given / when / then 见注释，断言在此实现。
// 实现一条用例时删除该条的 skip 参数。

import 'package:flutter_test/flutter_test.dart';

void main() {
  // SYS-H-009 [P2] 关于页同屏展示五条版本轴与资源来源说明
  // 需求 REQ-16-29, REQ-16-33 / 章节 12.6
  // 屏幕 H6
  // given: 进入关于页
  // when: 浏览页面
  // then: 展示应用名称 LingLing
  // then: 同屏展示 appVersion、schemaVersion、ruleVersion、promptVersion、coverPoolVersion 五个版本号
  // then: 五个版本号各自独立取值，互不换算
  // then: 展示封面资源来源说明，标注资源为原创角色或已授权 IP
  // then: 展示数据来源说明与本地数据存储位置说明
  testWidgets('关于页字段', (tester) async {
    // 实现 SYS-H-009 的断言
  }, skip: 'SYS-H-009 待实现');

}
