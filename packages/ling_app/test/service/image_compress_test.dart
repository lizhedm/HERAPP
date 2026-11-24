// 本文件由 tests/generate.py 从 tests/registry/ 生成，测试名与用例 ID 一一对应。
// 用例的 given / when / then 见注释，断言在此实现。
// 实现一条用例时删除该条的 skip 参数。

import 'package:flutter_test/flutter_test.dart';

void main() {
  // SYS-F-012 [P0] 条目图片按 1:1 裁剪并压缩为长边不超过 1600 的 JPEG
  // 需求 REQ-16-51 / 章节 3.12
  // 屏幕 F2, F9
  // given: 从相册选择一张长边超过 1600 像素的 HEIC 图片
  // when: 完成 1:1 裁剪并确认
  // then: 长边按比例缩放至上限，不足上限的图片保持原尺寸
  // then: 统一转码为 JPEG，HEIC 在此步转为 JPEG
  // then: 剥离地理位置、设备型号与时间戳，按朝向旋转像素后写入正向图
  // then: 压缩结果超过体积上限时按递降的质量重压，仍超限则提示换一张
  // then: 非 JPEG、PNG、HEIC、WebP 的文件在选择阶段即被拒绝并给出格式提示
  test('裁剪与压缩口径', () {
    // 实现 SYS-F-012 的断言
  }, skip: 'SYS-F-012 待实现');

}
