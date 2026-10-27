"""アムハラ語の数字と買い物フレーズ集を生成する。

出力(アムハラ語フォルダ直下):
  アムハラ語数字と買い物フレーズ集.html        Web版(Artifact用。doctypeなしの断片)
  アムハラ語数字と買い物フレーズ集-print.html  印刷用(A4縦。Edgeヘッドレスで PDF 化)
  アムハラ語数字と買い物フレーズ集.md          テキスト版

見た目・相手別の4形・備考内のゲエズ文字の扱いは build_greetings.py と共通。
カタカナは学習用の目安(数字の読みは学習ロードマップの表記に合わせた)。
"""
import html
import json
from pathlib import Path

import build_greetings as g

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
NAME = "アムハラ語数字と買い物フレーズ集"
WEB_URL = "https://claude.ai/artifact/3mLJsShFPCZo2FcfhDRo2y"

esc, ge_spans, FORMS = g.esc, g.ge_spans, g.FORMS

# 数字: 値 -> (フィデル, ローマ字, カタカナ)
UNITS = {
    0: ("ዜሮ", "zero", "ゼロ"),
    1: ("አንድ", "and", "アンド"),
    2: ("ሁለት", "hulät", "フレト"),
    3: ("ሶስት", "sost", "ソスト"),
    4: ("አራት", "arat", "アラト"),
    5: ("አምስት", "amməst", "アムスト"),
    6: ("ስድስት", "sədəst", "シディスト"),
    7: ("ሰባት", "säbat", "セバト"),
    8: ("ስምንት", "səmmənt", "シミント"),
    9: ("ዘጠኝ", "zäṭäñ", "ゼテニュ"),
    10: ("አስር", "assər", "アスル"),
}
TEEN = ("አስራ", "asra", "アスラ")  # 11〜19 は アスラ+一の位
TENS = {
    20: ("ሀያ", "haya", "ハヤ"),
    30: ("ሰላሳ", "sälasa", "セラサ"),
    40: ("አርባ", "arba", "アルバ"),
    50: ("ሀምሳ", "hamsa", "ハムサ"),
    60: ("ስልሳ", "səlsa", "シルサ"),
    70: ("ሰባ", "säba", "セバ"),
    80: ("ሰማንያ", "sämanya", "セマニヤ"),
    90: ("ዘጠና", "zäṭäna", "ゼテナ"),
}
HUNDRED = ("መቶ", "mäto", "メト")
THOUSAND = ("ሺህ", "ših", "シフ")
MILLION = ("ሚሊዮን", "miliyon", "ミリヨン")

# 大きな数・組み立ての例(数字の読みはスクリプトで組み立てる)
BIG = [100, 200, 500, 1000, 2000, 10000, 100000, 1000000]
EXAMPLES = [(15, ""), (25, ""), (68, ""), (150, "150ブル。市場でよく聞く値段"),
            (250, ""), (1500, ""), (2019, "エチオピア暦の今年(2026年9月〜)"), (25000, "")]

# ゲエズ数字(エチオピア数字)。ゼロはない
GEEZ_DIGITS = "፩፪፫፬፭፮፯፰፱"
GEEZ_TENS = "፲፳፴፵፶፷፸፹፺"
GEEZ_HUNDRED, GEEZ_MYRIAD = "፻", "፼"


def words(n):
    """数を [(フィデル, ローマ字, カタカナ), ...] の語の並びにする(0〜9,999,999)。"""
    def below100(n):
        if n <= 10:
            return [UNITS[n]]
        if n < 20:
            return [TEEN, UNITS[n - 10]]
        t, u = divmod(n, 10)
        return [TENS[t * 10]] + ([UNITS[u]] if u else [])

    def below1000(n):
        h, r = divmod(n, 100)
        out = [] if h == 0 else [HUNDRED] if h == 1 else [UNITS[h], HUNDRED]
        return out + (below100(r) if r else [])

    if n == 0:
        return [UNITS[0]]
    m, rest = divmod(n, 1000000)
    t, r = divmod(rest, 1000)
    out = []
    if m:
        out += below1000(m) + [MILLION]
    if t:
        out += ([THOUSAND] if t == 1 else below1000(t) + [THOUSAND])
    if r:
        out += below1000(r)
    return out


def say(n):
    w = words(n)
    return " ".join(x[0] for x in w), " ".join(x[1] for x in w), "・".join(x[2] for x in w)


def geez(n):
    """1〜9999 をゲエズ数字にする。百の位の1は書かない(100 = ፻)。"""
    def pair(p):
        t, u = divmod(p, 10)
        return (GEEZ_TENS[t - 1] if t else "") + (GEEZ_DIGITS[u - 1] if u else "")
    hi, lo = divmod(n, 100)
    return ((pair(hi) if hi > 1 else "") + GEEZ_HUNDRED if hi else "") + pair(lo)


GEEZ_CHART = ([(GEEZ_DIGITS[i], i + 1) for i in range(9)] + [(GEEZ_TENS[i], (i + 1) * 10) for i in range(9)]
              + [(GEEZ_HUNDRED, 100), (GEEZ_MYRIAD, 10000)])
GEEZ_EXAMPLES = [(25, "二十+五"), (100, "百の位の1は書かない"), (110, "百+十"),
                 (2019, "二十 百 十九 = 20×100+19"), (10000, "万は ፼ 1字")]

MONEY = [
    ("ブル(エチオピアの通貨)", "ብር", "bərr", "ブル", "もとの意味は「銀」。"),
    ("サンティム(1ブルの100分の1)", "ሳንቲም", "santim", "サンティム", "「硬貨」の意味もある。"),
    ("50サンティム", "ሀምሳ ሳንቲም", "hamsa santim", "ハムサ・サンティム", ""),
    ("25ブル", "ሀያ አምስት ብር", "haya amməst bərr", "ハヤ・アムスト・ブル", "数のあとに ብር を置く。"),
    ("お金", "ገንዘብ", "gänzäb", "ゲンゼブ", ""),
    ("お釣り", "መልስ", "mäls", "メルス", "もとの意味は「答え・返事」。"),
    ("値段", "ዋጋ", "waga", "ワガ", ""),
]

# 買い物フレーズ。形式は build_greetings.py と同じ
SECTIONS = [
    {"ge": "ዋጋ", "ja": "値段を聞く", "phrases": [
        {"ja": "いくらですか", "ge": "ስንት ነው?", "rom": "sənt näw?", "kana": "シント・ネウ?",
         "note": "ስንት は「いくつ・いくら」。品物を指さしながら言えば通じる。"},
        {"ja": "これはいくらですか", "ge": "ይሄ ስንት ነው?", "rom": "yəhe sənt näw?", "kana": "イヘ・シント・ネウ?",
         "note": "ይሄ(イヘ)は「これ」。"},
        {"ja": "1キロいくらですか", "ge": "አንድ ኪሎ ስንት ነው?", "rom": "and kilo sənt näw?", "kana": "アンド・キロ・シント・ネウ?",
         "note": "野菜や果物は市場でキロ単位で売られる。ግማሽ ኪሎ(ギッマシュ・キロ)= 500グラム。"},
        {"ja": "〜ブルです", "ge": "… ብር ነው", "rom": "… bərr näw", "kana": "… ブル・ネウ",
         "note": "店の人の答え方。例: ሀምሳ ብር ነው(ハムサ・ブル・ネウ)= 50ブルです。"},
        {"ja": "いちばん安くていくらですか", "ge": "የመጨረሻ ዋጋ ስንት ነው?", "rom": "yämäčärräša waga sənt näw?",
         "kana": "イェメチェレシャ・ワガ・シント・ネウ?", "note": "直訳は「最後の値段はいくらですか」。"},
    ]},
    {"ge": "ድርድር", "ja": "値段の交渉", "phrases": [
        {"ja": "高いです", "ge": "ውድ ነው", "rom": "wədd näw", "kana": "ウッド・ネウ", "note": ""},
        {"ja": "高すぎます", "ge": "በጣም ውድ ነው", "rom": "bäṭam wədd näw", "kana": "ベタム・ウッド・ネウ",
         "note": "በጣም(ベタム)は「とても」。"},
        {"ja": "安いです", "ge": "ርካሽ ነው", "rom": "rəkaš näw", "kana": "ルカシュ・ネウ", "note": ""},
        {"ja": "まけてください", "forms": {
            "m": ("ቀንስልኝ", "qänsəlləñ", "ケンスィッレニュ"),
            "f": ("ቀንሺልኝ", "qänšilləñ", "ケンシッレニュ"),
            "p": ("ይቀንሱልኝ", "yəqänsulləñ", "イケンスッレニュ"),
            "pl": ("ቀንሱልኝ", "qänsulləñ", "ケンスッレニュ")},
         "note": "ቀነሰ(減らす)+ -ልኝ(私のために)。「私のために減らして」。"},
        {"ja": "〜ブルでどうですか", "ge": "በ… ብር ይሆናል?", "rom": "bä… bərr yəhonal?", "kana": "ベ… ブル・イホナル?",
         "note": "例: በስልሳ ብር ይሆናል?(ベシルサ・ブル・イホナル?)= 60ブルでどうですか。"},
        {"ja": "いいでしょう(決まり)", "ge": "እሺ፣ ይሁን", "rom": "əšši, yəhun", "kana": "イッシ、イフン",
         "note": "ይሁን は「そうなりますように」。値段が決まったときに。"},
    ]},
    {"ge": "መግዛት", "ja": "買う・頼む", "phrases": [
        {"ja": "〜はありますか", "ge": "… አለ?", "rom": "… allä?", "kana": "… アッレ?",
         "note": "例: ውሃ አለ?(ウィハ・アッレ?)= 水はありますか。答えは አለ(アッレ = ある)/ የለም(イェッレム = ない)。"},
        {"ja": "〜が欲しいです", "ge": "… እፈልጋለሁ", "rom": "… əfälləgallähu", "kana": "… イフェッリガッレフ",
         "note": "ፈለገ(欲しがる・探す)から。例: ቡና እፈልጋለሁ(ブンナ・イフェッリガッレフ)= コーヒーが欲しいです。"},
        {"ja": "これをください", "forms": {
            "m": ("ይሄን ስጠኝ", "yəhen səṭäñ", "イヘン・スィテニュ"),
            "f": ("ይሄን ስጪኝ", "yəhen səčiñ", "イヘン・スィチニュ"),
            "p": ("ይሄን ይስጡኝ", "yəhen yəsṭuñ", "イヘン・イストゥニュ"),
            "pl": ("ይሄን ስጡኝ", "yəhen səṭuñ", "イヘン・スィトゥニュ")},
         "note": "ይሄን を数や品物に替えれば「〜をください」。例: ሁለት ኪሎ ስጠኝ(フレト・キロ・スィテニュ)= 2キロください。"},
        {"ja": "見せてください", "forms": {
            "m": ("አሳየኝ", "asayäñ", "アサイェニュ"),
            "f": ("አሳዪኝ", "asayiñ", "アサイニュ"),
            "p": ("ያሳዩኝ", "yasayuñ", "ヤサユニュ"),
            "pl": ("አሳዩኝ", "asayuñ", "アサユニュ")},
         "note": "-ኝ(私に)。手に取って見たいときに。"},
        {"ja": "ちょっと待ってください", "forms": {
            "m": ("ትንሽ ቆይ", "tənnəš qoy", "ティンニシュ・コイ"),
            "f": ("ትንሽ ቆዪ", "tənnəš qoyi", "ティンニシュ・コイイ"),
            "p": ("ትንሽ ይቆዩ", "tənnəš yəqoyu", "ティンニシュ・イコユ"),
            "pl": ("ትንሽ ቆዩ", "tənnəš qoyu", "ティンニシュ・コユ")},
         "note": "ትንሽ(ティンニシュ)は「少し」。お金を数えるときなどに。"},
        {"ja": "いりません", "ge": "አልፈልግም", "rom": "alfälləgəm", "kana": "アルフェッリグム",
         "note": "「欲しくない」。አል- … -ም で否定(አልገባኝም と同じ形)。አመሰግናለሁ を添えるとやわらかい。"},
    ]},
]

# 品物の単語: (日本語, フィデル, ローマ字, カタカナ)
GOODS = [
    ("水", "ውሃ", "wəha", "ウィハ"),
    ("コーヒー", "ቡና", "bunna", "ブンナ"),
    ("お茶", "ሻይ", "šay", "シャイ"),
    ("牛乳", "ወተት", "wätät", "ウェテト"),
    ("パン", "ዳቦ", "dabo", "ダボ"),
    ("インジェラ", "እንጀራ", "ənǧära", "インジェラ"),
    ("卵", "እንቁላል", "ənqulal", "インクラル"),
    ("鶏肉", "ዶሮ", "doro", "ドロ"),
    ("肉", "ስጋ", "səga", "スガ"),
    ("バナナ", "ሙዝ", "muz", "ムズ"),
    ("オレンジ", "ብርቱካን", "bərtukan", "ブルトゥカン"),
    ("トマト", "ቲማቲም", "timatim", "ティマティム"),
    ("玉ねぎ", "ሽንኩርት", "šənkurt", "シンクルト"),
    ("市場", "ገበያ", "gäbäya", "ゲベヤ"),
    ("店", "ሱቅ", "suq", "スク"),
    ("大きい", "ትልቅ", "təlləq", "ティッリク"),
    ("小さい / 少し", "ትንሽ", "tənnəš", "ティンニシュ"),
    ("たくさん", "ብዙ", "bəzu", "ブズ"),
    ("半分", "ግማሽ", "gəmmaš", "ギッマシュ"),
    ("キロ", "ኪሎ", "kilo", "キロ"),
]

# 会話例: (話し手, フィデル, カタカナ, 日本語)
DIALOGUE = [
    ("A", "ይቅርታ፣ ሙዝ አለ?", "イキルタ、ムズ・アッレ?", "すみません、バナナはありますか。"),
    ("B", "አዎ፣ አለ።", "アウォ、アッレ。", "はい、あります。"),
    ("A", "አንድ ኪሎ ስንት ነው?", "アンド・キロ・シント・ネウ?", "1キロいくらですか。"),
    ("B", "ሰማንያ ብር ነው።", "セマニヤ・ブル・ネウ。", "80ブルです。"),
    ("A", "በጣም ውድ ነው! ቀንስልኝ።", "ベタム・ウッド・ネウ! ケンスィッレニュ。", "高すぎます! まけてください。"),
    ("B", "እሺ፣ ሰባ ብር።", "イッシ、セバ・ブル。", "わかりました、70ブル。"),
    ("A", "በስልሳ ብር ይሆናል?", "ベシルサ・ブル・イホナル?", "60ブルでどうですか。"),
    ("B", "እሺ፣ ይሁን።", "イッシ、イフン。", "いいでしょう。"),
    ("A", "ሁለት ኪሎ ስጠኝ።", "フレト・キロ・スィテニュ。", "2キロください。"),
    ("B", "መቶ ሀያ ብር ነው።", "メト・ハヤ・ブル・ネウ。", "120ブルです。"),
    ("A", "አመሰግናለሁ!", "アメセギナレフ!", "ありがとう!"),
]

ENDINGS = [
    ("男性へ", "−", "語尾なし", "ቀንስ · ስጥ"),
    ("女性へ", "-ኢ", "-i", "ቀንሺ · ስጪ"),
    ("目上の人へ", "ይ- … -ኡ", "yə- … -u", "ይቀንሱ · ይስጡ"),
    ("複数の人へ", "-ኡ", "-u", "ቀንሱ · ስጡ"),
]

RULES = [
    "11〜19 は アスラ(አስራ)のあとに一の位を置く: 11 = አስራ አንድ、15 = አስራ አምስት。",
    "21 以上は十の位と一の位を並べるだけ: 25 = ሀያ አምስት。日本語と同じ順で、「と」にあたる語は入らない。",
    "百・千は 100 = መቶ、200 = ሁለት መቶ のように前に数を置く。1 のときは数を付けない(アンド を付けて አንድ ሺህ とも言う)。",
    "1万は「10 千」= አስር ሺህ、10万は「100 千」= መቶ ሺህ。万の単位はなく、千で数える(英語と同じ)。",
]

NOTES = [
    "市場(ገበያ)や露店では値段の交渉が普通。最初の値段の半分〜7割くらいから始めて、笑顔で歩み寄る。スーパーや値札のある店では交渉しない。",
    "値段はアラビア数字(1, 2, 3…)で書かれる。ゲエズ数字は暦・教会・聖書の章や節の番号などで使い、ゼロはない。",
    "エチオピアの時刻は日の出(朝6時)から数える。1 ሰዓት(アンド・セアト)は午前7時、6 ሰዓት は正午。約束の時間はどちらの数え方か確かめる。",
    "「まけて」「ください」などの頼みごとは相手で形が変わる。迷ったら「目上の人へ」の形を選べば失礼にならない。",
    "カタカナは目安。放出音(ጠ ጣ ቅ など)は日本語にない音なので、音源で確認すること。",
]

SOURCES = ("数字・お金・時刻は Wikivoyage「Amharic phrasebook」、単語の綴りと意味は Wiktionary の各語の記事"
           "(ውድ・ብር・ሳንቲም・ቀነሰ・መልስ・ግማሽ・ፈለገ・ዋጋ・ገበያ・ሱቅ ほか)、ゲエズ数字は Unicode のエチオピア文字表をもとに作成"
           "(2026-10-27)。ርካሽ・ሚሊዮን と命令形(ስጠኝ・አሳየኝ・ቆይ)は辞書で直接確認できず、一般的な形と活用の規則から作成した。")


def css(printable):
    base = g.css(printable)
    if printable:
        return base + """
  .grid4 { display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px; }
  .rules { margin: 0; padding-left: 1.15em; font-size: 8.6pt; display: flex; flex-direction: column; gap: 3px; }
  .gzchart { display: grid; grid-template-columns: repeat(10, 1fr); gap: 4px; }
  .gzchart div { background: var(--surface); border: 1px solid var(--border); border-radius: 3px; text-align: center; padding: 3px 0; }
  .gzchart .g { font-family: var(--f-ge); font-size: 15pt; color: var(--accent); display: block; line-height: 1.3; }
  .gzchart .v { font-size: 8pt; color: var(--ink-muted); }
  td.num { font-family: var(--f-rom); font-weight: 700; text-align: right; }
  td .gzn { font-family: var(--f-ge); color: var(--accent); }
"""
    return base + """
  .lead { margin: 0; font-size: 0.88rem; max-width: 70ch; }
  .cards { display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 8px; }
  .card { background: var(--surface); border: 1px solid var(--border); border-radius: 6px; padding: 10px 14px;
    display: flex; flex-direction: column; gap: 1px; min-width: 0; }
  .card .n { font-family: var(--f-rom); font-weight: 700; font-size: 1.05rem; display: flex; justify-content: space-between; gap: 8px; }
  .card .n .gzn { font-family: var(--f-ge); color: var(--accent); font-weight: 400; }
  .card .gez { font-family: var(--f-ge); font-size: 1.35rem; line-height: 1.35; overflow-wrap: anywhere; }
  .card .kt { color: var(--accent); font-size: 0.88rem; }
  .card .rom { color: var(--ink-muted); font-size: 0.8rem; }
  .card .ja { font-weight: 700; font-size: 0.9rem; }
  .card .note { font-size: 0.78rem; color: var(--ink-muted); }
  .rules { margin: 0; padding-left: 1.15em; font-size: 0.88rem; display: flex; flex-direction: column; gap: 4px; max-width: 75ch; }

  .conv { background: var(--surface); border: 1px solid var(--border); border-left: 4px solid var(--accent);
    border-radius: 6px; padding: 16px 20px; display: flex; flex-direction: column; gap: 12px; }
  .conv label { font-weight: 700; font-size: 0.9rem; }
  .conv .row { display: flex; flex-wrap: wrap; gap: 8px; align-items: center; }
  .conv input { font: inherit; font-family: var(--f-rom); font-size: 1.15rem; width: 11em; max-width: 100%;
    padding: 6px 10px; border: 1px solid var(--border); border-radius: 4px; background: var(--bg); color: var(--ink); }
  .conv input:focus-visible, .conv button:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
  .conv button { font: inherit; font-size: 0.82rem; cursor: pointer; padding: 4px 10px; border-radius: 4px;
    border: 1px solid var(--border); background: var(--surface-alt); color: var(--ink); }
  .conv button:hover { border-color: var(--accent-soft); }
  .conv .out { display: flex; flex-direction: column; gap: 2px; min-height: 5.5em; }
  .conv .out .gez { font-family: var(--f-ge); font-size: 1.7rem; line-height: 1.35; overflow-wrap: anywhere; }
  .conv .out .kt { color: var(--accent); }
  .conv .out .rom { color: var(--ink-muted); font-size: 0.88rem; }
  .conv .out .gzline { font-size: 0.88rem; color: var(--ink-muted); }
  .conv .out .gzline b { font-family: var(--f-ge); font-size: 1.3rem; color: var(--accent); font-weight: 400; }
  .conv .err { color: var(--accent); font-size: 0.88rem; }

  .gzchart { display: grid; grid-template-columns: repeat(auto-fill, minmax(64px, 1fr)); gap: 6px; }
  .gzchart div { background: var(--surface); border: 1px solid var(--border); border-radius: 4px; text-align: center; padding: 6px 0; }
  .gzchart .g { font-family: var(--f-ge); font-size: 1.6rem; color: var(--accent); display: block; line-height: 1.3; }
  .gzchart .v { font-size: 0.8rem; color: var(--ink-muted); font-family: var(--f-rom); }
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
    <div class="mark ge">ገበያ</div>
    <div class="titles">
      <h1>アムハラ語 数字と買い物フレーズ集</h1>
      <p>0 から 百万までの数え方、ゲエズ数字、ブルとサンティム、市場で値段を聞いてまけてもらうまでのフレーズ。頼みごとは話しかける相手(男性・女性・目上・複数)で形が変わるので、その形も並べた。</p>
    </div>
  </header>"""


def sec_h(ge, ja, extra=""):
    return f'<h2 class="sec"><span class="ge">{esc(ge)}</span>{esc(ja)}{extra}</h2>'


def number_rows():
    """数字の各ブロック: (見出しge, 見出しja, [(値, 備考)])"""
    return [
        ("ቁጥሮች", "0〜10", [(n, "") for n in range(11)]),
        ("ከ11 እስከ 90", "11〜19 と 十の位", [(n, "") for n in (11, 12, 15, 19)] + [(n, "") for n in TENS]),
        ("ትላልቅ ቁጥሮች", "百・千・百万", [(n, "") for n in BIG]),
        ("ምሳሌ", "組み立ての例", EXAMPLES),
    ]


def gz_or_dash(n):
    return geez(n) if 1 <= n <= 9999 else ("፼" if n == 10000 else "")


def notes_html():
    items = "\n".join(f"      <li>{ge_spans(n)}</li>" for n in NOTES)
    return f'  <div class="notes">\n    <h3>使うときの注意</h3>\n    <ul>\n{items}\n    </ul>\n  </div>'


def rules_html():
    return '<ul class="rules">' + "".join(f"<li>{ge_spans(r)}</li>" for r in RULES) + "</ul>"


def build_web():
    out = [head(False), '<div class="page">', masthead()]
    blocks = number_rows()
    for i, (ge, ja, rows) in enumerate(blocks):
        cards = []
        for n, note in rows:
            fid, rom, kana = say(n)
            gz = gz_or_dash(n)
            cards.append(f'<div class="card"><span class="n">{n:,}<span class="gzn">{gz}</span></span>'
                         f'<span class="gez">{esc(fid)}</span><span class="kt">{esc(kana)}</span>'
                         f'<span class="rom">{esc(rom)}</span>'
                         + (f'<span class="note">{esc(note)}</span>' if note else "") + '</div>')
        lead = rules_html() if i == 1 else ""
        out.append(f'  <section class="scene">{sec_h(ge, ja)}\n    {lead}\n    <div class="cards">{"".join(cards)}</div>\n  </section>')

    out.append(f"""  <section class="scene">{sec_h("ቁጥር ቀይር", "数をアムハラ語にしてみる")}
    <div class="conv">
      <label for="num">0〜9,999,999 の数を入れる</label>
      <div class="row"><input id="num" type="number" inputmode="numeric" min="0" max="9999999" step="1" value="150">
        <span class="row" id="quick"></span></div>
      <div class="out" id="out" aria-live="polite"></div>
    </div>
  </section>""")

    chart = "".join(f'<div><span class="g">{c}</span><span class="v">{v:,}</span></div>' for c, v in GEEZ_CHART)
    exs = "".join(f'<div class="card"><span class="n">{n:,}<span class="gzn">{geez(n) if n < 10000 else GEEZ_MYRIAD}</span></span>'
                  f'<span class="note">{esc(note)}</span></div>' for n, note in GEEZ_EXAMPLES)
    out.append(f"""  <section class="scene">{sec_h("የግዕዝ ቁጥሮች", "ゲエズ数字")}
    <p class="lead">エチオピア独自の数字。1〜9、10〜90、100、10000 の20字を組み合わせる。ゼロはなく、暦・教会・聖書の章節番号などで使う(値段は 1, 2, 3… のアラビア数字)。</p>
    <div class="gzchart">{chart}</div>
    <div class="cards">{exs}</div>
  </section>""")

    money = "".join(f'<div class="card"><span class="ja">{esc(ja)}</span><span class="gez">{esc(ge)}</span>'
                    f'<span class="kt">{esc(kana)}</span><span class="rom">{esc(rom)}</span>'
                    + (f'<span class="note">{ge_spans(note)}</span>' if note else "") + '</div>'
                    for ja, ge, rom, kana, note in MONEY)
    out.append(f'  <section class="scene">{sec_h("ገንዘብ", "お金")}\n'
               '    <p class="lead">通貨はブル(ብር)。1ブル = 100サンティム(ሳንቲም)。</p>\n'
               f'    <div class="cards">{money}</div>\n  </section>')

    btns = "\n".join(
        f'      <button type="button" data-k="{k}" aria-pressed="{str(k == "m").lower()}">'
        f'<span class="lbl">{lbl}</span><span class="suf">{esc(e[1])}<span class="rom">{esc(e[2])}</span></span>'
        f'<span class="ex">{esc(e[3])}</span></button>'
        for (k, lbl), e in zip(FORMS, ENDINGS))
    out.append(f"""  <div class="ends-wrap">
    {sec_h("ለማን?", "頼みごとは相手で形が変わる")}
    <p>「まけて」「ください」のような頼みごと(命令形)は、相手によって語尾が変わる。下のボタンで相手を選ぶと、フレーズがその形に切り替わる。-ልኝ は「私のために」、-ኝ は「私に」。</p>
    <div class="ends" role="group" aria-label="話しかける相手">
{btns}
    </div>
  </div>
  <div id="list"></div>""")

    goods = "".join(f'<div class="card"><span class="ja">{esc(ja)}</span><span class="gez">{esc(ge)}</span>'
                    f'<span class="kt">{esc(kana)}</span><span class="rom">{esc(rom)}</span></div>'
                    for ja, ge, rom, kana in GOODS)
    out.append(f'  <section class="scene">{sec_h("ዕቃዎች", "品物と買い物の単語")}\n    <div class="cards">{goods}</div>\n  </section>')

    lines = "\n".join(
        f'      <div class="line"><span class="sp">{sp}</span><div><span class="gez">{esc(ge)}</span>'
        f'<span class="kt">{esc(kt)}</span><span class="tr">{esc(ja)}</span></div></div>'
        for sp, ge, kt, ja in DIALOGUE)
    out.append(f'  <section class="scene">{sec_h("በገበያ", "市場での会話の例", '<span class="rom" style="font-size:.8rem;color:var(--ink-muted)">A(客)が男性の店主 B に話しかける場面</span>')}\n'
               f'    <div class="dlg">\n{lines}\n    </div>\n  </section>')
    out.append(notes_html())
    out.append(f"  <footer>{ge_spans(SOURCES)}</footer>\n</div>")

    num = {"units": UNITS, "teen": TEEN, "tens": TENS, "hundred": HUNDRED, "thousand": THOUSAND,
           "million": MILLION, "gd": GEEZ_DIGITS, "gt": GEEZ_TENS}
    out.append(f"""<script>
  const SECTIONS = {json.dumps(SECTIONS, ensure_ascii=False)};
  const FORMS = {json.dumps(FORMS, ensure_ascii=False)};
  const NUM = {json.dumps(num, ensure_ascii=False)};
  const esc = s => String(s).replace(/[&<>"]/g, c => ({{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}}[c]));
  const geSpan = s => esc(s).replace(/([\\u1200-\\u139f\\u2d80-\\u2ddf]+(?:\\s[\\u1200-\\u139f]+)*)/g, '<span class="ge">$1</span>');

  // 数 → 語の並び(build_shopping.py の words() と同じ規則)
  function below100(n) {{
    if (n <= 10) return [NUM.units[n]];
    if (n < 20) return [NUM.teen, NUM.units[n - 10]];
    const u = n % 10;
    return [NUM.tens[n - u]].concat(u ? [NUM.units[u]] : []);
  }}
  function below1000(n) {{
    const h = Math.floor(n / 100), r = n % 100;
    const out = h === 0 ? [] : h === 1 ? [NUM.hundred] : [NUM.units[h], NUM.hundred];
    return out.concat(r ? below100(r) : []);
  }}
  function words(n) {{
    if (n === 0) return [NUM.units[0]];
    const m = Math.floor(n / 1e6), t = Math.floor(n / 1000) % 1000, r = n % 1000;
    let out = [];
    if (m) out = out.concat(below1000(m), [NUM.million]);
    if (t) out = out.concat(t === 1 ? [NUM.thousand] : below1000(t).concat([NUM.thousand]));
    if (r) out = out.concat(below1000(r));
    return out;
  }}
  function geez(n) {{
    const pair = p => (p >= 10 ? NUM.gt[Math.floor(p / 10) - 1] : "") + (p % 10 ? NUM.gd[p % 10 - 1] : "");
    const hi = Math.floor(n / 100), lo = n % 100;
    return (hi ? (hi > 1 ? pair(hi) : "") + "፻" : "") + pair(lo);
  }}
  const inp = document.getElementById("num"), outEl = document.getElementById("out");
  function convert() {{
    const v = inp.value.trim(), n = Number(v);
    if (v === "" || !Number.isInteger(n) || n < 0 || n > 9999999) {{
      outEl.innerHTML = '<span class="err">0〜9,999,999 の整数を入れてください。</span>'; return;
    }}
    const w = words(n);
    const gz = n >= 1 && n <= 9999 ? `ゲエズ数字 <b>${{geez(n)}}</b>` : n === 10000 ? "ゲエズ数字 <b>፼</b>"
      : n === 0 ? "ゲエズ数字にゼロはない" : "ゲエズ数字は 1〜9,999 まで表示";
    outEl.innerHTML = `<span class="gez">${{esc(w.map(x => x[0]).join(" "))}}</span>
      <span class="kt">${{esc(w.map(x => x[2]).join("・"))}}</span>
      <span class="rom">${{esc(w.map(x => x[1]).join(" "))}}</span><span class="gzline">${{gz}}</span>`;
  }}
  document.getElementById("quick").innerHTML = [25, 80, 120, 350, 1500, 2019, 10000]
    .map(n => `<button type="button" data-n="${{n}}">${{n.toLocaleString()}}</button>`).join("");
  document.getElementById("quick").addEventListener("click", e => {{
    const b = e.target.closest("button"); if (!b) return;
    inp.value = b.dataset.n; convert();
  }});
  inp.addEventListener("input", convert);
  convert();

  let who = "m";
  try {{ const v = localStorage.getItem("amh-shop-who"); if (v && FORMS.some(f => f[0] === v)) who = v; }} catch (e) {{}}
  function phrase(p) {{
    const label = Object.fromEntries(FORMS);
    let ge = p.ge, rom = p.rom, kana = p.kana, tag = "", others = "";
    if (p.forms) {{
      [ge, rom, kana] = p.forms[who];
      tag = `<span class="tag">${{label[who]}}</span>`;
      others = `<div class="others">${{FORMS.filter(f => f[0] !== who).map(f =>
        `<span>${{f[1]}} <b>${{esc(p.forms[f[0]][0])}}</b></span>`).join("")}}</div>`;
    }}
    return `<div class="ph"><div class="ja">${{esc(p.ja)}}${{tag ? "<br>" + tag : ""}}</div>
      <div class="body"><span class="gez">${{esc(ge)}}</span>
      <div><span class="kt">${{esc(kana)}}</span><span class="rom">${{esc(rom)}}</span></div>
      ${{p.note ? `<div class="note">${{geSpan(p.note)}}</div>` : ""}}${{others}}</div></div>`;
  }}
  function render() {{
    document.getElementById("list").innerHTML = SECTIONS.map(s =>
      `<section class="scene"><h2 class="sec"><span class="ge">${{esc(s.ge)}}</span>${{esc(s.ja)}}</h2>
       <div class="list">${{s.phrases.map(phrase).join("")}}</div></section>`).join("");
    document.querySelectorAll(".ends button").forEach(b => b.setAttribute("aria-pressed", String(b.dataset.k === who)));
  }}
  document.querySelectorAll(".ends button").forEach(b => b.addEventListener("click", () => {{
    who = b.dataset.k;
    try {{ localStorage.setItem("amh-shop-who", who); }} catch (e) {{}}
    render();
  }}));
  render();
</script>""")
    return "\n".join(out) + "\n"


def build_print():
    out = [head(True), '<div class="page">', masthead()]
    blocks = number_rows()
    tables = []
    for ge, ja, rows in blocks:
        trs = []
        for n, note in rows:
            fid, rom, kana = say(n)
            trs.append(f'<tr><td class="num">{n:,}</td><td><span class="gzn">{gz_or_dash(n)}</span></td>'
                       f'<td><span class="gez">{esc(fid)}</span></td>'
                       f'<td><span class="kt">{esc(kana)}</span><span class="rom">{esc(rom)}</span>'
                       + (f'<span class="rom">{esc(note)}</span>' if note else "") + '</td></tr>')
        tables.append(f'<section>{sec_h(ge, ja)}<table><colgroup><col style="width:17%"><col style="width:14%">'
                      '<col style="width:34%"><col></colgroup>'
                      '<thead><tr><th>数</th><th>ゲエズ数字</th><th>フィデル</th><th>読み方</th></tr></thead>'
                      f'<tbody>{"".join(trs)}</tbody></table></section>')
    out.append(f'  <div class="grid4">{tables[0]}{tables[1]}</div>')
    out.append(f'  <section>{sec_h("ሕግ", "数の作り方")}{rules_html()}</section>')
    out.append(f'  <div class="grid4">{tables[2]}{tables[3]}</div>')

    chart = "".join(f'<div><span class="g">{c}</span><span class="v">{v:,}</span></div>' for c, v in GEEZ_CHART)
    exs = "".join(f'<tr><td class="num">{n:,}</td><td><span class="gez">{geez(n) if n < 10000 else GEEZ_MYRIAD}</span></td>'
                  f'<td class="note">{esc(note)}</td></tr>' for n, note in GEEZ_EXAMPLES)
    out.append(f'  <section style="break-inside:avoid">{sec_h("የግዕዝ ቁጥሮች", "ゲエズ数字")}'
               '<p style="margin:0;font-size:8.6pt">1〜9、10〜90、100、10000 の20字を組み合わせる。ゼロはなく、暦・教会・聖書の章節番号などで使う(値段はアラビア数字)。</p>'
               f'<div class="gzchart">{chart}</div>'
               '<table><colgroup><col style="width:17%"><col style="width:20%"><col></colgroup>'
               f'<tbody>{exs}</tbody></table></section>')

    money = "".join(f'<tr><td class="ja">{esc(ja)}</td><td><span class="gez">{esc(ge)}</span></td>'
                    f'<td><span class="kt">{esc(kana)}</span><span class="rom">{esc(rom)}</span></td>'
                    f'<td class="note">{ge_spans(note)}</td></tr>' for ja, ge, rom, kana, note in MONEY)
    out.append(f'  <section style="break-inside:avoid">{sec_h("ገንዘብ", "お金(1ブル = 100サンティム)")}'
               '<table><colgroup><col style="width:24%"><col style="width:24%"><col style="width:28%"><col></colgroup>'
               '<thead><tr><th>日本語</th><th>フィデル</th><th>読み方</th><th>備考</th></tr></thead>'
               f'<tbody>{money}</tbody></table></section>')

    ends = "\n".join(
        f'<div><span class="lbl">{lbl}</span><span class="suf">{esc(e[1])}</span> '
        f'<span class="rom">{esc(e[2])}</span><span class="ex">{esc(e[3])}</span></div>'
        for (k, lbl), e in zip(FORMS, ENDINGS))
    out.append(f'  <section>{sec_h("ለማን?", "頼みごとは相手で形が変わる")}'
               '<p style="margin:0;font-size:8.6pt">命令形の語尾。-ልኝ は「私のために」、-ኝ は「私に」。</p>\n'
               f'  <div class="ends">\n{ends}\n  </div></section>')
    for s in SECTIONS:
        bodies = []
        for p in s["phrases"]:
            forms = [(lbl, *p["forms"][k]) for k, lbl in FORMS] if "forms" in p else [("", p["ge"], p["rom"], p["kana"])]
            span = f' rowspan="{len(forms)}"' if len(forms) > 1 else ""
            rows = []
            for i, (lbl, ge, rom, kana) in enumerate(forms):
                lead = (f'<td class="ja"{span}>{esc(p["ja"])}</td>' if i == 0 else "")
                tail = (f'<td class="note"{span}>{ge_spans(p["note"])}</td>' if i == 0 else "")
                rows.append(f'<tr>{lead}<td class="who">{lbl}</td><td><span class="gez">{esc(ge)}</span></td>'
                            f'<td><span class="kt">{esc(kana)}</span><span class="rom">{esc(rom)}</span></td>{tail}</tr>')
            bodies.append("<tbody>" + "".join(rows) + "</tbody>")
        out.append(f'  <section>{sec_h(s["ge"], s["ja"])}\n'
                   '  <table><colgroup><col style="width:16%"><col style="width:9%"><col style="width:25%">'
                   '<col style="width:28%"><col></colgroup>\n'
                   '  <thead><tr><th>日本語</th><th>相手</th><th>フィデル</th><th>読み方</th><th>備考</th></tr></thead>\n'
                   f'  {chr(10).join(bodies)}\n  </table></section>')

    half = (len(GOODS) + 1) // 2
    def goods_table(items):
        rows = "".join(f'<tr><td class="ja">{esc(ja)}</td><td><span class="gez">{esc(ge)}</span></td>'
                       f'<td><span class="kt">{esc(kana)}</span><span class="rom">{esc(rom)}</span></td></tr>'
                       for ja, ge, rom, kana in items)
        return ('<table><colgroup><col style="width:32%"><col style="width:30%"><col></colgroup>'
                f'<thead><tr><th>日本語</th><th>フィデル</th><th>読み方</th></tr></thead><tbody>{rows}</tbody></table>')
    out.append(f'  <section style="break-inside:avoid">{sec_h("ዕቃዎች", "品物と買い物の単語")}'
               f'<div class="grid4">{goods_table(GOODS[:half])}{goods_table(GOODS[half:])}</div></section>')

    rows = "\n".join(
        f'<tr><td style="width:2.2em;font-weight:700;color:var(--accent)">{sp}</td>'
        f'<td><span class="gez">{esc(ge)}</span><span class="kt">{esc(kt)}</span></td><td>{esc(ja)}</td></tr>'
        for sp, ge, kt, ja in DIALOGUE)
    out.append(f'  <section class="dlg">{sec_h("በገበያ", "市場での会話の例(A = 客、B = 男性の店主)")}\n'
               '  <table><colgroup><col style="width:2.2em"><col style="width:62%"><col></colgroup>'
               f'<tbody>\n{rows}\n</tbody></table></section>')
    out.append(notes_html())
    out.append(f"  <footer>{ge_spans(SOURCES)}</footer>\n</div>\n</body>\n</html>")
    return "\n".join(out) + "\n"


def build_md():
    md = [f"# {NAME}", "",
          "0 から百万までの数え方、ゲエズ数字、お金、市場での値段交渉のフレーズ。フィデル / ローマ字 / カタカナ読みの順。", ""]
    if WEB_URL:
        md += [f"Web版: {WEB_URL}(数を入れるとアムハラ語の読みとゲエズ数字を表示する変換つき)", ""]
    for ge, ja, rows in number_rows():
        md += [f"## {ja}({ge})", "", "| 数 | ゲエズ数字 | フィデル | ローマ字 | カタカナ目安 |", "|---|---|---|---|---|"]
        for n, note in rows:
            fid, rom, kana = say(n)
            md.append(f"| {n:,} | {gz_or_dash(n)} | {fid} | {rom} | {kana}{'(' + note + ')' if note else ''} |")
        md.append("")
        if ja.startswith("11"):
            md += ["### 数の作り方", ""] + [f"- {r}" for r in RULES] + [""]
    md += ["## ゲエズ数字(የግዕዝ ቁጥሮች)", "",
           "1〜9、10〜90、100、10000 の20字を組み合わせる。ゼロはなく、暦・教会・聖書の章節番号などで使う(値段はアラビア数字)。", "",
           "| " + " | ".join(c for c, v in GEEZ_CHART) + " |", "|" + "---|" * len(GEEZ_CHART),
           "| " + " | ".join(f"{v:,}" for c, v in GEEZ_CHART) + " |", "", "| 数 | ゲエズ数字 | 説明 |", "|---|---|---|"]
    md += [f"| {n:,} | {geez(n) if n < 10000 else GEEZ_MYRIAD} | {note} |" for n, note in GEEZ_EXAMPLES]
    md += ["", "## お金(ገንዘብ)", "", "1ブル = 100サンティム。", "",
           "| 日本語 | フィデル | ローマ字 | カタカナ目安 | 備考 |", "|---|---|---|---|---|"]
    md += [f"| {ja} | {ge} | {rom} | {kana} | {note} |" for ja, ge, rom, kana, note in MONEY]
    md += ["", "## 頼みごとは相手で形が変わる", "", "命令形の語尾。-ልኝ は「私のために」、-ኝ は「私に」。", "",
           "| 相手 | 語尾 | ローマ字 | 例 |", "|---|---|---|---|"]
    md += [f"| {lbl} | {e[1]} | {e[2]} | {e[3]} |" for (k, lbl), e in zip(FORMS, ENDINGS)]
    for s in SECTIONS:
        md += ["", f"## {s['ja']}({s['ge']})", "",
               "| 日本語 | フィデル | ローマ字 | カタカナ目安 | 備考 |", "|---|---|---|---|---|"]
        for p in s["phrases"]:
            if "forms" in p:
                for i, (k, lbl) in enumerate(FORMS):
                    ge, rom, kana = p["forms"][k]
                    md.append(f"| {p['ja']}({lbl}) | {ge} | {rom} | {kana} | {p['note'] if i == 0 else ''} |")
            else:
                md.append(f"| {p['ja']} | {p['ge']} | {p['rom']} | {p['kana']} | {p['note']} |")
    md += ["", "## 品物と買い物の単語(ዕቃዎች)", "", "| 日本語 | フィデル | ローマ字 | カタカナ目安 |", "|---|---|---|---|"]
    md += [f"| {ja} | {ge} | {rom} | {kana} |" for ja, ge, rom, kana in GOODS]
    md += ["", "## 市場での会話の例(A = 客、B = 男性の店主)", ""]
    md += [f"- **{sp}**: {ge}  \n  {kt} — {ja}" for sp, ge, kt, ja in DIALOGUE]
    md += ["", "## 使うときの注意", ""] + [f"- {n}" for n in NOTES]
    md += ["", "---", f"出典: {SOURCES}", ""]
    return "\n".join(md)


if __name__ == "__main__":
    (ROOT / f"{NAME}.html").write_text(build_web(), encoding="utf-8")
    (ROOT / f"{NAME}-print.html").write_text(build_print(), encoding="utf-8")
    (ROOT / f"{NAME}.md").write_text(build_md(), encoding="utf-8")
    print("ok")
