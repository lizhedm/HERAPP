# LingLing 配置项清单

技术方案 6.4 要求全部可配置项集中在 `AppConfig`（只读）与 `UserPreference`（用户可写）两个结构，
服务内部不出现硬编码阈值。本文件是配置项的单一出处，含键名、类型、默认值、取值范围、生效时机。

`tests/check_config.py` 在 CI 中校验本文件与代码结构的键名集合一致。
新增配置项时同时更新结构定义、默认值、本文件、以及一个断言默认值的测试，缺一项则构建失败。

生效时机的三种取值含义固定：

- **启动** 启动时读取一次，修改后需重启应用
- **即时** 写入后当前界面立即生效
- **下次同步** 写入后在下一次同步或下一次评估调度时生效

---

## AppConfig 只读配置

来源为配置文件，`ConfigService` 只读取不写入。需求 3.7 列出该结构的四个分组。

### sync 同步

| 键名 | 类型 | 默认值 | 取值范围 | 生效时机 | 需求 |
| --- | --- | --- | --- | --- | --- |
| `sync.baseUrl` | string | 无，必填 | 合法 http/https URL | 启动 | 3.7 |
| `sync.authHeader` | string | `Authorization` | 非空字符串 | 启动 | 3.7 |
| `sync.token` | string | 无，必填 | 非空字符串，存入系统安全存储 | 启动 | 3.7、11 |
| `sync.manifestPath` | string | `/v1/manifest` | 以 `/` 开头的路径 | 启动 | 3.7 |
| `sync.dayFilePathTemplate` | string | `/v1/days/{date}` | 含 `{date}` 占位符的路径 | 启动 | 3.7 |
| `sync.timeoutSeconds` | int | 30 | 5-120 | 下次同步 | 3.7 |
| `sync.retryCount` | int | 3 | 0-10 | 下次同步 | 3.7、3.6 |
| `sync.batchSize` | int | 30 | 1-100 | 下次同步 | 3.7 |
| `sync.autoSyncOnLaunch` | bool | true | — | 启动 | 3.7 |
| `sync.scheduledIntervalMinutes` | int | 0 | 0 表示关闭，否则 15-1440 | 启动 | 3.7 |

### ai AI 服务

| 键名 | 类型 | 默认值 | 取值范围 | 生效时机 | 需求 |
| --- | --- | --- | --- | --- | --- |
| `ai.baseUrl` | string | 无，必填 | 合法 http/https URL | 启动 | 3.7 |
| `ai.model` | string | `deepseek-flash` | 非空字符串，后端启动时校验可用 | 下次同步 | 3.7、技术方案 3.4 |
| `ai.promptVersion` | string | `v1` | 与后端 `prompts/` 下的版本文件对应 | 下次同步 | 3.7、6.2 |
| `ai.apiKey` | string | 无，必填 | 非空字符串，存入系统安全存储 | 启动 | 3.7、11 |
| `ai.concurrency` | int | 3 | 1-5 | 下次同步 | 3.7、6.3 |
| `ai.maxDatesPerSync` | int | 300 | 1-1000 | 下次同步 | 3.7、6.3 |

### thresholds 阈值

全部取自需求的判定条件，调整后 `ruleVersion` 递增并清空派生缓存重算。

| 键名 | 类型 | 默认值 | 取值范围 | 生效时机 | 需求 |
| --- | --- | --- | --- | --- | --- |
| `thresholds.configLoadTimeoutSeconds` | int | 8 | 3-30 | 启动 | 3.1 |
| `thresholds.fogBalanceBelow` | int | 40 | 0-100 | 即时 | 7.2 |
| `thresholds.balanceMinMessages` | int | 4 | 1-50 | 即时 | 6.4 |
| `thresholds.snowMessageCountBelow` | int | 10 | 0-100 | 即时 | 7.2 |
| `thresholds.snowEmotionAtLeast` | int | 50 | 0-100 | 即时 | 7.2 |
| `thresholds.highlightOverallAtLeast` | int | 85 | 0-100 | 即时 | 8.1 |
| `thresholds.highlightEmotionAtLeast` | int | 70 | 0-100 | 即时 | 8.1 |
| `thresholds.highlightOverallAlone` | int | 90 | 0-100 | 即时 | 8.1 |
| `thresholds.funMomentCountAtLeast` | int | 2 | 1-3 | 即时 | 8.1 |
| `thresholds.summaryMaxChars` | int | 120 | 10-200 | 即时 | 4.8、6.2 |
| `thresholds.noteMaxChars` | int | 200 | 10-500 | 即时 | 4.9 |
| `thresholds.highlightCandidateMax` | int | 3 | 1-10 | 下次同步 | 6.2 |
| `thresholds.gateGraceMinutes` | int | 10 | 1-120 | 即时 | 3.10 |
| `thresholds.gateMaxAttempts` | int | 5 | 3-10 | 即时 | 3.10 |
| `thresholds.gateLockoutSeconds` | int | 60 | 30-600 | 即时 | 3.10 |

### image 图片处理

压缩与缓存的全部数值取自需求 3.12。质量阶梯以逗号分隔的降序整数表达，`ImageService` 按序重压直至体积达标。

| 键名 | 类型 | 默认值 | 取值范围 | 生效时机 | 需求 |
| --- | --- | --- | --- | --- | --- |
| `image.maxEdgePixels` | int | 1600 | 512-4096 | 即时 | 3.12 |
| `image.qualitySteps` | string | `80,70,60` | 1-3 个 1-100 的降序整数 | 即时 | 3.12 |
| `image.maxBytes` | int | 2097152 | 262144-10485760 | 即时 | 3.12 |
| `image.compressTimeoutSeconds` | int | 3 | 1-30 | 即时 | 3.12 |
| `image.thumbEdgePixels` | int | 320 | 96-1024 | 启动 | 3.12 |
| `image.cacheMaxBytes` | int | 209715200 | 52428800-2147483648 | 即时 | 3.12 |
| `image.unreferencedRetentionDays` | int | 7 | 1-90 | 下次同步 | 3.12 |

### coverPools 封面资源池

| 键名 | 类型 | 默认值 | 取值范围 | 生效时机 | 需求 |
| --- | --- | --- | --- | --- | --- |
| `coverPools.manifestPath` | string | `assets/cover/manifest.json` | 仓库内相对路径 | 启动 | 5.2、10.1 |
| `coverPools.version` | string | `pool-2026.11` | 非空字符串，展示于关于页 | 启动 | 10.3、12.6 |
| `coverPools.fallbackAsset` | string | `assets/cover/placeholder.png` | 仓库内相对路径 | 启动 | 10.3 |

### gate 访问密码

`gate.password` 作用域为后端：由 `ops/set_password.py` 写入后端库，客户端配置文件中不存在该键。其余三项作用域为客户端。

| 键名 | 类型 | 默认值 | 取值范围 | 生效时机 | 需求 |
| --- | --- | --- | --- | --- | --- |
| `gate.password` | string | `QWEasdZXC@2026` | 长度不少于 8 位且含字母与数字 | 下次同步 | 3.10 |
| `gate.hashAlgo` | string | `argon2id` | 固定值 | 启动 | 3.10 |
| `gate.defaultPasswordHash` | string | 无，必填 | argon2id 哈希串 | 启动 | 3.10 |
| `gate.defaultSalt` | string | 无，必填 | base64 编码的 16 字节盐值 | 启动 | 3.10 |

---

## UserPreference 用户可写偏好

保存在本地缓存库，由设置页写入，随回写队列提交后端，因此主题与显示偏好在各端一致。

| 键名 | 类型 | 默认值 | 取值范围 | 生效时机 | 需求 |
| --- | --- | --- | --- | --- | --- |
| `theme` | Theme | `PAPER_CALENDAR` | 需求 14.26 的 4 个取值 | 即时 | 12.2、13 |
| `cardDefaultState` | CardState | `COVER` | 需求 14.1 的 2 个取值 | 下次进入月视图 | 12.4、13 |
| `trendMetric` | TrendMetric | `OVERALL_SCORE` | 需求 14.24 的 3 个取值 | 下次进入趋势页 | 12.4、13 |
| `trendGranularity` | TrendGranularity | `MONTH` | 需求 14.25 的 3 个取值 | 下次进入趋势页 | 12.4、13 |
| `curveOverlay` | bool | false | — | 下次进入趋势页 | 12.4、13 |
| `statsExpanded` | bool | false | — | 下次进入日详情 | 12.4、13 |
| `updatedAt` | datetime | 写入时间 | — | 即时 | 13 |

`cardDefaultState` 作用于进入月视图时的卡片初始化。单张卡片切换后的当前状态为视图层临时状态，
随月视图生命周期存在，不写回本结构也不参与回写。

---

## 密钥处理

`sync.token` 与 `ai.apiKey` 两项的值存入系统安全存储，配置文件中只保留占位符。
两项均不写入日志、不进入崩溃上报、不出现在界面展示。需求 11 与技术方案 9.2 规定其轮换方式。

`gate.password` 的明文只存在于执行 `ops/set_password.py` 时的命令行入参，脚本写入后端库的是
argon2id 哈希与盐值。`/v1/gate` 只下发哈希与盐值，客户端取到后存入系统安全存储。
明文不落盘、不进日志、不出现在任何接口响应中。
