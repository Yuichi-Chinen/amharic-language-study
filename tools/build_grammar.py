"""アムハラ語の基礎文法まとめを生成する。

出力(アムハラ語フォルダ直下):
  アムハラ語基礎文法.html        Web版(Artifact用。doctypeなしの断片)
  アムハラ語基礎文法-print.html  印刷用(A4縦。Edgeヘッドレスで PDF 化)
  アムハラ語基礎文法.md          テキスト版

表のセルは、文字列なら日本語の説明、(フィデル, ローマ字, カタカナ) のタプルならアムハラ語として描く。
見た目は build_greetings.py と共通。
"""
import json
from pathlib import Path

import build_greetings as g

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
NAME = "アムハラ語基礎文法"
WEB_URL = "https://claude.ai/artifact/1W92sWYiL2N3Kf1DqCrJer"

esc, ge_spans = g.esc, g.ge_spans

# 人称: (日本語, 代名詞, 〜です, 〜ではありません, 所有「〜の家」, 欲しい(現在), 欲しかった(過去), 欲しくない(否定))
PERSONS = [
    ("私", ("እኔ", "əne", "イネ"), ("ነኝ", "näññ", "ネニュ"), ("አይደለሁም", "aydällähumm", "アイデッレフム"),
     ("ቤቴ", "bete", "ベテ"), ("እፈልጋለሁ", "əfälləgallähu", "イフェッリガッレフ"),
     ("ፈለግኩ", "fällägku", "フェッレグク"), ("አልፈልግም", "alfälləgəm", "アルフェッリグム")),
    ("あなた(男性)", ("አንተ", "antä", "アンテ"), ("ነህ", "näh", "ネフ"), ("አይደለህም", "aydällähəmm", "アイデッレヒム"),
     ("ቤትህ", "betəh", "ベティフ"), ("ትፈልጋለህ", "təfälləgalläh", "ティフェッリガッレフ"),
     ("ፈለግክ", "fällägk", "フェッレギク"), ("አትፈልግም", "atfälləgəm", "アティフェッリグム")),
    ("あなた(女性)", ("አንቺ", "anči", "アンチ"), ("ነሽ", "näš", "ネシュ"), ("አይደለሽም", "aydälläšəmm", "アイデッレシム"),
     ("ቤትሽ", "betəš", "ベティシュ"), ("ትፈልጊያለሽ", "təfälləgiyalläš", "ティフェッリギヤッレシュ"),
     ("ፈለግሽ", "fällägš", "フェッレギシュ"), ("አትፈልጊም", "atfälləgim", "アティフェッリギム")),
    ("あなた(目上)", ("እርስዎ", "ərswo", "イルスウォ"), ("ነዎት", "näwot", "ネウォト"), ("አይደሉም", "aydällumm", "アイデッルム"),
     ("ቤትዎ", "betwo", "ベトウォ"), ("ይፈልጋሉ", "yəfälləgallu", "イフェッリガッル"),
     ("ፈለጉ", "fällägu", "フェッレグ"), ("አይፈልጉም", "ayfälləgum", "アイフェッリグム")),
    ("彼", ("እሱ", "əssu", "イッス"), ("ነው", "näw", "ネウ"), ("አይደለም", "aydällämm", "アイデッレム"),
     ("ቤቱ", "betu", "ベトゥ"), ("ይፈልጋል", "yəfälləgal", "イフェッリガル"),
     ("ፈለገ", "fällägä", "フェッレゲ"), ("አይፈልግም", "ayfälləgəm", "アイフェッリグム")),
    ("彼女", ("እሷ", "əsswa", "イッスワ"), ("ናት", "nat", "ナト"), ("አይደለችም", "aydälläččəmm", "アイデッレッチム"),
     ("ቤቷ", "betwa", "ベトワ"), ("ትፈልጋለች", "təfälləgalläčč", "ティフェッリガッレッチ"),
     ("ፈለገች", "fällägäčč", "フェッレゲッチ"), ("አትፈልግም", "atfälləgəm", "アティフェッリグム")),
    ("あの方(目上)", ("እሳቸው", "əssaččäw", "イッサッチェウ"), ("ናቸው", "naččäw", "ナッチェウ"), ("አይደሉም", "aydällumm", "アイデッルム"),
     ("ቤታቸው", "betaččäw", "ベタッチェウ"), ("ይፈልጋሉ", "yəfälləgallu", "イフェッリガッル"),
     ("ፈለጉ", "fällägu", "フェッレグ"), ("አይፈልጉም", "ayfälləgum", "アイフェッリグム")),
    ("私たち", ("እኛ", "əñña", "イッニャ"), ("ነን", "nän", "ネン"), ("አይደለንም", "aydällänəmm", "アイデッレニム"),
     ("ቤታችን", "betaččən", "ベタッチン"), ("እንፈልጋለን", "ənfälləgallän", "インフェッリガッレン"),
     ("ፈለግን", "fällägn", "フェッレグン"), ("አንፈልግም", "anfälləgəm", "アンフェッリグム")),
    ("あなたたち", ("እናንተ", "ənnantä", "インナンテ"), ("ናችሁ", "naččəhu", "ナッチュフ"), ("አይደላችሁም", "aydällaččəhumm", "アイデッラッチュフム"),
     ("ቤታችሁ", "betaččəhu", "ベタッチュフ"), ("ትፈልጋላችሁ", "təfälləgallaččəhu", "ティフェッリガラッチュフ"),
     ("ፈለጋችሁ", "fällägaččəhu", "フェッレガッチュフ"), ("አትፈልጉም", "atfälləgum", "アティフェッリグム")),
    ("彼ら", ("እነሱ", "ənnässu", "インネッス"), ("ናቸው", "naččäw", "ナッチェウ"), ("አይደሉም", "aydällumm", "アイデッルム"),
     ("ቤታቸው", "betaččäw", "ベタッチェウ"), ("ይፈልጋሉ", "yəfälləgallu", "イフェッリガッル"),
     ("ፈለጉ", "fällägu", "フェッレグ"), ("አይፈልጉም", "ayfälləgum", "アイフェッリグム")),
]
PLURAL_SUBJ = {"私たち", "あなたたち", "彼ら"}

# 文を作る練習の述語: (日本語, 単数形, 複数形)
PREDICATES = [
    ("学生", ("ተማሪ", "tämari", "テマリ"), ("ተማሪዎች", "tämariwočč", "テマリウォッチ")),
    ("元気", ("ደህና", "dähna", "デフナ"), ("ደህና", "dähna", "デフナ")),
    ("日本の出身", ("ከጃፓን", "käǰapan", "ケジャパン"), ("ከጃፓን", "käǰapan", "ケジャパン")),
]


def subj_rows():
    return [p[0] for p in PERSONS]


# セクション: ge, ja, lead(箇条書き), cols, rows
SECTIONS = [
    {"ge": "ዓረፍተ ነገር", "ja": "文の形", "lead": [
        "語順は日本語と同じ「主語・目的語・動詞」。動詞や「〜です」は文の最後に来る。",
        "主語の代名詞はよく省かれる。ኢትዮጵያዊ ነው(イトッピヤウィ・ネウ)だけで「彼はエチオピア人だ」。",
        "疑問文は語順を変えず、文の終わりを上げて言う。"],
     "cols": ["アムハラ語", "語ごとの意味", "日本語"],
     "rows": [
         [("ኢትዮጵያ አፍሪካ ውስጥ ናት", "ʾityop̣p̣ya afrika wəsṭ nat", "イトッピヤ・アフリカ・ウスト・ナト"),
          "エチオピア / アフリカ / 中 / です", "エチオピアはアフリカにある。"],
         [("እሱ ወደ ከተማ መጣ", "əssu wädä kätäma mäṭṭa", "イッス・ウェデ・ケテマ・メッタ"),
          "彼 / 〜へ / 町 / 来た", "彼は町へ来た。"],
         [("እኔ ቡና እፈልጋለሁ", "əne bunna əfälləgallähu", "イネ・ブンナ・イフェッリガッレフ"),
          "私 / コーヒー / 欲しい", "私はコーヒーが欲しい。"],
         [("ልጁ ውሻውን አባረረ", "ləǧ-u wəšša-w-ən abbarrärä", "ルジュ・ウッシャウン・アッバッレレ"),
          "その男の子 / その犬を / 追い払った", "男の子は犬を追い払った。"],
     ]},
    {"ge": "ተውላጠ ስም", "ja": "人称代名詞と「〜の」", "lead": [
        "「あなた」は相手で4つ(男性・女性・目上・複数)。「彼・彼女」にも目上の人を指す እሳቸው がある。",
        "「〜の」は名詞の後ろに語尾を付ける: ቤት(ベト = 家)→ ቤቴ(私の家)。「私のもの」は የ- を付けて የኔ(イェネ)。"],
     "cols": ["日本語", "代名詞", "〜の家(ቤት + 語尾)"],
     "rows": [[p[0], p[1], p[4]] for p in PERSONS]},
    {"ge": "ነው", "ja": "「〜です」と「〜ではありません」", "lead": [
        "「〜です」は文の最後に置き、主語に合わせて形を変える。",
        "否定は አይደለም(アイデッレム)を同じように変える。彼女の ናት は ነች(ネッチ)とも言う。",
        "例文の ተማሪ(テマリ)は「学生」。複数の主語では複数形 ተማሪዎች にする。"],
     "cols": ["主語", "〜です", "例文", "〜ではありません"],
     "rows": [[f"{p[0]} {p[1][0]}", p[2],
               (f"{p[1][0]} {'ተማሪዎች' if p[0] in PLURAL_SUBJ else 'ተማሪ'} {p[2][0]}",
                f"{p[1][1]} {'tämariwočč' if p[0] in PLURAL_SUBJ else 'tämari'} {p[2][1]}",
                f"{p[1][2]}・{'テマリウォッチ' if p[0] in PLURAL_SUBJ else 'テマリ'}・{p[2][2]}"),
               p[3]] for p in PERSONS]},
    {"ge": "አለ", "ja": "「ある・いる」と「持っている」", "lead": [
        "存在は አለ(アッレ = ある・いる)、否定は የለም(イェッレム = ない・いない)。",
        "「持つ」という動詞はない。አለ に「〜に」の語尾を付けて「私にはある」= 持っている と言う。"],
     "cols": ["日本語", "アムハラ語", "例"],
     "rows": [
         ["ある・いる", ("አለ", "allä", "アッレ"), ("ውሃ አለ", "wəha allä", "ウィハ・アッレ")],
         ["ない・いない", ("የለም", "yälläm", "イェッレム"), ("ውሃ የለም", "wəha yälläm", "ウィハ・イェッレム")],
         ["私は持っている", ("አለኝ", "alläñ", "アッレニュ"), ("ገንዘብ አለኝ", "gänzäb alläñ", "ゲンゼブ・アッレニュ")],
         ["私は持っていない", ("የለኝም", "yälläññəm", "イェッレニム"), ("ገንዘብ የለኝም", "gänzäb yälläññəm", "ゲンゼブ・イェッレニム")],
         ["あなた(男性)は持っている", ("አለህ", "alläh", "アッレフ"), ("ልጅ አለህ?", "ləǧ alläh?", "ルジ・アッレフ?")],
         ["彼は持っている", ("አለው", "alläw", "アッレウ"), "語尾は 彼 -ው、彼女 -ት(አላት アッラト)"],
         ["私たちは持っている", ("አለን", "allän", "アッレン"), "あなたたち አላችሁ、彼ら አላቸው"],
     ]},
    {"ge": "ስም", "ja": "名詞に付く語尾", "lead": [
        "「その」にあたる冠詞は名詞の後ろに付く。男性名詞は -ኡ、女性名詞は -ዋ。",
        "目的語が特定のもの(その〜、人の名前、〜の〜)のときは -ን(〜を)を付ける。"],
     "cols": ["はたらき", "語尾", "例", "意味"],
     "rows": [
         ["その(男性)", ("-ኡ", "-u", "ウ"), ("ቤቱ", "betu", "ベトゥ"), "その家"],
         ["その(女性)", ("-ዋ", "-wa", "ワ"), ("ሠራተኛዋ", "särratäññawa", "セッラテニャワ"), "その(女性の)働き手"],
         ["複数", ("-ኦች", "-očč", "オッチ"), ("ቤቶች", "betočč", "ベトッチ"), "家々"],
         ["複数 + その", ("-ኦቹ", "-očču", "オッチュ"), ("ቤቶቹ", "betočču", "ベトッチュ"), "それらの家"],
         ["〜を(目的語)", ("-ን", "-n", "ン"), ("ቤቱን", "betun", "ベトゥン"), "その家を"],
         ["〜の", ("የ-", "yä-", "イェ"), ("የልጁ ቤት", "yäləǧu bet", "イェルジュ・ベト"), "その男の子の家"],
     ]},
    {"ge": "ይህ እና ያ", "ja": "「これ」と「あれ」", "lead": [
        "「これ・あれ」も男性・女性・複数で形が変わる。話し言葉では ይህ を ይሄ(イヘ)とも言う。",
        "目的語では -ን を付ける: ይህን(ይሄን)ስጠኝ = これをください。"],
     "cols": ["", "これ(近く)", "あれ(遠く)"],
     "rows": [
         ["男性・もの", ("ይህ / ይሄ", "yəh / yəhe", "イフ / イヘ"), ("ያ", "ya", "ヤ")],
         ["女性", ("ይቺ", "yəčči", "イッチ"), ("ያቺ", "yačči", "ヤッチ")],
         ["複数", ("እነዚህ", "ənnäzzih", "インネッズィフ"), ("እነዚያ", "ənnäzziya", "インネッズィヤ")],
     ]},
    {"ge": "ጥያቄ", "ja": "疑問詞", "lead": [
        "疑問詞は、答えの語が入る位置に置く(日本語と同じ)。"],
     "cols": ["日本語", "疑問詞", "例文", "意味"],
     "rows": [
         ["何", ("ምን", "mən", "ミン"), ("ይሄ ምንድን ነው?", "yəhe mənəddən näw?", "イヘ・ミニッディン・ネウ?"), "これは何ですか。"],
         ["誰", ("ማን", "man", "マン"), ("ስምህ ማን ነው?", "səməh man näw?", "スミフ・マン・ネウ?"), "お名前は?(男性へ)"],
         ["どこ", ("የት", "yät", "イェト"), ("ባንክ የት ነው?", "bank yät näw?", "バンク・イェト・ネウ?"), "銀行はどこですか。"],
         ["いつ", ("መቼ", "mäče", "メチェ"), ("መቼ ትሄዳለህ?", "mäče təhedalläh?", "メチェ・ティヘダッレフ?"), "いつ行くの?(男性へ)"],
         ["なぜ", ("ለምን", "lämən", "レミン"), ("ለምን?", "lämən?", "レミン?"), "なぜ?"],
         ["どう", ("እንዴት", "əndet", "インデト"), ("እንዴት ነህ?", "əndet näh?", "インデト・ネフ?"), "元気?(男性へ)"],
         ["いくつ・いくら", ("ስንት", "sənt", "シント"), ("ስንት ነው?", "sənt näw?", "シント・ネウ?"), "いくらですか。"],
         ["どれ", ("የትኛው", "yätəññaw", "イェティニャウ"), ("የትኛው ነው?", "yätəññaw näw?", "イェティニャウ・ネウ?"), "どれですか。"],
     ]},
    {"ge": "በ ከ ወደ ለ", "ja": "前置詞", "lead": [
        "前置詞は名詞の前に置く。1文字のものは名詞にくっつけて書く(በ + ቤት → በቤት)。",
        "「中」「上」は名詞の後ろに ውስጥ・ላይ を置いて組み合わせる: በቤት ውስጥ(ベベト・ウスト)= 家の中で。"],
     "cols": ["意味", "前置詞", "例", "例の意味"],
     "rows": [
         ["〜で・〜に(場所・手段)", ("በ-", "bä-", "ベ"), ("በአዲስ አበባ", "bä'addis abäba", "ベアディス・アベバ"), "アディスアベバで"],
         ["〜から", ("ከ-", "kä-", "ケ"), ("ከጃፓን ነኝ", "käǰapan näñ", "ケジャパン・ネニュ"), "日本から来ました(日本の出身です)"],
         ["〜へ", ("ወደ", "wädä", "ウェデ"), ("ወደ ገበያ", "wädä gäbäya", "ウェデ・ゲベヤ"), "市場へ"],
         ["〜のために・〜に", ("ለ-", "lä-", "レ"), ("ለእኔ", "lä'əne", "レイネ"), "私のために"],
         ["〜の", ("የ-", "yä-", "イェ"), ("የኢትዮጵያ ቡና", "yä'ityop̣p̣ya bunna", "イェイトッピヤ・ブンナ"), "エチオピアのコーヒー"],
         ["〜について", ("ስለ", "səlä", "スレ"), ("ስለ ኢትዮጵያ", "səlä ityop̣p̣ya", "スレ・イトッピヤ"), "エチオピアについて"],
     ]},
    {"ge": "ግስ", "ja": "動詞の活用(ፈለገ 欲しい)", "lead": [
        "動詞は主語によって前と後ろの語尾が変わる。例は ፈለገ(フェッレゲ = 欲しい・探す)。",
        "現在・未来は「前の語尾 + 語幹 + -አለ…」、過去は「語幹 + 後ろの語尾」、否定は「አ(ል)- + 語幹 + -ም」。",
        "目上の人への形は「彼ら」と同じ。過去の「私」は ፈለግሁ(フェッレグフ)とも言う。"],
     "cols": ["主語", "現在・未来(欲しい)", "過去(欲しかった)", "否定(欲しくない)"],
     "rows": [[p[0], p[5], p[6], p[7]] for p in PERSONS]},
    {"ge": "አልገባኝም", "ja": "覚えたフレーズを分解する", "lead": [
        "これまでのフレーズ集の決まり文句も、ここまでの規則でできている。"],
     "cols": ["フレーズ", "分解", "意味"],
     "rows": [
         [("ደህና ነኝ", "dähna näñ", "デフナ・ネニュ"), "ደህና(元気)+ ነኝ(私は〜です)", "元気です"],
         [("ስሜ ኬንጂ ነው", "səme kenǰi näw", "スメ・ケンジ・ネウ"), "ስም(名前)+ -ኤ(私の)/ ኬንጂ / ነው(〜です)", "私の名前はケンジです"],
         [("ስንት ነው?", "sənt näw?", "シント・ネウ?"), "ስንት(いくつ)+ ነው(〜です)", "いくらですか"],
         [("አልገባኝም", "algäbbaññəm", "アルゲバニム"), "አል-(否定)+ ገባ(入る・わかる)+ -ኝ(私に)+ -ም(否定)", "わかりません"],
         [("እፈልጋለሁ", "əfälləgallähu", "イフェッリガッレフ"), "እ-(私が)+ ፈልግ(欲しい)+ -አለሁ(現在)", "欲しいです"],
         [("ቀንስልኝ", "qänsəlləñ", "ケンスィッレニュ"), "ቀንስ(減らせ・男性へ)+ -ልኝ(私のために)", "まけてください"],
         [("ከባንኩ አጠገብ", "käbanku aṭägäb", "ケバンク・アテゲブ"), "ከ-(〜から)+ ባንክ + -ኡ(その)+ አጠገብ(隣)", "銀行の隣"],
     ]},
]

NOTES = [
    "アムハラ語は「あなた」「彼・彼女」で男女と目上を区別する。目上の人への形は「彼ら」(3人称複数)と同じ形を借りている。",
    "主語の代名詞は省くのが普通。動詞や「〜です」の形で主語がわかる(ደህና ነኝ だけで「私は元気です」)。",
    "この資料は入門用に形を1つに絞った。地域や話し手によって別の形(ነች と ናት、ፈለግኩ と ፈለግሁ など)も使われる。",
    "カタカナは目安。放出音(ጠ ጣ ቅ など)は日本語にない音なので、音源で確認すること。",
]

SOURCES = ("代名詞・所有の語尾・「〜です」と否定・指示詞・名詞の語尾・動詞の活用は Wikipedia「Amharic」の Grammar の節"
           "(同記事の表の誤植 አይደለህመ→አይደለህም、ትሰብራለችሁ→ትሰብራላችሁ、ይበሩ→ይስበሩ は正しい形に直して参照)、"
           "単語は Wiktionary(ተማሪ・ምን・መቼ・እንዴት・የትኛው・ከተማ・ጃፓን・ኢትዮጵያ・ልጅ ほか)をもとに作成(2026-10-27)。"
           "ፈለገ の活用は同記事の型(Type B)に当てはめて作り、ለምን・ስለ は辞書の見出しでは確認できなかった。")


def cell_html(c):
    if isinstance(c, tuple):
        ge, rom, kana = c
        return (f'<td><span class="gez">{esc(ge)}</span><span class="kt">{esc(kana)}</span>'
                f'<span class="rom">{esc(rom)}</span></td>')
    return f'<td class="ja">{ge_spans(c)}</td>'


def table_html(s):
    head = "".join(f"<th>{esc(c)}</th>" for c in s["cols"])
    body = "".join("<tr>" + "".join(cell_html(c) for c in r) + "</tr>" for r in s["rows"])
    return f'<table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>'


def lead_html(s):
    return '<ul class="lead">' + "".join(f"<li>{ge_spans(x)}</li>" for x in s["lead"]) + "</ul>"


def css(printable):
    base = g.css(printable)
    if printable:
        return base + """
  ul.lead { margin: 0; padding-left: 1.15em; font-size: 8.6pt; display: flex; flex-direction: column; gap: 2px; }
  td.ja { font-weight: 400; }
  td .kt { font-size: 8.6pt; }
  /* 表は行の途中でだけ改ページしない(build_greetings の tbody 指定を上書き) */
  tbody { break-inside: auto; }
  ul.lead { break-after: avoid; }
"""
    return base + """
  ul.lead { margin: 0; padding-left: 1.15em; font-size: 0.88rem; display: flex; flex-direction: column; gap: 4px; max-width: 75ch; }
  ul.lead .ge, td .ge { font-family: var(--f-ge); }
  .tbl { overflow-x: auto; border: 1px solid var(--border); border-radius: 6px; background: var(--surface); }
  .tbl table { border-collapse: collapse; width: 100%; min-width: 520px; }
  .tbl th, .tbl td { text-align: left; vertical-align: top; padding: 9px 14px; border-bottom: 1px solid var(--border); }
  .tbl tbody tr:last-child td { border-bottom: 0; }
  .tbl th { background: var(--surface-alt); font-size: 0.75rem; color: var(--ink-muted); letter-spacing: 0.05em; font-weight: 700; }
  .tbl td.ja { font-size: 0.88rem; }
  .tbl td .gez { font-family: var(--f-ge); font-size: 1.25rem; line-height: 1.35; display: block; }
  .tbl td .kt { color: var(--accent); font-size: 0.85rem; display: block; }
  .tbl td .rom { color: var(--ink-muted); font-size: 0.78rem; display: block; }

  .build { background: var(--surface); border: 1px solid var(--border); border-left: 4px solid var(--accent);
    border-radius: 6px; padding: 16px 20px; display: flex; flex-direction: column; gap: 12px; }
  .build .lbl { font-size: 0.78rem; font-weight: 700; color: var(--ink-muted); letter-spacing: 0.04em; }
  .chips { display: flex; flex-wrap: wrap; gap: 6px; }
  .chips button { font: inherit; font-size: 0.85rem; cursor: pointer; padding: 5px 11px; border-radius: 4px;
    border: 1px solid var(--border); background: var(--bg); color: var(--ink); }
  .chips button:hover { border-color: var(--accent-soft); }
  .chips button[aria-pressed="true"] { border-color: var(--accent); box-shadow: inset 0 0 0 1px var(--accent); }
  .chips button:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
  .chips button .ge { font-family: var(--f-ge); margin-left: 4px; }
  .sent { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 10px; }
  .sent > div { border-top: 1px dashed var(--border); padding-top: 8px; display: flex; flex-direction: column; gap: 1px; min-width: 0; }
  .sent .tag { font-size: 0.75rem; color: var(--ink-muted); font-weight: 700; }
  .sent .gez { font-family: var(--f-ge); font-size: 1.55rem; line-height: 1.35; overflow-wrap: anywhere; }
  .sent .gez b { color: var(--accent); font-weight: 600; }
  .sent .kt { color: var(--accent); font-size: 0.9rem; }
  .sent .rom { color: var(--ink-muted); font-size: 0.82rem; }
  .sent .tr { font-size: 0.88rem; }
"""


def head(printable):
    title = NAME + (" 印刷用" if printable else "")
    fonts = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
             '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
             '<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+Ethiopic:wght@400;600;700'
             '&family=Noto+Sans+JP:wght@400;500;700&family=Noto+Serif:ital,wght@0,400;1,400&display=swap" rel="stylesheet">')
    if printable:
        return (f'<!doctype html>\n<html lang="ja">\n<head>\n<meta charset="utf-8">\n<title>{title}</title>\n'
                f'{fonts}\n<style>{css(True)}</style>\n</head>\n<body>\n')
    return (f'<title>{title}</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n'
            f'{fonts}\n<style>{css(False)}</style>\n')


def masthead():
    return """  <header class="masthead">
    <div class="mark ge">ሰዋሰው</div>
    <div class="titles">
      <h1>アムハラ語 基礎文法</h1>
      <p>語順、人称代名詞、「〜です」、「ある・持っている」、名詞の語尾、「これ・あれ」、疑問詞、前置詞、動詞の活用。学習ロードマップ Step4 の「文法の骨格」を、フレーズ集の決まり文句とつなげてまとめた。</p>
    </div>
  </header>"""


def sec_h(ge, ja):
    return f'<h2 class="sec"><span class="ge">{esc(ge)}</span>{esc(ja)}</h2>'


def notes_html():
    items = "\n".join(f"      <li>{ge_spans(n)}</li>" for n in NOTES)
    return f'  <div class="notes">\n    <h3>覚えておくこと</h3>\n    <ul>\n{items}\n    </ul>\n  </div>'


def build_web():
    out = [head(False), '<div class="page">', masthead()]
    for i, s in enumerate(SECTIONS):
        out.append(f'  <section class="scene">{sec_h(s["ge"], s["ja"])}\n    {lead_html(s)}\n'
                   f'    <div class="tbl">{table_html(s)}</div>\n  </section>')
        if s["ge"] == "ነው":
            out.append(f"""  <section class="scene">{sec_h("እኔ … ነኝ", "主語を入れ替えて言ってみる")}
    <div class="build">
      <span class="lbl">主語</span><div class="chips" id="subj" role="group" aria-label="主語"></div>
      <span class="lbl">述語</span><div class="chips" id="pred" role="group" aria-label="述語"></div>
      <div class="sent" aria-live="polite">
        <div><span class="tag">〜です</span><span class="gez" id="s-ge"></span><span class="kt" id="s-kt"></span><span class="rom" id="s-rom"></span><span class="tr" id="s-ja"></span></div>
        <div><span class="tag">〜ではありません</span><span class="gez" id="n-ge"></span><span class="kt" id="n-kt"></span><span class="rom" id="n-rom"></span><span class="tr" id="n-ja"></span></div>
      </div>
    </div>
  </section>""")
    out.append(notes_html())
    out.append(f"  <footer>{ge_spans(SOURCES)}</footer>\n</div>")
    persons = [{"ja": p[0], "pro": p[1], "cop": p[2], "neg": p[3], "pl": p[0] in PLURAL_SUBJ} for p in PERSONS]
    preds = [{"ja": ja, "sg": sg, "pl": pl} for ja, sg, pl in PREDICATES]
    out.append(f"""<script>
  const PERSONS = {json.dumps(persons, ensure_ascii=False)};
  const PREDS = {json.dumps(preds, ensure_ascii=False)};
  const esc = s => String(s).replace(/[&<>"]/g, c => ({{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}}[c]));
  let si = 0, pi = 0;
  try {{
    const v = JSON.parse(localStorage.getItem("amh-gram-build") || "null");
    if (v && PERSONS[v[0]] && PREDS[v[1]]) [si, pi] = v;
  }} catch (e) {{}}
  const subjEl = document.getElementById("subj"), predEl = document.getElementById("pred");
  subjEl.innerHTML = PERSONS.map((p, i) => `<button type="button" data-i="${{i}}">${{esc(p.ja)}}<span class="ge">${{esc(p.pro[0])}}</span></button>`).join("");
  predEl.innerHTML = PREDS.map((p, i) => `<button type="button" data-i="${{i}}">${{esc(p.ja)}}<span class="ge">${{esc(p.sg[0])}}</span></button>`).join("");
  function set(id, v) {{ document.getElementById(id).textContent = v; }}
  function render() {{
    const s = PERSONS[si], p = PREDS[pi], w = s.pl ? p.pl : p.sg;
    document.getElementById("s-ge").innerHTML = `${{esc(s.pro[0])}} ${{esc(w[0])}} <b>${{esc(s.cop[0])}}</b>`;
    set("s-kt", `${{s.pro[2]}}・${{w[2]}}・${{s.cop[2]}}`);
    set("s-rom", `${{s.pro[1]}} ${{w[1]}} ${{s.cop[1]}}`);
    set("s-ja", `${{s.ja}}は${{p.ja}}です。`);
    document.getElementById("n-ge").innerHTML = `${{esc(s.pro[0])}} ${{esc(w[0])}} <b>${{esc(s.neg[0])}}</b>`;
    set("n-kt", `${{s.pro[2]}}・${{w[2]}}・${{s.neg[2]}}`);
    set("n-rom", `${{s.pro[1]}} ${{w[1]}} ${{s.neg[1]}}`);
    set("n-ja", `${{s.ja}}は${{p.ja}}ではありません。`);
    subjEl.querySelectorAll("button").forEach(b => b.setAttribute("aria-pressed", String(+b.dataset.i === si)));
    predEl.querySelectorAll("button").forEach(b => b.setAttribute("aria-pressed", String(+b.dataset.i === pi)));
    try {{ localStorage.setItem("amh-gram-build", JSON.stringify([si, pi])); }} catch (e) {{}}
  }}
  subjEl.addEventListener("click", e => {{ const b = e.target.closest("button"); if (b) {{ si = +b.dataset.i; render(); }} }});
  predEl.addEventListener("click", e => {{ const b = e.target.closest("button"); if (b) {{ pi = +b.dataset.i; render(); }} }});
  render();
</script>""")
    return "\n".join(out) + "\n"


def build_print():
    out = [head(True), '<div class="page">', masthead()]
    for s in SECTIONS:
        out.append(f'  <section>{sec_h(s["ge"], s["ja"])}{lead_html(s)}{table_html(s)}</section>')
    out.append(notes_html())
    out.append(f"  <footer>{ge_spans(SOURCES)}</footer>\n</div>\n</body>\n</html>")
    return "\n".join(out) + "\n"


def cell_md(c):
    return f"{c[0]}<br>{c[1]} / {c[2]}" if isinstance(c, tuple) else c


def build_md():
    md = [f"# {NAME}", "",
          "学習ロードマップ Step4「文法の骨格」のまとめ。アムハラ語のセルは フィデル / ローマ字 / カタカナ目安 の順。", ""]
    if WEB_URL:
        md += [f"Web版: {WEB_URL}(主語と述語を選んで「〜です」「〜ではありません」の文を作る練習つき)", ""]
    for s in SECTIONS:
        md += [f"## {s['ja']}({s['ge']})", ""] + [f"- {x}" for x in s["lead"]] + [""]
        md += ["| " + " | ".join(s["cols"]) + " |", "|" + "---|" * len(s["cols"])]
        md += ["| " + " | ".join(cell_md(c) for c in r) + " |" for r in s["rows"]]
        md.append("")
    md += ["## 覚えておくこと", ""] + [f"- {n}" for n in NOTES]
    md += ["", "---", f"出典: {SOURCES}", ""]
    return "\n".join(md)


if __name__ == "__main__":
    (ROOT / f"{NAME}.html").write_text(build_web(), encoding="utf-8")
    (ROOT / f"{NAME}-print.html").write_text(build_print(), encoding="utf-8")
    (ROOT / f"{NAME}.md").write_text(build_md(), encoding="utf-8")
    print("ok")
