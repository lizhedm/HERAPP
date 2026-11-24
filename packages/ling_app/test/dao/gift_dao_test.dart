// 本文件由 tests/generate.py 从 tests/registry/ 生成，测试名与用例 ID 一一对应。
// 用例的 given / when / then 见注释，断言在此实现。
// 实现一条用例时删除该条的 skip 参数。

import 'package:flutter_test/flutter_test.dart';

void main() {
  // SYS-F-020 [P0] 礼物默认按计划日期升序，无日期条目排在最后
  // 需求 REQ-16-24 / 章节 11.3
  // 屏幕 F8
  // given: 若干礼物条目，部分有计划日期、部分无计划日期
  // when: 按默认排序查询礼物列表
  // then: 有计划日期的条目按日期升序排在前
  // then: 无计划日期的条目排在最后，其中按更新时间降序
  // then: 主列表隐藏已取消与已归档状态的条目
  test('礼物默认排序', () {
    // 实现 SYS-F-020 的断言
  }, skip: 'SYS-F-020 待实现');

}
