#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""LingLing 规则参考实现（oracle）。

本模块是需求文档确定性映射规则的唯一可执行参考，供两个用途：

1. 系统测试用例清单中「期望值」的生成与校验，避免手写期望值出错。
2. 客户端 ling_core 的跨语言对照基准，Dart 实现与本模块对同一组输入必须得出相同结果。

规则来源逐条标注需求章节。任何规则变更先改需求文档，再改本模块，再改 Dart 实现。
只依赖标准库，Python 3.9 可运行。
"""

from __future__ import annotations

import unicodedata

RULE_VERSION = 1

# ── 需求 7.1 / 5.1：两套独立的加权合成 ──────────────────────────────

WEATHER_WEIGHTS = {"overall": 0.5, "emotion": 0.3, "intimacy": 0.2}
COVER_WEIGHTS = {"intimacy": 0.6, "emotion": 0.4}


def round_half_up(value: float) -> int:
    """四舍五入取整。

    Python 内置 round 用银行家舍入（round(0.5) == 0），需求的「四舍五入」
    指 0.5 进位，因此显式实现，避免 86.5 这类边界与 Dart 的 round 不一致。
    """
    import math

    return math.floor(value + 0.5) if value >= 0 else math.ceil(value - 0.5)


def weather_score(overall: int, emotion: int, intimacy: int) -> int:
    """天气综合分。需求 7.1。"""
    return round_half_up(overall * 0.5 + emotion * 0.3 + intimacy * 0.2)


def cover_score(intimacy: int, emotion: int) -> int:
    """封面综合关系分。需求 5.1。与天气综合分独立计算。"""
    return round_half_up(intimacy * 0.6 + emotion * 0.4)


# ── 需求 7.2：日天气判定，12 条优先级 ───────────────────────────────

WEATHER_BANDS = [
    (95, 100, "RAINBOW"),
    (85, 94, "SUNNY"),
    (75, 84, "PARTLY_CLOUDY"),
    (65, 74, "CLOUDY"),
    (55, 64, "WINDY"),
    (45, 54, "LIGHT_RAIN"),
    (35, 44, "RAIN"),
    (25, 34, "HEAVY_RAIN"),
    (0, 24, "THUNDERSTORM"),
]


def weather_by_band(score: int) -> str:
    """按天气综合分做字典映射。需求 7.2 第 4-12 条。"""
    for low, high, weather in WEATHER_BANDS:
        if low <= score <= high:
            return weather
    raise ValueError(f"天气综合分越界: {score}")


def day_weather(
    eval_status: str,
    synced: bool,
    msg_count: int,
    confidence: int = None,
    overall: int = None,
    emotion: int = None,
    intimacy: int = None,
) -> str:
    """日天气。需求 7.2，按优先级依次判定，前一条命中即停止。

    STALE 日期沿用上次成功评估的分数，由调用方传入该分数，从第 2 条起参与判定。
    """
    # 优先级 1：待评估
    if not synced or msg_count == 0 or eval_status in ("PENDING", "RUNNING", "FAILED"):
        return "PENDING"
    # 优先级 2：雾
    if confidence is not None and confidence < 40:
        return "FOG"
    # 优先级 3：雪
    if msg_count < 10 and emotion is not None and emotion >= 50:
        return "SNOW"
    # 优先级 4-12：综合分区间
    return weather_by_band(weather_score(overall, emotion, intimacy))


def period_weather(scores: list) -> dict:
    """周 / 月天气。需求 7.3。周期天气不应用雾与雪规则。"""
    if not scores:
        return {"weather": "PENDING", "avgScore": None}
    avg = round_half_up(sum(scores) / len(scores))
    return {"weather": weather_by_band(avg), "avgScore": avg}


# ── 需求 5.1 / 5.2：封面等级、辅助档位、池内变体 ─────────────────────

COVER_LEVEL_BANDS = [(0, 20, "L1"), (21, 40, "L2"), (41, 60, "L3"), (61, 80, "L4"), (81, 100, "L5")]
INTIMACY_TIER_BANDS = [(0, 20, "D1"), (21, 40, "D2"), (41, 60, "D3"), (61, 80, "D4"), (81, 100, "D5")]
EMOTION_TIER_BANDS = [(0, 25, "E1"), (26, 50, "E2"), (51, 75, "E3"), (76, 100, "E4")]

INTIMACY_TIER_MID = {"D1": 10, "D2": 30, "D3": 50, "D4": 70, "D5": 90}
EMOTION_TIER_MID = {"E1": 13, "E2": 38, "E3": 63, "E4": 88}

# 需求 5.2：综合关系分由亲密度与情绪分推导，这两个子池在算术上无法成立
UNREACHABLE_SUBPOOLS = {("L1", "V4"), ("L5", "V1")}
IMAGES_PER_SUBPOOL = 5


def _band(bands: list, value: int) -> str:
    for low, high, name in bands:
        if low <= value <= high:
            return name
    raise ValueError(f"分值越界: {value}")


def cover_level(intimacy: int, emotion: int) -> str:
    """封面等级 L1-L5。需求 5.1。"""
    return _band(COVER_LEVEL_BANDS, cover_score(intimacy, emotion))


def intimacy_tier(intimacy: int) -> str:
    """亲密度档 D1-D5。需求 5.1。"""
    return _band(INTIMACY_TIER_BANDS, intimacy)


def emotion_tier(emotion: int) -> str:
    """情绪档 E1-E4。需求 5.1。"""
    return _band(EMOTION_TIER_BANDS, emotion)


def cover_variant(d_tier: str, e_tier: str) -> str:
    """池内变体 V1-V4。需求 5.2，按档位中值差判定。"""
    gap = INTIMACY_TIER_MID[d_tier] - EMOTION_TIER_MID[e_tier]
    if gap <= -25:
        return "V1"
    if gap < 0:
        return "V2"
    if gap < 25:
        return "V3"
    return "V4"


def stable_hash(text: str) -> int:
    """FNV-1a 32 位哈希。

    需求 5.2 要求同一日期稳定取到同一张图。语言内置哈希不保证跨运行实例稳定，
    因此固定算法，使 Python 与 Dart 对同一日期得出同一索引。
    """
    h = 0x811C9DC5
    for byte in text.encode("utf-8"):
        h ^= byte
        h = (h * 0x01000193) & 0xFFFFFFFF
    return h


def select_cover(intimacy: int, emotion: int, date: str, pool_size: int = IMAGES_PER_SUBPOOL) -> dict:
    """封面选图。需求 5.2，pool[等级][变体][日期哈希 % 子池张数]。"""
    level = cover_level(intimacy, emotion)
    variant = cover_variant(intimacy_tier(intimacy), emotion_tier(emotion))
    if (level, variant) in UNREACHABLE_SUBPOOLS:
        return {"level": level, "variant": variant, "assetKey": "cover/placeholder", "reachable": False}
    index = stable_hash(date) % pool_size
    return {
        "level": level,
        "variant": variant,
        "assetKey": f"cover/{level}/{variant}/{index}",
        "reachable": True,
    }


def reachable_subpools() -> set:
    """穷举全部整数输入，返回实际可达的 (等级, 变体) 集合。需求 5.2。"""
    found = set()
    for intimacy in range(101):
        for emotion in range(101):
            found.add(
                (cover_level(intimacy, emotion), cover_variant(intimacy_tier(intimacy), emotion_tier(emotion)))
            )
    return found


# ── 需求 8.1：高光触发与类型判定 ──────────────────────────────────

HIGHLIGHT_TRIGGER = "总分 ≥ 85 且情绪分 ≥ 70；或总分 ≥ 90"


def highlight_triggered(overall: int, emotion: int) -> bool:
    """高光触发条件。需求 8.1。"""
    return (overall >= 85 and emotion >= 70) or overall >= 90


def highlight_type(overall: int, emotion: int, intimacy: int, fun_count: int) -> str:
    """高光类型。需求 8.1，5 条优先级，前一条命中即停止。未触发返回 None。"""
    if not highlight_triggered(overall, emotion):
        return None
    if overall >= 90 and emotion >= 85 and intimacy >= 85:
        return "OVERALL"
    if intimacy >= 90:
        return "HIGH_INTIMACY"
    if emotion >= 90:
        return "HIGH_EMOTION"
    if fun_count >= 2:
        return "FUN"
    return "HIGH_SCORE"


# ── 需求 9.4：30 种情绪 → 6 色系，情绪分 → 4 明度档 ──────────────────

EMOTION_COLOR_FAMILY = {
    "开心": "WARM_YELLOW", "兴奋": "WARM_YELLOW", "调皮": "WARM_YELLOW",
    "骄傲": "WARM_YELLOW", "期待": "WARM_YELLOW",
    "亲昵": "PINK", "宠溺": "PINK", "感动": "PINK", "感激": "PINK", "吃醋": "PINK",
    "平静": "LIGHT_GREEN", "治愈": "LIGHT_GREEN", "释然": "LIGHT_GREEN", "中性": "LIGHT_GREEN",
    "低落": "LIGHT_BLUE", "难过": "LIGHT_BLUE", "委屈": "LIGHT_BLUE",
    "失望": "LIGHT_BLUE", "怀念": "LIGHT_BLUE",
    "生气": "ORANGE_RED", "烦躁": "ORANGE_RED", "焦虑": "ORANGE_RED", "纠结": "ORANGE_RED",
    "无聊": "GRAY_BROWN", "疲惫": "GRAY_BROWN", "冷淡": "GRAY_BROWN", "尴尬": "GRAY_BROWN",
    "无奈": "GRAY_BROWN", "愧疚": "GRAY_BROWN", "惊讶": "GRAY_BROWN",
}

BRIGHTNESS_BANDS = [(76, 100, "VIVID"), (51, 75, "MID_HIGH"), (26, 50, "MID_LOW"), (0, 25, "DIM")]


def emotion_color(emotion_type: str, emotion_score: int, eval_status: str = "SUCCESS") -> dict:
    """情绪着色。需求 9.3、9.4。待评估使用中性灰。"""
    if eval_status in ("PENDING", "RUNNING", "FAILED"):
        return {"family": "NEUTRAL_GRAY", "brightness": None}
    return {
        "family": EMOTION_COLOR_FAMILY[emotion_type],
        "brightness": _band(BRIGHTNESS_BANDS, emotion_score),
    }


# ── 需求 6.1：互动统计 ───────────────────────────────────────────

SEGMENT_GAP_MINUTES = 30


def text_length(content: str) -> int:
    """字数口径。需求 6.1：仅 TEXT 类型 content 的 Unicode 码点数，不含首尾空白。"""
    return len(content.strip())


def segment_count(timestamps: list) -> int:
    """连续对话段数。需求 6.1：相邻消息间隔超过 30 分钟视为新段。"""
    if not timestamps:
        return 0
    ordered = sorted(timestamps)
    segments = 1
    for prev, cur in zip(ordered, ordered[1:]):
        if (cur - prev) > SEGMENT_GAP_MINUTES * 60:
            segments += 1
    return segments


def longest_segment(timestamps: list) -> int:
    """最长连续对话条数。需求 6.1 第 11 项。"""
    if not timestamps:
        return 0
    ordered = sorted(timestamps)
    best = run = 1
    for prev, cur in zip(ordered, ordered[1:]):
        run = 1 if (cur - prev) > SEGMENT_GAP_MINUTES * 60 else run + 1
        best = max(best, run)
    return best


# ── 需求 6.4：置信度 ────────────────────────────────────────────

FOG_CONFIDENCE_THRESHOLD = 40

# ── 需求 6.3：评估调度 ──────────────────────────────────────────

EVAL_CONCURRENCY_DEFAULT = 3
EVAL_CONCURRENCY_RANGE = (1, 5)
EVAL_BATCH_CAP = 300


def eval_queue(dates: list, cap: int = EVAL_BATCH_CAP) -> dict:
    """评估队列。需求 6.3：按日期倒序，超过上限的保持 PENDING。"""
    ordered = sorted(dates, reverse=True)
    return {"queued": ordered[:cap], "deferred": ordered[cap:]}


# ── 需求 6.5：脱敏 ─────────────────────────────────────────────

# 顺序即优先级，固定不变：
# 邮箱先行，使整个邮箱作为一个整体被替换，避免局部数字被号码规则切走。
# 身份证先于银行卡，两者在 18 位纯数字上重叠，需求 6.5 表格以身份证为先。
# 长号码先于短号码，验证码规则只认与「验证码」「码」相邻的数字，不误伤普通数字。
MASK_RULES = [
    ("EMAIL", r"[\w.+-]+@[\w-]+\.[\w.-]+", "[邮箱]"),
    ("ID_CARD", r"(?<!\d)\d{17}[\dXx](?!\d)", "[身份证号]"),
    ("BANK_CARD", r"(?<!\d)\d{16,19}(?!\d)", "[银行卡号]"),
    ("PHONE", r"(?<!\d)1\d{10}(?!\d)", "[手机号]"),
    ("ADDRESS", r"[\u4e00-\u9fa5]{2,8}(?:省|市)[\u4e00-\u9fa5]{2,8}(?:区|县)[\u4e00-\u9fa5\d]{2,20}号", "[地址]"),
]

# 验证码带上下文条件，用捕获组保留「验证码」字样与分隔符。需求 6.5。
VERIFY_CODE_PATTERN = r"(验证码|码)([\s:：是为]{0,3})(\d{4,8})(?!\d)"
VERIFY_CODE_REPLACEMENT = r"\1\2[验证码]"


def mask(text: str) -> str:
    """脱敏。需求 6.5，按 MASK_RULES 的固定顺序执行，最后处理验证码。"""
    import re

    for _name, pattern, placeholder in MASK_RULES:
        text = re.sub(pattern, placeholder, text)
    return re.sub(VERIFY_CODE_PATTERN, VERIFY_CODE_REPLACEMENT, text)


# ── 需求 9.2：周期键 ───────────────────────────────────────────


def period_key(date: str, granularity: str) -> str:
    """周期键。周为 ISO 8601，周一为周首。需求 9.2。"""
    import datetime

    d = datetime.date.fromisoformat(date)
    if granularity == "WEEK":
        iso_year, iso_week, _ = d.isocalendar()
        return f"{iso_year}-W{iso_week:02d}"
    if granularity == "MONTH":
        return f"{d.year}-{d.month:02d}"
    if granularity == "YEAR":
        return str(d.year)
    raise ValueError(f"未知粒度: {granularity}")


def trend_average(values: list) -> int:
    """趋势聚合。需求 9.2：SUCCESS 与 STALE 日期的算术平均并四舍五入；空则缺失。"""
    return round_half_up(sum(values) / len(values)) if values else None
