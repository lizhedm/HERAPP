# LingLing 需求追溯矩阵

本文件由 `tests/generate.py` 从 `tests/registry/` 生成，改动用例清单后重新生成。
每条需求验收标准至少对应一条用例，每条用例对应一个可定位的测试标识。
`tests/validate.py` 在 CI 中强制这两条性质，覆盖缺口会阻断合并。

需求验收标准 39 条，用例 141 条，测试标识 141 个。

## 需求 → 用例 → 屏幕 → 测试

| 需求编号 | 用例 ID | 优先级 | 层 | 屏幕 | 用例标题 | 测试标识 |
| --- | --- | --- | --- | --- | --- | --- |
| REQ-16-01 | SYS-A-001 | P0 | widget | A1 | 启动页在 8 秒内完成配置加载后按自动同步开关分流 | `packages/ling_app/test/widget/splash_test.dart::配置加载成功分流` |
| REQ-16-01 | SYS-A-002 | P0 | widget | A1, A2 | 配置加载超过 8 秒展示超时态并支持重新计时 | `packages/ling_app/test/widget/splash_test.dart::配置加载超时` |
| REQ-16-01 | SYS-BACKEND-014 | P0 | contract | — | OpenAPI 契约与后端实现双向一致 | `backend/tests/test_contract.py::双向契约一致` |
| REQ-16-01 | SYS-PERF-001 | P0 | perf | A1, B3, D1, E1 | 启动配置加载、月视图、日详情、趋势页满足性能预算 | `packages/ling_app/test/perf/budget_test.dart::性能预算全项` |
| REQ-16-02 | SYS-A-003 | P0 | widget | A3 | 配置缺失进入待配置态，操作限于重新加载与查看说明 | `packages/ling_app/test/widget/pending_config_test.dart::待配置只读提示` |
| REQ-16-02 | SYS-A-004 | P0 | widget | A4 | 同步返回 401 或 403 进入鉴权失败态并提供离线查看 | `packages/ling_app/test/widget/auth_failed_test.dart::鉴权失败提示与离线查看` |
| REQ-16-02 | SYS-A-008 | P0 | widget | A7 | 同步失败展示原因分类与最近同步时间 | `packages/ling_app/test/widget/sync_failed_test.dart::失败原因分类` |
| REQ-16-03 | SYS-A-005 | P0 | widget | A5 | 同步中展示 5 个阶段与批量进度且不阻塞浏览 | `packages/ling_app/test/widget/syncing_test.dart::同步阶段与进度` |
| REQ-16-03 | SYS-A-006 | P0 | integration | A5, A6 | 取消同步保留已落盘日期并清空待执行评估队列 | `packages/ling_app/integration_test/sync_cancel_test.dart::取消同步落盘与队列` |
| REQ-16-03 | SYS-A-007 | P0 | integration | A6 | 继续同步从未完成日期断点续传并重新入队评估 | `packages/ling_app/integration_test/sync_cancel_test.dart::断点续传` |
| REQ-16-03 | SYS-A-010 | P1 | widget | B3, H1 | 后台同步保持当前页面并以轻提示呈现 | `packages/ling_app/test/widget/background_sync_test.dart::后台同步轻提示` |
| REQ-16-03 | SYS-A-011 | P0 | integration | — | 聊天文件以远端为权威，用户数据同步不覆盖 | `packages/ling_app/integration_test/sync_conflict_test.dart::用户数据不被覆盖` |
| REQ-16-03 | SYS-BACKEND-014 | P0 | contract | — | OpenAPI 契约与后端实现双向一致 | `backend/tests/test_contract.py::双向契约一致` |
| REQ-16-03 | SYS-PERF-002 | P1 | perf | A5 | 全量同步峰值内存不超过预算 | `packages/ling_app/test/perf/sync_memory_test.dart::同步内存预算` |
| REQ-16-04 | SYS-A-009 | P0 | integration | A8 | 部分成功展示失败日期列表并支持单日与批量重试 | `packages/ling_app/integration_test/partial_success_test.dart::单日与批量重试` |
| REQ-16-04 | SYS-A-012 | P1 | backend | A8 | 清单与日文件按约定格式解析，字段缺失时该日期标记失败 | `backend/tests/test_importer.py::文件格式解析与容错` |
| REQ-16-04 | SYS-D-016 | P1 | integration | D7b, D1 | 同步这一天仅拉取该日期并刷新页面状态 | `packages/ling_app/integration_test/single_day_sync_test.dart::单日同步` |
| REQ-16-04 | SYS-H-010 | P0 | integration | H8, H1 | 失败日期列表支持单日与批量重试并在清空后隐藏入口 | `packages/ling_app/integration_test/failed_dates_test.dart::失败列表重试与清空` |
| REQ-16-05 | SYS-B-001 | P0 | integration | B1, B2, B3, D1 | 时间墙层级为年视图到月份选择页到月视图到日详情 | `packages/ling_app/integration_test/timewall_nav_test.dart::时间墙层级下钻` |
| REQ-16-05 | SYS-B-002 | P0 | widget | B1 | 年份卡片展示 5 项摘要且均分口径仅含已评估日期 | `packages/ling_app/test/widget/year_view_test.dart::年份卡片摘要` |
| REQ-16-05 | SYS-B-004 | P0 | widget | B2 | 月份选择页为 12 格宫格，无记录月份为禁用态 | `packages/ling_app/test/widget/month_picker_test.dart::月份宫格状态` |
| REQ-16-06 | SYS-B-005 | P0 | widget | B3 | 月视图日卡片 2 列排列且顶部切换器可切换月份 | `packages/ling_app/test/widget/month_view_test.dart::月视图布局与切换` |
| REQ-16-06 | SYS-B-006 | P0 | widget | B3, C1, C2, C3, D1 | 卡片主体点击切换三态，右下角箭头进入日详情 | `packages/ling_app/test/widget/day_card_test.dart::卡片点击区域分工` |
| REQ-16-06 | SYS-B-010 | P0 | widget | C1, C2, C3 | 三态各自展示约定的字段与角标 | `packages/ling_app/test/widget/day_card_test.dart::三态字段与角标` |
| REQ-16-06 | SYS-B-013 | P0 | widget | C5, C6, D7b | 未同步日卡片为禁用态，不参与三态循环但可长按 | `packages/ling_app/test/widget/day_card_test.dart::未同步卡片行为` |
| REQ-16-06 | SYS-B-015 | P1 | perf | B3 | 月视图在 500 毫秒内完成首帧，滚动保持 16 毫秒帧预算 | `packages/ling_app/test/perf/month_view_perf_test.dart::月视图渲染预算` |
| REQ-16-06 | SYS-PERF-001 | P0 | perf | A1, B3, D1, E1 | 启动配置加载、月视图、日详情、趋势页满足性能预算 | `packages/ling_app/test/perf/budget_test.dart::性能预算全项` |
| REQ-16-07 | SYS-B-007 | P0 | widget | B3, C1, C2, C3 | 卡片三态按张独立切换，切换单张不影响同屏其他卡片 | `packages/ling_app/test/widget/day_card_test.dart::三态按张独立` |
| REQ-16-07 | SYS-B-008 | P0 | integration | B3, H4 | 进入月视图按设置页默认卡片状态初始化，离开后不持久化 | `packages/ling_app/integration_test/card_state_test.dart::默认状态初始化` |
| REQ-16-08 | SYS-B-011 | P0 | widget | C3, C4 | 总结来源标识区分已编辑与 AI，空总结按两种情形取文案 | `packages/ling_app/test/widget/day_card_test.dart::总结来源与空文案` |
| REQ-16-08 | SYS-B-012 | P1 | widget | C1, D5 | 待重评卡片按上次成功结果展示并增加待重评标识 | `packages/ling_app/test/widget/day_card_test.dart::待重评卡片展示` |
| REQ-16-08 | SYS-B-014 | P2 | widget | C5 | 未同步日已有用户总结时占位区展示该总结 | `packages/ling_app/test/widget/day_card_test.dart::未同步日用户总结` |
| REQ-16-08 | SYS-C-008 | P0 | widget | C4 | 评估缺失卡片展示降级内容并提供操作提示 | `packages/ling_app/test/widget/day_card_test.dart::评估缺失降级` |
| REQ-16-08 | SYS-D-012 | P1 | widget | D3 | 评估中展示加载态且对话流保持可读 | `packages/ling_app/test/widget/day_detail_test.dart::评估中加载态` |
| REQ-16-08 | SYS-D-013 | P0 | widget | D4 | 评估失败展示失败状态与重试入口 | `packages/ling_app/test/widget/day_detail_test.dart::评估失败重试` |
| REQ-16-09 | SYS-C-001 | P0 | widget | C6 | 长按动作面板含收藏、编辑总结、添加备注与取消 | `packages/ling_app/test/widget/day_card_actions_test.dart::动作面板项目` |
| REQ-16-09 | SYS-C-002 | P1 | integration | C6, C1 | 收藏切换后关闭面板并刷新卡片标记 | `packages/ling_app/integration_test/favorite_test.dart::收藏切换与持久化` |
| REQ-16-09 | SYS-D-011 | P0 | integration | D1, D3 | 重新评估覆盖 AI 结果并刷新版本与元数据字段 | `packages/ling_app/integration_test/re_evaluate_test.dart::重新评估字段刷新` |
| REQ-16-10 | SYS-C-003 | P0 | widget | C7 | 编辑总结上限 50 字，超出后保存按钮为禁用态 | `packages/ling_app/test/widget/summary_edit_test.dart::总结字数上限` |
| REQ-16-10 | SYS-C-004 | P0 | integration | C7, C3 | 恢复为 AI 总结清空用户总结字段并还原来源标识 | `packages/ling_app/integration_test/summary_edit_test.dart::恢复为 AI 总结` |
| REQ-16-10 | SYS-C-005 | P1 | widget | C7 | 总结未保存退出有二次确认 | `packages/ling_app/test/widget/summary_edit_test.dart::未保存二次确认` |
| REQ-16-10 | SYS-C-006 | P1 | integration | C4, C7 | 无评估的日期允许编辑总结并在卡片上展示 | `packages/ling_app/integration_test/summary_edit_test.dart::无评估日编辑总结` |
| REQ-16-11 | SYS-C-007 | P0 | integration | C8, C1 | 备注上限 200 字且非空时卡片显示备注图标 | `packages/ling_app/integration_test/note_edit_test.dart::备注字数与标记` |
| REQ-16-12 | SYS-D-001 | P0 | widget | D2 | 互动统计按需求顺序呈现 12 项且占比项使用堆叠条 | `packages/ling_app/test/widget/day_stats_test.dart::互动统计 12 项顺序` |
| REQ-16-12 | SYS-D-002 | P1 | widget | D2, D7a | 消息条数为 0 时 12 项统计全部显示占位符 | `packages/ling_app/test/widget/day_stats_test.dart::零消息统计占位` |
| REQ-16-12 | SYS-D-003 | P1 | service | D1, D2 | 系统消息不计入任何统计项与对话段判定 | `packages/ling_app/test/service/stats_service_test.dart::系统消息排除` |
| REQ-16-12 | SYS-D-010 | P0 | widget | D1 | 日详情对话流以气泡呈现并左右区分双方 | `packages/ling_app/test/widget/day_detail_test.dart::对话流呈现` |
| REQ-16-12 | SYS-D-015 | P0 | widget | D7a, D7b | 当日无消息与该日未同步为两种独立空状态 | `packages/ling_app/test/widget/day_detail_test.dart::两种空状态区分` |
| REQ-16-12 | SYS-D-018 | P1 | perf | D1 | 日详情在 300 毫秒内完成首帧 | `packages/ling_app/test/perf/day_detail_perf_test.dart::日详情渲染预算` |
| REQ-16-12 | SYS-PERF-001 | P0 | perf | A1, B3, D1, E1 | 启动配置加载、月视图、日详情、趋势页满足性能预算 | `packages/ling_app/test/perf/budget_test.dart::性能预算全项` |
| REQ-16-12 | SYS-RULE-040 | P0 | rule | D2 | 字数口径为 TEXT 类型内容的 Unicode 码点数且不含首尾空白 | `packages/ling_core/test/stats_test.dart::字数口径` |
| REQ-16-12 | SYS-RULE-041 | P0 | rule | D2 | 连续对话段按 30 分钟间隔切分，恰好 30 分钟归入同一段 | `packages/ling_core/test/stats_test.dart::对话段切分` |
| REQ-16-12 | SYS-RULE-042 | P1 | rule | D2 | 最长连续对话条数取各段条数的最大值 | `packages/ling_core/test/stats_test.dart::最长连续对话` |
| REQ-16-13 | SYS-BACKEND-005 | P0 | backend | D4 | AI 输出 JSON 解析失败记录失败状态并保留重试入口 | `backend/tests/test_ai_client.py::JSON 解析失败处理` |
| REQ-16-13 | SYS-BACKEND-013 | P1 | widget | D6 | 置信度低于 40 时日详情显示低置信度提示且分数照常展示 | `packages/ling_app/test/widget/day_detail_test.dart::低置信度提示` |
| REQ-16-13 | SYS-RULE-005 | P0 | rule | D6 | 置信度低于 40 时日天气为雾并遮蔽综合分区间 | `packages/ling_core/test/weather_test.dart::雾优先级` |
| REQ-16-14 | SYS-H-008 | P1 | widget | H6 | 规则说明页同时展示封面与天气两套规则并标注区别 | `packages/ling_app/test/widget/rules_page_test.dart::两套规则同屏展示` |
| REQ-16-14 | SYS-RULE-001 | P0 | rule | — | 天气综合分按总分 0.5、情绪 0.3、亲密 0.2 加权并四舍五入 | `packages/ling_core/test/weather_test.dart::天气综合分加权` |
| REQ-16-14 | SYS-RULE-002 | P0 | rule | — | 天气综合分与封面综合关系分对同一组分数互不影响 | `packages/ling_core/test/composite_isolation_test.dart::双综合分独立` |
| REQ-16-14 | SYS-RULE-045 | P0 | rule | — | 四舍五入在 0.5 边界向上进位，与语言内置银行家舍入区分 | `packages/ling_core/test/stats_test.dart::四舍五入口径` |
| REQ-16-15 | SYS-D-014 | P1 | widget | D5 | 待重评展示状态提示并沿用上次成功结果 | `packages/ling_app/test/widget/day_detail_test.dart::待重评状态提示` |
| REQ-16-15 | SYS-RULE-003 | P0 | rule | — | 天气综合分区间映射在每个区间端点取到唯一天气 | `packages/ling_core/test/weather_test.dart::天气区间端点` |
| REQ-16-15 | SYS-RULE-004 | P0 | rule | C4, C5, D7a, D7b, D8 | 日天气优先级 1 待评估覆盖未同步、零消息与未完成评估三种情形 | `packages/ling_core/test/weather_test.dart::待评估优先级` |
| REQ-16-15 | SYS-RULE-005 | P0 | rule | D6 | 置信度低于 40 时日天气为雾并遮蔽综合分区间 | `packages/ling_core/test/weather_test.dart::雾优先级` |
| REQ-16-15 | SYS-RULE-006 | P0 | rule | — | 消息少于 10 条且情绪分不低于 50 时日天气为雪并遮蔽综合分区间 | `packages/ling_core/test/weather_test.dart::雪优先级` |
| REQ-16-15 | SYS-RULE-008 | P1 | rule | D5 | STALE 日期沿用上次成功评估的分数参与天气判定 | `packages/ling_core/test/weather_test.dart::STALE 沿用上次结果` |
| REQ-16-16 | SYS-RULE-007 | P0 | rule | B1, B2, B3, E1 | 周期天气取该周期天气综合分平均值并跳过雾与雪规则 | `packages/ling_core/test/weather_test.dart::周期天气` |
| REQ-16-17 | SYS-G-001 | P0 | widget | G1 | 高光列表按日期倒序展示并显示类型标识 | `packages/ling_app/test/widget/highlight_list_test.dart::高光列表排序` |
| REQ-16-17 | SYS-G-002 | P1 | widget | G3 | 高光列表按类型筛选后仅保留命中类型 | `packages/ling_app/test/widget/highlight_list_test.dart::高光类型筛选` |
| REQ-16-17 | SYS-G-003 | P0 | integration | D1, G1 | 手动标记高光写入记录并在列表中可见 | `packages/ling_app/integration_test/highlight_manual_test.dart::手动标记高光` |
| REQ-16-17 | SYS-G-004 | P1 | widget | G1, G2 | 长按删除高光有二次确认，取消后记录保留 | `packages/ling_app/test/widget/highlight_list_test.dart::删除高光二次确认` |
| REQ-16-17 | SYS-G-005 | P2 | widget | G4 | 无高光时展示空状态并说明触发条件 | `packages/ling_app/test/widget/highlight_list_test.dart::高光空状态` |
| REQ-16-17 | SYS-RULE-020 | P0 | rule | G1 | 高光触发条件为总分不低于 85 且情绪分不低于 70，或总分不低于 90 | `packages/ling_core/test/highlight_test.dart::高光触发条件` |
| REQ-16-17 | SYS-RULE-021 | P0 | rule | G1, G3 | 高光类型按 5 条优先级判定，前一条命中即停止 | `packages/ling_core/test/highlight_test.dart::高光类型优先级` |
| REQ-16-18 | SYS-B-009 | P1 | widget | B4, E1 | 周定位态高亮该周 7 张卡片并插入周摘要行 | `packages/ling_app/test/widget/month_view_test.dart::周定位态` |
| REQ-16-18 | SYS-E-001 | P0 | widget | E1, E2 | 趋势页曲线与情绪日历为 Tab 切换且各自保留粒度 | `packages/ling_app/test/widget/trend_page_test.dart::趋势 Tab 切换` |
| REQ-16-18 | SYS-E-002 | P0 | widget | E1 | 曲线在缺评估日期处断开而非插值 | `packages/ling_app/test/widget/trend_page_test.dart::曲线断点` |
| REQ-16-18 | SYS-E-003 | P1 | widget | E1, B3, B4, D1 | 点击曲线数据点跳转该点对应周期 | `packages/ling_app/test/widget/trend_page_test.dart::数据点跳转` |
| REQ-16-18 | SYS-E-006 | P2 | widget | E4 | 趋势页无评估数据时展示空状态并引导同步 | `packages/ling_app/test/widget/trend_page_test.dart::趋势空状态` |
| REQ-16-18 | SYS-PERF-001 | P0 | perf | A1, B3, D1, E1 | 启动配置加载、月视图、日详情、趋势页满足性能预算 | `packages/ling_app/test/perf/budget_test.dart::性能预算全项` |
| REQ-16-18 | SYS-RULE-043 | P0 | rule | E1, E2 | 周期键按 ISO 8601 计算，周一为周首且跨年周归属正确 | `packages/ling_core/test/stats_test.dart::周期键计算` |
| REQ-16-18 | SYS-RULE-044 | P0 | rule | E1 | 趋势聚合取已评估日期的算术平均并四舍五入，空周期缺失 | `packages/ling_core/test/stats_test.dart::趋势聚合` |
| REQ-16-19 | SYS-E-004 | P0 | widget | E2 | 情绪日历按色系与明度着色并支持点击进入日详情 | `packages/ling_app/test/widget/emotion_calendar_test.dart::日历着色` |
| REQ-16-19 | SYS-E-005 | P2 | widget | E3 | 情绪色系速查页列出 6 色系与 30 种情绪的完整对应 | `packages/ling_app/test/widget/emotion_legend_test.dart::色系速查完整性` |
| REQ-16-19 | SYS-RULE-030 | P0 | rule | E2, E3 | 30 种情绪完整映射到 6 个色系，无遗漏无重复归属 | `packages/ling_core/test/emotion_test.dart::情绪色系全映射` |
| REQ-16-19 | SYS-RULE-031 | P0 | rule | E2, E3 | 情绪分决定明度档，4 个区间在端点取到唯一明度 | `packages/ling_core/test/emotion_test.dart::情绪明度端点` |
| REQ-16-19 | SYS-RULE-032 | P0 | rule | E2 | 待评估日期情绪着色为中性灰且不带明度 | `packages/ling_core/test/emotion_test.dart::待评估中性灰` |
| REQ-16-20 | SYS-F-001 | P0 | dao | F1 | 喜好默认按星级降序排列，星级相同按更新时间降序 | `packages/ling_app/test/dao/preference_dao_test.dart::默认排序` |
| REQ-16-20 | SYS-F-002 | P0 | widget | F2 | 喜好条目字段默认值与星级取值范围 | `packages/ling_app/test/widget/preference_form_test.dart::表单默认值` |
| REQ-16-20 | SYS-F-007 | P0 | integration | F4, F12 | 长按删除喜好有二次确认，关联礼物保留并断开关联 | `packages/ling_app/integration_test/preference_delete_test.dart::删除喜好断开关联` |
| REQ-16-20 | SYS-F-011 | P2 | widget | F7 | 喜好空状态与无匹配结果为两套文案 | `packages/ling_app/test/widget/preference_list_test.dart::喜好空状态区分` |
| REQ-16-20 | SYS-F-028 | P1 | widget | F1, F8 | 喜好与礼物为同一页面的两个 Tab | `packages/ling_app/test/widget/preference_page_test.dart::双 Tab 结构` |
| REQ-16-21 | SYS-F-004 | P0 | widget | F3 | 内置分类为固定 26 项，编辑与删除只对自定义分类开放 | `packages/ling_app/test/widget/category_manage_test.dart::内置与自定义分类权限` |
| REQ-16-21 | SYS-F-005 | P0 | integration | F3, F5 | 删除自定义分类后相关喜好重置为其他并清理筛选条件 | `packages/ling_app/integration_test/category_delete_test.dart::删除分类级联处理` |
| REQ-16-22 | SYS-F-006 | P0 | integration | F1, F5 | 共同喜好为标记字段，5 种状态通过筛选查看 | `packages/ling_app/integration_test/common_status_test.dart::共同喜好状态语义` |
| REQ-16-23 | SYS-F-008 | P0 | integration | F4, F6, F8 | 加入礼物清单带入名称含优先级字段并跳转礼物 Tab | `packages/ling_app/integration_test/add_gift_test.dart::加入礼物清单跳转` |
| REQ-16-24 | SYS-F-020 | P0 | dao | F8 | 礼物默认按计划日期升序，无日期条目排在最后 | `packages/ling_app/test/dao/gift_dao_test.dart::礼物默认排序` |
| REQ-16-24 | SYS-F-023 | P1 | integration | F13 | 归档视图展示已取消与已归档条目并支持恢复 | `packages/ling_app/integration_test/gift_archive_test.dart::归档与恢复` |
| REQ-16-24 | SYS-F-027 | P2 | widget | F14 | 礼物空状态与无匹配结果为两套文案 | `packages/ling_app/test/widget/gift_list_test.dart::礼物空状态区分` |
| REQ-16-24 | SYS-F-028 | P1 | widget | F1, F8 | 喜好与礼物为同一页面的两个 Tab | `packages/ling_app/test/widget/preference_page_test.dart::双 Tab 结构` |
| REQ-16-25 | SYS-F-022 | P0 | integration | F10 | 礼物状态支持任意跳转与回退并自动写入送出日期 | `packages/ling_app/integration_test/gift_status_test.dart::状态流转与送出日期` |
| REQ-16-26 | SYS-F-024 | P0 | integration | F12, F1 | 礼物详情来源追溯可跳转喜好，三种关联情形各有呈现 | `packages/ling_app/integration_test/gift_source_test.dart::来源追溯三种情形` |
| REQ-16-26 | SYS-F-026 | P1 | integration | F8 | 删除礼物后重算来源喜好的已加入礼物标记 | `packages/ling_app/integration_test/gift_delete_test.dart::已加入礼物标记重算` |
| REQ-16-27 | SYS-F-009 | P0 | widget | F5 | 喜好筛选 3 项常用默认展开，其余收在更多筛选 | `packages/ling_app/test/widget/preference_filter_test.dart::筛选分组与展开` |
| REQ-16-27 | SYS-F-010 | P1 | integration | F5, F11 | 筛选条件跨会话保留 | `packages/ling_app/integration_test/filter_state_test.dart::筛选跨会话保留` |
| REQ-16-27 | SYS-F-025 | P0 | widget | F11 | 礼物筛选 3 项常用默认展开，其余收在更多筛选 | `packages/ling_app/test/widget/gift_filter_test.dart::礼物筛选分组` |
| REQ-16-28 | SYS-F-003 | P0 | widget | F2 | 喜好名称为空时保存禁用，点击后显示字段级红色提示 | `packages/ling_app/test/widget/preference_form_test.dart::名称必填校验` |
| REQ-16-28 | SYS-F-021 | P0 | widget | F9 | 礼物表单必填项有默认值，名称为空时保存禁用 | `packages/ling_app/test/widget/gift_form_test.dart::礼物表单默认值与校验` |
| REQ-16-29 | SYS-H-001 | P0 | widget | H1 | 设置首页分组展示 5 个入口与同步摘要 | `packages/ling_app/test/widget/settings_test.dart::设置首页分组` |
| REQ-16-29 | SYS-H-005 | P0 | integration | H4, B3, E1, D2 | 显示偏好含 5 项配置且各自作用于对应页面 | `packages/ling_app/integration_test/display_preference_test.dart::显示偏好五项生效` |
| REQ-16-29 | SYS-H-006 | P0 | dao | H2, H4 | 用户偏好默认值与同步、配置重载后的保留 | `packages/ling_app/test/dao/user_preference_dao_test.dart::偏好默认值与保留` |
| REQ-16-29 | SYS-H-008 | P1 | widget | H6 | 规则说明页同时展示封面与天气两套规则并标注区别 | `packages/ling_app/test/widget/rules_page_test.dart::两套规则同屏展示` |
| REQ-16-29 | SYS-H-009 | P2 | widget | H7 | 关于页同屏展示五条版本轴与资源来源说明 | `packages/ling_app/test/widget/about_page_test.dart::关于页字段` |
| REQ-16-29 | SYS-MIGRATE-001 | P0 | dao | — | 数据库迁移保留用户数据并可重复执行 | `packages/ling_app/test/dao/migration_test.dart::迁移幂等与数据保留` |
| REQ-16-30 | SYS-B-003 | P1 | widget | B0 | 年视图无同步记录时展示空状态并引导至设置页 | `packages/ling_app/test/widget/year_view_test.dart::年视图空状态` |
| REQ-16-30 | SYS-H-002 | P0 | integration | H1, B0 | 立即同步为手动触发同步的唯一入口 | `packages/ling_app/integration_test/manual_sync_test.dart::立即同步入口` |
| REQ-16-31 | SYS-H-003 | P0 | integration | H2 | 主题选择页以 2 列网格展示 4 套主题且点击立即生效 | `packages/ling_app/integration_test/theme_test.dart::主题切换与持久化` |
| REQ-16-31 | SYS-H-004 | P0 | golden | H2, H3, B3 | 主题作用范围限于呈现样式，映射规则在 4 套主题下一致 | `packages/ling_app/test/golden/theme_golden_test.dart::四主题月视图黄金图` |
| REQ-16-31 | SYS-H-011 | P2 | golden | H3 | 主题应用效果对照页呈现同一月份在 4 套主题下的差异 | `packages/ling_app/test/golden/theme_compare_golden_test.dart::主题对照黄金图` |
| REQ-16-32 | SYS-COVER-001 | P1 | widget | C1, H2, H3 | 封面情绪蒙层不透明度按主题取 4 个固定值 | `packages/ling_app/test/widget/cover_overlay_test.dart::主题蒙层不透明度` |
| REQ-16-32 | SYS-H-011 | P2 | golden | H3 | 主题应用效果对照页呈现同一月份在 4 套主题下的差异 | `packages/ling_app/test/golden/theme_compare_golden_test.dart::主题对照黄金图` |
| REQ-16-33 | SYS-COVER-002 | P1 | service | C1 | 不可达子池命中时回落到占位图并记录告警 | `packages/ling_app/test/service/cover_service_test.dart::不可达子池占位回落` |
| REQ-16-33 | SYS-COVER-003 | P1 | integration | — | 封面资源清单与寻址表在构建期校验一致 | `packages/ling_app/integration_test/cover_manifest_test.dart::资源清单一致性` |
| REQ-16-33 | SYS-H-009 | P2 | widget | H7 | 关于页同屏展示五条版本轴与资源来源说明 | `packages/ling_app/test/widget/about_page_test.dart::关于页字段` |
| REQ-16-33 | SYS-RULE-010 | P0 | rule | C1 | 封面综合关系分按亲密 0.6、情绪 0.4 加权并四舍五入 | `packages/ling_core/test/cover_test.dart::封面综合关系分加权` |
| REQ-16-33 | SYS-RULE-011 | P0 | rule | C1, H6 | 封面等级 L1-L5 在每个区间端点取到唯一等级 | `packages/ling_core/test/cover_test.dart::封面等级端点` |
| REQ-16-33 | SYS-RULE-012 | P0 | rule | H6 | 亲密度档 D1-D5 与情绪档 E1-E4 在端点取到唯一档位 | `packages/ling_core/test/cover_test.dart::亲密度档端点` |
| REQ-16-33 | SYS-RULE-013 | P0 | rule | H6 | 情绪档 E1-E4 在端点取到唯一档位 | `packages/ling_core/test/cover_test.dart::情绪档端点` |
| REQ-16-33 | SYS-RULE-014 | P0 | rule | C1, H6 | 池内变体由档位中值差决定，5×4 查找表的 20 个格子逐一对应 | `packages/ling_core/test/cover_test.dart::池内变体查找表` |
| REQ-16-33 | SYS-RULE-015 | P0 | rule | H6 | 穷举全部整数输入得到 18 个可达子池，不可达子池恰为 L1V4 与 L5V1 | `packages/ling_core/test/cover_test.dart::子池可达性穷举` |
| REQ-16-33 | SYS-RULE-016 | P0 | rule | B3, C1 | 同一日期在同一档位组合下稳定取到同一张封面图 | `packages/ling_core/test/cover_test.dart::日期哈希稳定选图` |
| REQ-16-33 | SYS-RULE-017 | P0 | rule | — | FNV-1a 哈希对固定输入给出固定值，Dart 与 Python 结果一致 | `packages/ling_core/test/cover_test.dart::稳定哈希跨语言一致` |
| REQ-16-34 | SYS-BACKEND-001 | P0 | backend | A5, C4 | 单次同步超过 300 个日期时仅前 300 个进入队列，其余保持待评估 | `backend/tests/test_queue.py::单次上限 300` |
| REQ-16-34 | SYS-BACKEND-002 | P0 | backend | — | 评估并发数为 3 且配置项取值限制在 1-5 | `backend/tests/test_queue.py::并发上限` |
| REQ-16-34 | SYS-BACKEND-003 | P0 | integration | C4, D3 | 待评估日期进入日详情时触发单日评估并优先于队列剩余任务 | `packages/ling_app/integration_test/eval_priority_test.dart::单日评估抢占` |
| REQ-16-34 | SYS-BACKEND-004 | P0 | backend | D4, H8 | 队列任务失败按配置重试，耗尽后置为失败且队列继续 | `backend/tests/test_queue.py::失败重试与队列续行` |
| REQ-16-34 | SYS-BACKEND-008 | P0 | backend | D7a | 消息条数为 0 的日期不调用 AI 且不计入任何聚合 | `backend/tests/test_queue.py::零消息跳过评估` |
| REQ-16-34 | SYS-RULE-053 | P0 | backend | A5, H1 | 评估队列按日期倒序排序并在 300 条上限处截断 | `backend/tests/test_queue.py::队列排序与截断` |
| REQ-16-35 | SYS-BACKEND-006 | P0 | backend | — | 评估缓存键由日期、文件哈希、提示词版本三者构成 | `backend/tests/test_store.py::缓存键命中与失效` |
| REQ-16-35 | SYS-BACKEND-007 | P0 | integration | D5 | 提示词版本变更只对新同步日期生效，历史日期保留原结果 | `packages/ling_app/integration_test/prompt_version_test.dart::提示词版本生效范围` |
| REQ-16-35 | SYS-D-011 | P0 | integration | D1, D3 | 重新评估覆盖 AI 结果并刷新版本与元数据字段 | `packages/ling_app/integration_test/re_evaluate_test.dart::重新评估字段刷新` |
| REQ-16-36 | SYS-BACKEND-010 | P0 | backend | D1 | 脱敏在内存副本上执行，本地存储与对话流保留原文 | `backend/tests/test_mask.py::脱敏不落盘` |
| REQ-16-36 | SYS-BACKEND-011 | P1 | backend | — | 姓名与昵称保留原文，供亲密度判定使用 | `backend/tests/test_mask.py::姓名昵称保留` |
| REQ-16-36 | SYS-BACKEND-012 | P1 | backend | D1 | 非文本消息以类型占位符送入提示词，条数照常计入 | `backend/tests/test_prompt.py::非文本占位符` |
| REQ-16-36 | SYS-H-007 | P2 | widget | H5 | 隐私说明页说明本地加密、安全存储与脱敏口径 | `packages/ling_app/test/widget/privacy_page_test.dart::隐私说明内容` |
| REQ-16-36 | SYS-RULE-050 | P0 | backend | — | 脱敏按固定顺序替换 6 类结构化敏感信息 | `backend/tests/test_mask.py::六类敏感信息替换` |
| REQ-16-36 | SYS-RULE-051 | P0 | backend | — | 验证码只替换与验证码字样相邻的数字，普通数字保留原文 | `backend/tests/test_mask.py::验证码上下文识别` |
| REQ-16-36 | SYS-RULE-052 | P1 | backend | — | 详细地址识别省市区与门牌号组合 | `backend/tests/test_mask.py::详细地址识别` |
| REQ-16-37 | SYS-D-004 | P0 | integration | D1, D2 | 日期归属以后端切分时区为权威，设备时区变化不改变统计 | `packages/ling_app/integration_test/timezone_test.dart::时区基准权威性` |
| REQ-16-38 | SYS-BACKEND-009 | P0 | integration | D8, C4 | 当天为进行中日期，保持待评估并在次日进入队列 | `packages/ling_app/integration_test/today_test.dart::进行中日期处理` |
| REQ-16-38 | SYS-D-017 | P0 | widget | D8 | 当天进行中展示状态提示且统计实时计算 | `packages/ling_app/test/widget/day_detail_test.dart::当天进行中提示` |
| REQ-16-39 | SYS-F-006 | P0 | integration | F1, F5 | 共同喜好为标记字段，5 种状态通过筛选查看 | `packages/ling_app/integration_test/common_status_test.dart::共同喜好状态语义` |

## 屏幕 → 用例

| 屏幕 | 用例 ID |
| --- | --- |
| A1 | SYS-A-001, SYS-A-002, SYS-PERF-001 |
| A2 | SYS-A-002 |
| A3 | SYS-A-003 |
| A4 | SYS-A-004 |
| A5 | SYS-A-005, SYS-A-006, SYS-BACKEND-001, SYS-PERF-002, SYS-RULE-053 |
| A6 | SYS-A-006, SYS-A-007 |
| A7 | SYS-A-008 |
| A8 | SYS-A-009, SYS-A-012 |
| B0 | SYS-B-003, SYS-H-002 |
| B1 | SYS-B-001, SYS-B-002, SYS-RULE-007 |
| B2 | SYS-B-001, SYS-B-004, SYS-RULE-007 |
| B3 | SYS-A-010, SYS-B-001, SYS-B-005, SYS-B-006, SYS-B-007, SYS-B-008, SYS-B-015, SYS-E-003, SYS-H-004, SYS-H-005, SYS-PERF-001, SYS-RULE-007, SYS-RULE-016 |
| B4 | SYS-B-009, SYS-E-003 |
| C1 | SYS-B-006, SYS-B-007, SYS-B-010, SYS-B-012, SYS-C-002, SYS-C-007, SYS-COVER-001, SYS-COVER-002, SYS-RULE-010, SYS-RULE-011, SYS-RULE-014, SYS-RULE-016 |
| C2 | SYS-B-006, SYS-B-007, SYS-B-010 |
| C3 | SYS-B-006, SYS-B-007, SYS-B-010, SYS-B-011, SYS-C-004 |
| C4 | SYS-B-011, SYS-BACKEND-001, SYS-BACKEND-003, SYS-BACKEND-009, SYS-C-006, SYS-C-008, SYS-RULE-004 |
| C5 | SYS-B-013, SYS-B-014, SYS-RULE-004 |
| C6 | SYS-B-013, SYS-C-001, SYS-C-002 |
| C7 | SYS-C-003, SYS-C-004, SYS-C-005, SYS-C-006 |
| C8 | SYS-C-007 |
| D1 | SYS-B-001, SYS-B-006, SYS-BACKEND-010, SYS-BACKEND-012, SYS-D-003, SYS-D-004, SYS-D-010, SYS-D-011, SYS-D-016, SYS-D-018, SYS-E-003, SYS-G-003, SYS-PERF-001 |
| D2 | SYS-D-001, SYS-D-002, SYS-D-003, SYS-D-004, SYS-H-005, SYS-RULE-040, SYS-RULE-041, SYS-RULE-042 |
| D3 | SYS-BACKEND-003, SYS-D-011, SYS-D-012 |
| D4 | SYS-BACKEND-004, SYS-BACKEND-005, SYS-D-013 |
| D5 | SYS-B-012, SYS-BACKEND-007, SYS-D-014, SYS-RULE-008 |
| D6 | SYS-BACKEND-013, SYS-RULE-005 |
| D7a | SYS-BACKEND-008, SYS-D-002, SYS-D-015, SYS-RULE-004 |
| D7b | SYS-B-013, SYS-D-015, SYS-D-016, SYS-RULE-004 |
| D8 | SYS-BACKEND-009, SYS-D-017, SYS-RULE-004 |
| E1 | SYS-B-009, SYS-E-001, SYS-E-002, SYS-E-003, SYS-H-005, SYS-PERF-001, SYS-RULE-007, SYS-RULE-043, SYS-RULE-044 |
| E2 | SYS-E-001, SYS-E-004, SYS-RULE-030, SYS-RULE-031, SYS-RULE-032, SYS-RULE-043 |
| E3 | SYS-E-005, SYS-RULE-030, SYS-RULE-031 |
| E4 | SYS-E-006 |
| F1 | SYS-F-001, SYS-F-006, SYS-F-024, SYS-F-028 |
| F2 | SYS-F-002, SYS-F-003 |
| F3 | SYS-F-004, SYS-F-005 |
| F4 | SYS-F-007, SYS-F-008 |
| F5 | SYS-F-005, SYS-F-006, SYS-F-009, SYS-F-010 |
| F6 | SYS-F-008 |
| F7 | SYS-F-011 |
| F8 | SYS-F-008, SYS-F-020, SYS-F-026, SYS-F-028 |
| F9 | SYS-F-021 |
| F10 | SYS-F-022 |
| F11 | SYS-F-010, SYS-F-025 |
| F12 | SYS-F-007, SYS-F-024 |
| F13 | SYS-F-023 |
| F14 | SYS-F-027 |
| G1 | SYS-G-001, SYS-G-003, SYS-G-004, SYS-RULE-020, SYS-RULE-021 |
| G2 | SYS-G-004 |
| G3 | SYS-G-002, SYS-RULE-021 |
| G4 | SYS-G-005 |
| H1 | SYS-A-010, SYS-H-001, SYS-H-002, SYS-H-010, SYS-RULE-053 |
| H2 | SYS-COVER-001, SYS-H-003, SYS-H-004, SYS-H-006 |
| H3 | SYS-COVER-001, SYS-H-004, SYS-H-011 |
| H4 | SYS-B-008, SYS-H-005, SYS-H-006 |
| H5 | SYS-H-007 |
| H6 | SYS-H-008, SYS-RULE-011, SYS-RULE-012, SYS-RULE-013, SYS-RULE-014, SYS-RULE-015 |
| H7 | SYS-H-009 |
| H8 | SYS-BACKEND-004, SYS-H-010 |

## 分层统计

| 层 | 用例数 | P0 | P1 | P2 |
| --- | --- | --- | --- | --- |
| widget | 56 | 33 | 15 | 8 |
| integration | 31 | 24 | 7 | 0 |
| rule | 27 | 25 | 2 | 0 |
| backend | 14 | 10 | 4 | 0 |
| perf | 4 | 1 | 3 | 0 |
| dao | 4 | 4 | 0 | 0 |
| service | 2 | 0 | 2 | 0 |
| golden | 2 | 1 | 0 | 1 |
| contract | 1 | 1 | 0 | 0 |
| **合计** | **141** | **99** | **33** | **9** |
