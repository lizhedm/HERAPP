// 本文件由 tests/generate.py 从 tests/registry/ 生成，测试名与用例 ID 一一对应。
// 用例的 given / when / then 见注释，断言在此实现。
// 实现一条用例时删除该条的 skip 参数。

import 'package:integration_test/integration_test.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  // SYS-F-022 [P0] 礼物状态支持任意跳转与回退并自动写入送出日期
  // 需求 REQ-16-25 / 章节 11.4
  // 屏幕 F10
  // given: 某礼物状态为想法
  // when: 直接跳转到已送出，再回退到待购买，再跳转到已收到
  // then: 状态选择浮层列出全部状态供直接选择，支持任意跳转与回退
  // then: 变更为已送出时自动写入当天日期为送出日期
  // then: 变更为已收到时送出日期为空则自动写入当天日期
  // then: 送出日期可手动修改，并在条目详情与列表项上展示
  testWidgets('状态流转与送出日期', (tester) async {
    // 实现 SYS-F-022 的断言
  }, skip: 'SYS-F-022 待实现');

}
