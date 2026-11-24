// 本文件由 tests/generate.py 从 tests/registry/ 生成，测试名与用例 ID 一一对应。
// 用例的 given / when / then 见注释，断言在此实现。
// 实现一条用例时删除该条的 skip 参数。

import 'package:integration_test/integration_test.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  // SYS-F-008 [P0] 加入礼物清单带入名称含优先级字段并跳转礼物 Tab
  // 需求 REQ-16-23 / 章节 10.7
  // 屏幕 F4, F6, F8
  // given: 某喜好条目，礼物列表已设置筛选条件
  // when: 在长按面板选择加入礼物清单，填写表单并保存
  // then: 表单自动带入喜好名称，含分类、等级、场合、预算档、状态、优先级、计划日期、备注字段
  // then: 保存后跳转礼物 Tab 并定位到新建条目
  // then: 跳转前清除礼物列表的全部筛选条件并重置筛选状态，确保新建条目可见
  // then: 一个喜好可生成多个礼物条目，礼物保留关联喜好 ID
  testWidgets('加入礼物清单跳转', (tester) async {
    // 实现 SYS-F-008 的断言
  }, skip: 'SYS-F-008 待实现');

}
