#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""校验线框图手机壳内不出现开发字段。

线框图的约定是手机壳内只放最终呈现给用户的界面内容，实现说明放在手机壳外的
meta 区。这条约定靠人工检查会漏，本脚本把它变成 CI 门禁：

1. 从生成的 HTML 中取出每个 `<div class="ph">` 到紧随其后的 `<div class="meta">`
   之间的内容，即手机壳内的界面；手机壳之后的 meta 区是给开发看的标注，不在校验范围。
2. 在其中搜索开发字段的字面量：服务类名、枚举标识、数据库字段名、内部公式与
   等级代号。命中即失败并打印所在屏幕编号，便于定位。

屏幕编号从手机壳前最近的 `<span class="sid">` 取得。只依赖标准库。
"""

from __future__ import annotations

import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
HTML = os.path.join(ROOT, "低保真线框图-LingLing-V1.1.html")

# 每条规则为 (正则, 说明)。正则在手机壳内容上做搜索。
FORBIDDEN = [
    (r"\b[A-Z][A-Za-z]*(?:Service|Repository|Engine|Queue|DAO|Dao)\b", "服务或数据访问类名"),
    (r"\b(?:AppConfig|UserPreference|DailyEvaluation|DayChatFile|HighlightMemory"
     r"|PreferenceItem|PreferenceCategoryCustom|GiftItem|DayCardUserData"
     r"|WriteBackItem|GateCredential|SyncState|FilterState)\b", "实体或表名"),
    (r"\b(?:IDLE|SYNCING|CANCELLED|SUCCESS|PARTIAL_SUCCESS|FAILED|PENDING"
     r"|RUNNING|STALE|PENDING_CONFIG|AUTH_FAILED|CONFIG_TIMEOUT|CONFLICT"
     r"|ACCEPTED|COVER|SUMMARY|DATE|FOG|SNOW|RAINBOW|SUNNY|THUNDERSTORM)\b", "枚举标识"),
    (r"\b(?:schemaVersion|promptVersion|ruleVersion|coverPoolVersion|appVersion"
     r"|evalVersion|preferenceId|commonStatus|cardDefaultState|userSummary"
     r"|updatedAt|entityKey|fileHash|confidence|manifest|ETag)\b", "字段名"),
    (r"\bL[1-5]\b(?!\s*[）)])", "封面等级代号"),
    (r"\bV[1-4]\b", "封面子池变体代号"),
    (r"[×*]\s*0\.[0-9]", "内部权重公式"),
    (r"置信度\s*\d", "置信度数值"),
    (r"\bargon2id\b|password_hash|gate\.password", "密码实现细节"),
]

errors: list[str] = []


def main() -> int:
    if not os.path.exists(HTML):
        print(f"  线框图文件缺失: {os.path.basename(HTML)}")
        return 1
    html = open(HTML, encoding="utf-8").read()

    # 逐个手机壳取内容，并回溯最近的屏幕编号
    checked = 0
    for m in re.finditer(r'<div class="ph">(.*?)<div class="meta">', html, re.S):
        inner = m.group(1)
        before = html[: m.start()]
        sids = re.findall(r'<span class="sid">([A-H]\d+[a-z]?)</span>', before)
        sid = sids[-1] if sids else "?"
        checked += 1
        # 去掉 HTML 标签与内联样式，只在可见文本上判定
        text = re.sub(r"<[^>]+>", " ", re.sub(r'style="[^"]*"', " ", inner))
        for pattern, label in FORBIDDEN:
            for hit in set(re.findall(pattern, text)):
                errors.append(f"{sid} 手机壳内出现{label}: {hit!r}")

    print(f"  手机壳内容校验覆盖 {checked} 个手机壳")
    if errors:
        print(f"\n校验失败，共 {len(errors)} 项:")
        for e in sorted(set(errors)):
            print(f"  - {e}")
        return 1
    print("\n校验通过，手机壳内只含界面呈现内容。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
