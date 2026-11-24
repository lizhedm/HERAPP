#!/usr/bin/env bash
# LingLing 一键测试入口。
#
# 每次改需求、改规则、改代码后执行本脚本即可确认功能是否正常。
# 按从快到慢排序，前一阶段失败即停止，使最常见的错误在几秒内暴露。
#
#   1. 一致性校验   用例清单、产物同步、枚举、规则字面量、配置、线框图   必跑，约 2 秒
#   2. 规则对照     ling_core 读 oracle_fixtures 对同一输入断言      需 dart
#   3. 客户端测试   规则、服务、DAO、Widget、黄金图                 需 flutter
#   4. 后端测试     脱敏、队列、解析降级、提示词、契约                需 pytest
#   5. 集成测试     同步、评估端到端                                需 flutter 且 --full
#
# 第 1 阶段的六项检查全部只依赖 Python 标准库，在任何机器上都能跑，
# 覆盖的是最容易在评审中漏过的机械一致性：需求与用例、文档与代码、规则归属、
# 以及线框图手机壳内只呈现界面内容这条约定。
#
# 缺少 dart / flutter / pytest 时跳过对应阶段并在结尾汇总，不作为失败。
# 本机未装工具链时第 1 阶段仍然有效，规则正确性与覆盖完整性照常受保护。
#
# 用法：
#   tests/run.sh           跑到第 4 阶段
#   tests/run.sh --full    加跑集成测试
#   tests/run.sh --quick   只跑第 1 阶段

set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

FULL=0
QUICK=0
for arg in "$@"; do
  case "$arg" in
    --full)  FULL=1 ;;
    --quick) QUICK=1 ;;
    *) echo "未知参数: $arg"; exit 2 ;;
  esac
done

SKIPPED=()

step()  { printf '\n\033[1m[%s] %s\033[0m\n' "$1" "$2"; }
check() { printf '\n  \033[1m· %s\033[0m\n' "$1"; }
die()   { printf '\n\033[31m失败于 %s\033[0m\n' "$1"; exit 1; }

step 1/5 "一致性校验"

# 清单是全部测试产物的事实来源，先校验它，再校验由它派生的产物。
check "用例清单"
python3 tests/validate.py || die "用例清单校验"

check "产物同步"
python3 tests/check_generated.py || die "产物同步检查"

check "枚举一致性"
python3 tests/check_enums.py || die "枚举一致性校验"

check "规则字面量"
python3 tests/check_rule_literals.py || die "规则字面量扫描"

check "配置项清单"
python3 tests/check_config.py || die "配置项清单校验"

check "线框图手机壳内容"
python3 tests/check_wireframe_ui.py || die "线框图手机壳内容校验"

if [ "$QUICK" = 1 ]; then
  printf '\n\033[32m一致性校验通过\033[0m\n'
  exit 0
fi

step 2/5 "规则对照"
if command -v dart >/dev/null 2>&1; then
  ( cd packages/ling_core && dart test ) || die "规则对照"
else
  SKIPPED+=("第 2 阶段：未安装 dart")
  echo "  跳过，未安装 dart"
fi

step 3/5 "客户端测试"
if command -v flutter >/dev/null 2>&1; then
  ( cd packages/ling_app && flutter test ) || die "客户端测试"
else
  SKIPPED+=("第 3 阶段：未安装 flutter")
  echo "  跳过，未安装 flutter"
fi

step 4/5 "后端测试"
if python3 -c "import pytest" >/dev/null 2>&1; then
  python3 -m pytest backend/tests -q || die "后端测试"
else
  SKIPPED+=("第 4 阶段：未安装 pytest")
  echo "  跳过，未安装 pytest"
fi

step 5/5 "集成测试"
if [ "$FULL" != 1 ]; then
  echo "  跳过，加 --full 执行"
elif command -v flutter >/dev/null 2>&1; then
  ( cd packages/ling_app && flutter test integration_test ) || die "集成测试"
else
  SKIPPED+=("第 5 阶段：未安装 flutter")
  echo "  跳过，未安装 flutter"
fi

if [ ${#SKIPPED[@]} -gt 0 ]; then
  printf '\n未执行的阶段:\n'
  for item in "${SKIPPED[@]}"; do echo "  - $item"; done
fi

printf '\n\033[32m测试通过\033[0m\n'
