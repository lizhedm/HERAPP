#!/usr/bin/env python3
"""
把 Markdown 需求文档转成 Word (.docx)。
手工构建 OOXML，不依赖 python-docx。
支持：标题层级、段落、无序列表、表格、代码块、行内 code/粗体。
"""

import os, re, struct, zipfile, html

SRC = "/Users/zhe/Documents/TophantAIGit/HERAPP/需求文档V1.1.md"
OUT = "/Users/zhe/Documents/TophantAIGit/HERAPP/个人关系聊天回忆App-需求描述文档V1.1.docx"
START_LINE = 1

# ─── 读取最后一轮的文档内容 ──────────────────────────────────────────────────
with open(SRC, encoding="utf-8") as f:
    all_lines = f.read().split("\n")
lines = all_lines[START_LINE - 1:]

# ─── XML 辅助 ────────────────────────────────────────────────────────────────
def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;")
             .replace(">", "&gt;").replace('"', "&quot;"))

def runs_from_inline(text):
    """解析行内 `code` 和 **bold**，返回 run XML 列表。"""
    out = []
    # 先按 ` 分段，再在非 code 段里处理 **bold**
    parts = re.split(r"(`[^`]+`)", text)
    for part in parts:
        if not part:
            continue
        if part.startswith("`") and part.endswith("`") and len(part) > 2:
            code = esc(part[1:-1])
            out.append(
                '<w:r><w:rPr><w:rFonts w:ascii="Menlo" w:hAnsi="Menlo" '
                'w:eastAsia="Menlo"/><w:sz w:val="20"/>'
                '<w:shd w:val="clear" w:fill="F2F2F2"/></w:rPr>'
                f'<w:t xml:space="preserve">{code}</w:t></w:r>')
        else:
            for sub in re.split(r"(\*\*[^*]+\*\*)", part):
                if not sub:
                    continue
                if sub.startswith("**") and sub.endswith("**") and len(sub) > 4:
                    out.append('<w:r><w:rPr><w:b/></w:rPr>'
                               f'<w:t xml:space="preserve">{esc(sub[2:-2])}</w:t></w:r>')
                else:
                    out.append('<w:r>'
                               f'<w:t xml:space="preserve">{esc(sub)}</w:t></w:r>')
    return out or ['<w:r><w:t xml:space="preserve"></w:t></w:r>']

def p_heading(text, level):
    sizes = {1: 40, 2: 32, 3: 28, 4: 24}
    sz = sizes.get(level, 24)
    before = {1: 0, 2: 360, 3: 280, 4: 220}.get(level, 200)
    color = {1: "1F3864", 2: "2E5496", 3: "2E5496", 4: "404040"}.get(level, "404040")
    runs = "".join(
        r.replace("<w:rPr>", f'<w:rPr><w:b/><w:sz w:val="{sz}"/>'
                              f'<w:szCs w:val="{sz}"/><w:color w:val="{color}"/>')
         if "<w:rPr>" in r else
         r.replace("<w:r>", f'<w:r><w:rPr><w:b/><w:sz w:val="{sz}"/>'
                            f'<w:szCs w:val="{sz}"/><w:color w:val="{color}"/></w:rPr>')
        for r in runs_from_inline(text))
    return (f'<w:p><w:pPr><w:spacing w:before="{before}" w:after="120"/>'
            f'<w:keepNext/></w:pPr>{runs}</w:p>')

def p_text(text, indent=0, after=120):
    ind = f'<w:ind w:left="{indent}"/>' if indent else ""
    return (f'<w:p><w:pPr><w:spacing w:after="{after}" w:line="300" '
            f'w:lineRule="auto"/>{ind}</w:pPr>'
            f'{"".join(runs_from_inline(text))}</w:p>')

def p_bullet(text, depth=0):
    indent = 360 + depth * 360
    return (f'<w:p><w:pPr><w:spacing w:after="60" w:line="290" w:lineRule="auto"/>'
            f'<w:ind w:left="{indent}" w:hanging="240"/></w:pPr>'
            f'<w:r><w:t xml:space="preserve">• </w:t></w:r>'
            f'{"".join(runs_from_inline(text))}</w:p>')

def p_quote(text):
    return (f'<w:p><w:pPr><w:spacing w:after="80"/><w:ind w:left="360"/>'
            f'<w:pBdr><w:left w:val="single" w:sz="18" w:space="8" '
            f'w:color="8EAADB"/></w:pBdr></w:pPr>'
            f'<w:r><w:rPr><w:i/><w:color w:val="404040"/></w:rPr>'
            f'<w:t xml:space="preserve">{esc(text)}</w:t></w:r></w:p>')

def p_code_block(code_lines):
    rows = []
    for ln in code_lines:
        rows.append(
            '<w:p><w:pPr><w:spacing w:after="0" w:line="240" w:lineRule="auto"/>'
            '<w:ind w:left="240"/><w:shd w:val="clear" w:fill="F7F7F7"/></w:pPr>'
            '<w:r><w:rPr><w:rFonts w:ascii="Menlo" w:hAnsi="Menlo" '
            'w:eastAsia="Menlo"/><w:sz w:val="18"/></w:rPr>'
            f'<w:t xml:space="preserve">{esc(ln)}</w:t></w:r></w:p>')
    return "".join(rows) + '<w:p><w:pPr><w:spacing w:after="120"/></w:pPr></w:p>'

def tbl(header, rows):
    ncol = len(header)
    width = 9360
    cw = width // ncol

    def cell(txt, is_hdr):
        shd = '<w:shd w:val="clear" w:fill="D9E2F3"/>' if is_hdr else ""
        bold = "<w:b/>" if is_hdr else ""
        return (f'<w:tc><w:tcPr><w:tcW w:w="{cw}" w:type="dxa"/>{shd}'
                f'<w:vAlign w:val="center"/></w:tcPr>'
                f'<w:p><w:pPr><w:spacing w:after="0" w:before="40"/></w:pPr>'
                f'<w:r><w:rPr>{bold}<w:sz w:val="20"/></w:rPr>'
                f'<w:t xml:space="preserve">{esc(txt)}</w:t></w:r></w:p></w:tc>')

    out = ['<w:tbl><w:tblPr><w:tblStyle w:val="TableGrid"/>'
           f'<w:tblW w:w="{width}" w:type="dxa"/>'
           '<w:tblBorders>'
           '<w:top w:val="single" w:sz="4" w:color="A6A6A6"/>'
           '<w:left w:val="single" w:sz="4" w:color="A6A6A6"/>'
           '<w:bottom w:val="single" w:sz="4" w:color="A6A6A6"/>'
           '<w:right w:val="single" w:sz="4" w:color="A6A6A6"/>'
           '<w:insideH w:val="single" w:sz="4" w:color="A6A6A6"/>'
           '<w:insideV w:val="single" w:sz="4" w:color="A6A6A6"/>'
           '</w:tblBorders></w:tblPr>']
    out.append('<w:tr><w:trPr><w:tblHeader/></w:trPr>'
               + "".join(cell(h, True) for h in header) + '</w:tr>')
    for r in rows:
        r = (r + [""] * ncol)[:ncol]
        out.append('<w:tr>' + "".join(cell(c, False) for c in r) + '</w:tr>')
    out.append('</w:tbl><w:p><w:pPr><w:spacing w:after="160"/></w:pPr></w:p>')
    return "".join(out)

# ─── 解析 Markdown ───────────────────────────────────────────────────────────
body = []
i = 0
while i < len(lines):
    raw = lines[i]
    line = raw.rstrip()
    stripped = line.strip()

    # 空行
    if not stripped:
        i += 1
        continue

    # 分隔线
    if re.fullmatch(r"-{3,}", stripped):
        body.append('<w:p><w:pPr><w:pBdr><w:bottom w:val="single" w:sz="6" '
                    'w:space="1" w:color="BFBFBF"/></w:pBdr>'
                    '<w:spacing w:after="160"/></w:pPr></w:p>')
        i += 1
        continue

    # 代码块围栏
    if stripped.startswith("```"):
        i += 1
        buf = []
        while i < len(lines) and not lines[i].strip().startswith("```"):
            buf.append(lines[i])
            i += 1
        i += 1
        body.append(p_code_block(buf))
        continue

    # 裸 json 标记行（原文里有单独一行 json）
    if stripped == "json":
        i += 1
        continue

    # 标题
    m = re.match(r"^(#{1,6})\s+(.*)$", stripped)
    if m:
        body.append(p_heading(m.group(2).strip(), len(m.group(1))))
        i += 1
        continue

    # 引用
    if stripped.startswith("> "):
        body.append(p_quote(stripped[2:].strip()))
        i += 1
        continue

    # 表格
    if stripped.startswith("|") and i + 1 < len(lines) \
       and re.match(r"^\|[\s:|-]+\|$", lines[i+1].strip()):
        hdr = [c.strip() for c in stripped.strip("|").split("|")]
        i += 2
        rws = []
        while i < len(lines) and lines[i].strip().startswith("|"):
            rws.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
            i += 1
        body.append(tbl(hdr, rws))
        continue

    # 列表项（支持缩进层级）
    m = re.match(r"^(\s*)[-*]\s+(.*)$", raw)
    if m:
        depth = len(m.group(1)) // 2
        body.append(p_bullet(m.group(2).strip(), depth))
        i += 1
        continue

    # 有序列表
    m = re.match(r"^(\s*)(\d+)\.\s+(.*)$", raw)
    if m:
        depth = len(m.group(1)) // 2
        indent = 360 + depth * 360
        body.append(
            f'<w:p><w:pPr><w:spacing w:after="60" w:line="290" w:lineRule="auto"/>'
            f'<w:ind w:left="{indent}" w:hanging="300"/></w:pPr>'
            f'<w:r><w:t xml:space="preserve">{m.group(2)}. </w:t></w:r>'
            f'{"".join(runs_from_inline(m.group(3).strip()))}</w:p>')
        i += 1
        continue

    # 普通段落
    body.append(p_text(stripped))
    i += 1

print(f"解析完成：{len(body)} 个块")

# ─── 组装 docx ───────────────────────────────────────────────────────────────
document_xml = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
  '<w:document '
  'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
  'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
  '<w:body>' + "".join(body) +
  '<w:sectPr><w:pgSz w:w="11906" w:h="16838"/>'
  '<w:pgMar w:top="1134" w:right="1134" w:bottom="1134" w:left="1134" '
  'w:header="851" w:footer="992" w:gutter="0"/></w:sectPr>'
  '</w:body></w:document>')

styles_xml = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
  '<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
  '<w:docDefaults><w:rPrDefault><w:rPr>'
  '<w:rFonts w:ascii="PingFang SC" w:eastAsia="PingFang SC" w:hAnsi="PingFang SC"/>'
  '<w:sz w:val="21"/><w:szCs w:val="21"/></w:rPr></w:rPrDefault></w:docDefaults>'
  '<w:style w:type="table" w:styleId="TableGrid"><w:name w:val="Table Grid"/>'
  '<w:tblPr></w:tblPr></w:style>'
  '</w:styles>')

content_types = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
  '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
  '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
  '<Default Extension="xml" ContentType="application/xml"/>'
  '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
  '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>'
  '</Types>')

rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
  '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
  '<Relationship Id="rId1" '
  'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" '
  'Target="word/document.xml"/></Relationships>')

doc_rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
  '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
  '<Relationship Id="rIdS" '
  'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" '
  'Target="styles.xml"/></Relationships>')

with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("[Content_Types].xml", content_types)
    z.writestr("_rels/.rels", rels)
    z.writestr("word/document.xml", document_xml)
    z.writestr("word/_rels/document.xml.rels", doc_rels)
    z.writestr("word/styles.xml", styles_xml)

print(f"输出: {OUT}  ({os.path.getsize(OUT)/1024:.0f} KB)")
