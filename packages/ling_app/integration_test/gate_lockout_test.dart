// 本文件由 tests/generate.py 从 tests/registry/ 生成，测试名与用例 ID 一一对应。
// 用例的 given / when / then 见注释，断言在此实现。
// 实现一条用例时删除该条的 skip 参数。

import 'package:integration_test/integration_test.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  // SYS-A-015 [P0] 连续错误 5 次锁定 60 秒且跨重启继续生效
  // 需求 REQ-16-42 / 章节 3.10
  // 屏幕 A2, A3
  // given: 处于门禁页，错误次数为 0
  // when: 连续输入 5 次错误密码，重启应用，倒计时结束后再输错一次
  // then: 第 5 次错误后进入锁定态，输入框禁用并显示剩余秒数
  // then: 重启应用后锁定态与剩余秒数继续生效，重启不绕过锁定
  // then: 倒计时结束后输入框恢复可用
  // then: 恢复后再次输错立即重新锁定 60 秒
  testWidgets('错误锁定与跨重启', (tester) async {
    // 实现 SYS-A-015 的断言
  }, skip: 'SYS-A-015 待实现');

}
