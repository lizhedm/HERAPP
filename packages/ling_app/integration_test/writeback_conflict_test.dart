// 本文件由 tests/generate.py 从 tests/registry/ 生成，测试名与用例 ID 一一对应。
// 用例的 given / when / then 见注释，断言在此实现。
// 实现一条用例时删除该条的 skip 参数。

import 'package:integration_test/integration_test.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  // SYS-A-022 [P0] 同步以远端版本覆盖本地缓存并在覆盖本地编辑时提示
  // 需求 REQ-16-49 / 章节 3.11
  // 屏幕 D1, C6
  // given: 某日总结在本端已编辑并回写成功，随后该条在另一端被改为更新的版本
  // when: 本端执行同步
  // then: 远端版本覆盖本地缓存，界面展示远端版本
  // then: 本地编辑被覆盖时提示「该条内容已在其他设备上更新，已显示最新版本」
  // then: 回写队列中尚未提交的编辑不被同步清除
  testWidgets('远端覆盖与提示', (tester) async {
    // 实现 SYS-A-022 的断言
  }, skip: 'SYS-A-022 待实现');

}
