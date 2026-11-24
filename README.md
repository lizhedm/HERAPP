# LingLing

以「每天一张关系卡片」为核心的关系记录应用。保存聊天记录、生成每日评估、
展示关系趋势、管理个人喜好与礼物清单、沉淀高分高光回忆。

后端部署在一台联网 Mac 上并持有全量数据作为权威源，前端用 Flutter 支持多端，
AI 评估调用 DeepSeek 在线 API。

## 当前生效的文档

开发以下列文件为准。同一事实只在一处定义，其余位置引用而不复述。

| 文件 | 作用 |
| --- | --- |
| `需求文档V1.1.md` | 功能、实现逻辑、数据模型、验收标准 |
| `技术方案V1.0.md` | 架构、数据方案、接口、测试与上线方案 |
| `低保真线框图-LingLing-V1.1.html` | 64 个屏幕的低保真原型，手机壳内只放界面呈现内容 |
| `docs/config-reference.md` | 全部可配置项的键名、默认值、取值范围、生效时机 |
| `docs/traceability.md` | 需求、屏幕、测试用例的追溯矩阵 |

V1.0 的需求文档与线框图记录的是已被 V1.1 取代的口径，其中的评分维度与待确认
事项均已变更，按它实现会得到错误结果，因此不在仓库中保留。需要查阅历史口径时
从 `c9c26b3` 取出。

## 产物生成

Word 产物由 Markdown 生成，线框图由脚本生成，三者都不手工编辑：

```bash
python3 make_req_docx_v11.py      # 需求文档V1.1.md  → LingLing-需求描述文档V1.1.docx
python3 make_tech_docx_v10.py     # 技术方案V1.0.md  → LingLing-技术实现方案V1.0.docx
python3 build_wireframe_v11.py    #                 → 低保真线框图-LingLing-V1.1.html
```

## 校验

```bash
bash tests/run.sh --quick   # 六项一致性校验
python3 tests/generate.py   # 由用例清单生成测试骨架与追溯矩阵
```

六项校验各自负责一类一致性，任一项失败则构建失败：

| 脚本 | 校验内容 |
| --- | --- |
| `validate.py` | 文档结构、需求与屏幕覆盖率、评分规则 oracle 的输入输出对、版本轴 |
| `check_generated.py` | 生成产物与用例清单同步，测试骨架文件齐全无孤儿 |
| `check_enums.py` | 需求 14 章的枚举定义与各处引用一致 |
| `check_rule_literals.py` | 规则数值不在代码中硬编码 |
| `check_config.py` | 配置项清单与代码结构的键名集合一致 |
| `check_wireframe_ui.py` | 线框图手机壳内只含界面呈现内容 |

## 目录

| 路径 | 内容 |
| --- | --- |
| `packages/ling_core/` | 评分、天气、封面寻址等纯函数，不依赖 Flutter |
| `packages/ling_app/` | Flutter 客户端 |
| `backend/` | 后端服务 |
| `tests/` | 用例清单、校验脚本、oracle 固定数据、测试骨架 |
| `docs/` | 配置项清单与追溯矩阵 |
| `assets/` | 线框图样式表；封面资源池按 `coverPools.manifestPath` 落于 `assets/cover/` |
| `.github/workflows/` | 客户端、后端、一致性、集成、安全五条流水线 |

`ops/set_password.py` 由技术方案规定用于写入访问密码的哈希与盐值，与封面资源池
同属尚未落地的部分，路径以 `docs/config-reference.md` 的记录为准。
