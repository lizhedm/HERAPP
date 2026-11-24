// 本文件由 tests/generate.py 从 tests/registry/ 生成，测试名与用例 ID 一一对应。
// 用例的 given / when / then 见注释，断言在此实现。
// 实现一条用例时删除该条的 skip 参数。

import 'package:flutter_test/flutter_test.dart';

void main() {
  // SYS-F-002 [P0] 喜好条目字段默认值与星级取值范围
  // 需求 REQ-16-20 / 章节 10.2
  // 屏幕 F2
  // given: 打开新增喜好表单
  // when: 观察初始状态
  // then: 类型默认为喜欢，分类默认为其他，星级默认为 3 星
  // then: 星级取值为 1-5 星
  // then: 备注上限 200 字，图片与共同喜好标记为可选
  testWidgets('表单默认值', (tester) async {
    // 实现 SYS-F-002 的断言
  }, skip: 'SYS-F-002 待实现');

  // SYS-F-003 [P0] 喜好名称为空时保存禁用，点击后显示字段级红色提示
  // 需求 REQ-16-28 / 章节 10.3
  // 屏幕 F2
  // given: 新增喜好表单，名称为空
  // when: 点击置灰的保存按钮后开始输入名称
  // then: 保存按钮为禁用态
  // then: 点击后名称输入框下方显示红色提示「请填写喜好名称」且边框变红
  // then: 开始输入后提示自动消失、边框恢复，保存按钮变为可用
  testWidgets('名称必填校验', (tester) async {
    // 实现 SYS-F-003 的断言
  }, skip: 'SYS-F-003 待实现');

}
