"""アムハラ語フィデル全文字の書き順(フィデル表の全258文字)を生成する。

出力(アムハラ語フォルダ直下):
  アムハラ語フィデル全書き順.html        Web版(Artifact用。doctypeなしの断片)
  アムハラ語フィデル全書き順-print.html  印刷用(A4横。Edgeヘッドレスで PDF 化)
  アムハラ語フィデル全書き順.md          テキスト版

段I(基本形)34文字の筆順は build_stroke_order.py、段II〜VIIと唇音化系列の224文字は
fidel_forms_all.py にある。字形の下図は Noto Sans Ethiopic(SIL OFL)のアウトラインを
glyph_outlines_all.json に書き出したもの(座標系は build_stroke_order.py と同じ)。
ローマ字・カタカナは「アムハラ語フィデル表.md」から読み込む。
"""
import json
import re
from pathlib import Path

from build_stroke_order import LETTERS, ORDERS, PRINCIPLES, TOKENS, CSS, SCRIPT, CIRCLED, ge_spans
from fidel_forms_all import FORMS, BASE, expand

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUTLINES = json.loads((HERE / "glyph_outlines_all.json").read_text(encoding="utf-8"))
VOWELS = [o[1] for o in ORDERS]  # ä u i a e ɨ o

# 34系列(フィデル表と同じ並び)。各系列は基本形のコードポイントから7文字
SERIES = [(L[0], L[1][:-1], L[2], [chr(ord(L[0]) + k) for k in range(7)]) for L in LETTERS]
# 唇音化系列: (表示名, 元の系列, 文字, 段)
LABIAL = [
    ("qʷ", "ቀ", "ቈቊቋቌቍ"),
    ("ḫʷ", "ኀ", "ኈኊኋኌኍ"),
    ("kʷ", "ከ", "ኰኲኳኴኵ"),
    ("gʷ", "ገ", "ጐጒጓጔጕ"),
]
LABIAL_ORDERS = [0, 2, 3, 4, 5]  # 段I・III・IV・V・VI


def load_readings():
    """フィデル表.md から 文字 → (ローマ字, カタカナ) を読む。"""
    md = (ROOT / "アムハラ語フィデル表.md").read_text(encoding="utf-8")
    out = {}
    for ch, rom, kana in re.findall(r"\| (\S) /([^/]+)/ (\S+) ", md):
        out[ch] = (rom, kana)
    for ch, rom in re.findall(r"\| (\S) ([^\s|]*ʷ[^\s|]*) ", md):
        out[ch] = (rom, "")
    return out


READINGS = load_readings()


def entry(ch):
    """文字 → (筆順パス一覧, [(画数, 説明)], 派生元)。"""
    if ch in BASE:
        L = BASE[ch]
        return L[3], [(1, s) for s in L[4]], L[5]
    strokes, steps = FORMS[ch]
    groups = []
    for s, t in zip(strokes, steps):
        if s.startswith("="):
            ref = s[1:].partition(":")[0]
            n = len(expand([s]))
            groups.append((n, f"{ref} と同じ" if t == "=" else t))
        else:
            groups.append((1, t))
    return expand(strokes), groups, None


def numbers(start, n):
    return CIRCLED[start - 1] if n == 1 else f"{CIRCLED[start - 1]}〜{CIRCLED[start + n - 2]}"


def svg_for(ch, strokes):
    o = OUTLINES[ch]
    side = max(o["w"] + 120, 960)
    vx, vy = o["w"] / 2 - side / 2, 510 - side / 2
    grid = "".join(
        f'<line class="gr" x1="{vx:.0f}" y1="{y}" x2="{vx + side:.0f}" y2="{y}"/>' for y in (186, 543, 900)
    )
    parts = [f'<svg viewBox="{vx:.0f} {vy:.0f} {side:.0f} {side:.0f}" role="img" '
             f'aria-label="{ch} の書き順({len(strokes)}画)">', grid, f'<path class="gl" d="{o["d"]}"/>']
    for i, d in enumerate(strokes, 1):
        parts.append(f'<path class="st c{i}" d="{d}" pathLength="1"/>')
    for i, d in enumerate(strokes, 1):
        x, y = d[1:].split(" ")[:2]
        parts.append(f'<circle class="dot c{i}" cx="{x}" cy="{y}" r="40"/>'
                     f'<text class="num" x="{x}" y="{y}">{i}</text>')
    parts.append("</svg>")
    return "".join(parts)


def card(ch, order, printable):
    strokes, groups, src = entry(ch)
    rom, kana = READINGS[ch]
    lis, k = [], 1
    for n, t in groups:
        cls = f"c{k}" if n == 1 else "same"
        lis.append(f'<li><span class="n {cls}">{numbers(k, n)}</span><span>{ge_spans(t)}</span></li>')
        k += n
    from_ = f'<span class="from">{ge_spans(src)} に線を足した形</span>' if src else ""
    btn = "" if printable else f'<button type="button" data-play>再生</button>'
    kana_html = f"<small>{kana}</small>" if kana else ""
    return (f'<article class="card" id="g{ord(ch):x}"><header><span class="glyph">{ch}</span>'
            f'<span class="meta"><span class="rom">{rom}</span>{kana_html}</span>'
            f'<span class="count"><b>{ORDERS[order][0]}</b>{len(strokes)}画</span></header>'
            f'{from_}{svg_for(ch, strokes)}<ol>{"".join(lis)}</ol>{btn}</article>')


EXTRA_TOKENS = """
  :root { --s6: #1F7A78; }
  @media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) { --s6: #5CC4C0; } }
  :root[data-theme="dark"] { --s6: #5CC4C0; }
"""

EXTRA_CSS = """
  .c6 { stroke: var(--s6); color: var(--s6); } circle.c6 { fill: var(--s6); }
  .legend .c6 { background: var(--s6); }
  .card ol .same { color: var(--ink-muted); }
  .card { padding: 10px 10px 12px; gap: 6px; }
  .card .glyph { font-size: 1.7rem; }
  .card .count { display: flex; flex-direction: column; align-items: flex-end; line-height: 1.25; }
  .card .count b { font-weight: 700; color: var(--accent); font-family: var(--f-rom); }
  .card ol { font-size: 0.76rem; line-height: 1.5; }
  .card ol li { grid-template-columns: auto 1fr; gap: 5px; }
  .card button { font-size: 0.74rem; padding: 2px 10px; }
  .cards7 { display: grid; grid-template-columns: repeat(auto-fill, minmax(158px, 1fr)); gap: 8px; }
  @media (min-width: 1100px) { .cards7 { grid-template-columns: repeat(7, minmax(0, 1fr)); } }
  .cards7.lab { grid-template-columns: repeat(auto-fill, minmax(158px, 1fr)); }
  @media (min-width: 1100px) { .cards7.lab { grid-template-columns: repeat(7, minmax(0, 1fr)); } }
  section.series { gap: 10px; scroll-margin-top: 12px; }
  section.series h2 a { margin-left: auto; font-size: 0.78rem; font-weight: 400; color: var(--accent); }
  nav.index { display: grid; grid-template-columns: repeat(auto-fill, minmax(58px, 1fr)); gap: 6px; }
  nav.index a {
    display: flex; flex-direction: column; align-items: center; padding: 6px 4px; text-decoration: none;
    background: var(--surface); border: 1px solid var(--border); border-radius: 4px; color: var(--ink);
  }
  nav.index a:hover { border-color: var(--accent); }
  nav.index a:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
  nav.index .ge { font-size: 1.5rem; line-height: 1.2; }
  nav.index small { font-family: var(--f-rom); font-style: italic; font-size: 0.72rem; color: var(--ink-muted); }
  nav.index a.lab { background: var(--surface-alt); }
"""

PRINT_CSS = """
  @page { size: A4 landscape; margin: 8mm 9mm; }
  body { padding: 0; font-size: 11px; background: #fff; }
  :root { --bg: #FBF9F4; --surface: #fff; }
  .page { max-width: none; gap: 10px; padding-inline: 2px; }
  .mark { font-size: 2.2rem; }
  .cards7, .cards7.lab { grid-template-columns: repeat(7, minmax(0, 1fr)); gap: 5px; }
  .card { padding: 5px 6px 6px; gap: 3px; break-inside: avoid; }
  .card .glyph { font-size: 1.35rem; }
  .card ol { font-size: 0.6rem; line-height: 1.38; gap: 1px; }
  .card .meta small, .card .count, .card .from { font-size: 0.58rem; }
  .card button { display: none; }
  .card svg { width: 76%; align-self: center; }
  .note { font-size: 0.78rem; padding: 6px 12px; max-width: none; }
  ol.rules { grid-template-columns: repeat(5, minmax(0, 1fr)); }
  ol.rules li { font-size: 0.7rem; padding: 6px 8px; }
  .orders th, .orders td { padding: 3px 8px; }
  .orders td.ex { font-size: 1.05rem; }
  nav.index { display: none; }
  section.series { break-inside: avoid; gap: 5px; }
  section.series h2 { font-size: 0.95rem; }
  section.series h2 a { display: none; }
  section.intro2 { break-after: page; }
  table { font-size: 0.74rem; }
  tr { break-inside: avoid; }
"""


def section(sid, title, sub, chars, orders, lab, printable):
    cards = "".join(card(ch, o, printable) for ch, o in zip(chars, orders))
    top = "" if printable else '<a href="#top">一覧へ戻る ↑</a>'
    return (f'<section class="series" id="{sid}"><h2>{title} <span class="rd">{sub}</span>{top}</h2>'
            f'<div class="cards7{" lab" if lab else ""}">{cards}</div></section>')


def build_html(printable):
    head = [
        '<meta charset="utf-8">' if printable else "",
        "<title>フィデル全書き順</title>",
        "" if printable else '<meta name="claude:viewport-fit-sides" content="cover">',
        '<link rel="preconnect" href="https://fonts.googleapis.com">',
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>',
        '<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+Ethiopic:wght@400;700'
        '&family=Noto+Sans+JP:wght@400;500;700&family=Noto+Serif:ital,wght@0,400;1,400&display=swap" rel="stylesheet">',
        "<style>" + TOKENS + EXTRA_TOKENS + CSS + EXTRA_CSS + (PRINT_CSS if printable else "") + "</style>",
    ]
    rules = "".join(f"<li><b>{t}</b>{ge_spans(d)}</li>" for t, d in PRINCIPLES)
    legend = "".join(f'<span><i class="c{i}"></i>{CIRCLED[i - 1]} {i}画目</span>' for i in range(1, 7))
    orders = "".join(
        f'<tr><td class="ord">{o} <span class="rom">{v}</span></td><td>{ge_spans(how)}</td>'
        f'<td class="ex">{ex}</td><td class="nt">{ge_spans(nt)}</td></tr>'
        for o, v, how, ex, nt in ORDERS
    )
    index = "".join(f'<a href="#s{ord(b):x}"><span class="ge">{b}</span><small>{c}</small></a>' for b, c, _, _ in SERIES)
    index += "".join(f'<a class="lab" href="#s{ord(chars[0]):x}"><span class="ge">{chars[0]}</span><small>{n}</small></a>'
                     for n, _, chars in LABIAL)
    secs = "".join(
        section(f"s{ord(b):x}", f'<span class="ge">{b}</span> {c} 系列', name, chars, range(7), False, printable)
        for b, c, name, chars in SERIES
    )
    secs += "".join(
        section(f"s{ord(chars[0]):x}", f'<span class="ge">{chars[0]}</span> {n} 系列',
                f"唇音化 — {src} 系列から派生。段II・VIIはない", chars, LABIAL_ORDERS, True, printable)
        for n, src, chars in LABIAL
    )
    total = len(SERIES) * 7 + sum(len(c) for _, _, c in LABIAL)
    strokes = sum(len(entry(ch)[0]) for _, _, _, cs in SERIES for ch in cs) + \
        sum(len(entry(ch)[0]) for _, _, cs in LABIAL for ch in cs)
    body = f"""
<div class="page" id="top">
  <header class="masthead">
    <span class="mark">ፊደል</span>
    <div class="titles">
      <h1>アムハラ語 フィデル全書き順</h1>
      <p>フィデル表の全{total}文字(34系列×7段+唇音化20字・計{strokes}画)の書き順を、字形の上に色と番号で示しました。番号の丸が書き始めの位置です。</p>
    </div>
  </header>

  <p class="note">ゲエズ文字には公式に定められた筆順はなく、教材や書き手によって違いがあります。この資料は、基本の34文字の「書き順ガイド」と同じ5つの原則で選んだ<b>学習用の目安</b>です。下図の字形は Noto Sans Ethiopic で、段によっては手書きや他のフォントと形が違う文字(ሂ・ሚ・ዒ など)もあります。そのときはフォントの形どおりに書き順を付けています。</p>

  <section class="principles">
    <h2>書き順の原則 <span class="rd">基本の34文字と同じ5つの決まり</span></h2>
    <ol class="rules">{rules}</ol>
  </section>

  <section class="orders intro2">
    <h2>段ごとの印 <span class="rd">基本形を書いてから、最後に印を足す</span></h2>
    <div class="tbl-wrap"><table>
      <thead><tr><th>段</th><th>形の変え方</th><th>例</th><th>補足</th></tr></thead>
      <tbody>{orders}</tbody>
    </table></div>
    <div class="legend">{legend}<span>灰色の番号 … 基本形と同じ画</span></div>
  </section>

  <nav class="index" aria-label="系列の一覧">{index}</nav>

  {secs}

  <footer>音価・カタカナ読みは「アムハラ語フィデル表」、基本の34文字の説明は「フィデル書き順ガイド」を参照してください。字形: Noto Sans Ethiopic(SIL Open Font License)。2026-10-26 作成。</footer>
</div>
"""
    return "\n".join(h for h in head if h) + body + ("" if printable else SCRIPT)


def build_md():
    lines = [
        "# アムハラ語 フィデル全書き順",
        "",
        "フィデル表の全258文字(34系列×7段+唇音化20字)の書き順を、文字ごとに画の順で説明する。",
        "図(色と番号付き)は Web版・PDF を参照。",
        "",
        "> ゲエズ文字には公式に定められた筆順はなく、教材や書き手によって違いがある。",
        "> この資料は基本の34文字の書き順ガイドと同じ原則で選んだ**学習用の目安**。",
        "> 字形は Noto Sans Ethiopic に合わせている(手書きと形が違う文字もある)。",
        "",
        "## 書き順の原則",
        "",
    ]
    lines += [f"{i}. **{t}** — {d}" for i, (t, d) in enumerate(PRINCIPLES, 1)]

    def rows(chars, orders):
        out = ["| 段 | 文字 | ローマ字 | 読み | 画数 | 書き順 |", "|---|---|---|---|---|---|"]
        for ch, o in zip(chars, orders):
            strokes, groups, src = entry(ch)
            rom, kana = READINGS[ch]
            desc, k = [], 1
            for n, t in groups:
                desc.append(numbers(k, n) + t)
                k += n
            note = f"({src} に線を足した形)" if src else ""
            out.append(f"| {ORDERS[o][0]} | {ch} | {rom} | {kana} | {len(strokes)} | {' '.join(desc)}{note} |")
        return out

    for b, c, name, chars in SERIES:
        lines += ["", f"## {b} {c} 系列({name})", ""] + rows(chars, range(7))
    for n, src, chars in LABIAL:
        lines += ["", f"## {chars[0]} {n} 系列(唇音化・{src} 系列から派生)", ""] + rows(chars, LABIAL_ORDERS)
    lines += ["", "---",
              "字形: Noto Sans Ethiopic(SIL Open Font License)。生成: `tools/build_stroke_order_all.py`(2026-10-26)。", ""]
    return "\n".join(lines)


if __name__ == "__main__":
    (ROOT / "アムハラ語フィデル全書き順.html").write_text(build_html(False), encoding="utf-8")
    (ROOT / "アムハラ語フィデル全書き順-print.html").write_text(build_html(True), encoding="utf-8")
    (ROOT / "アムハラ語フィデル全書き順.md").write_text(build_md(), encoding="utf-8")
    n = sum(len(c) for _, _, _, c in SERIES) + sum(len(c) for _, _, c in LABIAL)
    print("ok", n, "letters")
