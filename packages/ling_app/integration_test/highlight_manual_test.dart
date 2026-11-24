// 本文件由 tests/generate.py 从 tests/registry/ 生成，测试名与用例 ID 一一对应。
// 用例的 given / when / then 见注释，断言在此实现。
// 实现一条用例时删除该条的 skip 参数。

import 'package:integration_test/integration_test.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  // SYS-G-003 [P0] 手动标记高光写入记录并在列表中可见
  // 需求 REQ-16-17 / 章节 8.2
  // 屏幕 D1, G1
  // given: 某日评估成功但未自动触发高光
  // when: 在日详情页手动标记为高光
  // then: 该日出现在高光列表中
  // then: 记录标明来源为手动标记
  // then: 重新评估不覆盖手动标记
  testWidgets('手动标记高光', (tester) async {
    // 实现 SYS-G-003 的断言
  }, skip: 'SYS-G-003 待实现');

}
