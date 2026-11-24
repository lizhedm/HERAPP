#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成低保真线框图 HTML。
手机壳内只放界面呈现内容，实现说明放在手机壳外的 meta 区。
"""
import io, os

CSS = open("/tmp/wf_css.txt", encoding="utf-8").read()
# 补充 2 列栅格（主题预览与月视图卡片墙使用）
CSS = CSS.replace("</style>",
    ".g2{display:grid;grid-template-columns:repeat(2,1fr);gap:4px}\n</style>")
OUT = "/Users/zhe/Documents/TophantAIGit/HERAPP/低保真线框图-个人关系聊天回忆App-V1.1.html"

P = []          # 页面片段累积
def w(s): P.append(s)

# ─────────────────────────────────────────────── 复用组件
def phone(title, body, nav=None, bar=True, ics=""):
    """生成一个手机壳。nav: 5 项中高亮的名字"""
    items = ["时间墙", "趋势", "喜好礼物", "回忆", "设置"]
    navhtml = ""
    if nav:
        navhtml = '<div class="pnav">' + "".join(
            f'<span class="{"on" if n==nav else ""}">{n}</span>' for n in items
        ) + '</div>'
    barhtml = '<div class="pbar"><span>09:41</span><span>▮▮▮</span></div>' if bar else ""
    ttl = ""
    if title:
        ttl = f'<div class="ttl"><span>{title}</span>{ics}</div>'
    return (f'<div class="ph">{barhtml}{ttl}'
            f'<div class="body">{body}</div>{navhtml}</div>')

def screen(sid, name, pos, body_html, meta_html):
    return (f'<div class="screen">\n'
            f'  <div class="sc-head"><span class="sid">{sid}</span><h3>{name}</h3>\n'
            f'  <span class="pos">流程位置：{pos}</span></div>\n'
            f'  <div class="sc-body">\n    {body_html}\n'
            f'    <div class="meta">{meta_html}</div>\n'
            f'  </div>\n</div>\n')

def meta(elements, actions, goto, notes=None):
    s = '<h4>关键元素</h4><ul>' + "".join(f'<li>{x}</li>' for x in elements) + '</ul>'
    s += '<h4>用户可执行操作</h4><ul>' + "".join(f'<li>{x}</li>' for x in actions) + '</ul>'
    s += '<h4>操作后去向</h4><ul>' + "".join(f'<li>{x}</li>' for x in goto) + '</ul>'
    if notes:
        s += "".join(f'<div class="tbd"><b>规则</b>{n}</div>' for n in notes)
    return s

def to(t):
    return f'<span class="to">→ {t}</span>'

def grp(gid, title, note):
    w(f'<div class="grp" id="{gid}">\n<h2>{title}</h2>\n'
      f'<div class="gnote">{note}</div>\n<div class="screens">\n')

def endgrp():
    w('</div>\n</div>\n')

# ═══════════════════════════════════════════════ 文档头
w(f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>个人关系聊天回忆 App · 低保真线框图</title>
{CSS}
</head>
<body>
<div class="wrap">
<h1>个人关系聊天回忆 App · 低保真线框图</h1>
<p class="sub">依据《个人关系聊天回忆 App 需求描述文档》绘制 · 表达信息层级、核心文案、按钮位置与页面状态 · 正式视觉设计另行输出</p>

<div class="doc">
  <p><b>页面内容约定</b>：手机壳内只放最终呈现给用户的界面内容（文案、数据、控件）。实现说明、服务与字段名、判定规则一律放在手机壳右侧的「关键元素 / 用户可执行操作 / 操作后去向 / 规则」区域，开发时不要把这些说明绘制到界面上。</p>
  <p><b>阅读方式</b>：按用户真实使用顺序分为 A–H 共 8 组，每组内含正常流程与异常/空/加载状态。每屏标注编号、页面名称、流程位置、可执行操作、操作后去向（<span class="to">→ 目标屏</span>）。</p>
  <p><b>图例</b>：实线框＝已明确元素；<span class="box d" style="display:inline-block;padding:0 4px">虚线框</span>＝占位/未填充数据；斜线块＝图片占位；<span class="tbd" style="display:inline-block;padding:0 5px"><b>规则</b>执行规则</span>＝该屏适用的判定规则，位于手机壳外。</p>
  <p><b>底部导航（固定 5 项）</b>：时间墙 / 趋势 / 喜好与礼物 / 回忆 / 设置。</p>
  <div class="idx">
    <a href="#ga">A 启动与同步（8 屏）</a><a href="#gb">B 时间墙 年→月份→月（5 屏）</a><a href="#gc">C 日卡片三态与长按（7 屏）</a>
    <a href="#gd">D 日详情与评估（9 屏）</a><a href="#ge">E 趋势与热力图（4 屏）</a><a href="#gf">F 喜好与礼物（14 屏）</a>
    <a href="#gg">G 回忆（高光）（4 屏）</a><a href="#gh">H 设置（8 屏）</a><a href="#rules">规则速查</a><a href="#pending">待确认事项</a>
  </div>
</div>

<div class="doc">
<h4 style="margin:0 0 4px;font-size:13px">核心交互流程总图</h4>
<pre class="flow">
启动
 └─ A1 启动页 ──ConfigService 读 AppConfig · 超时上限 8s
      ├─ 超时 ────────────────────► A2 配置加载超时 CONFIG_TIMEOUT ──► 重新加载（重新计时）
      ├─ 配置缺失 ────────────────► A3 待配置 PENDING_CONFIG（只读提示页）
      ├─ 401/403 ────────────────► A4 鉴权失败 AUTH_FAILED（只读提示页）
      └─ 配置有效 ─► A5 同步中 SYNCING ─ manifest → 比对 date+version/ETag → 增量拉日文件
                        ├─ 用户取消 ──► A6 已取消 CANCELLED（已落盘保留 · 继续同步断点续传）
                        ├─ FAILED ───► A7 同步失败（失败原因分类 + 重试 / 离线查看）
                        ├─ PARTIAL ──► A8 部分成功（失败日期列表 · 单日重试 + 批量重试）
                        └─ SUCCESS ──► StatsService 本地统计 → EvaluationService 送 AI
                                        │  AI: PENDING → RUNNING → SUCCESS / FAILED / STALE
                                        │  AI 输出含 confidence，置信度 &lt;40 → 日天气 FOG；0 消息日与当天保持 PENDING
                                        │  调度：日期倒序 · 并发 3 · 单次上限 300 · 超出部分进日详情时单日评估
                                        ▼
                                     B1 年视图（无数据 → B0 空状态）· 展示年度均分
                                        │ 点击年份
                                        ▼
                                     B2 年内月份选择页（12 格 · 3 列 × 4 行 · 无记录为禁用态）
                                        │ 点击有记录月份
                                        ▼
                                     B3 月视图 日卡片墙（2 列 · 顶部月份切换器 + 本月天气/均分 · B4 为周定位态）
                                        ├─ 点击卡片主体 ──► C1 封面 → C2 日期数字 → C3 总结 → C1（每张卡片独立切换，进入月视图时按默认状态初始化）
                                        │                     ├─ 评估缺失 ──► C4 占位封面降级
                                        │                     └─ 未同步日 ──► C5 占位态（长按可编辑总结/备注）
                                        ├─ 长按卡片 ──► C6 底部动作面板（收藏 / 编辑总结 / 添加备注）
                                        │                     ├─ 编辑总结 ──► C7 编辑总结（≤50 字 · 恢复为 AI 总结 · 未保存二次确认）
                                        │                     └─ 添加备注 ──► C8 备注（≤200 字 · 非空显示备注图标）
                                        └─ 点击右下角箭头 ──► D1 日详情
                                                              ├─ 展开互动统计 ──► D2（12 项 · 占比用堆叠条 · 连续段阈值 30 分钟）
                                                              ├─ RUNNING ──► D3 评估中
                                                              ├─ FAILED ──► D4 评估失败 ──► 重试
                                                              ├─ STALE ──► D5 待重评 ──► 重新评估（版本号递增）
                                                              ├─ 低置信度 ──► D6 置信度提示行（天气显示为雾）
                                                              ├─ 当日无消息 ──► D7a（可编辑总结 · 无同步入口）
                                                              ├─ 该日未同步 ──► D7b（提供「同步这一天」）
                                        └─ 当天进行中 ──► D8（待评估 · 可看对话与统计 · 次日解锁评估）
                                     高分日（总分≥85且情绪分≥70，或总分≥90）─ HighlightService
                                        └─ 类型优先级：综合高光 → 高亲密 → 高情绪 → 有趣对话 → 高总分
                                     日详情「标记为高光」──► 手动高光（类型固定综合高光）

底部导航并列分支
 ├─ 趋势 ──► E1 曲线 Tab（指标 总分/亲密度/情绪分 · 粒度 周/月/年 · 默认当前周期 · 缺评估断开）
 │            ├─ 点击数据点 ──► 周粒度→D1 日详情 / 月粒度→B4 月视图周定位态 / 年粒度→B3 该月月视图
 │            ├─ E2 情绪日历 Tab（6 色系 × 情绪分明度 · 待评估中性灰 · 点击→D1）
 │            ├─ E3 色系图例
 │            └─ E4 趋势无数据空状态
 ├─ 喜好与礼物（同页双 Tab）
 │   ├─ 喜好 Tab ──► F1 喜好列表（星级降序 · 长按操作面板）
 │   │      ├─ 新增/编辑 ──► F2（名称必填 · 字段级红色校验提示）
 │   │      ├─ 分类选择 ──► F3 分类管理（内置不可改 · 自定义可增删改 · 删除后相关喜好归「其他」）
 │   │      ├─ 长按删除 ──► F4 删除确认（关联礼物保留 · preferenceId 置空）
 │   │      ├─ 筛选 ──► F5 底部浮层（常用：类型/分类/星级 展开 · 更多：共同喜好/已加礼物/有图片 折叠 · 多选 · 跨会话保留）
 │   │      ├─ 加入礼物清单 ──► F6（含优先级字段 · 保存后跳礼物 Tab 定位新建条目）
 │   │      └─ F7 空状态 / 无匹配结果
 │   └─ 礼物 Tab ──► F8 礼物清单（计划日期升序 · 隐藏已取消/已归档）
 │          ├─ 新增/编辑 ──► F9（名称必填 · 关联喜好下拉可改可解除 · 送出日期展示）
 │          ├─ 状态流转 ──► F10 浮层（全状态可任意跳转回退 · 已送出/已收到自动写送出日期）
 │          ├─ 筛选 ──► F11 底部浮层（常用：状态/分类/优先级 · 更多：等级/场合/预算档/有关联喜好）
 │          ├─ 来源追溯 ──► F12 详情跳回 F1 定位（已删除显示「来源喜好已删除」）
 │          ├─ F13 归档视图（已取消 + 已归档 · 可恢复）
 │          └─ F14 空状态 / 无匹配结果
 ├─ 回忆 ──► G1 高光列表（日期倒序 · 顶部类型筛选条）
 │            ├─ 点击 ──► D1 日详情
 │            ├─ 长按 ──► G2 删除确认（标记 deleted · 重评仍达标可再生成）
 │            ├─ G3 类型筛选态
 │            └─ G4 空状态（展示配置阈值数字 + 去时间墙看看）
 └─ 设置 ──► H1 设置首页（同步状态 + 立即同步 + 查看失败日期 + 主题）
              ├─ 主题 ──► H2 主题选择（纸月历 / 星图 / 色域 / 磨砂玻璃 · 点击即应用）
              │             └─ H3 主题应用效果对照
              ├─ 显示偏好 ──► H4（默认卡片状态 / 趋势默认指标 / 趋势默认粒度 / 曲线叠加 / 统计默认展开）
              ├─ 隐私说明 ──► H5
              ├─ 封面与天气规则说明 ──► H6（两套综合分公式 + L1-L5 + 天气优先级 + 情绪色系）
              ├─ 关于 ──► H7（版本 / 提示词版本 / 资源池版本 / 数据来源 / 存储位置）
              └─ 失败日期列表 ──► H8（单日重试 + 批量重试，与 A8 同组件）
</pre>
</div>
''')
print("头部完成")

# ═══════════════════════════════════════════════ A 启动与同步
grp("ga", "A · 启动与同步（需求 3）",
    "应用启动必经链路。配置与鉴权凭据由代码或配置文件提供，待配置页与鉴权失败页均为只读提示页。"
    "同步状态枚举：IDLE / SYNCING / CANCELLED / SUCCESS / PARTIAL_SUCCESS / FAILED / PENDING_CONFIG / AUTH_FAILED / CONFIG_TIMEOUT。")

# A1 启动页加载中
w(screen("A1", "启动页 · 配置加载（加载中）", "应用冷启动第一屏 · 超时上限 8 秒",
  phone("", '''<div class="ctr">
    <div class="img" style="width:62px;height:62px">LOGO</div>
    <div style="font-size:11px;font-weight:700">关系回忆</div>
    <div class="box d" style="width:100%">读取配置中…</div>
    <div class="skel" style="width:70%"></div>
  </div>''', bar=True),
  meta(
    ["应用图标与名称", "加载提示「读取配置中…」", "骨架占位条",
     "读取内容：sync / ai / thresholds / coverPools / cardDefaultState / displayPreference"],
    ["等待加载完成（无可点击元素）"],
    [f"配置有效 {to('A5 同步中')}", f"配置缺失或关键字段为空 {to('A3 待配置')}",
     f"返回 401/403 {to('A4 鉴权失败')}", f"超过 8 秒 {to('A2 配置加载超时')}"],
    ["启动页存在，加载超时上限 8 秒。", "鉴权凭据由配置文件提供，配置有效即直接进入同步流程。"])))

# A2 配置超时
w(screen("A2", "配置加载超时 CONFIG_TIMEOUT（异常）", "A1 之后分支 · 加载超过 8 秒",
  phone("", '''<div class="ctr">
    <div class="box" style="width:58px;height:58px;display:flex;align-items:center;justify-content:center;font-size:20px">!</div>
    <div style="font-size:11px;font-weight:700">配置加载超时</div>
    <div class="box" style="width:100%;font-size:9.5px;color:#444">请检查应用配置文件后重新启动</div>
    <div class="btn pri" style="width:100%">重新加载</div>
  </div>''', bar=True),
  meta(
    ["超时图标", "标题「配置加载超时」",
     "正文「配置加载超时，请检查应用配置文件后重新启动」", "「重新加载」按钮"],
    ["点击「重新加载」"],
    [f"重新计时后配置有效 {to('A5 同步中')}", f"再次超时 {to('A2 本屏')}",
     f"配置缺失 {to('A3 待配置')}"],
    ["加载超时上限 8 秒；点击「重新加载」重新计时。"])))

# A3 待配置
w(screen("A3", "待配置 PENDING_CONFIG（异常）", "A1 之后分支 · 配置缺失或关键字段为空",
  phone("", '''<div class="ctr">
    <div class="box" style="width:58px;height:58px;display:flex;align-items:center;justify-content:center;font-size:20px">⚙</div>
    <div style="font-size:11px;font-weight:700">未检测到有效配置</div>
    <div class="box" style="width:100%;font-size:9px;color:#444;text-align:left">
      请在应用配置文件中填写后端地址与鉴权信息，然后重新启动应用
    </div>
    <div class="btn" style="width:100%">重新加载配置</div>
    <div class="btn" style="width:100%">查看配置说明</div>
  </div>''', bar=True),
  meta(
    ["只读提示图标与标题", "正文说明配置由代码或配置文件提供",
     "「重新加载配置」按钮", "「查看配置说明」入口"],
    ["点击「重新加载配置」", "点击「查看配置说明」"],
    [f"配置已补全 {to('A5 同步中')}", f"仍缺失 {to('A3 本屏')}",
     f"查看说明 {to('H6 封面与天气规则说明 / H5 隐私说明')}"],
    ["配置由代码或配置文件维护，本屏操作限于重新加载与查看说明。"])))

# A4 鉴权失败
w(screen("A4", "鉴权失败 AUTH_FAILED（异常）", "同步请求返回 401 / 403",
  phone("", '''<div class="ctr">
    <div class="box" style="width:58px;height:58px;display:flex;align-items:center;justify-content:center;font-size:20px">✕</div>
    <div style="font-size:11px;font-weight:700">鉴权失败</div>
    <div class="box" style="width:100%;font-size:9px;color:#444;text-align:left">
      配置文件中的 Token 已失效，请更新配置文件后重新启动应用
    </div>
    <div class="btn pri" style="width:100%">重试同步</div>
    <div class="btn" style="width:100%">离线查看已同步内容</div>
  </div>''', bar=True),
  meta(
    ["失败图标与标题「鉴权失败」",
     "正文「配置文件中的 Token 已失效，请更新配置文件后重新启动应用」",
     "「重试同步」按钮", "「离线查看已同步内容」按钮"],
    ["点击「重试同步」", "点击「离线查看已同步内容」"],
    [f"鉴权通过 {to('A5 同步中')}", f"仍失败 {to('A4 本屏')}",
     f"离线查看 {to('B1 年视图（仅已同步数据）')}"],
    ["Token 由配置文件维护，本屏操作限于重试同步与离线查看。"])))

# A5 同步中（含取消）
w(screen("A5", "同步中 SYNCING（加载中）", "配置有效后自动进入 · 可中途取消",
  phone("时间墙", '''<div class="box" style="background:#f0f0f0">
      <div style="font-weight:700;font-size:10px">同步中 12 / 30</div>
      <div class="skel" style="width:40%;margin-top:3px"></div>
    </div>
    <div class="box" style="font-size:9px;line-height:1.7">
      ✓ 请求 manifest<br>
      ✓ 比对本地版本<br>
      ✓ 拉取日文件 30/30<br>
      ✓ 本地统计<br>
      ● AI 评估 12/30
    </div>
    <div class="btn" style="width:100%">取消同步</div>
    <div class="hr"></div>
    <div class="lbl">已同步内容可继续浏览</div>
    <div class="g3">
      <div class="dcard">11</div><div class="dcard">12</div><div class="dcard d"></div>
    </div>''', nav="时间墙"),
  meta(
    ["同步阶段清单（manifest → 比对 → 拉取 → 统计 → 评估）",
     "批量进度与评估进度「评估中 N / M」", "「取消同步」按钮", "已同步卡片可浏览区"],
    ["点击「取消同步」", "继续浏览已同步内容", f"切底部导航 {to('B1 / E1 / F1 / G1 / H1')}"],
    [f"全部成功 {to('B1 年视图')}", f"用户取消 {to('A6 已取消')}",
     f"部分日期失败 {to('A8 部分成功')}", f"整体失败 {to('A7 同步失败')}",
     f"401/403 {to('A4 鉴权失败')}"],
    ["「取消同步」停止发起新请求，中断正在传输的请求，已完整落盘的日文件保留；同时清空待执行的 AI 评估队列，正在执行的单日评估保留至结束。",
     "评估调度：本次新增或变更的全部日期立即入队，按日期倒序从最近开始，并发 3，单次同步上限 300 个日期。",
     "超过 300 个时取最近 300 个入队，更早日期保持待评估，用户进入其日详情时触发单日评估。",
     "当天为进行中日期，不进入评估队列，跨入次日后入队。",
     "同步不阻塞浏览。"])))

# A6 已取消
w(screen("A6", "同步已取消 CANCELLED", "A5 用户点击取消同步后",
  phone("时间墙", '''<div class="box" style="background:#f0f0f0">
      <div style="font-weight:700;font-size:10px">同步已取消</div>
      <div style="font-size:9px;color:#555;margin-top:2px">已同步 12 天，剩余 18 天未同步</div>
    </div>
    <div class="btn pri" style="width:100%">继续同步</div>
    <div class="hr"></div>
    <div class="lbl">已同步日期可正常浏览</div>
    <div class="g3">
      <div class="dcard">11</div><div class="dcard">12</div><div class="dcard d" style="color:#aaa">未同步</div>
    </div>''', nav="时间墙"),
  meta(
    ["取消状态条「同步已取消」", "进度摘要「已同步 N 天，剩余 M 天未同步」",
     "「继续同步」按钮", "已同步与未同步日卡片并存"],
    ["点击「继续同步」", "浏览已同步日期", f"切底部导航 {to('B1 / E1 / F1 / G1 / H1')}"],
    [f"继续同步 {to('A5 同步中（断点续传）')}",
     f"浏览未同步日 {to('D7b 该日未同步')}"],
    ["继续同步从未完成日期断点续传，不重新拉取已落盘日期。"])))

# A7 同步失败
w(screen("A7", "同步失败 FAILED（异常恢复）", "A5 之后分支 · 网络/超时/服务端/重试耗尽",
  phone("", '''<div class="ctr">
    <div class="box" style="width:58px;height:58px;display:flex;align-items:center;justify-content:center;font-size:20px">⚠</div>
    <div style="font-size:11px;font-weight:700">同步失败</div>
    <div class="box" style="width:100%;font-size:9px;text-align:left;line-height:1.7">
      失败原因：请求超时<br>
      上次成功同步：11-12 23:00
    </div>
    <div class="btn pri" style="width:100%">重试同步</div>
    <div class="btn" style="width:100%">离线查看已同步内容</div>
  </div>''', bar=True),
  meta(
    ["整页失败态", "失败原因分类（网络不可用 / 请求超时 / 服务端错误 / 重试次数耗尽）",
     "最近一次同步时间", "「重试同步」与「离线查看已同步内容」"],
    ["点击「重试同步」", "点击「离线查看已同步内容」"],
    [f"重试成功 {to('B1 年视图')}", f"部分成功 {to('A8 部分成功')}",
     f"再次失败 {to('A7 本屏')}", f"离线查看 {to('B1 年视图（仅已同步数据）')}"],
    ["同步失败按整页失败态呈现，展示失败原因分类与最近成功同步时间。"])))

# A8 部分成功
w(screen("A8", "部分成功 PARTIAL_SUCCESS（异常恢复）", "A5 之后分支 · 部分日期拉取失败",
  phone("", '''<div class="ttl"><span>同步结果</span></div>
    <div class="box" style="background:#f0f0f0;font-size:9.5px">
      成功 27 天 · 失败 3 天
    </div>
    <div class="lbl">失败日期</div>
    <div class="box" style="font-size:9px;padding:3px">
      <div style="display:flex;justify-content:space-between;align-items:center">
        <span>11-05 请求超时</span><span class="btn" style="padding:1px 4px">重试</span></div>
      <div class="hr"></div>
      <div style="display:flex;justify-content:space-between;align-items:center">
        <span>11-08 服务端错误</span><span class="btn" style="padding:1px 4px">重试</span></div>
      <div class="hr"></div>
      <div style="display:flex;justify-content:space-between;align-items:center">
        <span>11-09 请求超时</span><span class="btn" style="padding:1px 4px">重试</span></div>
    </div>
    <div class="btn pri" style="width:100%">重试全部失败项</div>
    <div class="btn" style="width:100%">继续浏览</div>''', bar=True),
  meta(
    ["成功/失败天数摘要", "失败日期列表（来源 SyncState.failedDates，每条含日期与失败原因）",
     "每行单日「重试」按钮", "底部「重试全部失败项」按钮"],
    ["点击某日期行的「重试」（仅重拉该日）", "点击「重试全部失败项」", "点击「继续浏览」"],
    [f"该日成功则从列表移除；全部成功 {to('B1 年视图')}",
     f"仍有失败 {to('A8 本屏（列表更新）')}", f"继续浏览 {to('B1 年视图')}"],
    ["向用户暴露失败日期列表，重试粒度同时支持单日与批量。",
     "设置页同样提供该列表入口（H6），两处使用同一组件。"])))
endgrp()
print("A 组完成：8 屏")

# ═══════════════════════════════════════════════ B 时间墙
grp("gb", "B · 时间墙 年 → 月份 → 月（需求 4.1-4.3）",
    "四级导航：年视图 → 年内月份选择页 → 月视图日卡片墙 → 日详情。年视图不展示年度关系天气。"
    "月视图日卡片按 2 列排列，顶部为月份切换器。")

# B0 空状态
w(screen("B0", "时间墙 · 无数据（空状态）", "首次启动且无任何已同步日期",
  phone("时间墙", '''<div class="ctr">
    <div class="img" style="width:54px;height:54px">空</div>
    <div style="font-size:10.5px;font-weight:700">还没有聊天记录</div>
    <div class="box" style="width:100%;font-size:9px;color:#555">
      应用会按配置自动同步聊天记录，同步完成后这里会按年月展示
    </div>
    <div class="btn" style="width:100%">查看同步状态</div>
  </div>''', nav="时间墙"),
  meta(
    ["空状态插图与标题「还没有聊天记录」",
     "说明行「应用会按配置自动同步聊天记录，同步完成后这里会按年月展示」",
     "「查看同步状态」按钮"],
    ["点击「查看同步状态」"],
    [f"查看同步状态 {to('H1 设置首页同步分组')}",
     f"同步产生数据后 {to('B1 年视图')}"],
    ["同步由启动自动同步开关与定时同步间隔驱动；"
     "用户侧手动触发入口统一收在设置页（H1「立即同步」）。"])))

# B1 年视图
w(screen("B1", "时间墙 · 年视图（正常）", "同步成功后的默认落地屏",
  phone("时间墙", '''<div class="box">
      <div style="font-weight:700;font-size:12px">2026</div>
      <div style="font-size:9px;color:#555;margin-top:2px">
        有记录 3 个月 · 共 62 天<br>平均总分 78 · 平均亲密度 81</div>
    </div>
    <div class="box">
      <div style="font-weight:700;font-size:12px">2025</div>
      <div style="font-size:9px;color:#555;margin-top:2px">
        有记录 12 个月 · 共 340 天<br>平均总分 74 · 平均亲密度 76</div>
    </div>
    <div class="box d" style="color:#aaa;font-size:9px">更早年份…</div>''', nav="时间墙"),
  meta(
    ["年份卡片列表（倒序）",
     "每卡显示：年份、有记录月份数、总天数、平均总分、平均亲密度",
     "年度均分与记录量"],
    ["点击年份卡片"],
    [f"点击年份 {to('B2 年内月份选择页')}"],
    ["年视图不展示年度关系天气，周期天气仅在月份格、月视图顶部与趋势页展示。"])))

# B2 年内月份选择页（新增）
w(screen("B2", "年内月份选择页", "B1 点击年份后进入 · 12 格宫格",
  phone("2026", '''<div class="g3" style="gap:5px">
      <div class="box" style="text-align:center;font-size:9px;padding:4px">
        <b style="font-size:11px">1月</b><br>31天<br>☀ 82</div>
      <div class="box" style="text-align:center;font-size:9px;padding:4px">
        <b style="font-size:11px">2月</b><br>28天<br>⛅ 76</div>
      <div class="box" style="text-align:center;font-size:9px;padding:4px">
        <b style="font-size:11px">3月</b><br>30天<br>☁ 68</div>
      <div class="box" style="text-align:center;font-size:9px;padding:4px;color:#bbb;background:#f5f5f5">
        <b style="font-size:11px">4月</b><br>无记录</div>
      <div class="box" style="text-align:center;font-size:9px;padding:4px;color:#bbb;background:#f5f5f5">
        <b style="font-size:11px">5月</b><br>无记录</div>
      <div class="box" style="text-align:center;font-size:9px;padding:4px;color:#bbb;background:#f5f5f5">
        <b style="font-size:11px">6月</b><br>无记录</div>
      <div class="box d" style="text-align:center;font-size:9px;padding:4px;color:#bbb">7月</div>
      <div class="box d" style="text-align:center;font-size:9px;padding:4px;color:#bbb">8月</div>
      <div class="box d" style="text-align:center;font-size:9px;padding:4px;color:#bbb">9月</div>
      <div class="box d" style="text-align:center;font-size:9px;padding:4px;color:#bbb">10月</div>
      <div class="box" style="text-align:center;font-size:9px;padding:4px">
        <b style="font-size:11px">11月</b><br>13天<br>🌈 88</div>
      <div class="box d" style="text-align:center;font-size:9px;padding:4px;color:#bbb">12月</div>
    </div>''', nav="时间墙",
    ics='<span class="ic">← 2026 →</span>'),
  meta(
    ["12 个月宫格，3 列 × 4 行",
     "每格显示：月份名、该月有记录天数、该月关系天气图标、该月平均总分",
     "无记录月份格为禁用态",
     "顶部年份标题与上下年切换"],
    ["点击有记录的月份格", "切换上一年 / 下一年", "返回年视图"],
    [f"点击有记录月份 {to('B3 月视图')}",
     f"点击置灰月份 → 无响应",
     f"返回 {to('B1 年视图')}"],
    ["点击年份后先进入 12 个月的该年维度展示页，再点击某个月进入月视图，不直接落到某个月。",
     "月份格展示该月关系天气（按该月有评估日期的天气综合分平均值映射）。"])))

# B3 月视图
w(screen("B3", "月视图 · 日卡片墙（正常，核心屏）", "B2 点击月份后进入 · 2 列卡片墙",
  phone("", '''<div class="ttl" style="font-size:11px">
      <span class="ic">◀</span><span>2026年11月</span><span class="ic">▶</span></div>
    <div class="box" style="background:#f0f0f0;font-size:9px;padding:3px">
      本月 🌈 彩虹 · 均分 88 · 亲密度 85</div>
    <div class="row" style="gap:5px">
      <div class="dcard" style="min-height:62px;padding:0;position:relative">
        <div class="img" style="flex:1;border:0;font-size:8px">L5 封面</div>
        <div style="position:absolute;top:2px;left:3px;font-size:8px;background:#fff;padding:0 2px">11</div>
        <div style="position:absolute;top:2px;right:3px;font-size:8px">🌈😊</div>
        <div style="position:absolute;bottom:2px;left:3px;font-size:7.5px">★📝</div>
        <div style="position:absolute;bottom:2px;right:2px;border:1px solid #111;background:#fff;font-size:8px;padding:0 3px">›</div>
      </div>
      <div class="dcard" style="min-height:62px;padding:0;position:relative">
        <div class="img" style="flex:1;border:0;font-size:8px">L4 封面</div>
        <div style="position:absolute;top:2px;left:3px;font-size:8px;background:#fff;padding:0 2px">12</div>
        <div style="position:absolute;top:2px;right:3px;font-size:8px">☀😌</div>
        <div style="position:absolute;bottom:2px;right:2px;border:1px solid #111;background:#fff;font-size:8px;padding:0 3px">›</div>
      </div>
    </div>
    <div class="row" style="gap:5px">
      <div class="dcard" style="min-height:62px;padding:0;position:relative">
        <div class="img" style="flex:1;border:0;font-size:8px">L3 封面</div>
        <div style="position:absolute;top:2px;left:3px;font-size:8px;background:#fff;padding:0 2px">13</div>
        <div style="position:absolute;bottom:2px;right:2px;border:1px solid #111;background:#fff;font-size:8px;padding:0 3px">›</div>
      </div>
      <div class="dcard d" style="min-height:62px;background:#f5f5f5;color:#aaa;align-items:center;justify-content:center;position:relative">
        <div style="text-align:center;font-size:8.5px">14<br>未同步</div>
        <div style="position:absolute;bottom:2px;right:2px;border:1px solid #bbb;background:#fff;font-size:8px;padding:0 3px;color:#999">›</div>
      </div>
    </div>''', nav="时间墙"),
  meta(
    ["顶部月份切换器：◀ 2026年11月 ▶，点击年月文字返回月份选择页",
     "顶部摘要：本月关系天气、本月平均总分、本月平均亲密度",
     "日卡片 2 列排列，卡片面积更大以容纳三态内容",
     "卡片角标区：高光标记 ★、收藏标记、备注标记 📝",
     "卡片右下角独立箭头按钮 ›",
     "未同步日卡片置灰并显示「未同步」占位"],
    ["点击卡片主体 → 切换该张卡片的三态",
     "点击卡片右下角箭头 → 进入日详情",
     "长按卡片 → 底部动作面板",
     "点击 ◀ ▶ 切换上下月", "点击年月文字返回月份选择页"],
    [f"点击主体 {to('C1 → C2 → C3 → C1 循环')}",
     f"点击箭头 {to('D1 日详情')}",
     f"长按 {to('C6 底部动作面板')}",
     f"点击年月 {to('B2 月份选择页')}",
     f"未同步日点箭头 {to('D7b 该日未同步')}"],
    ["点击切换三态，卡片上的独立箭头进入详情，两个手势不再冲突。",
     "月份切换采用顶部切换器，卡片墙 2 列。",
     "未同步日在月视图置灰并标注「未同步」。"])))
endgrp()
print("B 组完成：5 屏")

# B4 月视图周定位态
w(screen("B4", "月视图 · 周定位态", "从 E1 趋势月粒度数据点跳入",
  phone("", '''<div class="ttl" style="font-size:11px">
      <span class="ic">◀</span><span>2026年11月</span><span class="ic">▶</span></div>
    <div class="box" style="background:#f0f0f0;font-size:9px;padding:3px">
      本月 🌈 彩虹 · 均分 88 · 亲密度 85</div>
    <div class="box" style="font-size:8.6px;padding:3px;display:flex;justify-content:space-between;align-items:center">
      <span>2026 年第 46 周 · 11/9-11/15 · ⛅ · 均分 82</span>
      <span class="ic">显示全月</span></div>
    <div class="g2">
      <div class="dcard" style="min-height:52px;border:1.6px solid #333">9<br><span style="font-size:7px">晴 · 85</span></div>
      <div class="dcard" style="min-height:52px;border:1.6px solid #333">10<br><span style="font-size:7px">多云 · 79</span></div>
      <div class="dcard" style="min-height:52px;border:1.6px solid #333">11<br><span style="font-size:7px">晴 · 86</span></div>
      <div class="dcard" style="min-height:52px;border:1.6px solid #333">12<br><span style="font-size:7px">阴 · 72</span></div>
    </div>
    <div class="g2" style="margin-top:4px">
      <div class="dcard" style="min-height:52px;opacity:.5">16<br><span style="font-size:7px">晴 · 88</span></div>
      <div class="dcard" style="min-height:52px;opacity:.5">17<br><span style="font-size:7px">多云 · 76</span></div>
    </div>''', nav="时间墙"),
  meta(
    ["顶部月份切换器与本月摘要，与 B3 一致",
     "摘要区下方插入一行周摘要：周序号、起止日期、周天气、周均分",
     "周摘要行右侧「显示全月」按钮",
     "该周 7 张卡片加描边高亮，其余卡片常规展示"],
    ["浏览该周卡片", "点击「显示全月」清除高亮", "点击卡片主体切换该张卡片三态",
     "点击右下角箭头进入日详情"],
    [f"显示全月 {to('B3 月视图（普通态）')}",
     f"点击箭头 {to('D1 日详情')}",
     f"切换月份 {to('B3 月视图（普通态）')}"],
    ["进入方式：趋势页月粒度曲线的数据点对应单周，点击后跳转该周起始日所属月份的月视图并自动滚动至该周第一张卡片。",
     "跨月的周在起始日所属月份展示，落在其他月份的日期不加高亮。",
     "点击「显示全月」清除高亮与周摘要行，回到 B3 普通月视图。"])))

# ═══════════════════════════════════════════════ C 日卡片三态与长按
grp("gc", "C · 日卡片三态与长按（需求 4.4-4.7）",
    "三态顺序：封面 → 日期数字 → 一句话总结 → 封面。<b>每张卡片独立切换</b>，切换单张卡片不影响同屏其他卡片，"
    "默认状态在设置页 H4 配置。长按面板含收藏、编辑总结、添加备注，重新评估入口位于日详情 D1。")

# C1 封面态
w(screen("C1", "日卡片 · 封面状态 COVER（默认态）", "B3 月视图卡片状态之一",
  phone("2026年11月", '''<div class="row" style="gap:5px">
      <div class="dcard" style="min-height:70px;padding:0;position:relative">
        <div class="img" style="flex:1;border:0;font-size:8px">L5 封面图<br>（资源池按日期哈希）</div>
        <div style="position:absolute;top:2px;left:3px;font-size:8.5px;background:#fff;padding:0 2px">11</div>
        <div style="position:absolute;top:2px;right:3px;font-size:9px">🌈 😊</div>
        <div style="position:absolute;bottom:2px;left:3px;font-size:8px">★ 📝</div>
        <div style="position:absolute;bottom:2px;right:2px;border:1px solid #111;background:#fff;font-size:8px;padding:0 3px">›</div>
      </div>
      <div class="dcard" style="min-height:70px;padding:0;position:relative">
        <div class="img" style="flex:1;border:0;font-size:8px">L4 封面图</div>
        <div style="position:absolute;top:2px;left:3px;font-size:8.5px;background:#fff;padding:0 2px">12</div>
        <div style="position:absolute;top:2px;right:3px;font-size:9px">☀ 😌</div>
        <div style="position:absolute;bottom:2px;right:2px;border:1px solid #111;background:#fff;font-size:8px;padding:0 3px">›</div>
      </div>
    </div>
    <div class="lbl">综合关系分 = 亲密度×0.6 + 情绪分×0.4</div>
    <div class="box" style="font-size:8.5px;padding:3px">
      L1 0-20 · L2 21-40 · L3 41-60 · L4 61-80 · L5 81-100</div>''', nav="时间墙"),
  meta(
    ["封面等级图片铺满卡片（资源池按日期哈希选图）",
     "左上角日期角标", "右上角天气图标与情绪图标",
     "角标区：高光标记 ★、收藏标记、备注标记 📝",
     "右下角独立箭头 ›"],
    ["点击卡片主体切换到日期数字状态", "点击箭头进入日详情", "长按打开动作面板"],
    [f"点击主体 {to('C2 日期数字状态（仅该张卡片）')}",
     f"点击箭头 {to('D1 日详情')}", f"长按 {to('C6 动作面板')}"],
    ["进入月视图时按 UserPreference.cardDefaultState 初始化全部卡片；单张切换结果在当次浏览期间保持，离开月视图回到默认状态。"])))

# C2 日期数字态
w(screen("C2", "日卡片 · 日期数字状态 DATE", "C1 点击主体后 · 仅该张卡片",
  phone("2026年11月", '''<div class="row" style="gap:5px">
      <div class="dcard" style="min-height:70px;position:relative;align-items:center;justify-content:center">
        <div style="font-size:26px;font-weight:700;text-align:center;line-height:1">11</div>
        <div style="font-size:8.5px;text-align:center;margin-top:2px">🌈 😊 · 88 / 85</div>
        <div style="position:absolute;bottom:2px;left:3px;font-size:8px">★ 📝</div>
        <div style="position:absolute;bottom:2px;right:2px;border:1px solid #111;background:#fff;font-size:8px;padding:0 3px">›</div>
      </div>
      <div class="dcard" style="min-height:70px;position:relative;align-items:center;justify-content:center">
        <div style="font-size:26px;font-weight:700;text-align:center;line-height:1">12</div>
        <div style="font-size:8.5px;text-align:center;margin-top:2px">☀ 😌 · 82 / 80</div>
        <div style="position:absolute;bottom:2px;right:2px;border:1px solid #111;background:#fff;font-size:8px;padding:0 3px">›</div>
      </div>
    </div>''', nav="时间墙"),
  meta(
    ["大号日期数字居中",
     "下方一行：天气图标、情绪图标、总分 / 亲密度数值",
     "角标区：高光、收藏、备注标记", "右下角箭头 ›"],
    ["点击卡片主体切换到一句话总结状态", "点击箭头进入日详情", "长按打开动作面板"],
    [f"点击主体 {to('C3 一句话总结状态')}",
     f"点击箭头 {to('D1 日详情')}", f"长按 {to('C6 动作面板')}"],
    None)))

# C3 总结态
w(screen("C3", "日卡片 · 一句话总结状态 SUMMARY", "C2 点击主体后 · 含来源标识",
  phone("2026年11月", '''<div class="row" style="gap:5px">
      <div class="dcard" style="min-height:70px;position:relative">
        <div style="font-size:8px;display:flex;justify-content:space-between">
          <span>11 🌈 😊</span><span class="tag k">已编辑</span></div>
        <div style="font-size:9px;line-height:1.5;margin-top:3px">
          今天聊了旅行计划，互相分享了很多期待。</div>
        <div style="position:absolute;bottom:2px;left:3px;font-size:8px">★ 📝</div>
        <div style="position:absolute;bottom:2px;right:2px;border:1px solid #111;background:#fff;font-size:8px;padding:0 3px">›</div>
      </div>
      <div class="dcard" style="min-height:70px;position:relative">
        <div style="font-size:8px;display:flex;justify-content:space-between">
          <span>12 ☀ 😌</span><span class="tag">AI</span></div>
        <div style="font-size:9px;line-height:1.5;margin-top:3px">
          日常闲聊，氛围轻松。</div>
        <div style="position:absolute;bottom:2px;right:2px;border:1px solid #111;background:#fff;font-size:8px;padding:0 3px">›</div>
      </div>
    </div>
    <div class="lbl">来源标识</div>
    <div class="box" style="font-size:8.5px;padding:3px">
      <span class="tag k">已编辑</span> 用户改过 ·
      <span class="tag">AI</span> AI 原始总结</div>''', nav="时间墙"),
  meta(
    ["总结文字占据卡片主体",
     "顶部一行：日期、天气图标、情绪图标",
     "总结右上角来源标识：「已编辑」或「AI」",
     "角标区：高光、收藏、备注标记"],
    ["点击卡片主体切回封面状态", "点击箭头进入日详情", "长按打开动作面板"],
    [f"点击主体 {to('C1 封面状态')}",
     f"点击箭头 {to('D1 日详情')}", f"长按 {to('C6 动作面板')}"],
    ["界面标明总结来源：用户编辑过显示「已编辑」标签，未编辑显示「AI」标签。"])))

# C4 评估缺失降级
w(screen("C4", "日卡片 · 评估缺失降级（异常/首次）", "评估未完成或失败时的卡片表现",
  phone("2026年11月", '''<div class="row" style="gap:5px">
      <div class="dcard" style="min-height:70px;padding:0;position:relative">
        <div class="img d" style="flex:1;border:0;font-size:8px;background:#f2f2f2">默认占位封面</div>
        <div style="position:absolute;top:2px;left:3px;font-size:8.5px;background:#fff;padding:0 2px">15</div>
        <div style="position:absolute;top:2px;right:3px;font-size:9px">⏳</div>
        <div style="position:absolute;bottom:2px;right:2px;border:1px solid #111;background:#fff;font-size:8px;padding:0 3px">›</div>
      </div>
      <div class="dcard" style="min-height:70px;position:relative">
        <div style="font-size:8px">16 ⏳</div>
        <div style="font-size:9px;color:#999;line-height:1.5;margin-top:3px">今天还没有总结</div>
        <div style="font-size:8px;color:#777;margin-top:auto">评估进行中…</div>
        <div style="position:absolute;bottom:2px;right:2px;border:1px solid #111;background:#fff;font-size:8px;padding:0 3px">›</div>
      </div>
    </div>
    <div class="lbl">总结为空时的三种文案</div>
    <div class="box" style="font-size:8.5px;padding:3px;line-height:1.7">
      评估未完成 → 今天还没有总结<br>
      评估失败 → 总结生成失败<br>
      未同步日 → 这天还没有同步</div>''', nav="时间墙"),
  meta(
    ["封面状态降级为默认占位封面",
     "天气图标显示 ⏳ 待评估 PENDING",
     "总结状态按三种情形显示对应浅灰文案",
     "卡片底部提供对应操作提示", "日期状态与总结状态继续可用"],
    ["点击主体仍可切换三态", "点击箭头进入日详情查看评估状态", "长按打开动作面板"],
    [f"点击箭头（评估中） {to('D3 评估中')}",
     f"点击箭头（评估失败） {to('D4 评估失败')}",
     f"长按 {to('C6 动作面板')}"],
    ["总结为空时按评估未完成、评估失败、未同步三种情形显示不同文案，均为浅灰色。"])))

# C5 未同步日卡片
w(screen("C5", "日卡片 · 未同步日", "该日期在服务端存在、本地尚未拉取",
  phone("2026年11月", '''<div class="row" style="gap:5px">
      <div class="dcard d" style="min-height:70px;background:#f5f5f5;color:#aaa;align-items:center;justify-content:center;position:relative">
        <div style="text-align:center;font-size:9px;line-height:1.6">
          <span style="font-size:18px;font-weight:700">14</span><br>未同步</div>
        <div style="position:absolute;bottom:2px;right:2px;border:1px solid #bbb;background:#fff;font-size:8px;padding:0 3px;color:#999">›</div>
      </div>
      <div class="dcard d" style="min-height:70px;background:#f5f5f5;color:#aaa;align-items:center;justify-content:center;position:relative">
        <div style="text-align:center;font-size:9px;line-height:1.6">
          <span style="font-size:18px;font-weight:700">17</span><br>未同步</div>
        <div style="position:absolute;bottom:2px;right:2px;border:1px solid #bbb;background:#fff;font-size:8px;padding:0 3px;color:#999">›</div>
      </div>
    </div>
    <div class="hr"></div>
    <div class="box" style="font-size:9px">点击箭头进入日详情的未同步空状态，<br>在那里可「同步这一天」</div>''', nav="时间墙"),
  meta(
    ["卡片整体置灰", "显示日期与「未同步」占位标识",
     "卡片主体为占位区，长按可编辑总结与备注", "右下角箭头进入日详情"],
    ["点击右下角箭头进入日详情未同步态"],
    [f"点击箭头 {to('D7b 该日未同步（提供「同步这一天」）')}"],
    ["未同步日在月视图置灰并标注「未同步」，单日同步入口放在日详情（D7b）。"])))

# C6 长按动作面板
w(screen("C6", "日卡片长按 · 底部动作面板", "B3 / C1-C4 长按卡片后弹出",
  phone("2026年11月", '''<div class="row" style="gap:5px;opacity:.45">
      <div class="dcard" style="min-height:52px"><div class="img" style="flex:1;border:0"></div></div>
      <div class="dcard" style="min-height:52px"><div class="img" style="flex:1;border:0"></div></div>
    </div>
    <div class="ovl"><div class="sheet">
      <div style="font-size:9px;color:#666;text-align:center">11月11日</div>
      <div class="hr"></div>
      <div class="btn">★ 收藏</div>
      <div class="btn">编辑总结</div>
      <div class="btn">添加备注</div>
      <div class="hr"></div>
      <div class="btn">取消</div>
    </div></div>''', nav="时间墙"),
  meta(
    ["底部动作面板，顶部显示日期",
     "操作项：收藏 / 取消收藏、编辑总结、添加备注 / 编辑备注、取消",
     "重新评估入口位于日详情"],
    ["点击「收藏」切换 favorite", "点击「编辑总结」", "点击「添加备注」", "点击「取消」或遮罩关闭"],
    [f"收藏 → 写 DayCardUserData.favorite，关闭面板 {to('B3 月视图（标记刷新）')}",
     f"编辑总结 {to('C7 编辑一句话总结')}",
     f"添加备注 {to('C8 添加 / 编辑备注')}",
     f"取消 {to('B3 月视图')}"],
    ["菜单形态为底部动作面板。",
     "重新评估入口位于日详情 D1。"])))

# C7 编辑总结
w(screen("C7", "编辑一句话总结", "C6 / D1 进入 · 上限 50 字",
  phone("编辑总结", '''<div class="lbl">11月11日</div>
    <div class="inp" style="min-height:52px;color:#111;font-size:9.5px">
      今天聊了旅行计划，互相分享了很多期待。</div>
    <div style="display:flex;justify-content:space-between;font-size:8.5px;color:#666">
      <span>用户总结优先展示</span><span>19 / 50</span></div>
    <div class="btn">恢复为 AI 总结</div>
    <div class="hr"></div>
    <div class="lbl">AI 原始总结</div>
    <div class="box d" style="font-size:9px;color:#777">日常闲聊，氛围轻松。</div>
    <div style="margin-top:auto"></div>
    <div class="row"><div class="btn">取消</div><div class="btn pri">保存</div></div>''',
    ics='<span class="ic">←</span>'),
  meta(
    ["文本输入框，预填当前展示的总结",
     "实时字数计数 19 / 50",
     "「恢复为 AI 总结」按钮（AI 原始总结为空时置灰）",
     "AI 原始总结只读对照区", "取消 / 保存按钮"],
    ["编辑文本", "点击「恢复为 AI 总结」（输入框替换为 AI 原始总结）",
     "点击保存", "点击取消或返回"],
    [f"保存 → 写 userSummary，来源标识变「已编辑」 {to('调用来源屏')}",
     f"恢复为 AI 总结并保存 → 清空 userSummary，标识回「AI」 {to('调用来源屏')}",
     f"有改动点返回 {to('C7a 未保存二次确认')}",
     f"无改动点返回 {to('调用来源屏')}"],
    ["用户总结同样受 50 字限制，超出时禁用保存并提示「总结不超过 50 字」。",
     "提供「恢复为 AI 总结」能力。",
     "未保存退出需二次确认。",
     "无评估的日期也允许编辑总结。"])))

# C8 备注
w(screen("C8", "添加 / 编辑备注", "C6 / D1 进入 · 上限 200 字",
  phone("备注", '''<div class="lbl">11月11日</div>
    <div class="inp" style="min-height:84px;color:#111;font-size:9.5px">
      这天她提到想去北海道看雪，<br>记一下，冬天可以安排。</div>
    <div style="display:flex;justify-content:flex-end;font-size:8.5px;color:#666">
      <span>28 / 200</span></div>
    <div class="box" style="font-size:8.5px;padding:3px">
      备注非空时，日卡片三态均显示 📝 标记</div>
    <div style="margin-top:auto"></div>
    <div class="row"><div class="btn">取消</div><div class="btn pri">保存</div></div>''',
    ics='<span class="ic">←</span>'),
  meta(
    ["多行文本输入框", "实时字数计数 28 / 200",
     "备注标记说明", "取消 / 保存按钮"],
    ["编辑备注文本", "点击保存", "点击取消或返回"],
    [f"保存 → 写 DayCardUserData.note，卡片显示 📝 {to('调用来源屏')}",
     f"有改动点返回 {to('C8a 未保存二次确认')}",
     f"无改动点返回 {to('调用来源屏')}"],
    ["备注字数上限 200 字，超出时禁用保存并提示「备注不超过 200 字」。",
     "备注非空时在日卡片角标区增加备注图标 📝。",
     "未保存退出需二次确认，文案「备注尚未保存，确认放弃修改？」。"])))
endgrp()
print("C 组完成：8 屏")

# ═══════════════════════════════════════════════ D 日详情与评估
grp("gd", "D · 日详情与评估（需求 4.8-4.9 / 6）",
    "由 B3 卡片右下角箭头进入。AI 输出新增 confidence 置信度字段，置信度 &lt;40 时日天气映射为雾并显示提示行。"
    "亮点与有趣内容只读。当日无消息与该日未同步为两种独立空状态。")

# D1 对话流
w(screen("D1", "日详情 · 对话流（正常 SUCCESS，核心屏）", "B3 点击卡片右下角箭头进入",
  phone("11月11日", '''<div class="box" style="background:#f0f0f0;font-size:9px;padding:3px">
      🌈 彩虹 · 😊 开心 82 · 总分 88 · 亲密度 85</div>
    <div class="box d" style="font-size:9px;display:flex;justify-content:space-between">
      <span>▸ 互动统计</span><span>展开</span></div>
    <div class="bub">早安，今天天气不错</div>
    <div class="bub me">刚醒，准备出门了</div>
    <div class="bub">要不要周末去看看那家店</div>
    <div class="bub me">好啊，我查下营业时间</div>
    <div class="hr"></div>
    <div class="lbl">亮点（只读）</div>
    <div class="box d" style="font-size:8.5px">一起确定了旅行日期</div>
    <div class="lbl">有趣内容（只读）</div>
    <div class="box d" style="font-size:8.5px">互相吐槽表情包</div>''',
    nav="时间墙", ics='<span class="ic">←</span><span class="ic">⋯</span>'),
  meta(
    ["顶部评估条：天气、情绪、总分、亲密度",
     "「互动统计」折叠区（默认展开状态由设置 H2 控制）",
     "聊天气泡对话流，左右区分双方，含时间与类型",
     "亮点区与有趣内容区（只读，不可编辑）",
     "右上角 ⋯ 菜单：重新评估、标记为高光、编辑总结、编辑备注、收藏"],
    ["展开互动统计", "点击 ⋯ 打开操作菜单", "点击「重新评估」", "点击「标记为高光」",
     "编辑总结 / 备注 / 切换收藏"],
    [f"展开统计 {to('D2 互动统计展开')}",
     f"重新评估 {to('D3 评估中')}",
     f"标记为高光 → 生成手动高光 {to('G1 高光列表可见')}",
     f"编辑总结 {to('C7')}", f"编辑备注 {to('C8')}",
     f"返回 {to('B3 月视图')}"],
    ["亮点与有趣内容只读展示，不可编辑。",
     "「标记为高光」入口在日详情提供，手动高光类型固定为综合高光。",
     "「重新评估」入口仅在本屏提供。"])))

# D2 互动统计
w(screen("D2", "日详情 · 互动统计展开（12 项图形化）", "D1 展开折叠区后",
  phone("11月11日", '''<div class="box" style="background:#f0f0f0;font-size:9px;padding:3px">
      ▾ 互动统计</div>
    <div class="row" style="gap:4px">
      <div class="box" style="text-align:center;font-size:8.5px;padding:3px">
        <b style="font-size:13px">146</b><br>消息总条数</div>
      <div class="box" style="text-align:center;font-size:8.5px;padding:3px">
        <b style="font-size:13px">2,380</b><br>消息总字数</div>
    </div>
    <div class="lbl">条数占比</div>
    <div style="display:flex;height:13px;border:1px solid #999;font-size:8px">
      <div style="flex:62;background:#111;color:#fff;text-align:center">我 62%</div>
      <div style="flex:38;background:#ddd;text-align:center">TA 38%</div></div>
    <div class="lbl">字数占比</div>
    <div style="display:flex;height:13px;border:1px solid #999;font-size:8px">
      <div style="flex:55;background:#111;color:#fff;text-align:center">我 55%</div>
      <div style="flex:45;background:#ddd;text-align:center">TA 45%</div></div>
    <div class="row" style="gap:4px">
      <div class="box" style="text-align:center;font-size:8px;padding:2px">
        <b>16.3</b><br>平均字数</div>
      <div class="box" style="text-align:center;font-size:8px;padding:2px">
        <b>14/19</b><br>双方均值</div>
    </div>
    <div class="lbl">时间轴</div>
    <div class="box" style="font-size:8px;padding:2px;display:flex;justify-content:space-between">
      <span>08:12 首条</span><span>──────</span><span>23:41 末条</span></div>
    <div class="g3" style="gap:3px">
      <div class="box" style="text-align:center;font-size:7.5px;padding:2px"><b>5</b><br>对话段</div>
      <div class="box" style="text-align:center;font-size:7.5px;padding:2px"><b>38</b><br>最长段</div>
      <div class="box" style="text-align:center;font-size:7.5px;padding:2px"><b>4分</b><br>间隔中位</div>
    </div>''', nav="时间墙", ics='<span class="ic">←</span>'),
  meta(
    ["1-2 数值卡片：消息总条数、总字数",
     "3-4 条数双色堆叠条 + 百分比标注",
     "5-6 字数双色堆叠条 + 百分比标注",
     "7-8 平均每条字数、双方平均并列卡片",
     "9 首末消息时间轴起止标注",
     "10-12 连续对话段数、最长连续条数、回复间隔中位数"],
    ["折叠统计区", "滚动查看全部 12 项"],
    [f"折叠 {to('D1 对话流')}"],
    ["统计项按固定顺序呈现并图形化：占比用双色水平堆叠条，时间用时间轴，其余用数值卡片。",
     "连续对话段判定：相邻消息间隔超过 30 分钟视为新段。"])))

# D3 评估中
w(screen("D3", "日详情 · 评估中 RUNNING（加载中）", "首次评估或点击重新评估后",
  phone("11月15日", '''<div class="box" style="background:#f0f0f0;font-size:9px;padding:3px">
      ⏳ 评估中…</div>
    <div class="skel" style="width:80%"></div>
    <div class="skel" style="width:55%"></div>
    <div class="hr"></div>
    <div class="bub">今天加班到很晚</div>
    <div class="bub me">辛苦了，早点休息</div>''',
    nav="时间墙", ics='<span class="ic">←</span>'),
  meta(
    ["评估状态条「评估中…」", "评估结果区骨架占位",
     "对话流正常展示", "统计区可展开（本地计算，与 AI 评估相互独立）"],
    ["浏览对话流", "展开互动统计", "返回月视图"],
    [f"评估成功 {to('D1 对话流（评估结果填充）')}",
     f"评估失败 {to('D4 评估失败')}", f"返回 {to('B3 月视图')}"],
    None)))

# D4 评估失败
w(screen("D4", "日详情 · 评估失败 FAILED（异常恢复）", "AI 调用失败或 JSON 解析失败",
  phone("11月16日", '''<div class="box" style="background:#f0f0f0;font-size:9px;padding:3px">
      ⚠ 评估失败
      <div style="font-size:8.5px;color:#555;margin-top:2px">AI 返回内容解析失败</div></div>
    <div class="btn" style="width:100%">重试评估</div>
    <div class="hr"></div>
    <div class="bub">在忙吗</div>
    <div class="bub me">刚开完会</div>''',
    nav="时间墙", ics='<span class="ic">←</span>'),
  meta(
    ["失败状态条与失败原因", "「重试评估」按钮",
     "对话流正常展示", "已有评估数据保留不被清空"],
    ["点击「重试评估」", "浏览对话流", "展开互动统计", "编辑总结（无评估也可编辑）"],
    [f"重试成功 {to('D1 对话流')}", f"重试仍失败 {to('D4 本屏')}",
     f"编辑总结 {to('C7')}"],
    ["评估失败时保留已有数据，同步与对话流继续可用；卡片总结状态显示「总结生成失败」。"])))

# D5 待重评
w(screen("D5", "日详情 · 待重评 STALE（状态提示）", "该日期聊天文件变更后",
  phone("11月10日", '''<div class="box" style="background:#f0f0f0;font-size:9px;padding:3px">
      ↻ 待重评
      <div style="font-size:8.5px;color:#555;margin-top:2px">聊天文件已更新，当前评估基于旧版本</div></div>
    <div class="btn pri" style="width:100%">重新评估</div>
    <div class="hr"></div>
    <div class="box" style="font-size:9px;padding:3px">
      ☀ 晴 · 😌 平静 72 · 总分 80 · 亲密度 78
      <div style="font-size:8px;color:#777">以上为上次评估结果</div></div>
    <div class="bub">刚补了几条消息</div>''',
    nav="时间墙", ics='<span class="ic">←</span>'),
  meta(
    ["待重评状态条与原因说明",
     "沿用上次成功评估的分数、天气、情绪与总结",
     "「重新评估」按钮", "旧评估结果正常展示"],
    ["点击「重新评估」", "继续浏览旧结果"],
    [f"重新评估 {to('D3 评估中')}",
     f"评估完成 → 覆盖 AI 原始结果、evalVersion 加 1 {to('D1 对话流')}"],
    ["评估缓存键 = 日期 + 聊天文件哈希 + 提示词版本号。该日期聊天文件变更时进入 STALE。",
     "STALE 期间沿用上次成功评估的分数、天气、封面与情绪着色参与各处计算，卡片角标显示「待重评」。",
     "提示词版本策略：新版本对其生效后新同步的日期生效；历史日期保留原结果与原 promptVersion，手动点击「重新评估」时使用当前版本。"])))

# D6 低置信度
w(screen("D6", "日详情 · 低置信度提示", "AI 返回 confidence &lt; 40 时",
  phone("11月18日", '''<div class="box" style="background:#f0f0f0;font-size:9px;padding:3px">
      🌫 雾 · 😐 中性 48 · 总分 52 · 亲密度 50</div>
    <div class="box" style="font-size:8.5px;padding:3px;border-style:dashed">
      ⓘ 本次评估置信度较低
      <div style="color:#666;margin-top:1px">置信度 32 / 100</div></div>
    <div class="btn" style="width:100%">重新评估</div>
    <div class="hr"></div>
    <div class="bub">嗯</div>
    <div class="bub me">👌</div>
    <div class="bub">在</div>''',
    nav="时间墙", ics='<span class="ic">←</span>'),
  meta(
    ["天气显示为 🌫 雾（置信度 &lt;40 的判定结果）",
     "置信度提示行「本次评估置信度较低」与数值",
     "封面与分数仍按评估结果展示",
     "「重新评估」按钮"],
    ["点击「重新评估」", "浏览对话流"],
    [f"重新评估 {to('D3 评估中')}",
     f"置信度提升至 ≥40 → 天气按分数区间映射 {to('D1 对话流')}"],
    ["AI 输出新增 confidence 字段（0-100）。",
     "置信度 &lt;40 → 日天气映射为雾，日详情显示置信度提示行。",
     "置信度参考：消息充足语义明确 70-100；偏少模糊 40-69；极少无法判断 0-39。"])))

# D7a 当日无消息
w(screen("D7a", "日详情 · 当日无消息（空状态）", "该日期已同步，文件内消息为空",
  phone("11月20日", '''<div class="ctr">
    <div class="img" style="width:50px;height:50px">空</div>
    <div style="font-size:10.5px;font-weight:700">这天没有聊天记录</div>
    <div class="box" style="width:100%;font-size:9px;color:#555">
      该日期已同步，文件内消息为空</div>
    <div class="btn" style="width:100%">写一句话总结</div>
    <div class="btn" style="width:100%">添加备注</div>
  </div>''', nav="时间墙", ics='<span class="ic">←</span>'),
  meta(
    ["空状态标题「这天没有聊天记录」",
     "说明行「该日期已同步，文件内消息为空」",
     "「写一句话总结」与「添加备注」按钮",
     "操作限于编辑总结与备注"],
    ["点击「写一句话总结」", "点击「添加备注」", "返回月视图"],
    [f"写总结 {to('C7 编辑一句话总结')}",
     f"添加备注 {to('C8 备注')}", f"返回 {to('B3 月视图')}"],
    ["当日无消息与该日未同步为两种独立空状态，文案与可执行操作不同。",
     "无评估日期允许用户编辑一句话总结。"])))

# D7b 该日未同步
w(screen("D7b", "日详情 · 该日未同步（空状态）", "该日期在服务端存在，本地尚未拉取",
  phone("11月14日", '''<div class="ctr">
    <div class="img d" style="width:50px;height:50px">未同步</div>
    <div style="font-size:10.5px;font-weight:700">这天还没有同步</div>
    <div class="box" style="width:100%;font-size:9px;color:#555">
      该日期在服务端存在，本地尚未拉取</div>
    <div class="btn pri" style="width:100%">同步这一天</div>
    <div class="btn" style="width:100%">写一句话总结</div>
  </div>''', nav="时间墙", ics='<span class="ic">←</span>'),
  meta(
    ["空状态标题「这天还没有同步」",
     "说明行「该日期在服务端存在，本地尚未拉取」",
     "「同步这一天」按钮（仅拉取该日期文件）",
     "「写一句话总结」按钮"],
    ["点击「同步这一天」", "点击「写一句话总结」", "返回月视图"],
    [f"同步后有消息 {to('D1 对话流')}",
     f"同步后文件为空 {to('D7a 当日无消息')}",
     f"同步失败 → 停留本屏并提示失败原因",
     f"写总结 {to('C7')}"],
    ["提供单日重试同步入口，与 A8 的单日重试使用同一服务能力。"])))

# D8 当天进行中
w(screen("D8", "日详情 · 当天进行中（状态提示）", "按后端时区计算的当天",
  phone("11月17日", '''<div class="box" style="background:#f0f0f0;font-size:9px;padding:3px">
      ⏱ 今天还在进行中
      <div style="font-size:8.5px;color:#555;margin-top:2px">评估在次日生成，今天先看聊天与统计</div></div>
    <div class="box" style="font-size:9px;padding:3px">
      天气 待评估 · 情绪 待评估 · 总分 -- · 亲密度 --</div>
    <div class="box d" style="font-size:8.6px;padding:3px">
      互动统计 42 条 · 1860 字 · 按当前已同步消息实时计算 <span class="ic">展开 ›</span></div>
    <div class="hr"></div>
    <div class="bub">午饭吃什么</div>
    <div class="bub me">楼下那家吧</div>
    <div class="row" style="margin-top:4px">
      <div class="btn">写一句话总结</div><div class="btn">添加备注</div></div>''',
    nav="时间墙", ics='<span class="ic">←</span>'),
  meta(
    ["进行中状态条「今天还在进行中」与说明行",
     "评估结果区：天气与情绪显示待评估，分数显示「--」",
     "互动统计按当前已同步消息实时计算",
     "对话流正常展示",
     "「写一句话总结」与「添加备注」入口"],
    ["浏览对话流", "展开互动统计", "编辑总结", "添加备注", "切换收藏"],
    [f"写总结 {to('C7 编辑一句话总结')}",
     f"添加备注 {to('C8 添加 / 编辑备注')}",
     f"跨入次日后入队评估 {to('D3 评估中')}",
     f"返回 {to('B3 月视图')}"],
    ["日期归属以后端切分日文件的时区为权威，设备时区变化不改变日期归属与统计结果。",
     "进行中日期不进入评估队列，评估状态保持 PENDING，日天气按优先级 1 显示为待评估，封面为默认占位封面。",
     "进行中日期不计入年/月均分、周期天气与趋势曲线。",
     "跨入次日后进入评估队列，评估完成时封面、天气、情绪、总结一次性落定，达标则生成高光。"])))

endgrp()
print("D 组完成：9 屏")

# ═══════════════════════════════════════════════ E 趋势
grp("ge", "E · 趋势与情绪日历（需求 9）",
    "曲线与情绪日历为同页两个 Tab。粒度为周/月/年三种，选择后默认显示当前周期。"
    "30 种情绪归入 6 个色系，色系表类型、明度表情绪分。缺评估日期曲线断开。")

# E1 曲线
w(screen("E1", "趋势 · 曲线 Tab（正常）", "底部导航「趋势」默认落地",
  phone("", '''<div class="ttl" style="font-size:11px;padding:4px 6px">
      <span>趋势</span></div>
    <div style="display:flex;font-size:9px;border-bottom:1px solid #111">
      <div style="flex:1;text-align:center;padding:3px;background:#111;color:#fff;font-weight:700">曲线</div>
      <div style="flex:1;text-align:center;padding:3px">情绪日历</div></div>
    <div><span class="chip on">总分</span><span class="chip">亲密度</span><span class="chip">情绪分</span></div>
    <div><span class="chip">周</span><span class="chip on">月</span><span class="chip">年</span></div>
    <div class="box" style="font-size:9px;padding:2px;display:flex;justify-content:space-between;align-items:center">
      <span class="ic">◀</span><span>2026年11月 · ⛅ 多云</span><span class="ic">▶</span></div>
    <div class="box" style="height:76px;position:relative;padding:4px">
      <svg viewBox="0 0 200 66" style="width:100%;height:100%">
        <polyline points="8,44 32,30 56,36 80,18" fill="none" stroke="#111" stroke-width="2"/>
        <polyline points="128,24 152,12 176,20" fill="none" stroke="#111" stroke-width="2"/>
        <circle cx="80" cy="18" r="3.4" fill="#111"/>
        <text x="86" y="14" font-size="7" fill="#111">★高光</text>
        <line x1="80" y1="18" x2="128" y2="24" stroke="#bbb" stroke-width="1" stroke-dasharray="2,2"/>
        <text x="92" y="38" font-size="6.5" fill="#888">缺评估·断开</text>
        <circle cx="8" cy="44" r="2.4" fill="#111"/><circle cx="32" cy="30" r="2.4" fill="#111"/>
        <circle cx="56" cy="36" r="2.4" fill="#111"/>
        <circle cx="128" cy="24" r="2.4" fill="#111"/><circle cx="152" cy="12" r="2.4" fill="#111"/>
        <circle cx="176" cy="20" r="2.4" fill="#111"/>
      </svg>
    </div>''', nav="趋势"),
  meta(
    ["顶部 Tab：曲线 / 情绪日历",
     "指标切换：总分 / 亲密度 / 情绪分，支持单选或叠加",
     "粒度切换：周 / 月 / 年（无日粒度）",
     "周期切换器 ◀ 当前周期 ▶，并显示该周期关系天气",
     "曲线含高光日标记 ★",
     "缺评估日期处曲线断开，不连线不补零"],
    ["切换指标", "切换粒度", "左右切换周期", "点击曲线数据点", "切到情绪日历 Tab"],
    [f"周粒度点击点（对应单日）{to('D1 日详情')}",
     f"月粒度点击点（对应单周）{to('该周日卡片列表')}",
     f"年粒度点击点（对应单月）{to('B3 该月月视图')}",
     f"切 Tab {to('E2 情绪日历')}"],
    ["粒度只有周/月/年，选择后默认显示当周/当月/当年，可左右切换其他周期。",
     "点击数据点跳转到该点对应的周期对象，不固定跳到天。",
     "缺评估日期曲线断开处理。",
     "曲线与热力图为 Tab 切换，非跳转页面。"])))

# E2 情绪日历
w(screen("E2", "趋势 · 情绪日历 Tab（正常）", "E1 切换 Tab 后",
  phone("", '''<div class="ttl" style="font-size:11px;padding:4px 6px"><span>趋势</span></div>
    <div style="display:flex;font-size:9px;border-bottom:1px solid #111">
      <div style="flex:1;text-align:center;padding:3px">曲线</div>
      <div style="flex:1;text-align:center;padding:3px;background:#111;color:#fff;font-weight:700">情绪日历</div></div>
    <div class="box" style="font-size:9px;padding:2px;display:flex;justify-content:space-between">
      <span class="ic">◀</span><span>2026年11月</span><span class="ic">▶</span></div>
    <div class="g7" style="gap:2px;font-size:7px;text-align:center;color:#666">
      <span>一</span><span>二</span><span>三</span><span>四</span><span>五</span><span>六</span><span>日</span></div>
    <div class="g7" style="gap:2px">
      <div style="height:15px;background:#ddd;border:1px solid #ccc"></div>
      <div style="height:15px;background:#ddd;border:1px solid #ccc"></div>
      <div style="height:15px;background:#ffd34d;border:1px solid #d9b038"></div>
      <div style="height:15px;background:#ffe9a3;border:1px solid #e0cd8e"></div>
      <div style="height:15px;background:#ff9fc4;border:1px solid #d98aa9"></div>
      <div style="height:15px;background:#b8e6c4;border:1px solid #9ec9a9"></div>
      <div style="height:15px;background:#ffd34d;border:1px solid #d9b038"></div>
      <div style="height:15px;background:#a8d8ff;border:1px solid #92bade"></div>
      <div style="height:15px;background:#ffb380;border:1px solid #dd9b6e"></div>
      <div style="height:15px;background:#ff7fae;border:1px solid #dd6e97"></div>
      <div style="height:15px;background:#ffd34d;border:1px solid #d9b038"></div>
      <div style="height:15px;background:#c9c0b5;border:1px solid #aaa399"></div>
      <div style="height:15px;background:#eaeaea;border:1px dashed #bbb"></div>
      <div style="height:15px;background:#eaeaea;border:1px dashed #bbb"></div>
    </div>
    <div class="lbl">色系图例</div>
    <div style="font-size:7.5px;line-height:1.9">
      <span style="display:inline-block;width:9px;height:9px;background:#ffd34d;border:1px solid #999"></span> 暖黄·愉悦
      <span style="display:inline-block;width:9px;height:9px;background:#ff9fc4;border:1px solid #999;margin-left:4px"></span> 粉红·亲密
      <span style="display:inline-block;width:9px;height:9px;background:#b8e6c4;border:1px solid #999;margin-left:4px"></span> 浅绿·平和<br>
      <span style="display:inline-block;width:9px;height:9px;background:#a8d8ff;border:1px solid #999"></span> 浅蓝·低落
      <span style="display:inline-block;width:9px;height:9px;background:#ffb380;border:1px solid #999;margin-left:4px"></span> 橙红·激动
      <span style="display:inline-block;width:9px;height:9px;background:#c9c0b5;border:1px solid #999;margin-left:4px"></span> 灰褐·疲惫<br>
      <span style="display:inline-block;width:9px;height:9px;background:#eaeaea;border:1px dashed #999"></span> 中性灰·待评估
    </div>''', nav="趋势"),
  meta(
    ["月历网格 7 列，含星期表头",
     "格子色系由情绪类型决定，明度与饱和度由情绪分决定",
     "情绪分越高越鲜艳明亮，越低越灰暗",
     "待评估日期中性灰填充（虚线边框）",
     "底部 6 色系图例 + 待评估图例", "月份切换器"],
    ["切换月份", "点击日期格", "切到曲线 Tab", "查看图例"],
    [f"点击日期 {to('D1 日详情')}", f"切 Tab {to('E1 曲线')}"],
    ["30 种情绪归入 6 个色系：暖黄（愉悦）、粉红（亲密）、浅绿（平和）、浅蓝（低落）、橙红（激动）、灰褐（疲惫）。",
     "色相表情绪类型，明度与饱和度表情绪分，同类型情绪同色系。",
     "明度档：76-100 最鲜艳、51-75 中高、26-50 中低、0-25 最灰暗。"])))

# E3 色系映射速查
w(screen("E3", "情绪色系映射速查（规则屏）", "E2 图例展开 / H4 规则说明页同表",
  phone("情绪色系", '''<div style="font-size:7.8px;line-height:1.75">
      <div style="display:flex;gap:3px;align-items:center;margin-bottom:2px">
        <span style="width:11px;height:11px;background:#ffd34d;border:1px solid #999;flex:0 0 11px"></span>
        <b>暖黄系</b> 开心·兴奋·调皮·骄傲·期待</div>
      <div style="display:flex;gap:3px;align-items:center;margin-bottom:2px">
        <span style="width:11px;height:11px;background:#ff9fc4;border:1px solid #999;flex:0 0 11px"></span>
        <b>粉红系</b> 亲昵·宠溺·感动·感激·吃醋</div>
      <div style="display:flex;gap:3px;align-items:center;margin-bottom:2px">
        <span style="width:11px;height:11px;background:#b8e6c4;border:1px solid #999;flex:0 0 11px"></span>
        <b>浅绿系</b> 平静·治愈·释然·中性</div>
      <div style="display:flex;gap:3px;align-items:center;margin-bottom:2px">
        <span style="width:11px;height:11px;background:#a8d8ff;border:1px solid #999;flex:0 0 11px"></span>
        <b>浅蓝系</b> 低落·难过·委屈·失望·怀念</div>
      <div style="display:flex;gap:3px;align-items:center;margin-bottom:2px">
        <span style="width:11px;height:11px;background:#ffb380;border:1px solid #999;flex:0 0 11px"></span>
        <b>橙红系</b> 生气·烦躁·焦虑·纠结</div>
      <div style="display:flex;gap:3px;align-items:center;margin-bottom:3px">
        <span style="width:11px;height:11px;background:#c9c0b5;border:1px solid #999;flex:0 0 11px"></span>
        <b>灰褐系</b> 无聊·疲惫·冷淡·尴尬·无奈·愧疚·惊讶</div>
    </div>
    <div class="hr"></div>
    <div class="lbl">明度随情绪分变化（以暖黄系为例）</div>
    <div style="display:flex;gap:2px">
      <div style="flex:1;height:17px;background:#ffd34d;border:1px solid #999;font-size:6.5px;text-align:center;line-height:17px">76-100</div>
      <div style="flex:1;height:17px;background:#ffe9a3;border:1px solid #999;font-size:6.5px;text-align:center;line-height:17px">51-75</div>
      <div style="flex:1;height:17px;background:#f2e6c4;border:1px solid #999;font-size:6.5px;text-align:center;line-height:17px">26-50</div>
      <div style="flex:1;height:17px;background:#dcd8cd;border:1px solid #999;font-size:6.5px;text-align:center;line-height:17px">0-25</div>
    </div>''', ics='<span class="ic">←</span>'),
  meta(
    ["6 个色系与 30 种情绪的完整映射表",
     "每色系的色块示例与所含情绪类型",
     "明度随情绪分变化的 4 档示例"],
    ["查阅映射关系", "返回"],
    [f"返回 {to('E2 情绪日历 / H4 规则说明')}"],
    ["颜色越鲜艳明亮代表情绪越好，越灰暗代表越差，与用户直觉对应。",
     "映射关系通过配置文件可调整。"])))

# E4 趋势空状态
w(screen("E4", "趋势 · 无数据（空状态）", "尚无任何评估结果时",
  phone("趋势", '''<div class="ctr">
    <div class="img" style="width:54px;height:54px">空</div>
    <div style="font-size:10.5px;font-weight:700">还没有可用的趋势数据</div>
    <div class="box" style="width:100%;font-size:9px;color:#555">
      完成聊天记录同步并生成每日评估后，这里会显示分数曲线与情绪日历</div>
    <div class="btn" style="width:100%">去时间墙看看</div>
  </div>''', nav="趋势"),
  meta(
    ["空状态标题「还没有可用的趋势数据」",
     "说明行「完成聊天记录同步并生成每日评估后，这里会显示分数曲线与情绪日历」",
     "「去时间墙看看」引导按钮"],
    ["点击「去时间墙看看」"],
    [f"点击引导 {to('B1 年视图')}",
     f"产生评估后 {to('E1 曲线')}"],
    ["空状态文案与引导按钮为本版新定。"])))
endgrp()
print("E 组完成：4 屏")

# ═══════════════════════════════════════════════ F 喜好与礼物
grp("gf", "F · 喜好与礼物（需求 10-11）",
    "同页双 Tab。喜好默认按星级降序，礼物默认按计划日期升序。筛选统一为底部浮层，常用维度默认展开、其余收进「更多筛选」，"
    "支持多选且跨会话保留。删除统一为长按触发 + 二次确认。共同喜好为喜好条目上的标记字段，通过筛选查看。")

# F1 喜好列表
w(screen("F1", "喜好 Tab · 列表（正常，核心屏）", "底部导航「喜好礼物」默认落地",
  phone("", '''<div class="ttl" style="font-size:11px;padding:4px 6px"><span>喜好与礼物</span>
      <span class="ic">🔍</span></div>
    <div style="display:flex;font-size:9px;border-bottom:1px solid #111">
      <div style="flex:1;text-align:center;padding:3px;background:#111;color:#fff;font-weight:700">喜好</div>
      <div style="flex:1;text-align:center;padding:3px">礼物</div></div>
    <div style="display:flex;justify-content:space-between;align-items:center">
      <span class="lbl">按星级降序 · 24 条</span>
      <span class="btn" style="padding:1px 5px;font-size:9px">筛选</span></div>
    <div class="box" style="font-size:9px;padding:4px">
      <div style="display:flex;justify-content:space-between">
        <b>草莓蛋糕</b><span>★★★★★</span></div>
      <div style="font-size:8px;color:#666">喜欢 · 甜点 · 共同喜欢 · 已加礼物</div></div>
    <div class="box" style="font-size:9px;padding:4px">
      <div style="display:flex;justify-content:space-between">
        <b>香菜</b><span>★★★★★</span></div>
      <div style="font-size:8px;color:#666">不喜欢 · 饮食 · 雷区</div></div>
    <div class="box" style="font-size:9px;padding:4px">
      <div style="display:flex;justify-content:space-between">
        <b>宫崎骏电影</b><span>★★★★☆</span></div>
      <div style="font-size:8px;color:#666">喜欢 · 影视 · 共同喜欢</div></div>
    <div class="box d" style="font-size:9px;color:#aaa;padding:3px">更多…</div>
    <div style="margin-top:auto"></div>
    <div class="btn pri" style="width:100%">+ 添加喜好</div>''', nav="喜好礼物"),
  meta(
    ["双 Tab：喜好 / 礼物",
     "排序说明「按星级降序」与总条数",
     "条目行：名称、星级、类型标识、分类、共同喜好标记、已加礼物标记",
     "喜欢与不喜欢统一列表，用类型标识区分",
     "搜索入口与筛选按钮", "底部「+ 添加喜好」"],
    ["点击条目查看/编辑", "长按条目打开操作面板", "点击「筛选」", "搜索", "点击「+ 添加喜好」"],
    [f"点击条目 {to('F2 编辑喜好')}",
     f"长按 {to('F4 操作面板（编辑 / 删除 / 加入礼物清单）')}",
     f"筛选 {to('F5 喜好筛选浮层')}",
     f"添加 {to('F2 新增喜好')}",
     f"切 Tab {to('F8 礼物清单')}"],
    ["默认排序：按星级降序，星级相同按更新时间降序。",
     "删除操作由长按触发。"])))

# F2 喜好编辑
w(screen("F2", "新增 / 编辑喜好条目", "F1 点击条目或「+ 添加喜好」",
  phone("添加喜好", '''<div class="lbl">名称（必填）</div>
    <div class="inp" style="border-color:#c00;color:#111">　</div>
    <div style="font-size:8.5px;color:#c00">请填写喜好名称</div>
    <div class="lbl">类型</div>
    <div><span class="chip on">喜欢</span><span class="chip">不喜欢</span></div>
    <div class="lbl">分类</div>
    <div class="inp" style="display:flex;justify-content:space-between"><span>其他</span><span>▾</span></div>
    <div class="lbl">星级</div>
    <div style="font-size:12px">★★★☆☆ <span style="font-size:8.5px;color:#666">默认 3</span></div>
    <div class="lbl">共同喜好标记</div>
    <div class="inp" style="display:flex;justify-content:space-between"><span>未设置</span><span>▾</span></div>
    <div class="lbl">备注（≤200）· 图片</div>
    <div class="row"><div class="inp">　</div><div class="img" style="height:22px">+图</div></div>
    <div style="margin-top:auto"></div>
    <div class="row"><div class="btn">取消</div><div class="btn dis">保存</div></div>''',
    ics='<span class="ic">←</span>'),
  meta(
    ["名称输入框（必填，校验失败时边框变红）",
     "字段级红色提示「请填写喜好名称」",
     "类型选择：喜欢 / 不喜欢，默认「喜欢」",
     "分类下拉（默认「其他」）",
     "星级 1-5 星，默认 3",
     "共同喜好标记下拉：共同喜欢 / 共同不喜欢 / TA 喜欢我不喜欢 / 待确认 / 独立喜好",
     "备注（≤200 字）、图片",
     "名称为空时保存按钮为禁用态"],
    ["填写名称", "选择类型 / 分类 / 星级 / 共同喜好标记",
     "点击分类下拉进入分类管理", "点击保存", "点击取消"],
    [f"保存成功 {to('F1 喜好列表')}",
     f"名称为空点保存 → 显示红色提示，停留本屏",
     f"分类下拉 {to('F3 分类管理')}", f"取消 {to('F1')}"],
    ["必填校验：名称为空时保存按钮为禁用态；点击后字段下方显示红色提示并将输入框边框变红，用户开始输入后提示消失。",
     "类型、分类均有默认值，表单打开即为已选中状态。",
     "「类型」代表 TA 的态度，共同喜好标记代表双方态度的组合关系；类型为喜欢且标记为「TA 喜欢我不喜欢」即 CONFLICT。"])))

# F3 分类管理
w(screen("F3", "分类管理", "F2 分类下拉中进入",
  phone("选择分类", '''<div class="lbl">内置分类（不可编辑删除）</div>
    <div style="font-size:8.5px;line-height:1.9">
      <span class="chip">饮食</span><span class="chip">饮品</span><span class="chip on">甜点</span>
      <span class="chip">音乐</span><span class="chip">影视</span><span class="chip">动漫</span>
      <span class="chip">游戏</span><span class="chip">书籍</span><span class="chip">运动</span>
      <span class="chip">旅行</span><span class="chip">其他</span>
      <span class="chip" style="color:#999">…共 26 项</span></div>
    <div class="hr"></div>
    <div class="lbl">我的分类（可编辑删除）</div>
    <div class="box" style="font-size:9px;padding:3px;display:flex;justify-content:space-between">
      <span>手冲咖啡</span><span style="font-size:8px">改 · 删</span></div>
    <div class="box" style="font-size:9px;padding:3px;display:flex;justify-content:space-between">
      <span>露营装备</span><span style="font-size:8px">改 · 删</span></div>
    <div class="btn" style="width:100%">+ 新增分类</div>
    <div class="box d" style="font-size:8px;color:#777">
      删除自定义分类后，使用该分类的喜好重置为「其他」</div>''',
    ics='<span class="ic">←</span>'),
  meta(
    ["内置分类区（26 项，chip 展示，不可编辑删除）",
     "我的分类区（用户自定义，每项带「改」「删」）",
     "「+ 新增分类」入口",
     "删除影响说明"],
    ["点击分类选中并返回", "点击「+ 新增分类」输入名称",
     "点击自定义分类的「改」重命名", "点击「删」删除自定义分类"],
    [f"选中分类 {to('F2 编辑喜好（分类已填）')}",
     f"新增分类 → 写入 PreferenceCategoryCustom，立即可选",
     f"删除自定义分类 → 相关喜好分类重置为「其他」"],
    ["分类支持自定义新增：内置分类不可编辑删除，用户新增的可编辑可删除。",
     "删除自定义分类时，使用该分类的喜好条目分类重置为「其他」。"])))

# F4 喜好长按面板 + 删除确认
w(screen("F4", "喜好长按面板 + 删除确认", "F1 长按条目后",
  phone("", '''<div class="box" style="font-size:9px;padding:3px;opacity:.45">草莓蛋糕 ★★★★★</div>
    <div class="box" style="font-size:9px;padding:3px;opacity:.45">香菜 ★★★★★</div>
    <div class="ovl mid"><div class="sheet" style="width:94%">
      <div style="font-weight:700;font-size:10px;text-align:center">删除确认</div>
      <div style="font-size:9px;text-align:center;line-height:1.6">
        删除后不可恢复，<br>确认删除「草莓蛋糕」？</div>
      <div class="box d" style="font-size:8px;color:#666">
        由它生成的礼物条目将保留，<br>并显示「来源喜好已删除」</div>
      <div class="row"><div class="btn">取消</div><div class="btn pri">删除</div></div>
    </div></div>''', nav="喜好礼物"),
  meta(
    ["长按先弹出操作面板：编辑、删除、加入礼物清单、取消",
     "选择删除后弹出二次确认弹窗",
     "确认文案「删除后不可恢复，确认删除「XXX」？」",
     "关联礼物处理说明"],
    ["点击「编辑」", "点击「删除」→ 二次确认", "点击「加入礼物清单」", "确认删除 / 取消"],
    [f"编辑 {to('F2 编辑喜好')}",
     f"加入礼物清单 {to('F6 加入礼物清单表单')}",
     f"确认删除 → 关联礼物保留、preferenceId 置空 {to('F1 列表（已移除该条）')}",
     f"取消 {to('F1 列表')}"],
    ["删除喜好需二次确认。",
     "删除后由它生成的礼物条目保留并断开关联，礼物详情显示「来源喜好已删除」。"])))

# F5 喜好筛选浮层
w(screen("F5", "喜好筛选（底部浮层）", "F1 点击「筛选」后",
  phone("", '''<div class="box" style="font-size:9px;padding:3px;opacity:.35">草莓蛋糕</div>
    <div class="ovl"><div class="sheet">
      <div style="display:flex;justify-content:space-between;font-size:10px;font-weight:700">
        <span>筛选</span><span style="font-size:8.5px;font-weight:400">重置筛选</span></div>
      <div class="hr"></div>
      <div class="lbl">类型（多选）</div>
      <div><span class="chip on">喜欢</span><span class="chip">不喜欢</span></div>
      <div class="lbl">分类（多选）</div>
      <div><span class="chip on">甜点</span><span class="chip on">影视</span>
        <span class="chip">饮食</span><span class="chip">音乐</span>
        <span class="chip" style="color:#999">展开全部</span></div>
      <div class="lbl">星级（多选）</div>
      <div><span class="chip">1</span><span class="chip">2</span><span class="chip">3</span>
        <span class="chip on">4</span><span class="chip on">5</span></div>
      <div class="hr"></div>
      <div class="box d" style="font-size:9px;text-align:center">▾ 更多筛选（3 项）</div>
      <div class="btn pri">查看 12 条结果</div>
    </div></div>''', nav="喜好礼物"),
  meta(
    ["底部浮层形态",
     "常用筛选默认展开：类型、分类、星级",
     "「更多筛选」折叠区：共同喜好状态（5 项）、是否已加入礼物清单、是否有图片",
     "所有维度支持多选（chip 多选态）",
     "「重置筛选」与结果数量按钮"],
    ["多选各维度条件", "展开「更多筛选」", "点击「重置筛选」", "点击「查看 N 条结果」"],
    [f"确认筛选 {to('F1 喜好列表（已过滤）')}",
     f"无匹配结果 {to('F7 无匹配结果态')}",
     f"重置 {to('F1 全量列表')}"],
    ["筛选维度多时，常用 3 个默认展开，其余收进「更多筛选」折叠区。",
     "各维度支持多选，筛选条件跨会话保留（写入 FilterState）。",
     "筛选呈现为底部浮层。"])))

# F6 加入礼物清单
w(screen("F6", "加入礼物清单（表单）", "F4 长按面板选择「加入礼物清单」",
  phone("加入礼物清单", '''<div class="lbl">礼物名称（带入喜好名称）</div>
    <div class="inp" style="color:#111">草莓蛋糕</div>
    <div class="lbl">礼物分类 · 礼物等级</div>
    <div class="row">
      <div class="inp" style="font-size:9px">日常小礼物 ▾</div>
      <div class="inp" style="font-size:9px">小 ▾</div></div>
    <div class="lbl">场合 · 预算档</div>
    <div class="row">
      <div class="inp" style="font-size:9px">生日 ▾</div>
      <div class="inp" style="font-size:9px">100-500 ▾</div></div>
    <div class="lbl">状态 · 优先级</div>
    <div class="row">
      <div class="inp" style="font-size:9px">想法 ▾</div>
      <div class="inp" style="font-size:9px">高 ▾</div></div>
    <div class="lbl">计划日期 · 备注</div>
    <div class="row">
      <div class="inp" style="font-size:9px">2026-12-20</div>
      <div class="inp" style="font-size:9px">　</div></div>
    <div style="margin-top:auto"></div>
    <div class="row"><div class="btn">取消</div><div class="btn pri">保存</div></div>''',
    ics='<span class="ic">←</span>'),
  meta(
    ["礼物名称自动带入喜好名称",
     "礼物分类、礼物等级", "场合、预算档",
     "状态、优先级",
     "计划日期、备注",
     "preferenceId 关联说明"],
    ["修改带入的名称", "选择各维度", "点击保存", "点击取消"],
    [f"保存成功 → 跳转礼物 Tab 并定位新建条目 {to('F8 礼物清单')}",
     f"取消 {to('F1 喜好列表')}"],
    ["表单包含优先级字段。",
     "保存后跳转礼物清单并定位到新建条目。",
     "一个喜好可生成多个礼物条目。"])))

# F7 喜好空状态
w(screen("F7", "喜好列表 · 空状态 / 无匹配结果", "无数据或筛选后无结果",
  phone("", '''<div style="display:flex;font-size:9px;border-bottom:1px solid #111">
      <div style="flex:1;text-align:center;padding:3px;background:#111;color:#fff;font-weight:700">喜好</div>
      <div style="flex:1;text-align:center;padding:3px">礼物</div></div>
    <div class="ctr">
      <div class="img" style="width:48px;height:48px">空</div>
      <div style="font-size:10px;font-weight:700">还没有记录喜好</div>
      <div class="box" style="width:100%;font-size:8.5px;color:#555">
        记下 TA 喜欢和不喜欢的东西，挑礼物的时候就有参考了</div>
      <div class="btn pri" style="width:100%">添加第一条喜好</div>
    </div>
    <div class="hr"></div>
    <div class="lbl">筛选后无结果时</div>
    <div class="box d" style="font-size:8.5px;text-align:center;line-height:1.6">
      没有符合条件的喜好<br>
      <span style="color:#666">试着减少筛选条件</span><br>
      <span class="btn" style="display:inline-block;padding:1px 6px;margin-top:2px">重置筛选</span></div>''',
    nav="喜好礼物"),
  meta(
    ["空状态：标题「还没有记录喜好」+ 说明行 + 「添加第一条喜好」",
     "无匹配结果：标题「没有符合条件的喜好」+ 说明行「试着减少筛选条件」+ 「重置筛选」",
     "两种空态文案与按钮不同"],
    ["点击「添加第一条喜好」", "点击「重置筛选」"],
    [f"添加 {to('F2 新增喜好')}", f"重置筛选 {to('F1 全量列表')}"],
    ["空状态与无匹配结果文案均为本版新定，两者区分呈现。"])))

# F8 礼物清单
w(screen("F8", "礼物 Tab · 清单（正常，核心屏）", "F1 切换 Tab 或 F6 保存后跳入",
  phone("", '''<div class="ttl" style="font-size:11px;padding:4px 6px"><span>喜好与礼物</span>
      <span class="ic">🔍</span></div>
    <div style="display:flex;font-size:9px;border-bottom:1px solid #111">
      <div style="flex:1;text-align:center;padding:3px">喜好</div>
      <div style="flex:1;text-align:center;padding:3px;background:#111;color:#fff;font-weight:700">礼物</div></div>
    <div style="display:flex;justify-content:space-between;align-items:center">
      <span class="lbl">按计划日期升序 · 9 条</span>
      <span class="btn" style="padding:1px 5px;font-size:9px">筛选</span></div>
    <div class="box" style="font-size:9px;padding:4px">
      <div style="display:flex;justify-content:space-between">
        <b>草莓蛋糕</b><span class="tag k">想法</span></div>
      <div style="font-size:8px;color:#666">日常小礼物 · 小 · 生日 · 高 · 计划 12-20</div></div>
    <div class="box" style="font-size:9px;padding:4px">
      <div style="display:flex;justify-content:space-between">
        <b>蓝牙耳机</b><span class="tag">已购买</span></div>
      <div style="font-size:8px;color:#666">实用礼物 · 中 · 纪念日 · 中 · 计划 12-25</div></div>
    <div class="box" style="font-size:9px;padding:4px">
      <div style="display:flex;justify-content:space-between">
        <b>手冲壶</b><span class="tag">已送出</span></div>
      <div style="font-size:8px;color:#666">定制礼物 · 中 · 日常 · 低 · 送出 11-08</div></div>
    <div class="box d" style="font-size:8px;color:#777">已取消 / 已归档条目不在此列表</div>
    <div style="margin-top:auto"></div>
    <div class="row">
      <div class="btn">归档视图</div><div class="btn pri">+ 添加礼物</div></div>''',
    nav="喜好礼物"),
  meta(
    ["排序说明「按计划日期升序」与总条数",
     "条目行：名称、状态标签、分类、等级、场合、优先级、计划/送出日期",
     "主列表隐藏「已取消」与「已归档」",
     "「归档视图」入口与「+ 添加礼物」"],
    ["点击条目编辑", "长按条目删除", "点击状态标签流转状态",
     "点击「筛选」", "点击「归档视图」", "点击「+ 添加礼物」"],
    [f"点击条目 {to('F9 编辑礼物')}",
     f"点击状态标签 {to('F10 状态流转浮层')}",
     f"筛选 {to('F11 礼物筛选浮层')}",
     f"归档视图 {to('F13 归档视图')}",
     f"长按 → 删除二次确认 {to('F8 列表')}"],
    ["默认排序：按计划日期升序，无计划日期排在最后并按更新时间降序。",
     "主列表隐藏已取消与已归档，另设独立归档视图。"])))

# F9 礼物编辑
w(screen("F9", "新增 / 编辑礼物条目", "F8 点击条目或「+ 添加礼物」",
  phone("编辑礼物", '''<div class="lbl">礼物名称（必填）</div>
    <div class="inp" style="color:#111">蓝牙耳机</div>
    <div class="lbl">关联喜好（下拉选择，可解除）</div>
    <div class="inp" style="display:flex;justify-content:space-between;font-size:9px">
      <span>无线耳机</span><span>▾</span></div>
    <div class="lbl">分类 · 等级 · 场合</div>
    <div class="g3" style="gap:3px">
      <div class="inp" style="font-size:8px">实用 ▾</div>
      <div class="inp" style="font-size:8px">中 ▾</div>
      <div class="inp" style="font-size:8px">纪念日 ▾</div></div>
    <div class="lbl">状态 · 优先级 · 预算档</div>
    <div class="g3" style="gap:3px">
      <div class="inp" style="font-size:8px">已购买 ▾</div>
      <div class="inp" style="font-size:8px">中 ▾</div>
      <div class="inp" style="font-size:8px">500-1000 ▾</div></div>
    <div class="lbl">计划日期 · 送出日期</div>
    <div class="row">
      <div class="inp" style="font-size:9px">2026-12-25</div>
      <div class="inp" style="font-size:9px;color:#aaa">未送出</div></div>
    <div class="lbl">备注（≤200）· 图片</div>
    <div class="row"><div class="inp">　</div><div class="img" style="height:22px">+图</div></div>
    <div style="margin-top:auto"></div>
    <div class="row"><div class="btn">取消</div><div class="btn pri">保存</div></div>''',
    ics='<span class="ic">←</span>'),
  meta(
    ["礼物名称（必填）",
     "关联喜好通过下拉选择变更或解除关联",
     "分类、等级、场合（均必填且有默认值）",
     "状态、优先级、预算档",
     "计划日期、送出日期（状态流转自动写入，可手动改）",
     "备注（≤200 字）、图片"],
    ["填写名称", "下拉变更或解除关联喜好", "选择各维度", "修改送出日期", "保存 / 取消"],
    [f"保存成功 {to('F8 礼物清单')}",
     f"名称为空点保存 → 红色提示「请填写礼物名称」",
     f"取消 {to('F8')}"],
    ["必填字段：礼物名称；分类、等级、场合、状态、优先级均有默认值。",
     "关联喜好通过下拉选择变更或解除，不手动编辑内容。",
     "送出日期在条目详情与列表项上展示。"])))

# F10 状态流转
w(screen("F10", "礼物状态流转（浮层）", "F8 点击状态标签后",
  phone("", '''<div class="box" style="font-size:9px;padding:3px;opacity:.35">蓝牙耳机 已购买</div>
    <div class="ovl"><div class="sheet">
      <div style="font-size:10px;font-weight:700;text-align:center">蓝牙耳机 · 状态</div>
      <div class="hr"></div>
      <div class="btn">想法</div>
      <div class="btn">待购买</div>
      <div class="btn pri">已购买（当前）</div>
      <div class="btn">已送出</div>
      <div class="btn">已收到</div>
      <div class="hr"></div>
      <div class="btn">已取消</div>
      <div class="btn">已归档</div>
      <div class="box d" style="font-size:7.8px;color:#666;line-height:1.5">
        已送出＝已寄出或交付，尚未确认收到<br>
        已收到＝已确认对方收到<br>
        切到已送出/已收到自动写入当天为送出日期</div>
    </div></div>''', nav="喜好礼物"),
  meta(
    ["全部 7 个状态直接列出，可任意跳转与回退",
     "当前状态高亮标注",
     "已送出 / 已收到语义说明",
     "送出日期自动写入说明"],
    ["点击任意状态直接切换"],
    [f"切到已送出 → 自动写入当天为送出日期 {to('F8 列表（状态与日期刷新）')}",
     f"切到已收到 → 送出日期为空时自动写入当天 {to('F8 列表')}",
     f"切到已取消 / 已归档 → 从主列表移除 {to('F13 归档视图可见')}"],
    ["状态支持任意跳转与回退，不限制只能正向流转。",
     "已送出表示快递已寄出或已交付但尚未确认收到；已收到表示已确认对方收到。",
     "状态变更为已送出或已收到时自动写入送出日期。"])))

# F11 礼物筛选
w(screen("F11", "礼物筛选（底部浮层）", "F8 点击「筛选」后",
  phone("", '''<div class="box" style="font-size:9px;padding:3px;opacity:.35">草莓蛋糕</div>
    <div class="ovl"><div class="sheet">
      <div style="display:flex;justify-content:space-between;font-size:10px;font-weight:700">
        <span>筛选</span><span style="font-size:8.5px;font-weight:400">重置筛选</span></div>
      <div class="hr"></div>
      <div class="lbl">状态（多选）</div>
      <div><span class="chip on">想法</span><span class="chip on">待购买</span>
        <span class="chip">已购买</span><span class="chip">已送出</span><span class="chip">已收到</span></div>
      <div class="lbl">分类（多选）</div>
      <div><span class="chip on">日常小礼物</span><span class="chip">生日礼物</span>
        <span class="chip" style="color:#999">展开全部</span></div>
      <div class="lbl">优先级（多选）</div>
      <div><span class="chip">低</span><span class="chip on">中</span><span class="chip on">高</span></div>
      <div class="hr"></div>
      <div class="box d" style="font-size:9px;text-align:center">▾ 更多筛选（4 项）</div>
      <div class="btn pri">查看 5 条结果</div>
    </div></div>''', nav="喜好礼物"),
  meta(
    ["底部浮层形态",
     "常用筛选默认展开：状态、分类、优先级",
     "「更多筛选」折叠区：等级、场合、<b>预算档</b>、是否有关联喜好",
     "所有维度支持多选", "「重置筛选」与结果数量按钮"],
    ["多选各维度", "展开「更多筛选」", "重置筛选", "查看结果"],
    [f"确认筛选 {to('F8 礼物清单（已过滤）')}",
     f"无匹配 {to('F14 无匹配结果态')}", f"重置 {to('F8 全量列表')}"],
    ["礼物筛选维度补充预算档。",
     "支持多选且条件跨会话持久化。",
     "常用 3 项默认展开，其余 4 项收进「更多筛选」。"])))

# F12 来源追溯
w(screen("F12", "礼物详情 · 来源追溯", "F8 点击条目进入详情区",
  phone("蓝牙耳机", '''<div class="box" style="font-size:9px;padding:4px">
      <div style="display:flex;justify-content:space-between">
        <b>蓝牙耳机</b><span class="tag">已购买</span></div>
      <div style="font-size:8px;color:#666;margin-top:2px">
        实用礼物 · 中 · 纪念日 · 优先级 中<br>预算 500-1000 · 计划 12-25</div></div>
    <div class="lbl">来源喜好</div>
    <div class="box" style="font-size:9px;padding:3px;display:flex;justify-content:space-between">
      <span>无线耳机</span><span class="ic">查看 ›</span></div>
    <div class="hr"></div>
    <div class="lbl">其他两种来源状态</div>
    <div class="box d" style="font-size:8.5px;padding:3px">无关联喜好</div>
    <div class="box d" style="font-size:8.5px;padding:3px;color:#999">
      来源喜好已删除<span style="font-size:7.5px">（纯文本）</span></div>
    <div style="margin-top:auto"></div>
    <div class="row"><div class="btn">编辑</div><div class="btn">状态</div></div>''',
    nav="喜好礼物", ics='<span class="ic">←</span>'),
  meta(
    ["礼物信息摘要区",
     "来源喜好行，可点击跳转",
     "三种来源状态：可跳转 / 无关联喜好 / 来源喜好已删除（显示为纯文本）",
     "编辑与状态入口"],
    ["点击来源喜好「查看」", "点击「编辑」", "点击「状态」"],
    [f"点击来源喜好 {to('F1 喜好 Tab 并定位该条目')}",
     f"编辑 {to('F9 编辑礼物')}", f"状态 {to('F10 状态流转')}"],
    ["礼物条目可反向跳转到来源喜好并定位。",
     "preferenceId 为空显示「无关联喜好」；来源喜好已删除时该行显示为纯文本「来源喜好已删除」。"])))

# F13 归档视图
w(screen("F13", "礼物归档视图", "F8 点击「归档视图」",
  phone("归档", '''<div class="lbl">已取消 / 已归档 · 4 条</div>
    <div class="box" style="font-size:9px;padding:4px">
      <div style="display:flex;justify-content:space-between">
        <b>限量手办</b><span class="tag">已取消</span></div>
      <div style="font-size:8px;color:#666">收藏品 · 大 · 生日 · 已下架</div>
      <div class="btn" style="margin-top:3px;padding:1px">恢复为「想法」</div></div>
    <div class="box" style="font-size:9px;padding:4px">
      <div style="display:flex;justify-content:space-between">
        <b>去年的围巾</b><span class="tag">已归档</span></div>
      <div style="font-size:8px;color:#666">实用礼物 · 小 · 已送出 2025-12-24</div>
      <div class="btn" style="margin-top:3px;padding:1px">恢复为「已送出」</div></div>
    <div class="box d" style="font-size:8px;color:#aaa">更多…</div>
    <div class="hr"></div>
    <div class="box d" style="font-size:8.5px;text-align:center;color:#777">
      归档为空时：没有已归档的礼物</div>''',
    nav="喜好礼物", ics='<span class="ic">←</span>'),
  meta(
    ["归档列表，展示已取消与已归档条目",
     "每条带「恢复为 XXX」按钮",
     "空状态文案「没有已归档的礼物」"],
    ["点击条目查看详情", "点击「恢复为 XXX」", "长按删除", "返回主列表"],
    [f"恢复状态 {to('F8 主列表（重新可见）')}",
     f"点击条目 {to('F9 编辑礼物')}", f"返回 {to('F8 礼物清单')}"],
    ["已取消与已归档条目默认在主列表隐藏，另设独立归档视图，支持恢复为其他状态。"])))

# F14 礼物空状态
w(screen("F14", "礼物清单 · 空状态 / 无匹配结果", "无数据或筛选后无结果",
  phone("", '''<div style="display:flex;font-size:9px;border-bottom:1px solid #111">
      <div style="flex:1;text-align:center;padding:3px">喜好</div>
      <div style="flex:1;text-align:center;padding:3px;background:#111;color:#fff;font-weight:700">礼物</div></div>
    <div class="ctr">
      <div class="img" style="width:48px;height:48px">空</div>
      <div style="font-size:10px;font-weight:700">礼物清单还是空的</div>
      <div class="box" style="width:100%;font-size:8.5px;color:#555">
        把想送的东西记下来，到了日子就不会手忙脚乱</div>
      <div class="btn pri" style="width:100%">添加第一个礼物</div>
    </div>
    <div class="hr"></div>
    <div class="lbl">筛选后无结果时</div>
    <div class="box d" style="font-size:8.5px;text-align:center;line-height:1.6">
      没有符合条件的礼物<br>
      <span style="color:#666">试着减少筛选条件</span><br>
      <span class="btn" style="display:inline-block;padding:1px 6px;margin-top:2px">重置筛选</span></div>''',
    nav="喜好礼物"),
  meta(
    ["空状态：标题「礼物清单还是空的」+ 说明行 + 「添加第一个礼物」",
     "无匹配结果：标题「没有符合条件的礼物」+ 「重置筛选」",
     "归档视图空态另有文案「没有已归档的礼物」"],
    ["点击「添加第一个礼物」", "点击「重置筛选」"],
    [f"添加 {to('F9 新增礼物')}", f"重置筛选 {to('F8 全量列表')}"],
    ["空状态文案与引导按钮为本版新定，三种空态（无数据 / 无匹配 / 归档为空）文案各自区分。"])))
endgrp()
print("F 组完成：14 屏")

# ═══════════════════════════════════════════════ G 回忆
grp("gg", "G · 回忆（高光）（需求 8）",
    "自动触发：总分≥85 且情绪分≥70，或总分≥90。类型按综合高光 → 高亲密 → 高情绪 → 有趣对话 → 高总分的优先级判定。"
    "日详情可手动标记高光。长按删除；该日期重新评估并仍达标时重新生成高光记录。")

# G1 高光列表
w(screen("G1", "回忆 · 高光列表（正常）", "底部导航「回忆」",
  phone("回忆", '''<div style="font-size:8.5px">
      <span class="chip on">全部</span><span class="chip">综合</span><span class="chip">高亲密</span>
      <span class="chip">高情绪</span><span class="chip">有趣</span><span class="chip">高总分</span></div>
    <div class="lbl">按日期倒序 · 7 条</div>
    <div class="box" style="font-size:9px;padding:0;display:flex;gap:4px">
      <div class="img" style="width:46px;height:46px;border:0;font-size:7px">L5</div>
      <div style="padding:3px;flex:1">
        <div style="display:flex;justify-content:space-between">
          <b>11月11日</b><span class="tag k">综合高光</span></div>
        <div style="font-size:8px;color:#666">🌈 88 / 85 · 😊 开心</div>
        <div style="font-size:8px">今天聊了旅行计划…</div></div></div>
    <div class="box" style="font-size:9px;padding:0;display:flex;gap:4px">
      <div class="img" style="width:46px;height:46px;border:0;font-size:7px">L5</div>
      <div style="padding:3px;flex:1">
        <div style="display:flex;justify-content:space-between">
          <b>11月03日</b><span class="tag">高亲密</span></div>
        <div style="font-size:8px;color:#666">☀ 91 / 93 · 🥰 亲昵</div>
        <div style="font-size:8px">说了很多心里话…</div></div></div>
    <div class="box" style="font-size:9px;padding:0;display:flex;gap:4px">
      <div class="img" style="width:46px;height:46px;border:0;font-size:7px">L4</div>
      <div style="padding:3px;flex:1">
        <div style="display:flex;justify-content:space-between">
          <b>10月28日</b><span class="tag">有趣对话</span></div>
        <div style="font-size:8px;color:#666">☀ 87 / 80 · 😄 调皮</div>
        <div style="font-size:8px">互相讲冷笑话…</div></div></div>''', nav="回忆"),
  meta(
    ["顶部类型筛选条：全部 + 5 种高光类型",
     "列表按日期倒序",
     "每条：封面缩略图、日期、高光类型标签、天气、总分/亲密度、情绪、总结摘要"],
    ["点击类型筛选条过滤", "点击条目进入日详情", "长按条目删除"],
    [f"点击条目 {to('D1 日详情')}",
     f"点击类型筛选 {to('G3 类型筛选态')}",
     f"长按 {to('G2 删除确认')}"],
    ["高光列表支持按高光类型筛选。",
     "高光快照含：日期、总分、情绪类型、情绪分、亲密度、总结、亮点、封面等级、天气、高光类型。"])))

# G2 删除确认
w(screen("G2", "删除高光确认（弹窗）", "G1 长按条目后",
  phone("回忆", '''<div class="box" style="font-size:9px;padding:3px;opacity:.4">11月11日 综合高光</div>
    <div class="box" style="font-size:9px;padding:3px;opacity:.4">11月03日 高亲密</div>
    <div class="ovl mid"><div class="sheet" style="width:94%">
      <div style="font-weight:700;font-size:10px;text-align:center">删除高光回忆</div>
      <div style="font-size:9px;text-align:center;line-height:1.6">
        确认删除 11月11日 的高光回忆？</div>
      <div class="box d" style="font-size:8px;color:#666;line-height:1.5">
        该日聊天记录与评估数据保持完整<br>
        删除为终态<br>
        重新评估若仍达标会再次自动生成</div>
      <div class="row"><div class="btn">取消</div><div class="btn pri">删除</div></div>
    </div></div>''', nav="回忆"),
  meta(
    ["删除确认弹窗", "影响说明三条",
     "取消 / 删除按钮"],
    ["点击「删除」", "点击「取消」或遮罩"],
    [f"删除 → 标记 HighlightMemory.deleted {to('G1 列表（已移除）')}",
     f"取消 {to('G1 列表')}"],
    ["长按触发删除，删除后标记 deleted，原始日数据保持完整。",
     "删除后该日期重新评估并仍达标时重新生成高光记录。",
     "已删除高光的日期重新评估后若仍满足触发条件，重新自动生成。"])))

# G3 类型筛选态
w(screen("G3", "回忆 · 类型筛选态", "G1 点击类型筛选条后",
  phone("回忆", '''<div style="font-size:8.5px">
      <span class="chip">全部</span><span class="chip">综合</span><span class="chip on">高亲密</span>
      <span class="chip">高情绪</span><span class="chip">有趣</span><span class="chip">高总分</span></div>
    <div class="lbl">高亲密 · 2 条</div>
    <div class="box" style="font-size:9px;padding:0;display:flex;gap:4px">
      <div class="img" style="width:46px;height:46px;border:0;font-size:7px">L5</div>
      <div style="padding:3px;flex:1">
        <div style="display:flex;justify-content:space-between">
          <b>11月03日</b><span class="tag">高亲密</span></div>
        <div style="font-size:8px;color:#666">☀ 91 / 93 · 🥰 亲昵</div></div></div>
    <div class="box" style="font-size:9px;padding:0;display:flex;gap:4px">
      <div class="img" style="width:46px;height:46px;border:0;font-size:7px">L5</div>
      <div style="padding:3px;flex:1">
        <div style="display:flex;justify-content:space-between">
          <b>09月14日</b><span class="tag">高亲密</span></div>
        <div style="font-size:8px;color:#666">🌈 89 / 92 · 🥰 亲昵</div></div></div>
    <div class="hr"></div>
    <div class="lbl">类型判定优先级</div>
    <div class="box" style="font-size:7.8px;line-height:1.6;padding:3px">
      1 综合高光 总分≥90 且情绪≥85 且亲密≥85<br>
      2 高亲密 亲密度≥90<br>
      3 高情绪 情绪分≥90<br>
      4 有趣对话 有趣内容≥2 条<br>
      5 高总分 其余达标情况</div>''', nav="回忆"),
  meta(
    ["选中的类型 chip 高亮",
     "结果数量提示",
     "过滤后的高光列表",
     "类型判定优先级速查"],
    ["切换类型筛选", "点击「全部」恢复", "点击条目进入日详情"],
    [f"点击条目 {to('D1 日详情')}", f"点击全部 {to('G1 完整列表')}"],
    ["高光类型按 5 级优先级判定，前一条命中即停止。",
     "手动标记的高光类型固定为综合高光。"])))

# G4 空状态
w(screen("G4", "回忆 · 无高光（空状态）", "尚无满足阈值的日期",
  phone("回忆", '''<div class="ctr">
    <div class="img" style="width:50px;height:50px">空</div>
    <div style="font-size:10.5px;font-weight:700">还没有高光回忆</div>
    <div class="box" style="width:100%;font-size:8.5px;color:#555;line-height:1.6">
      总分达到 85 且情绪分达到 70，<br>或总分达到 90 的日期<br>会自动成为高光回忆</div>
    <div class="btn pri" style="width:100%">去时间墙看看</div>
  </div>''', nav="回忆"),
  meta(
    ["空状态标题「还没有高光回忆」",
     "说明行展示当前阈值（85/70/90，从配置读取）",
     "「去时间墙看看」引导按钮"],
    ["点击「去时间墙看看」"],
    [f"点击引导 {to('B1 年视图')}",
     f"产生高光后 {to('G1 高光列表')}"],
    ["空状态向用户暴露具体阈值数字，数字从配置读取，不硬编码在文案中。"])))
endgrp()
print("G 组完成：4 屏")

# ═══════════════════════════════════════════════ H 设置
grp("gh", "H · 设置（需求 12）",
    "设置页提供同步状态与「立即同步」作为 A5/A7/A8 重试流程的用户侧落点。"
    "主题提供纸月历、星图、色域、磨砂玻璃 4 套，点击即应用。"
    "默认卡片状态决定进入月视图时全部卡片的初始状态，单张卡片的切换结果为视图层临时状态。")

# H1 设置首页
w(screen("H1", "设置首页", "底部导航「设置」",
  phone("设置", '''<div class="lbl">同步</div>
    <div class="box" style="font-size:9px;padding:4px">
      <div style="display:flex;justify-content:space-between">
        <span>同步状态</span><b>部分成功</b></div>
      <div style="font-size:8px;color:#666;margin-top:2px">
        上次同步 11-13 23:00<br>已同步 27 天 · 失败 3 天</div>
      <div class="row" style="margin-top:3px">
        <div class="btn">查看失败日期</div><div class="btn pri">立即同步</div></div></div>
    <div class="lbl">偏好</div>
    <div class="box" style="font-size:9px;padding:3px;display:flex;justify-content:space-between">
      <span>主题</span><span style="color:#666">纸月历 ›</span></div>
    <div class="box" style="font-size:9px;padding:3px;display:flex;justify-content:space-between">
      <span>显示偏好</span><span>›</span></div>
    <div class="lbl">说明</div>
    <div class="box" style="font-size:9px;padding:3px;display:flex;justify-content:space-between">
      <span>隐私说明</span><span>›</span></div>
    <div class="box" style="font-size:9px;padding:3px;display:flex;justify-content:space-between">
      <span>封面与天气规则说明</span><span>›</span></div>
    <div class="lbl">其他</div>
    <div class="box" style="font-size:9px;padding:3px;display:flex;justify-content:space-between">
      <span>关于</span><span>›</span></div>''', nav="设置"),
  meta(
    ["同步分组：同步状态、上次同步时间、已同步天数、失败天数",
     "「立即同步」按钮",
     "失败天数不为零时显示「查看失败日期」",
     "偏好分组：主题（右侧显示当前主题名）、显示偏好",
     "说明分组：隐私说明、封面与天气规则说明",
     "其他分组：关于"],
    ["点击「立即同步」", "点击「查看失败日期」", "进入各子页"],
    [f"立即同步 {to('A5 同步中')}",
     f"查看失败日期 {to('H8 失败日期列表')}",
     f"主题 {to('H2 主题选择')}", f"显示偏好 {to('H4')}", f"隐私说明 {to('H5')}",
     f"规则说明 {to('H6')}", f"关于 {to('H7')}"],
    ["设置页展示同步状态并提供「立即同步」，作为 A5/A7/A8 重试流程的用户侧落点。"])))

# H2 主题选择
w(screen("H2", "主题选择", "H1 进入 · 4 套主题单选",
  phone("主题", '''<div class="g2">
      <div class="box" style="padding:3px">
        <div class="img" style="height:46px">纸月历预览</div>
        <div style="font-size:9px;font-weight:700;margin-top:2px">纸月历 ✓</div>
        <div style="font-size:7.6px;color:#666">米白纸张 · 细网格 · 衬线标题</div></div>
      <div class="box" style="padding:3px">
        <div class="img" style="height:46px">星图预览</div>
        <div style="font-size:9px;font-weight:700;margin-top:2px">星图</div>
        <div style="font-size:7.6px;color:#666">深蓝夜空 · 星点连线</div></div>
      <div class="box" style="padding:3px">
        <div class="img" style="height:46px">色域预览</div>
        <div style="font-size:9px;font-weight:700;margin-top:2px">色域</div>
        <div style="font-size:7.6px;color:#666">纯白底 · 情绪色块铺满</div></div>
      <div class="box" style="padding:3px">
        <div class="img" style="height:46px">磨砂玻璃预览</div>
        <div style="font-size:9px;font-weight:700;margin-top:2px">磨砂玻璃</div>
        <div style="font-size:7.6px;color:#666">封面模糊 · 半透明面板</div></div>
    </div>''', nav="设置"),
  meta(
    ["2 列网格，4 个主题预览图",
     "每格：预览图、主题名、视觉特征说明",
     "当前选中项带勾选标识",
     "主题枚举：PAPER_CALENDAR / STAR_MAP / COLOR_FIELD / FROSTED_GLASS"],
    ["点击任一主题立即应用", "返回设置首页"],
    [f"选择主题 {to('H3 主题应用效果')}",
     f"返回 {to('H1 设置首页（主题行显示新主题名）')}"],
    ["点击立即应用并写入 UserPreference.theme，返回即生效。",
     "主题作用范围：全局底色、卡片容器样式、字体族、分隔线、按钮与标签样式。",
     "封面等级、天气图标、情绪色系的映射规则在 4 套主题下保持一致，随主题变化的部分限于呈现样式。"])))

# H3 主题应用效果
w(screen("H3", "主题应用效果 · 月视图对照", "H2 切换主题后的月视图呈现",
  phone("2026年11月", '''<div class="lbl">纸月历（默认）</div>
    <div class="g2">
      <div class="dcard" style="height:38px">13<br><span style="font-size:7px">晴 · 86</span></div>
      <div class="dcard" style="height:38px">14<br><span style="font-size:7px">多云 · 78</span></div>
    </div>
    <div class="lbl">星图</div>
    <div class="g2">
      <div class="dcard" style="height:38px;background:#2b3a55;color:#fff">13<br><span style="font-size:7px">晴 · 86</span></div>
      <div class="dcard" style="height:38px;background:#2b3a55;color:#fff">14<br><span style="font-size:7px">多云 · 78</span></div>
    </div>
    <div class="lbl">色域 / 磨砂玻璃</div>
    <div class="g2">
      <div class="dcard" style="height:38px;background:#ffd98a">13<br><span style="font-size:7px">晴 · 86</span></div>
      <div class="dcard" style="height:38px;background:#e8e8e8">14<br><span style="font-size:7px">多云 · 78</span></div>
    </div>''', nav="时间墙"),
  meta(
    ["同一份数据在 4 套主题下的卡片呈现对照",
     "日期、天气、分数等数据字段在各主题下一致",
     "随主题变化的部分：底色、卡片容器、字体、分隔线"],
    ["浏览对照效果", "返回设置继续切换"],
    [f"返回 {to('H2 主题选择')}", f"进入日详情 {to('D1 日详情')}"],
    ["情绪色系在各主题下保持相同色相序列，由主题调整饱和度与底色对比，越鲜艳明亮越好的辨识方向在 4 套主题下一致。",
     "封面状态在 4 套主题下均展示封面图，情绪色块以蒙层叠加：纸月历与星图 15%、色域 45%、磨砂玻璃 30%。日期角标、天气与情绪图标绘制在蒙层之上。"])))

# H2 显示偏好
w(screen("H4", "显示偏好", "H1 进入 · 5 项配置",
  phone("显示偏好", '''<div class="lbl">默认卡片状态</div>
    <div class="box" style="font-size:9px;padding:3px">
      <div style="display:flex;justify-content:space-between"><span>封面</span><span>●</span></div>
      <div class="hr"></div>
      <div style="display:flex;justify-content:space-between"><span>日期数字</span><span>○</span></div>
      <div class="hr"></div>
      <div style="display:flex;justify-content:space-between"><span>一句话总结</span><span>○</span></div></div>
    <div class="box d" style="font-size:8px;color:#666">
      修改后全部日卡片立即切换为所选状态</div>
    <div class="lbl">趋势默认指标</div>
    <div><span class="chip on">总分</span><span class="chip">亲密度</span><span class="chip">情绪分</span></div>
    <div class="lbl">趋势默认粒度</div>
    <div><span class="chip">周</span><span class="chip on">月</span><span class="chip">年</span></div>
    <div class="box" style="font-size:9px;padding:3px;display:flex;justify-content:space-between">
      <span>曲线叠加显示</span><span>○—</span></div>
    <div class="box" style="font-size:9px;padding:3px;display:flex;justify-content:space-between">
      <span>日详情互动统计默认展开</span><span>—●</span></div>''',
    nav="设置", ics='<span class="ic">←</span>'),
  meta(
    ["默认卡片状态单选：封面 / 日期数字 / 一句话总结",
     "修改后全部日卡片立即切换",
     "趋势默认指标单选", "趋势默认粒度单选",
     "曲线叠加显示开关", "日详情互动统计默认展开开关"],
    ["选择默认卡片状态", "选择趋势默认指标与粒度", "切换两个开关"],
    [f"修改默认卡片状态 → 下次进入月视图生效 {to('B3 月视图')}",
     f"修改趋势偏好 {to('E1 曲线（按新默认加载）')}"],
    ["默认卡片状态作用于进入月视图时的初始化；进入后单张卡片独立切换，切换结果随月视图生命周期存在。",
     "显示偏好共 5 项：默认卡片状态、趋势默认指标、趋势默认粒度、曲线叠加、统计默认展开。"])))

# H5 隐私说明
w(screen("H5", "隐私说明（只读）", "H1 进入",
  phone("隐私说明", '''<div class="box" style="font-size:9px;padding:4px;line-height:1.8">
      <b>本地存储</b><br>
      聊天记录在本地加密存储</div>
    <div class="box" style="font-size:9px;padding:4px;line-height:1.8">
      <b>凭据保管</b><br>
      后端 Token 与 AI Key 存入系统安全存储</div>
    <div class="box" style="font-size:9px;padding:4px;line-height:1.8">
      <b>AI 调用</b><br>
      AI 调用对手机号、身份证号、银行卡号、<br>邮箱、详细地址、验证码执行替换<br>本地保留原文</div>
    <div class="box" style="font-size:9px;padding:4px;line-height:1.8">
      <b>用户编辑数据</b><br>
      总结、备注、收藏、喜好、礼物仅保存在本地</div>''',
    nav="设置", ics='<span class="ic">←</span>'),
  meta(
    ["本地加密存储说明", "Token 与 AI Key 安全存储说明",
     "AI 调用脱敏说明（替换对象清单）", "用户编辑数据仅本地保存说明"],
    ["阅读", "返回"],
    [f"返回 {to('H1 设置首页')}"],
    None)))

# H4 封面与天气规则
w(screen("H6", "封面与天气规则说明（只读）", "H1 进入 · 合并展示三套规则",
  phone("规则说明", '''<div class="lbl">综合关系分</div>
    <div class="box" style="font-size:8.5px;padding:3px">
      = 亲密度 × 0.6 + 情绪分 × 0.4（四舍五入）</div>
    <div class="lbl">封面等级</div>
    <div class="box" style="font-size:8px;padding:3px;line-height:1.7">
      L1 0-20 · L2 21-40 · L3 41-60<br>L4 61-80 · L5 81-100</div>
    <div class="lbl">天气综合分</div>
    <div class="box" style="font-size:8.5px;padding:3px">
      = 总分 × 0.5 + 情绪分 × 0.3 + 亲密度 × 0.2
      <div style="font-size:7.6px;color:#666;margin-top:1px">
        与封面综合分独立计算，侧重当天体感</div></div>
    <div class="lbl">日天气判定优先级</div>
    <div class="box" style="font-size:7.6px;padding:3px;line-height:1.6">
      1 待评估 未同步或评估未完成<br>
      2 🌫 雾 置信度 &lt; 40<br>
      3 ❄ 雪 消息总条数 &lt; 10 且情绪分 ≥ 50<br>
      4-12 按天气综合分区间：<br>
      🌈95-100 ☀85-94 ⛅75-84 ☁65-74<br>
      🌬55-64 🌦45-54 🌧35-44 ⛈25-34 ⚡0-24</div>
    <div class="box d" style="font-size:7.8px;color:#666">
      雪与雾优先于分数区间，同一分数不会命中两种天气<br>
      周/月天气按天气综合分平均值映射，不应用雾与雪</div>
    <div class="lbl">情绪色系</div>
    <div class="box" style="font-size:7.6px;padding:3px">
      暖黄·粉红·浅绿·浅蓝·橙红·灰褐 6 色系<br>
      色相表类型，明度表情绪分 <span class="ic">查看全表 ›</span></div>''',
    nav="设置", ics='<span class="ic">←</span>'),
  meta(
    ["封面综合关系分公式（亲密度×0.6 + 情绪分×0.4）", "L1-L5 等级区间表",
     "天气综合分公式（总分×0.5 + 情绪分×0.3 + 亲密度×0.2）与权重含义",
     "日天气判定优先级表（含雾与雪触发条件）",
     "雪雾优先级与周期天气说明",
     "情绪色系概览与查看全表入口"],
    ["阅读规则", "点击「查看全表」", "返回"],
    [f"查看色系全表 {to('E3 情绪色系映射速查')}",
     f"返回 {to('H1 设置首页')}"],
    ["雪的可执行阈值：消息总条数 &lt; 10 且情绪分 ≥ 50。",
     "雾的可执行阈值：置信度 &lt;40（AI 输出新增 confidence 字段）。",
     "按优先级依次判定，前一条命中即停止，消除分数区间重叠冲突。",
     "本页同时展示封面规则与天气规则。"])))

# H5 关于
w(screen("H7", "关于（只读）", "H1 进入",
  phone("关于", '''<div class="ctr" style="flex:0 0 auto;padding:6px 0">
      <div class="img" style="width:44px;height:44px">LOGO</div>
      <div style="font-size:10px;font-weight:700">关系回忆</div>
      <div style="font-size:8.5px;color:#666">版本 1.1.0</div></div>
    <div class="box" style="font-size:8.5px;padding:3px;display:flex;justify-content:space-between">
      <span>AI 提示词版本</span><span class="mono">v2</span></div>
    <div class="box" style="font-size:8.5px;padding:3px;display:flex;justify-content:space-between">
      <span>封面资源池版本</span><span class="mono">pool-2026.11</span></div>
    <div class="box" style="font-size:8.5px;padding:3px;line-height:1.7">
      <b>资源来源</b><br>
      封面采用原创角色或已授权 IP 资源</div>
    <div class="box" style="font-size:8.5px;padding:3px;line-height:1.7">
      <b>数据来源</b><br>
      聊天记录来自配置的后端服务<br>
      评估由 AI 服务生成</div>
    <div class="box" style="font-size:8.5px;padding:3px;line-height:1.7">
      <b>本地存储位置</b><br>
      <span class="mono" style="font-size:7.5px">应用沙盒 /Documents/relation.db</span></div>''',
    nav="设置", ics='<span class="ic">←</span>'),
  meta(
    ["应用名称与版本号", "AI 提示词版本号",
     "封面资源池版本与资源来源说明",
     "数据来源说明", "本地数据存储位置说明"],
    ["阅读", "返回"],
    [f"返回 {to('H1 设置首页')}"],
    ["关于页内容为本版新定：版本、提示词版本、资源池版本、资源来源、数据来源、存储位置。"])))

# H8 失败日期列表
w(screen("H8", "失败日期列表", "H1 点击「查看失败日期」· 与 A8 同组件",
  phone("失败日期", '''<div class="box" style="background:#f0f0f0;font-size:9px;padding:3px">
      失败 3 天 · 上次尝试 11-13 23:00</div>
    <div class="box" style="font-size:9px;padding:3px">
      <div style="display:flex;justify-content:space-between;align-items:center">
        <span>11-05 请求超时</span><span class="btn" style="padding:1px 4px">重试</span></div>
      <div class="hr"></div>
      <div style="display:flex;justify-content:space-between;align-items:center">
        <span>11-08 服务端错误</span><span class="btn" style="padding:1px 4px">重试</span></div>
      <div class="hr"></div>
      <div style="display:flex;justify-content:space-between;align-items:center">
        <span>11-09 请求超时</span><span class="btn" style="padding:1px 4px">重试</span></div>
    </div>
    <div class="btn pri" style="width:100%">重试全部失败项</div>
    <div class="box d" style="font-size:8px;color:#777">
      与 A8 部分成功页使用同一组件</div>''',
    nav="设置", ics='<span class="ic">←</span>'),
  meta(
    ["失败天数与上次尝试时间",
     "失败日期列表（日期 + 失败原因 + 单日重试按钮）",
     "「重试全部失败项」按钮"],
    ["单日重试", "批量重试", "返回设置"],
    [f"重试成功则移除该行；全部成功 {to('H1 设置首页（状态更新）')}",
     f"返回 {to('H1 设置首页')}"],
    ["与 A8 使用同一组件，保证两处重试粒度一致。"])))
endgrp()
print("H 组完成：8 屏")

# ═══════════════════════════════════════════════ 规则速查
w('''<div class="grp" id="rules">
<h2>规则速查</h2>
<div class="gnote">全部可执行规则速查，与需求文档一致。</div>
<div class="doc" style="margin-top:16px">
<table class="tb">
<tr><th style="width:130px">规则项</th><th>规则内容</th></tr>
<tr><td>启动页</td><td>存在。配置加载超时上限 8 秒，超时文案「配置加载超时，请检查应用配置文件后重新启动」+「重新加载」按钮（重新计时）</td></tr>
<tr><td>登录流程</td><td>鉴权凭据由配置文件提供，配置有效即直接进入同步流程</td></tr>
<tr><td>配置录入</td><td>配置由代码或配置文件维护，待配置页为只读提示页</td></tr>
<tr><td>Token 更新</td><td>Token 由配置文件维护，鉴权失败页操作限于重试同步与离线查看</td></tr>
<tr><td>取消同步</td><td>提供「取消同步」。停止新请求、中断传输中请求，已落盘日文件保留；取消后可「继续同步」断点续传</td></tr>
<tr><td>同步失败形态</td><td>整页失败态，展示失败原因分类与最近成功同步时间</td></tr>
<tr><td>失败日期</td><td>向用户暴露失败日期列表，重试粒度支持单日 + 批量；设置页 H6 与 A8 同组件</td></tr>
<tr><td>手动同步按钮</td><td>时间墙空状态手动同步入口位于设置页「立即同步」</td></tr>
<tr><td>年度天气</td><td>年视图不展示年度关系天气</td></tr>
<tr><td>年→月导航</td><td>点击年份进入 12 个月宫格选择页（3 列 × 4 行，无记录置灰），再点月份进入月视图</td></tr>
<tr><td>卡片手势分工</td><td>点击卡片主体切换三态；卡片右下角独立箭头进入日详情</td></tr>
<tr><td>月份切换</td><td>顶部切换器 ◀ 年月 ▶，点击年月文字返回月份选择页</td></tr>
<tr><td>卡片墙列数</td><td>2 列，卡片面积加大以容纳三态内容</td></tr>
<tr><td>未同步日呈现</td><td>月视图置灰 + 「未同步」占位；点箭头进 D7b，提供「同步这一天」</td></tr>
<tr><td>卡片三态作用域</td><td>每张卡片独立切换，互不影响。进入月视图时按 UserPreference.cardDefaultState 初始化；单张切换结果为视图层临时状态</td></tr>
<tr><td>总结来源标识</td><td>用户编辑过显示「已编辑」，未编辑显示「AI」</td></tr>
<tr><td>总结为空文案</td><td>评估未完成「今天还没有总结」／评估失败「总结生成失败」／未同步「这天还没有同步」</td></tr>
<tr><td>长按菜单形态</td><td>底部动作面板，含收藏、编辑总结、添加备注；重新评估入口位于日详情</td></tr>
<tr><td>用户总结字数</td><td>上限 50 字，与 AI 输出同限制</td></tr>
<tr><td>恢复为 AI 总结</td><td>提供。保存后清空 userSummary，来源标识回「AI」；AI 原始总结为空时按钮置灰</td></tr>
<tr><td>未保存退出</td><td>总结与备注均需二次确认</td></tr>
<tr><td>备注标记与字数</td><td>备注非空时日卡片显示 📝 标记；字数上限 200 字</td></tr>
<tr><td>亮点与有趣内容</td><td>日详情只读展示，不可编辑</td></tr>
<tr><td>互动统计图形化</td><td>12 项固定顺序：占比用双色水平堆叠条，时间用时间轴，其余用数值卡片</td></tr>
<tr><td>连续对话段阈值</td><td>相邻消息间隔超过 30 分钟视为新段</td></tr>
<tr><td>评估置信度</td><td>AI 输出新增 confidence（0-100）。充足明确 70-100；偏少模糊 40-69；极少无法判断 0-39</td></tr>
<tr><td>天气综合分</td><td>= 总分 × 0.5 + 情绪分 × 0.3 + 亲密度 × 0.2（四舍五入）。与封面综合关系分（亲密度×0.6+情绪分×0.4）独立计算，DayWeather.score 存储天气综合分</td></tr>
<tr><td>天气判定</td><td>优先级：待评估 → 雾（置信度&lt;40）→ 雪（消息总条数 &lt; 10 且情绪分 ≥ 50）→ 天气综合分九档区间。前一条命中即停止</td></tr>
<tr><td>周期天气</td><td>周/月按有评估日期的天气综合分平均值映射，不应用雾与雪</td></tr>
<tr><td>无消息 vs 未同步</td><td>两种独立空状态。无消息可编辑总结、无同步入口；未同步提供「同步这一天」</td></tr>
<tr><td>无评估日编辑总结</td><td>允许</td></tr>
<tr><td>曲线点跳转</td><td>点对应什么就跳什么：周粒度→日详情、月粒度→该周日卡片列表、年粒度→该月月视图</td></tr>
<tr><td>曲线粒度与范围</td><td>仅周/月/年，无日粒度。选择后默认当前周期，可左右切换</td></tr>
<tr><td>曲线断点</td><td>缺评估日期断开，不连线不补零</td></tr>
<tr><td>曲线与热力图</td><td>同页 Tab 切换</td></tr>
<tr><td>情绪色系</td><td>30 种情绪归 6 色系：暖黄（愉悦）粉红（亲密）浅绿（平和）浅蓝（低落）橙红（激动）灰褐（疲惫）</td></tr>
<tr><td>情绪格子视觉</td><td>色相表情绪类型，明度与饱和度表情绪分。76-100 最鲜艳、51-75 中高、26-50 中低、0-25 最灰暗；待评估中性灰</td></tr>
<tr><td>喜好与礼物结构</td><td>同页双 Tab</td></tr>
<tr><td>喜好默认排序</td><td>星级降序，星级相同按更新时间降序</td></tr>
<tr><td>礼物默认排序</td><td>计划日期升序，无计划日期排最后并按更新时间降序</td></tr>
<tr><td>删除触发</td><td>统一长按触发，均需二次确认</td></tr>
<tr><td>必填校验</td><td>必填为空时保存按钮置灰；点击后字段下方红色提示 + 输入框边框变红，开始输入后消失</td></tr>
<tr><td>喜好必填项</td><td>名称、类型、分类（后两项有默认值）</td></tr>
<tr><td>礼物必填项</td><td>名称、分类、等级、场合、状态、优先级（除名称外均有默认值）</td></tr>
<tr><td>自定义分类</td><td>支持新增。内置 26 项不可编辑删除；自定义可编辑删除，删除后相关喜好重置为「其他」</td></tr>
<tr><td>删除喜好的连带</td><td>关联礼物保留并断开关联（preferenceId 置空），礼物显示「来源喜好已删除」</td></tr>
<tr><td>共同喜好</td><td>喜好条目上的标记字段，手动标记后在喜好列表筛选查看。取值：共同喜欢 / 共同不喜欢 / TA 喜欢我不喜欢 / 待确认 / 独立喜好</td></tr>
<tr><td>加入礼物表单</td><td>包含优先级字段；保存后跳转礼物 Tab 并定位新建条目</td></tr>
<tr><td>筛选形态</td><td>底部浮层。常用 2-3 项默认展开，其余收进「更多筛选」折叠区</td></tr>
<tr><td>喜好筛选维度</td><td>展开：类型/分类/星级；更多：共同喜好状态/是否已加礼物/是否有图片</td></tr>
<tr><td>礼物筛选维度</td><td>展开：状态/分类/优先级；更多：等级/场合/预算档/是否有关联喜好</td></tr>
<tr><td>筛选多选与持久化</td><td>全维度支持多选，条件跨会话保留（FilterState）</td></tr>
<tr><td>礼物归档</td><td>已取消与已归档在主列表隐藏，另设独立归档视图，支持恢复状态</td></tr>
<tr><td>礼物来源追溯</td><td>详情可跳转来源喜好并定位；无关联显示「无关联喜好」，已删除显示「来源喜好已删除」</td></tr>
<tr><td>关联喜好修改</td><td>通过下拉选择变更或解除关联</td></tr>
<tr><td>礼物状态流转</td><td>全状态可任意跳转与回退</td></tr>
<tr><td>已送出 vs 已收到</td><td>已送出＝已寄出或交付但未确认收到；已收到＝已确认对方收到</td></tr>
<tr><td>送出日期</td><td>状态变更为已送出时自动写入当天；变更为已收到且送出日期为空时自动写入当天；列表与详情展示</td></tr>
<tr><td>高光类型判定</td><td>优先级：综合高光（总分≥90 且情绪≥85 且亲密≥85）→ 高亲密（亲密≥90）→ 高情绪（情绪≥90）→ 有趣对话（有趣内容≥2）→ 高总分</td></tr>
<tr><td>高光类型筛选</td><td>支持。顶部横向筛选条，含「全部」+ 5 种类型</td></tr>
<tr><td>手动标记高光</td><td>日详情提供入口，类型固定为综合高光；已有高光时显示为「取消高光标记」</td></tr>
<tr><td>高光删除</td><td>长按触发 + 确认，标记 deleted；该日期重新评估并仍达标时重新生成</td></tr>
<tr><td>高光空状态</td><td>向用户暴露阈值数字，数字从配置读取</td></tr>
<tr><td>设置同步入口</td><td>设置页展示同步状态、上次同步时间、已同步/失败天数，提供「立即同步」与「查看失败日期」</td></tr>
<tr><td>显示偏好项</td><td>5 项：默认卡片状态、趋势默认指标、趋势默认粒度、曲线叠加显示、互动统计默认展开</td></tr>
<tr><td>主题</td><td>4 套单选：纸月历 PAPER_CALENDAR（默认）、星图 STAR_MAP、色域 COLOR_FIELD、磨砂玻璃 FROSTED_GLASS。点击即应用并写入 UserPreference.theme</td></tr>
<tr><td>主题作用范围</td><td>全局底色、卡片容器样式、字体族、分隔线、按钮与标签样式。封面等级、天气图标、情绪色系的映射规则在 4 套主题下一致</td></tr>
<tr><td>配置与偏好分离</td><td>AppConfig 只读（sync/ai/thresholds/coverPools）；UserPreference 可写（theme、cardDefaultState、趋势默认项等），同步与配置重载保留</td></tr>
<tr><td>STALE 表现</td><td>沿用上次成功评估的分数、天气、封面、情绪着色；卡片角标加「待重评」标识；曲线正常连线</td></tr>
<tr><td>评估版本</td><td>evalVersion 首次为 1，每次重新评估 +1；同时刷新 fileHash、promptVersion、evaluatedAt</td></tr>
<tr><td>提示词版本策略</td><td>新版本对其生效后新同步的日期生效；历史日期保留原结果与原 promptVersion，手动「重新评估」时使用当前版本</td></tr>
<tr><td>评估调度</td><td>同步完成后本次新增或变更的全部日期立即入队；按日期倒序从最近开始；并发 3（ai.concurrency 可配，1-5）；单次同步上限 300 个日期</td></tr>
<tr><td>超上限日期</td><td>超过 300 个时取最近 300 个入队，更早日期保持 PENDING，用户进入其日详情时触发单日评估并优先于队列剩余任务</td></tr>
<tr><td>脱敏对象</td><td>手机号、身份证号、银行卡号、邮箱、详细地址、验证码替换为占位标识；姓名与昵称保留原文；本地存储与对话流展示保留原文</td></tr>
<tr><td>时区基准</td><td>日期归属以后端切分日文件的时区为权威，日文件 date 即唯一标识；设备时区变化不改变日期归属与统计结果</td></tr>
<tr><td>当天数据</td><td>当天为进行中日期，保持 PENDING、天气显示待评估、封面为占位封面，可查看对话流与编辑总结备注；跨入次日后入队评估</td></tr>
<tr><td>封面情绪蒙层</td><td>4 套主题均展示封面图，情绪色块作蒙层叠加：纸月历 15% · 星图 15% · 色域 45% · 磨砂玻璃 30%（叠在模糊后的封面图上）</td></tr>
<tr><td>共同喜好语义</td><td>喜好「类型」代表 TA 的态度，commonStatus 代表双方态度组合。类型 = 喜欢且 commonStatus = CONFLICT 表示 TA 喜欢而我不喜欢</td></tr>
<tr><td>0 消息日</td><td>不调用 AI，状态保持 PENDING，不写入 DailyEvaluation，不计入均分、周期天气与曲线；12 项统计显示「--」</td></tr>
<tr><td>字数口径</td><td>仅统计 TEXT 类型 content 的 Unicode 码点数；其余类型字数计 0、条数照常计入；系统消息不计入统计与对话段判定</td></tr>
<tr><td>周期零评估降级</td><td>周期内已评估日期数为 0 时，周期天气取 PENDING、均分为空，界面显示「--」，月份格保持可点击</td></tr>
<tr><td>曲线聚合口径</td><td>周粒度每点为单日值；月/年粒度每点为周期内 SUCCESS 与 STALE 日期的算术平均并四舍五入。周以周一起始</td></tr>
<tr><td>periodKey 格式</td><td>周 2026-W46、月 2026-11、年 2026，跨年周按 ISO 8601 归属</td></tr>
<tr><td>周定位态</td><td>趋势月粒度数据点跳转该周起始日所属月份的月视图，该周 7 张卡片描边高亮 + 周摘要行 +「显示全月」</td></tr>
<tr><td>高光唯一性</td><td>同一日期最多一条有效高光（deleted=false），以日期为唯一键。重评后不再达标则置 deleted，类型变化则更新不新增</td></tr>
<tr><td>删除级联</td><td>删除礼物后重算来源喜好 giftAdded；删除自定义分类同步清理 FilterState 中该分类条件；跳转定位前清除目标列表筛选</td></tr>
<tr><td>未同步日卡片</td><td>不参与三态循环，卡片主体为占位区；长按面板的收藏、编辑总结、添加备注均可用；已有用户总结时占位区展示该总结</td></tr>
<tr><td>规则说明页</td><td>封面规则与天气规则合并展示，并链到情绪色系全表</td></tr>
<tr><td>关于页内容</td><td>版本号、AI 提示词版本、封面资源池版本、资源来源、数据来源、本地存储位置</td></tr>
</table>
</div>
</div>
''')

# ═══════════════════════════════════════════════ 待确认事项
w('''
<div class="grp" id="pending">
<h2>待确认事项</h2>
<div class="gnote">以下事项需产品决策后补入对应屏幕与需求章节，当前线框图未绘制对应界面。与需求文档第 17 章对应。</div>
<table class="tb">
<tr><th style="width:150px">事项</th><th>待确认的点</th><th style="width:88px">影响屏幕</th></tr>
<tr><td>封面辅助档位的选图机制与资源张数</td><td>亲密度档 D1-D5 与情绪档 E1-E4 标注「用于资源池微调」，与「每等级一个资源池按日期哈希轮换」的结合方式待确认：仅按 L1-L5 分 5 个池 / 按 L×D×E 细分 / L 决定主池而 D 或 E 决定同池内变体。决定美术资源总量与排期</td><td>C1 · H6</td></tr>
</table>
</div>
''')
print("待确认事项完成")

# ═══════════════════════════════════════════════ 页脚
w('''<footer>
<p><b>屏幕统计</b>：A 启动与同步 8 屏 · B 时间墙 5 屏 · C 日卡片 8 屏 · D 日详情 9 屏 ·
E 趋势 4 屏 · F 喜好与礼物 14 屏 · G 回忆 4 屏 · H 设置 8 屏 ——<b>共 60 屏</b>。</p>
<p><b>手机壳内外的分工</b>：手机壳内＝最终界面呈现内容；手机壳外的「关键元素 / 用户可执行操作 / 操作后去向 / 规则」＝给开发看的实现说明，不绘制到界面上。</p>
<p>配套文档：《个人关系聊天回忆 App 需求描述文档》。两份交付物中的阈值、文案、字段、优先级规则一一对应；文档第 17 章列出的待确认事项在本图中同样标注为待确认。</p>
</footer>
</div>
</body>
</html>''')
print("规则速查 + 页脚完成")

with open(OUT, "w", encoding="utf-8") as f:
    f.write("".join(P))
print(f"\n输出: {OUT}")
print(f"大小: {os.path.getsize(OUT)/1024:.0f} KB")
