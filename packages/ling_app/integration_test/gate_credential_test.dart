// 本文件由 tests/generate.py 从 tests/registry/ 生成，测试名与用例 ID 一一对应。
// 用例的 given / when / then 见注释，断言在此实现。
// 实现一条用例时删除该条的 skip 参数。

import 'package:integration_test/integration_test.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  // SYS-A-016 [P0] 密码哈希由后端下发并在每次成功同步后刷新，本地比对不依赖网络
  // 需求 REQ-16-43 / 章节 3.10
  // 屏幕 A2
  // given: 首次安装尚未成功同步，随后后台修改访问密码并完成一次同步
  // when: 依次在同步前、同步后、断网状态下校验密码
  // then: 尚未取到后端哈希时用配置文件内置的默认密码哈希校验，首次进入可用
  // then: 同步成功后缓存的哈希与盐值刷新，新密码生效且旧密码失效
  // then: 哈希与盐值存入系统安全存储，后端不下发明文
  // then: 断网状态下门禁照常校验，不发起网络请求
  testWidgets('哈希下发与刷新', (tester) async {
    // 实现 SYS-A-016 的断言
  }, skip: 'SYS-A-016 待实现');

}
