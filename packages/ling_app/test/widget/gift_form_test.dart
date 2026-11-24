// 本文件由 tests/generate.py 从 tests/registry/ 生成，测试名与用例 ID 一一对应。
// 用例的 given / when / then 见注释，断言在此实现。
// 实现一条用例时删除该条的 skip 参数。

import 'package:flutter_test/flutter_test.dart';

void main() {
  // SYS-F-021 [P0] 礼物表单必填项有默认值，名称为空时保存禁用
  // 需求 REQ-16-28 / 章节 11.1, 11.2
  // 屏幕 F9
  // given: 打开新增礼物表单
  // when: 观察初始状态并点击置灰的保存按钮
  // then: 分类默认为其他、等级默认为小、场合默认为日常、状态默认为想法、优先级默认为中，表单打开即为已选中
  // then: 预算档默认为待设定
  // then: 名称为空时保存按钮置灰，点击后显示红色提示「请填写礼物名称」
  // then: 礼物分类表达用途、礼物等级表达规模，两个字段独立保存
  testWidgets('礼物表单默认值与校验', (tester) async {
    // 实现 SYS-F-021 的断言
  }, skip: 'SYS-F-021 待实现');

}
