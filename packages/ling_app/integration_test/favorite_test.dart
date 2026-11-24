// 本文件由 tests/generate.py 从 tests/registry/ 生成，测试名与用例 ID 一一对应。
// 用例的 given / when / then 见注释，断言在此实现。
// 实现一条用例时删除该条的 skip 参数。

import 'package:integration_test/integration_test.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  // SYS-C-002 [P1] 收藏切换后关闭面板并刷新卡片标记
  // 需求 REQ-16-09 / 章节 4.7
  // 屏幕 C6, C1
  // given: 某日期未收藏
  // when: 长按卡片点击收藏，再次长按点击取消收藏
  // then: 收藏后面板关闭，卡片角标区出现收藏标记
  // then: 取消收藏后标记移除
  // then: 收藏状态持久化，重新进入月视图后保持
  testWidgets('收藏切换与持久化', (tester) async {
    // 实现 SYS-C-002 的断言
  }, skip: 'SYS-C-002 待实现');

}
