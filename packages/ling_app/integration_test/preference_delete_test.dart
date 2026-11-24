// 本文件由 tests/generate.py 从 tests/registry/ 生成，测试名与用例 ID 一一对应。
// 用例的 given / when / then 见注释，断言在此实现。
// 实现一条用例时删除该条的 skip 参数。

import 'package:integration_test/integration_test.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  // SYS-F-007 [P0] 长按删除喜好有二次确认，关联礼物保留并断开关联
  // 需求 REQ-16-20 / 章节 10.6
  // 屏幕 F4, F12
  // given: 某喜好已生成 2 个关联礼物条目
  // when: 长按该喜好选择删除并确认
  // then: 弹出二次确认，文案为「删除后不可恢复，确认删除「XXX」？」
  // then: 确认后喜好删除，2 个礼物条目保留且关联喜好 ID 置空
  // then: 礼物详情的来源追溯显示「来源喜好已删除」
  testWidgets('删除喜好断开关联', (tester) async {
    // 实现 SYS-F-007 的断言
  }, skip: 'SYS-F-007 待实现');

}
