// 本文件由 tests/generate.py 从 tests/registry/ 生成，测试名与用例 ID 一一对应。
// 用例的 given / when / then 见注释，断言在此实现。
// 实现一条用例时删除该条的 skip 参数。

import 'package:integration_test/integration_test.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  // SYS-C-004 [P0] 恢复为 AI 总结清空用户总结字段并还原来源标识
  // 需求 REQ-16-10 / 章节 4.8
  // 屏幕 C7, C3
  // given: 某日已有用户总结与 AI 原始总结
  // when: 点击恢复为 AI 总结并保存
  // then: 输入框内容替换为 AI 原始总结
  // then: 保存后用户总结字段清空，卡片来源标识回到「AI」
  // then: AI 原始总结为空时该按钮为禁用态
  testWidgets('恢复为 AI 总结', (tester) async {
    // 实现 SYS-C-004 的断言
  }, skip: 'SYS-C-004 待实现');

  // SYS-C-006 [P1] 无评估的日期允许编辑总结并在卡片上展示
  // 需求 REQ-16-10 / 章节 4.8
  // 屏幕 C4, C7
  // given: 某日期评估状态为待评估且无 AI 总结
  // when: 编辑并保存用户总结
  // then: 保存成功，用户总结写入该日期
  // then: 卡片一句话总结状态展示该总结并带「已编辑」标识
  // then: 恢复为 AI 总结按钮保持禁用态
  testWidgets('无评估日编辑总结', (tester) async {
    // 实现 SYS-C-006 的断言
  }, skip: 'SYS-C-006 待实现');

}
