"""アムハラ語フィデル書き順ガイドを生成する。

出力(アムハラ語フォルダ直下):
  アムハラ語フィデル書き順.html        Web版(Artifact用。doctypeなしの断片)
  アムハラ語フィデル書き順-print.html  印刷用(A4縦。Edgeヘッドレスで PDF 化)
  アムハラ語フィデル書き順.md          テキスト版

字形の下図は Noto Sans Ethiopic(SIL OFL)のアウトラインを glyph_outlines.json に
書き出したもの。座標系は font 単位(1000/em)で y を反転(svgY = 900 - fontY)。
筆順線(STROKES)はその字形の中心線を手で引いたもの。
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
OUTLINES = json.loads((HERE / "glyph_outlines.json").read_text(encoding="utf-8"))


def bowl(x):
    """ጨ の脚の下に付く右向きの小さな輪。"""
    return (f"M{x} 670 L{x+89} 670 C{x+165} 670 {x+195} 700 {x+195} 765 "
            f"C{x+195} 835 {x+155} 867 {x+55} 867 L{x} 867")


ARCH_LOW = "M135 900 L135 543 C135 420 200 329 310 329 C420 329 482 420 482 543 L482 900"
OVAL = ("M298 217 C170 217 115 300 115 440 L115 648 C115 790 170 870 298 870 "
        "C426 870 483 790 483 648 L483 440 C483 300 426 217 298 217")
BAR_LOW = "M30 895 C45 820 70 782 120 782 L480 782 C530 782 555 820 570 895"
TI_LEFT = "M135 900 L135 517 C135 330 230 226 424 226 L488 226 L488 {y}"
TI_RIGHT = "M488 270 C530 240 600 226 670 226 C790 226 840 300 840 450 L840 {y}"

# (文字, ローマ字, 伝統名, [筆順パス], [各画の説明], 派生元)
LETTERS = [
    ("ሀ", "hä", "Hoy",
     ["M135 186 L135 655 C135 800 200 870 308 870 C420 870 482 800 482 655 L482 186"],
     ["左上から下へ下ろし、底で丸く回って右の縦線を上へ"], None),
    ("ለ", "lä", "Läwe",
     ["M295 186 L517 900", "M300 378 C215 395 160 470 130 580 C110 660 95 760 87 900"],
     ["長い斜線を上から右下へ", "斜線の途中から弧を描いて左下へ"], None),
    ("ሐ", "ḥä", "Ḥäwt",
     ["M120 900 L120 720 C120 590 210 508 379 508 C548 508 638 590 638 720 L638 900", "M379 186 L379 900"],
     ["左下から上がって山形を描き、右下へ", "中央の縦線を上から下へ(山を貫く)"], None),
    ("መ", "mä", "May",
     ["M397 221 L397 790 C370 840 320 873 262 873 C160 873 115 790 115 588 C115 400 170 221 330 221 "
      "L690 221 C800 221 845 330 845 503 C845 680 790 791 690 791 L598 791", "M598 221 L598 791"],
     ["中央の縦線を下ろし、左下で回って左側を上がり、上辺を右へ進んで右の丸みを描く", "右の縦線を上から下へ"], None),
    ("ሠ", "śä", "Śäwt",
     ["M135 186 L135 690 C135 800 180 870 275 870 C370 870 417 800 417 690 L417 186",
      "M699 186 L699 590 C699 700 650 770 560 770 C490 770 445 740 425 700"],
     ["左の縦線を下ろし、底で回って中央の縦線を上へ", "右の縦線を下ろし、下で左へ曲げて中央の線につなぐ"], None),
    ("ረ", "rä", "Rəʾs",
     ["M403 186 C403 270 370 330 300 400 C200 495 97 570 97 705 C97 800 160 864 275 864 L500 864"],
     ["右上から曲線で左下へ下ろし、底で右へ折り返して横に引く"], None),
    ("ሰ", "sä", "Sat",
     [ARCH_LOW, "M310 140 L310 329"],
     ["左下から上がって山形を描き、右下へ", "頂上の短い縦線を上から下へ"], None),
    ("ሸ", "šä", "Sha",
     [ARCH_LOW, "M310 164 L310 329", "M60 164 L560 164"],
     ["山形(ሰ と同じ)", "頂上の短い縦線", "いちばん上の横棒を左から右へ"], "ሰ"),
    ("ቀ", "ḳä", "Ḳaf",
     ["M326 366 C160 366 86 420 86 500 C86 580 160 636 326 636 C490 636 566 580 566 500 C566 420 490 366 326 366",
      "M326 186 L326 900"],
     ["横長の輪を上から左回りに", "縦線を上から下へ(輪を貫く)"], None),
    ("በ", "bä", "Bet",
     ["M135 900 L135 430 C135 300 200 216 310 216 C420 216 482 300 482 430 L482 900"],
     ["左下から上がって山形を描き、右下へ下ろす"], None),
    ("ቨ", "vä", "Va",
     [ARCH_LOW.replace("329", "327"), "M70 164 L550 164"],
     ["山形(በ と同じ)", "上の横棒を左から右へ"], "በ"),
    ("ተ", "tä", "Täwe",
     ["M30 510 C45 440 70 400 120 400 L480 400 C530 400 555 440 570 510", "M300 186 L300 900"],
     ["横棒を左から右へ(両端は少し下へ払う)", "縦線を上から下へ"], None),
    ("ቸ", "čä", "Cha",
     ["M37 512 C52 440 77 400 127 400 L487 400 C537 400 562 440 577 512", "M307 164 L307 900", "M60 164 L560 164"],
     ["中段の横棒(ተ と同じ)", "縦線を上から下へ", "いちばん上の横棒"], "ተ"),
    ("ኀ", "ḫä", "Ḫarm",
     ["M240 187 L240 260 C240 350 300 395 408 400 L408 900", "M30 412 C45 340 70 300 120 300 L240 300"],
     ["上の短い縦線を下ろし、右へ曲がって右の縦線を下まで", "左の腕を左端から右へ"], None),
    ("ነ", "nä", "Nähas",
     ["M105 187 L105 260 C105 350 160 395 273 400 L273 900"],
     ["左上から下ろし、右へ曲がって右の縦線を下まで"], None),
    ("ኘ", "ñä", "Nya",
     ["M261 223 L261 310 C261 400 320 445 430 450 L430 900", "M40 223 L490 223"],
     ["ነ と同じ形", "上の横棒を左から右へ"], "ነ"),
    ("አ", "ʾä", "ʾÄlf",
     ["M106 187 L106 260 C106 350 160 400 250 403 L320 403 L106 900", "M290 555 C400 600 470 700 482 900"],
     ["左上から下ろして右へ曲がり、折り返して斜めに左下へ", "斜線の途中から右下へ弧を描く"], None),
    ("ከ", "kä", "Kaf",
     ["M95 140 L95 240 C95 300 125 335 175 360 C210 340 270 327 340 327 C450 327 512 410 512 543 L512 900",
      "M170 380 C166 420 165 470 165 543 L165 900"],
     ["左上から下ろして右へ回り込み、山形を描いて右下へ", "左の脚を上から下へ"], None),
    ("ኸ", "xä", "Xa",
     ["M270 164 L270 297 C270 350 300 385 348 405 C390 390 440 383 514 383 C625 383 688 460 688 600 L688 900",
      "M345 425 C341 470 340 520 340 600 L340 900", "M30 164 L500 164"],
     ["上から下ろして山形を描き、右下へ(ከ と同じ)", "左の脚を上から下へ", "上の横棒を左から右へ"], "ከ"),
    ("ወ", "wä", "Wäwe",
     ["M397 221 L397 790 C370 840 320 873 262 873 C160 873 115 790 115 588 C115 400 170 221 330 221 "
      "L488 221 C600 221 643 330 643 503 C643 680 590 791 488 791 L397 791"],
     ["中央の縦線を下ろし、左下で回って左側を上がり、上辺を右へ、右の丸みを描いて中央に戻る"], None),
    ("ዐ", "ʿä", "ʿÄyn",
     [OVAL],
     ["上の中央から左回りに縦長の輪を描く"], None),
    ("ዘ", "zä", "Zäy",
     ["M135 186 L135 900", "M413 186 L413 900", "M135 527 L413 527"],
     ["左の縦線を上から下へ", "右の縦線を上から下へ", "中央の横線を左から右へ"], None),
    ("ዠ", "žä", "Zha",
     ["M30 335 C45 260 80 222 140 222 C220 222 262 260 262 340 L262 900",
      "M772 335 C757 260 722 222 662 222 C582 222 540 260 540 340 L540 900", "M262 527 L540 527"],
     ["左の縦線(上端を左へ曲げて始める)", "右の縦線(上端を右へ曲げて始める)", "中央の横線を左から右へ"], "ዘ"),
    ("የ", "yä", "Yämän",
     ["M225 535 C320 510 385 450 385 350 C385 260 330 210 243 210 C155 210 95 260 95 350 "
      "C95 430 140 490 165 535 C215 610 241 680 241 790 L241 900"],
     ["輪の右下から右側を上がり、左回りに輪を描き、交点を抜けてそのまま縦線を下へ"], None),
    ("ደ", "dä", "Dänt",
     ["M232 471 C340 471 470 450 470 320 C470 250 420 209 352 209 C240 209 184 290 184 449 C184 560 230 680 300 782",
      BAR_LOW],
     ["輪の内側から右上へ回って左回りに輪を描き、左側から斜めに右下へ", "下の横棒を左から右へ(両端は下へ払う)"], None),
    ("ጀ", "jä", "Ja",
     ["M210 580 C320 580 441 560 441 450 C441 380 390 339 317 339 C210 339 161 410 161 520 C161 640 220 720 285 782",
      BAR_LOW, "M300 216 L300 339", "M45 216 L555 216"],
     ["輪と斜線(ደ と同じ)", "下の横棒", "上の短い縦線", "いちばん上の横棒"], "ደ"),
    ("ገ", "gä", "Gäml",
     ["M30 335 C45 260 80 222 142 222 C250 222 330 235 370 270 C420 310 435 380 435 500 L435 900"],
     ["左端の払いから右へ進み、右側で曲がって縦に下ろす"], None),
    ("ጠ", "ṭä", "Ṭäyt",
     [TI_LEFT.format(y=900), TI_RIGHT.format(y=900)],
     ["左下から上がって左の山を描き、中央の縦線を下まで", "中央の線の上から右の山を描いて右下へ"], None),
    ("ጨ", "č̣ä", "Cha'",
     [TI_LEFT.format(y=867), TI_RIGHT.format(y=867), bowl(135), bowl(488), bowl(840)],
     ["左の山と中央の縦線(ጠ と同じ)", "右の山", "左の脚の下に小さな輪", "中央の脚の下に小さな輪", "右の脚の下に小さな輪"], "ጠ"),
    ("ጰ", "p̣ä", "P̣äyt",
     ["M80 900 C80 790 110 720 170 660 C220 610 300 570 330 545 C380 505 408 460 408 397 C408 330 350 274 276 274 "
      "C200 274 140 330 140 400 C140 470 200 510 270 545 C400 610 471 700 471 880 L471 900", "M276 140 L276 274"],
     ["8の字(ጸ と同じ)", "上の短い縦線を上から下へ"], "ጸ"),
    ("ጸ", "ṣä", "Ṣädäy",
     ["M80 900 C80 760 105 670 170 600 C220 550 300 510 330 485 C380 445 408 400 408 337 C408 270 350 212 276 212 "
      "C200 212 140 270 140 340 C140 410 200 450 270 485 C400 550 471 640 471 860 L471 900"],
     ["左下から斜めに上がり、上の輪を左回りに描いて交点に戻り、右下へ下ろす"], None),
    ("ፀ", "ṣ́ä", "Ṣ́äppä",
     [OVAL, "M115 540 L483 540"],
     ["縦長の輪(ዐ と同じ)", "中央の横線を左から右へ"], "ዐ"),
    ("ፈ", "fä", "Äf",
     ["M446 176 C446 300 420 400 360 450 C300 510 220 540 160 590 C110 630 95 680 95 730 "
      "C95 820 150 866 225 866 C300 866 357 810 357 720 C357 640 300 600 230 590", "M330 866 L620 866"],
     ["右上から左下へ下ろし、下で輪を描いて止める", "下の横棒を右へ"], None),
    ("ፐ", "pä", "Psa",
     ["M30 340 C45 260 75 222 125 222 L475 222 C525 222 555 260 570 340", "M300 222 L300 900"],
     ["上の横棒を左から右へ(両端は下へ払う)", "縦線を上から下へ"], None),
]

CIRCLED = "①②③④⑤⑥"

PRINCIPLES = [
    ("左から右へ", "現代のゲエズ文字は左から右へ書きます。1文字の中でも、左にある線から書き始めます。"),
    ("縦の線は上から下へ", "脚が2本の山形(በ・ሰ など)は左下から書き始め、山を越えて右下まで一筆で書きます。"),
    ("輪は左回り", "ዐ・ቀ・የ・ጸ などの輪は、反時計回りに描きます。"),
    ("貫く線は後", "文字の中央を貫く縦線(ሐ・ቀ)や、2本の縦線をつなぐ横線(ዘ)は最後に書きます。"),
    ("足した線は最後", "派生した文字は、元の文字を書いてから横棒や短い線を足します。例: ሰ→ሸ、በ→ቨ、ተ→ቸ、ነ→ኘ、ከ→ኸ、ደ→ጀ、ጸ→ጰ、ዐ→ፀ。"),
]

# 母音の段ごとの形の変化(Noto Sans Ethiopic の字形で確認したもの)
ORDERS = [
    ("I", "ä", "基本の形", "ሀ ለ በ ነ ተ", "書き順はこの資料の基本形どおり。"),
    ("II", "u", "右側の中ほどに短い横線を足す", "ሁ ሉ ቡ ኑ ቱ", "例外: ሩ・ፉ は形が変わる。ዉ は右下に付く。"),
    ("III", "i", "右脚の下端に短い足を付ける", "ሂ ሊ ቢ ኒ ቲ", "足は右へ短く払う。"),
    ("IV", "a", "2本脚は左脚を短くする。1本脚は下端を左へ曲げる", "ሃ ላ ባ ና ታ", "ማ・ራ・ዋ は形が大きく変わる。"),
    ("V", "e", "右脚の下端に小さな輪を付ける", "ሄ ሌ ቤ ኔ ቴ", "輪は最後に描く。"),
    ("VI", "ɨ", "形の変わり方が不規則", "ህ ል ብ ን ት", "子音だけを表す段。1文字ずつ覚える。"),
    ("VII", "o", "右上に小さな輪を付ける。または脚の長さを変える", "ሆ ኖ ቶ ሞ ሮ", "ቦ・ጦ は右脚を短くする。ሎ は右脚の中ほどに輪。"),
]
SERIES = [0x1200, 0x1208, 0x1260, 0x1290, 0x1270]  # ሀ ለ በ ነ ተ の7段

TOKENS = """
  /* Layout: 写本の紙面に、字形カードを方眼で並べる。上に原則、下に母音の段 */
  :root {
    --bg: #EDEAE1; --surface: #F8F5ED; --surface-alt: #E2DDCD;
    --ink: #241F19; --ink-muted: #6E6455; --accent: #AC3527;
    --accent-soft: #DCC9AE; --border: #D6CFBC; --guide: #DDD5C4; --grid: #E6DFD0;
    --s1: #B23A2B; --s2: #2F5E8C; --s3: #3E7B3A; --s4: #A86A12; --s5: #7A3E8E;
    --f-ge: "Noto Serif Ethiopic", "Nyala", serif;
    --f-jp: "Noto Sans JP", "Hiragino Sans", "Yu Gothic", sans-serif;
    --f-rom: "Noto Serif", Georgia, serif;
  }
  @media (prefers-color-scheme: dark) {
    :root:not([data-theme="light"]) {
      color-scheme: dark;
      --bg: #1B1712; --surface: #241F19; --surface-alt: #2D2721;
      --ink: #EEE6D6; --ink-muted: #A6987F; --accent: #E06A54;
      --accent-soft: #493F35; --border: #3A332B; --guide: #3A332B; --grid: #2D2721;
      --s1: #E4705A; --s2: #78A8DA; --s3: #7DBA72; --s4: #E0A245; --s5: #C08AD6;
    }
  }
  :root[data-theme="dark"] {
    color-scheme: dark;
    --bg: #1B1712; --surface: #241F19; --surface-alt: #2D2721;
    --ink: #EEE6D6; --ink-muted: #A6987F; --accent: #E06A54;
    --accent-soft: #493F35; --border: #3A332B; --guide: #3A332B; --grid: #2D2721;
    --s1: #E4705A; --s2: #78A8DA; --s3: #7DBA72; --s4: #E0A245; --s5: #C08AD6;
  }
"""

CSS = """
  * { box-sizing: border-box; }
  body {
    margin: 0; background: var(--bg); color: var(--ink);
    font-family: var(--f-jp); line-height: 1.7;
    padding-left: max(16px, env(safe-area-inset-left, 0px));
    padding-right: max(16px, env(safe-area-inset-right, 0px));
    padding-block: clamp(20px, 4vw, 56px);
  }
  .page { max-width: 1180px; margin: 0 auto; display: flex; flex-direction: column; gap: 32px; }
  .ge { font-family: var(--f-ge); }
  .rom { font-family: var(--f-rom); font-style: italic; }

  header.masthead {
    display: flex; flex-wrap: wrap; align-items: baseline; gap: 14px 28px;
    padding-bottom: 20px; border-bottom: 2px solid var(--accent);
  }
  .mark { font-family: var(--f-ge); font-size: clamp(2.3rem, 6vw, 3.4rem); font-weight: 700; color: var(--accent); line-height: 1.1; }
  .titles { min-width: 0; flex: 1 1 320px; }
  .titles h1 { font-size: clamp(1.3rem, 2.6vw, 1.7rem); margin: 0 0 4px; text-wrap: balance; }
  .titles p { margin: 0; color: var(--ink-muted); font-size: 0.9rem; max-width: 66ch; }

  .note {
    margin: 0; font-size: 0.88rem; background: var(--surface);
    border: 1px solid var(--border); border-left: 4px solid var(--accent);
    border-radius: 4px; padding: 10px 14px; max-width: 86ch;
  }
  h2 { margin: 0; font-size: 1.15rem; display: flex; flex-wrap: wrap; align-items: baseline; gap: 4px 12px; text-wrap: balance; }
  h2 .ge { color: var(--accent); font-size: 1.4rem; }
  h2 .rd { font-size: 0.8rem; color: var(--ink-muted); font-weight: 400; }
  section { display: flex; flex-direction: column; gap: 14px; }

  ol.rules { list-style: none; margin: 0; padding: 0; display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: 10px; counter-reset: r; }
  ol.rules li { counter-increment: r; background: var(--surface); border: 1px solid var(--border); border-radius: 4px; padding: 10px 14px; font-size: 0.86rem; min-width: 0; }
  ol.rules b { display: block; font-size: 0.95rem; color: var(--accent); }
  ol.rules b::before { content: counter(r) ". "; }
  ol.rules .ge { font-size: 1.05em; }

  .legend { display: flex; flex-wrap: wrap; gap: 6px 16px; font-size: 0.8rem; color: var(--ink-muted); align-items: center; }
  .legend i { display: inline-block; width: 22px; height: 4px; border-radius: 2px; vertical-align: middle; margin-right: 6px; }

  .cards { display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 12px; }
  .card { background: var(--surface); border: 1px solid var(--border); border-radius: 4px; padding: 12px 14px 14px; display: flex; flex-direction: column; gap: 8px; min-width: 0; }
  .card header { display: flex; align-items: baseline; gap: 10px; }
  .card .glyph { font-family: var(--f-ge); font-size: 1.9rem; line-height: 1; color: var(--ink); }
  .card .meta { display: flex; flex-direction: column; line-height: 1.3; min-width: 0; }
  .card .meta .rom { font-size: 0.95rem; }
  .card .meta small { font-size: 0.72rem; color: var(--ink-muted); }
  .card .count { margin-left: auto; font-size: 0.75rem; color: var(--ink-muted); white-space: nowrap; font-variant-numeric: tabular-nums; }
  .card .from { font-size: 0.72rem; color: var(--accent); }
  .card svg { width: 100%; height: auto; aspect-ratio: 1; max-width: 100%; background: var(--bg); border-radius: 3px; }
  .card ol { margin: 0; padding: 0; list-style: none; display: flex; flex-direction: column; gap: 3px; font-size: 0.82rem; }
  .card ol li { display: grid; grid-template-columns: 1.4em 1fr; gap: 4px; }
  .card ol .n { font-weight: 700; }
  .card ol .ge { font-size: 1.05em; }
  .card button {
    align-self: flex-start; font: inherit; font-size: 0.8rem; padding: 4px 12px; cursor: pointer;
    background: transparent; color: var(--accent); border: 1px solid var(--accent); border-radius: 4px;
  }
  .card button:hover { background: var(--accent); color: var(--surface); }
  .card button:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }

  svg .gl { fill: var(--guide); }
  svg .gr { stroke: var(--grid); stroke-width: 3; }
  svg .st { fill: none; stroke-width: 26; stroke-linecap: round; stroke-linejoin: round; }
  svg .dot { stroke: var(--surface); stroke-width: 6; }
  svg .num { font: 700 46px var(--f-jp); fill: var(--surface); text-anchor: middle; dominant-baseline: central; }
  .c1 { stroke: var(--s1); color: var(--s1); } .c2 { stroke: var(--s2); color: var(--s2); }
  .c3 { stroke: var(--s3); color: var(--s3); } .c4 { stroke: var(--s4); color: var(--s4); }
  .c5 { stroke: var(--s5); color: var(--s5); }
  circle.c1 { fill: var(--s1); } circle.c2 { fill: var(--s2); } circle.c3 { fill: var(--s3); }
  circle.c4 { fill: var(--s4); } circle.c5 { fill: var(--s5); }
  .legend .c1 { background: var(--s1); } .legend .c2 { background: var(--s2); } .legend .c3 { background: var(--s3); }
  .legend .c4 { background: var(--s4); } .legend .c5 { background: var(--s5); }

  .tbl-wrap { overflow-x: auto; }
  table { border-collapse: collapse; width: 100%; background: var(--surface); font-size: 0.86rem; }
  th, td { border: 1px solid var(--border); padding: 6px 10px; text-align: left; vertical-align: top; }
  thead th { background: var(--surface-alt); font-weight: 500; white-space: nowrap; }
  td.ord { white-space: nowrap; font-weight: 700; color: var(--accent); }
  td.ex { font-family: var(--f-ge); font-size: 1.3rem; white-space: nowrap; letter-spacing: 0.15em; }
  td.nt { color: var(--ink-muted); font-size: 0.8rem; }
  table.series td, table.series th { text-align: center; }
  table.series td { font-family: var(--f-ge); font-size: 1.6rem; line-height: 1.3; }
  table.series th small { display: block; font-family: var(--f-rom); font-style: italic; font-weight: 400; }

  footer { font-size: 0.78rem; color: var(--ink-muted); border-top: 1px solid var(--border); padding-top: 12px; }
  footer a { color: var(--accent); }

  @media (prefers-reduced-motion: reduce) { .card button { display: none; } }
"""

PRINT_CSS = """
  @page { size: A4 portrait; margin: 11mm 10mm; }
  body { padding: 0; font-size: 12px; background: #fff; }
  :root { --bg: #FBF9F4; --surface: #fff; }
  .page { max-width: none; gap: 14px; padding-inline: 2px; }
  .mark { font-size: 2.4rem; }
  .cards { grid-template-columns: repeat(5, minmax(0, 1fr)); gap: 6px; }
  .card { padding: 7px 8px 8px; gap: 5px; break-inside: avoid; }
  .card .glyph { font-size: 1.5rem; }
  .card ol { font-size: 0.66rem; line-height: 1.45; }
  .card .meta small, .card .count, .card .from { font-size: 0.62rem; }
  .card button { display: none; }
  ol.rules { grid-template-columns: repeat(3, minmax(0, 1fr)); }
  ol.rules li { font-size: 0.78rem; padding: 7px 10px; }
  section.orders { break-before: page; }
  table { font-size: 0.8rem; }
  tr { break-inside: avoid; }
"""


def svg_for(ch, strokes):
    o = OUTLINES[ch]
    # 字形の縦範囲 y=30〜990 が収まる正方形。横幅の広い字(መ・ጠ・ጨ)は全体を縮める
    side = max(o["w"] + 120, 960)
    vx, vy = o["w"] / 2 - side / 2, 510 - side / 2
    grid = "".join(
        f'<line class="gr" x1="{vx:.0f}" y1="{y}" x2="{vx + side:.0f}" y2="{y}"/>' for y in (186, 543, 900)
    )
    parts = [f'<svg viewBox="{vx:.0f} {vy:.0f} {side:.0f} {side:.0f}" role="img" '
             f'aria-label="{ch} の書き順({len(strokes)}画)">', "<g>", grid,
             f'<path class="gl" d="{o["d"]}"/>']
    for i, d in enumerate(strokes, 1):
        parts.append(f'<path class="st c{i}" d="{d}" pathLength="1"/>')
    for i, d in enumerate(strokes, 1):
        x, y = d[1:].split(" ")[:2]
        parts.append(f'<circle class="dot c{i}" cx="{x}" cy="{y}" r="36"/>'
                     f'<text class="num" x="{x}" y="{y}">{i}</text>')
    parts.append("</g></svg>")
    return "".join(parts)


def ge_spans(text):
    """説明文中のエチオピア文字を .ge で囲む。"""
    out, buf = [], ""
    for c in text:
        is_ge = 0x1200 <= ord(c) <= 0x139F
        if is_ge:
            buf += c
        else:
            if buf:
                out.append(f'<span class="ge">{buf}</span>')
                buf = ""
            out.append(c)
    if buf:
        out.append(f'<span class="ge">{buf}</span>')
    return "".join(out)


def card(ch, rom, name, strokes, steps, src, printable):
    lis = "".join(
        f'<li><span class="n c{i}">{CIRCLED[i - 1]}</span><span>{ge_spans(s)}</span></li>'
        for i, s in enumerate(steps, 1)
    )
    from_ = f'<span class="from">{ge_spans(src)} に線を足した形</span>' if src else ""
    btn = "" if printable else f'<button type="button" id="play-{ord(ch):x}" data-play>なぞって再生</button>'
    return (f'<article class="card"><header><span class="glyph">{ch}</span>'
            f'<span class="meta"><span class="rom">{rom}</span><small>{name}</small></span>'
            f'<span class="count">{len(strokes)}画</span></header>'
            f'{from_}{svg_for(ch, strokes)}<ol>{lis}</ol>{btn}</article>')


SCRIPT = """
<script>
(() => {
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  document.querySelectorAll('[data-play]').forEach(btn => {
    btn.addEventListener('click', () => {
      if (reduce) return;
      const svg = btn.closest('.card').querySelector('svg');
      const paths = [...svg.querySelectorAll('.st')];
      svg.getAnimations({ subtree: true }).forEach(a => a.cancel());
      let t = 0;
      paths.forEach(p => {
        const dur = 450 + p.getTotalLength() * 0.55;
        p.animate([{ strokeDasharray: '1 1', strokeDashoffset: 1 }, { strokeDasharray: '1 1', strokeDashoffset: 0 }],
                  { duration: dur, delay: t, easing: 'ease-in-out', fill: 'backwards' });
        t += dur + 180;
      });
    });
  });
})();
</script>
"""


def build_html(printable):
    head = [
        '<meta charset="utf-8">' if printable else "",
        "<title>フィデル書き順ガイド</title>",
        "" if printable else '<meta name="claude:viewport-fit-sides" content="cover">',
        '<link rel="preconnect" href="https://fonts.googleapis.com">',
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>',
        '<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+Ethiopic:wght@400;700'
        '&family=Noto+Sans+JP:wght@400;500;700&family=Noto+Serif:ital,wght@0,400;1,400&display=swap" rel="stylesheet">',
        "<style>" + TOKENS + CSS + (PRINT_CSS if printable else "") + "</style>",
    ]
    rules = "".join(f"<li><b>{t}</b>{ge_spans(d)}</li>" for t, d in PRINCIPLES)
    legend = "".join(f'<span><i class="c{i}"></i>{CIRCLED[i - 1]} {i}画目</span>' for i in range(1, 6))
    cards = "".join(card(*L, printable) for L in LETTERS)
    orders = "".join(
        f'<tr><td class="ord">{o} <span class="rom">{v}</span></td><td>{ge_spans(how)}</td>'
        f'<td class="ex">{ex}</td><td class="nt">{ge_spans(nt)}</td></tr>'
        for o, v, how, ex, nt in ORDERS
    )
    s_head = "".join(f"<th>{o}<small>{v}</small></th>" for o, v, *_ in ORDERS)
    s_rows = "".join("<tr>" + "".join(f"<td>{chr(b + i)}</td>" for i in range(7)) + "</tr>" for b in SERIES)
    total = sum(len(L[3]) for L in LETTERS)
    body = f"""
<div class="page">
  <header class="masthead">
    <span class="mark">ፊደል</span>
    <div class="titles">
      <h1>アムハラ語 フィデル書き順ガイド</h1>
      <p>基本の34文字(段I・ä)の書き順を、字形の上に色と番号で示しました。番号の丸が書き始めの位置です。34文字・計{total}画。</p>
    </div>
  </header>

  <p class="note">ゲエズ文字には、漢字のような公式に定められた筆順はありません。教材や書き手によって違いがあります。この資料は、字形の構造から無理のない順序を選んだ<b>学習用の目安</b>です。下図の字形は Noto Sans Ethiopic です。</p>

  <section class="principles">
    <h2>書き順の原則 <span class="rd">この資料で使っている5つの決まり</span></h2>
    <ol class="rules">{rules}</ol>
  </section>

  <section class="letters">
    <h2><span class="ge">ሀ — ፐ</span> 基本の34文字 <span class="rd">フィデル表と同じ並び</span></h2>
    <div class="legend">{legend}</div>
    <div class="cards">{cards}</div>
  </section>

  <section class="orders">
    <h2>母音の7段の書き方 <span class="rd">基本形を書いてから、最後に印を足す</span></h2>
    <p class="note">段II〜VIIは、基本形(段I)を書いたあと、決まった位置に短い線や輪を足すか、脚の形を変えて作ります。足す線や輪は最後に書きます。段VIだけは変わり方が不規則です。</p>
    <div class="tbl-wrap"><table>
      <thead><tr><th>段</th><th>形の変え方</th><th>例</th><th>補足</th></tr></thead>
      <tbody>{orders}</tbody>
    </table></div>
    <div class="tbl-wrap"><table class="series">
      <thead><tr>{s_head}</tr></thead>
      <tbody>{s_rows}</tbody>
    </table></div>
  </section>

  <footer>34文字の音価・カタカナ読みは「アムハラ語フィデル表」を参照してください。字形: Noto Sans Ethiopic(SIL Open Font License)。2026-10-20 作成。</footer>
</div>
"""
    doc = "\n".join(h for h in head if h) + body + ("" if printable else SCRIPT)
    return doc


def build_md():
    lines = [
        "# アムハラ語 フィデル書き順ガイド",
        "",
        "基本の34文字(段I・ä)の書き順を、文字ごとに画の順で説明する。",
        "図(色と番号付き)は Web版・PDF を参照。",
        "",
        "> ゲエズ文字には公式に定められた筆順はなく、教材や書き手によって違いがある。",
        "> この資料は字形の構造から無理のない順序を選んだ**学習用の目安**。",
        "",
        "## 書き順の原則",
        "",
    ]
    lines += [f"{i}. **{t}** — {d}" for i, (t, d) in enumerate(PRINCIPLES, 1)]
    lines += ["", "## 基本の34文字", "", "| 文字 | ローマ字 | 画数 | 書き順 |", "|---|---|---|---|"]
    for ch, rom, name, strokes, steps, src in LETTERS:
        desc = " ".join(f"{CIRCLED[i]}{s}" for i, s in enumerate(steps))
        if src:
            desc += f"({src} に線を足した形)"
        lines.append(f"| {ch} | {rom} ({name}) | {len(strokes)} | {desc} |")
    lines += ["", "## 母音の7段の書き方", "",
              "基本形(段I)を書いたあと、決まった位置に線や輪を足すか、脚の形を変える。足す線や輪は最後に書く。", "",
              "| 段 | 母音 | 形の変え方 | 例 | 補足 |", "|---|---|---|---|---|"]
    lines += [f"| {o} | {v} | {how} | {ex} | {nt} |" for o, v, how, ex, nt in ORDERS]
    lines += ["", "---", "字形: Noto Sans Ethiopic(SIL Open Font License)。生成: `tools/build_stroke_order.py`(2026-10-20)。", ""]
    return "\n".join(lines)


if __name__ == "__main__":
    (ROOT / "アムハラ語フィデル書き順.html").write_text(build_html(False), encoding="utf-8")
    (ROOT / "アムハラ語フィデル書き順-print.html").write_text(build_html(True), encoding="utf-8")
    (ROOT / "アムハラ語フィデル書き順.md").write_text(build_md(), encoding="utf-8")
    print("ok", len(LETTERS), "letters,", sum(len(L[3]) for L in LETTERS), "strokes")
