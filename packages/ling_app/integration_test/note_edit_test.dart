// 本文件由 tests/generate.py 从 tests/registry/ 生成，测试名与用例 ID 一一对应。
// 用例的 given / when / then 见注释，断言在此实现。
// 实现一条用例时删除该条的 skip 参数。

import 'package:integration_test/integration_test.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  // SYS-C-007 [P0] 备注上限 200 字且非空时卡片显示备注图标
  // 需求 REQ-16-11 / 章节 4.9
  // 屏幕 C7, C1
  // given: 进入添加备注页
  // when: 输入 200 字保存，再输入第 201 字
  // then: 实时显示已输入字数，200 字时保存按钮可用
  // then: 超过 200 字时保存按钮为禁用态并提示「备注不超过 200 字」
  // then: 备注非空时日卡片两态均在角标区显示备注图标
  // then: 未保存退出弹出文案「备注尚未保存，确认放弃修改？」的二次确认
  testWidgets('备注字数与标记', (tester) async {
    // 实现 SYS-C-007 的断言
  }, skip: 'SYS-C-007 待实现');

}
