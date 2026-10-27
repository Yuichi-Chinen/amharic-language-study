"""アムハラ語の道案内フレーズ集を生成する。

出力(アムハラ語フォルダ直下):
  アムハラ語道案内フレーズ集.html        Web版(Artifact用。doctypeなしの断片)
  アムハラ語道案内フレーズ集-print.html  印刷用(A4縦。Edgeヘッドレスで PDF 化)
  アムハラ語道案内フレーズ集.md          テキスト版

見た目・相手別の4形・備考内のゲエズ文字の扱いは build_greetings.py と共通。
"""
import json
from pathlib import Path

import build_greetings as g

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
NAME = "アムハラ語道案内フレーズ集"
WEB_URL = "https://claude.ai/artifact/Md97yqAHnYG8rX1SHwssBa"

esc, ge_spans, FORMS = g.esc, g.ge_spans, g.FORMS

# 道順の指示(相手別の4形)。クイズでも使う
TURN_RIGHT = {"m": ("ወደ ቀኝ ታጠፍ", "wädä qäñ taṭäf", "ウェデ・ケニュ・タテフ"),
              "f": ("ወደ ቀኝ ታጠፊ", "wädä qäñ taṭäfi", "ウェデ・ケニュ・タテフィ"),
              "p": ("ወደ ቀኝ ይታጠፉ", "wädä qäñ yətaṭäfu", "ウェデ・ケニュ・イタテフ"),
              "pl": ("ወደ ቀኝ ታጠፉ", "wädä qäñ taṭäfu", "ウェデ・ケニュ・タテフ")}
TURN_LEFT = {"m": ("ወደ ግራ ታጠፍ", "wädä gəra taṭäf", "ウェデ・グラ・タテフ"),
             "f": ("ወደ ግራ ታጠፊ", "wädä gəra taṭäfi", "ウェデ・グラ・タテフィ"),
             "p": ("ወደ ግራ ይታጠፉ", "wädä gəra yətaṭäfu", "ウェデ・グラ・イタテフ"),
             "pl": ("ወደ ግራ ታጠፉ", "wädä gəra taṭäfu", "ウェデ・グラ・タテフ")}
GO_STRAIGHT = {"m": ("ቀጥታ ሂድ", "qäṭṭəta hid", "ケッティタ・ヒド"),
               "f": ("ቀጥታ ሂጂ", "qäṭṭəta hiǧi", "ケッティタ・ヒジ"),
               "p": ("ቀጥታ ይሂዱ", "qäṭṭəta yəhidu", "ケッティタ・イヒドゥ"),
               "pl": ("ቀጥታ ሂዱ", "qäṭṭəta hidu", "ケッティタ・ヒドゥ")}
STOP_HERE = {"m": ("እዚህ ቁም", "əzzih qum", "イッズィフ・クム"),
             "f": ("እዚህ ቁሚ", "əzzih qumi", "イッズィフ・クミ"),
             "p": ("እዚህ ይቁሙ", "əzzih yəqumu", "イッズィフ・イクム"),
             "pl": ("እዚህ ቁሙ", "əzzih qumu", "イッズィフ・クム")}
GO_BACK = {"m": ("ተመለስ", "tämäläs", "テメレス"),
           "f": ("ተመለሺ", "tämäläši", "テメレシ"),
           "p": ("ይመለሱ", "yəmmäläsu", "イメッレス"),
           "pl": ("ተመለሱ", "tämäläsu", "テメレス")}

SECTIONS = [
    {"ge": "የት ነው?", "ja": "場所を尋ねる", "phrases": [
        {"ja": "〜はどこですか", "ge": "… የት ነው?", "rom": "… yät näw?", "kana": "… イェト・ネウ?",
         "note": "የት は「どこ」。例: ባንክ የት ነው?(バンク・イェト・ネウ?)= 銀行はどこですか。"},
        {"ja": "トイレはどこですか", "ge": "መታጠቢያ ቤት የት ነው?", "rom": "mätaṭäbiya bet yät näw?",
         "kana": "メタテビヤ・ベト・イェト・ネウ?", "note": "ሽንት ቤት(シント・ベト)とも言う。"},
        {"ja": "遠いですか", "ge": "ሩቅ ነው?", "rom": "ruq näw?", "kana": "ルク・ネウ?",
         "note": "答えは ሩቅ ነው(遠い)/ ቅርብ ነው(クルブ・ネウ = 近い)。"},
        {"ja": "何分かかりますか", "ge": "ስንት ደቂቃ ይወስዳል?", "rom": "sənt däqiqa yəwäsdal?",
         "kana": "シント・デキカ・イウェスダル?", "note": "ደቂቃ は「分」。答えの例: አምስት ደቂቃ(アムスト・デキカ)= 5分。"},
        {"ja": "歩いて行けますか", "ge": "በእግር መሄድ ይቻላል?", "rom": "bä'əgər mähed yəččalal?",
         "kana": "ベイグル・メヘド・イッチャラル?", "note": "በእግር は「足で・歩いて」。"},
        {"ja": "地図で教えてください", "forms": {
            "m": ("ካርታ ላይ አሳየኝ", "karta lay asayäñ", "カルタ・ライ・アサイェニュ"),
            "f": ("ካርታ ላይ አሳዪኝ", "karta lay asayiñ", "カルタ・ライ・アサイニュ"),
            "p": ("ካርታ ላይ ያሳዩኝ", "karta lay yasayuñ", "カルタ・ライ・ヤサユニュ"),
            "pl": ("ካርታ ላይ አሳዩኝ", "karta lay asayuñ", "カルタ・ライ・アサユニュ")},
         "note": "直訳は「地図の上で見せて」。スマートフォンの地図を見せながら。"},
        {"ja": "道に迷いました", "ge": "ጠፋሁ", "rom": "ṭäffahu", "kana": "テッファフ",
         "note": "ጠፋ(なくなる・迷う)から。「私は迷った」。"},
    ]},
    {"ge": "አቅጣጫ", "ja": "道順の指示", "phrases": [
        {"ja": "右に曲がって", "forms": TURN_RIGHT,
         "note": "ወደ は「〜へ」、ቀኝ は「右」。Wikivoyage では目上の人にも複数形の ታጠፉ を使っている。"},
        {"ja": "左に曲がって", "forms": TURN_LEFT, "note": "ግራ は「左」。"},
        {"ja": "まっすぐ行って", "forms": GO_STRAIGHT, "note": "ቀጥታ は「まっすぐ」。ሂድ は「行け」。"},
        {"ja": "戻って", "forms": GO_BACK, "note": "行き過ぎたときに言われる。"},
        {"ja": "それから", "ge": "ከዚያ", "rom": "käzziya", "kana": "ケッズィヤ",
         "note": "道順をつなぐ。例: ቀጥታ ሂድ፣ ከዚያ ወደ ግራ ታጠፍ = まっすぐ行って、それから左に曲がって。"},
    ]},
    {"ge": "ቦታ", "ja": "位置の言い方", "phrases": [
        {"ja": "〜の隣です", "ge": "ከ… አጠገብ ነው", "rom": "kä… aṭägäb näw", "kana": "ケ… アテゲブ・ネウ",
         "note": "例: ከባንኩ አጠገብ ነው(ケバンク・アテゲブ・ネウ)= 銀行の隣です。語尾の -ኡ は「その」。"},
        {"ja": "〜の向かいです", "ge": "ከ… ፊት ለፊት ነው", "rom": "kä… fit läfit näw", "kana": "ケ… フィト・レフィト・ネウ",
         "note": "ፊት ለፊት は直訳で「顔と顔」。"},
        {"ja": "〜の後ろです", "ge": "ከ… ኋላ ነው", "rom": "kä… hwala näw", "kana": "ケ… フワラ・ネウ", "note": ""},
        {"ja": "右側です", "ge": "በቀኝ በኩል ነው", "rom": "bäqäñ bäkkul näw", "kana": "ベケニュ・ベックル・ネウ",
         "note": "左側は በግራ በኩል(ベグラ・ベックル)。"},
        {"ja": "ここです", "ge": "እዚህ ነው", "rom": "əzzih näw", "kana": "イッズィフ・ネウ", "note": ""},
        {"ja": "あそこです", "ge": "እዚያ ነው", "rom": "əzziya näw", "kana": "イッズィヤ・ネウ", "note": ""},
    ]},
    {"ge": "ታክሲ እና አውቶቢስ", "ja": "タクシー・バスに乗る", "phrases": [
        {"ja": "〜までいくらですか", "ge": "ወደ … ስንት ነው?", "rom": "wädä … sənt näw?", "kana": "ウェデ … シント・ネウ?",
         "note": "例: ወደ ቦሌ ስንት ነው?(ウェデ・ボレ・シント・ネウ?)= ボレまでいくら? タクシーは乗る前に値段を決める。"},
        {"ja": "〜まで行ってください", "forms": {
            "m": ("ወደ … ውሰደኝ", "wädä … wəsädäñ", "ウェデ … ウセデニュ"),
            "f": ("ወደ … ውሰጂኝ", "wädä … wəsäǧiñ", "ウェデ … ウセジニュ"),
            "p": ("ወደ … ይውሰዱኝ", "wädä … yəwsäduñ", "ウェデ … イウセドゥニュ"),
            "pl": ("ወደ … ውሰዱኝ", "wädä … wəsäduñ", "ウェデ … ウセドゥニュ")},
         "note": "直訳は「〜へ私を連れて行って」。"},
        {"ja": "このバスは〜へ行きますか", "ge": "ይሄ አውቶቢስ ወደ … ይሄዳል?", "rom": "yəhe awtobis wädä … yəhedal?",
         "kana": "イヘ・アウトビス・ウェデ … イヘダル?", "note": "ミニバスなら አውቶቢስ を ሚኒባስ(ミニバス)に。"},
        {"ja": "ここで止めてください", "forms": STOP_HERE, "note": "ቁም は「止まれ・立て」。"},
        {"ja": "降ります!", "ge": "ወራጅ አለ!", "rom": "wärraǧ allä!", "kana": "ウェッラジ・アッレ!",
         "note": "直訳は「降りる人がいます」。ミニバスで降りたいときの決まり文句。"},
    ]},
]

# 単語: (グループ見出しge, 見出しja, [(日本語, フィデル, ローマ字, カタカナ)])
WORDS = [
    ("አቅጣጫ", "方向・位置", [
        ("右", "ቀኝ", "qäñ", "ケニュ"), ("左", "ግራ", "gəra", "グラ"), ("まっすぐ", "ቀጥታ", "qäṭṭəta", "ケッティタ"),
        ("前・顔", "ፊት", "fit", "フィト"), ("後ろ", "ኋላ", "hwala", "フワラ"), ("隣・そば", "አጠገብ", "aṭägäb", "アテゲブ"),
        ("横", "ጎን", "gon", "ゴン"), ("向かい", "ፊት ለፊት", "fit läfit", "フィト・レフィト"),
        ("中", "ውስጥ", "wəsṭ", "ウスト"), ("外", "ውጭ", "wəčč", "ウッチ"), ("上", "ላይ", "lay", "ライ"),
        ("ここ", "እዚህ", "əzzih", "イッズィフ"), ("あそこ", "እዚያ", "əzziya", "イッズィヤ"),
        ("近い", "ቅርብ", "qərb", "クルブ"), ("遠い", "ሩቅ", "ruq", "ルク"),
        ("北", "ሰሜን", "sämen", "セメン"), ("南", "ደቡብ", "däbub", "デブブ"),
        ("東", "ምሥራቅ", "məsraq", "ムスラク"), ("西", "ምዕራብ", "məʿrab", "ムウラブ"),
    ]),
    ("ቦታዎች", "場所", [
        ("道", "መንገድ", "mängäd", "メンゲド"), ("銀行", "ባንክ", "bank", "バンク"),
        ("郵便局", "ፖስታ ቤት", "posta bet", "ポスタ・ベト"), ("ホテル", "ሆቴል", "hotel", "ホテル"),
        ("病院", "ሆስፒታል", "hospital", "ホスピタル"), ("レストラン", "ምግብ ቤት", "məgəb bet", "ミグブ・ベト"),
        ("教会", "ቤተ ክርስቲያን", "betä krəstiyan", "ベテ・クリスティヤン"), ("モスク", "መስጊድ", "mäsgid", "メスギド"),
        ("市場", "ገበያ", "gäbäya", "ゲベヤ"), ("トイレ", "ሽንት ቤት", "šənt bet", "シント・ベト"),
        ("空港", "አየር ማረፊያ", "ayär märäfiya", "アイェル・メレフィヤ"), ("広場・ロータリー", "አደባባይ", "addäbabay", "アッデババイ"),
        ("橋", "ድልድይ", "dəldəy", "ドゥルドゥイ"), ("駅・乗り場", "ጣቢያ", "ṭabiya", "タビヤ"),
    ]),
    ("መጓጓዣ", "乗り物・時間", [
        ("車", "መኪና", "mäkina", "メキナ"), ("タクシー", "ታክሲ", "taksi", "タクスィ"),
        ("バス", "አውቶቢስ", "awtobis", "アウトビス"), ("ミニバス", "ሚኒባስ", "minibas", "ミニバス"),
        ("電車", "ባቡር", "babur", "バブル"), ("三輪タクシー", "ባጃጅ", "baǧaǧ", "バジャジ"),
        ("地図", "ካርታ", "karta", "カルタ"), ("分", "ደቂቃ", "däqiqa", "デキカ"),
        ("時間・時計", "ሰዓት", "säʿat", "セアト"), ("歩いて", "በእግር", "bä'əgər", "ベイグル"),
    ]),
]

# クイズ: 道順の指示を聞いて方向を選ぶ
QUIZ = [("right", TURN_RIGHT, "右に曲がって"), ("left", TURN_LEFT, "左に曲がって"),
        ("straight", GO_STRAIGHT, "まっすぐ行って"), ("stop", STOP_HERE, "ここで止めて"),
        ("back", GO_BACK, "戻って")]
QUIZ_BUTTONS = [("left", "←", "左へ"), ("straight", "↑", "まっすぐ"), ("right", "→", "右へ"),
                ("back", "↓", "戻る"), ("stop", "■", "止まる")]

# 会話例: (話し手, フィデル, カタカナ, 日本語)
DIALOGUE = [
    ("A", "ይቅርታ፣ ቤተ ክርስቲያን የት ነው?", "イキルタ、ベテ・クリスティヤン・イェト・ネウ?", "すみません、教会はどこですか。"),
    ("B", "ቀጥታ ሂድ፣ ከዚያ ወደ ግራ ታጠፍ።", "ケッティタ・ヒド、ケッズィヤ・ウェデ・グラ・タテフ。", "まっすぐ行って、それから左に曲がって。"),
    ("A", "ሩቅ ነው?", "ルク・ネウ?", "遠いですか。"),
    ("B", "አይ፣ ቅርብ ነው። አምስት ደቂቃ።", "アイ、クルブ・ネウ。アムスト・デキカ。", "いいえ、近いです。5分です。"),
    ("B", "ከባንኩ ፊት ለፊት ነው።", "ケバンク・フィト・レフィト・ネウ。", "銀行の向かいです。"),
    ("A", "አመሰግናለሁ!", "アメセギナレフ!", "ありがとう!"),
    ("A", "ወደ ቦሌ ስንት ነው?", "ウェデ・ボレ・シント・ネウ?", "(タクシーで)ボレまでいくらですか。"),
    ("C", "ሶስት መቶ ብር።", "ソスト・メト・ブル。", "300ブル。"),
    ("A", "በጣም ውድ ነው። ሁለት መቶ ይሆናል?", "ベタム・ウッド・ネウ。フレト・メト・イホナル?", "高すぎます。200でどうですか。"),
    ("C", "እሺ፣ ግባ።", "イッシ、ギバ。", "いいよ、乗って。"),
    ("A", "እዚህ ቁም። አመሰግናለሁ!", "イッズィフ・クム。アメセギナレフ!", "ここで止めてください。ありがとう!"),
]

ENDINGS = [
    ("男性へ", "−", "語尾なし", "ታጠፍ · ሂድ"),
    ("女性へ", "-ኢ", "-i", "ታጠፊ · ሂጂ"),
    ("目上の人へ", "ይ- … -ኡ", "yə- … -u", "ይታጠፉ · ይሂዱ"),
    ("複数の人へ", "-ኡ", "-u", "ታጠፉ · ሂዱ"),
]

NOTES = [
    "エチオピアでは住所より目印で道を説明するのが普通。「〜の隣」「〜の向かい」と、銀行・教会・広場(አደባባይ)などの目印を組み合わせて覚える。",
    "道順の指示は命令形なので、教えてくれる人は自分(旅行者)に合わせた形で言う。男性の旅行者には ታጠፍ、女性の旅行者には ታጠፊ が聞こえてくる。",
    "タクシーにはメーターがないことが多い。乗る前に行き先と値段を決める(値段交渉は「数字と買い物フレーズ集」を参照)。",
    "ミニバスは呼び込みの係が行き先を叫んでいる。乗る前に行き先を確かめ、降りるときは ወራጅ አለ と声をかける。",
    "ボレ(ቦሌ)はアディスアベバの空港がある地区。地名は ወደ … の … に入れればよい。",
    "カタカナは目安。放出音(ጠ ጣ ቅ など)は日本語にない音なので、音源で確認すること。",
]

SOURCES = ("方向・「曲がる」の命令形・乗り物の名前は Wikivoyage「Amharic phrasebook」、単語の綴りと意味は Wiktionary の各語の記事"
           "(የት・ሩቅ・መንገድ・ጎዳና・ካርታ・ፊት・ላይ・ውስጥ・ውጭ・ግራ・ቀጥታ・ሰሜን・ደቡብ・ምዕራብ・ባንክ・ፖስታ ቤት・ሆስፒታል・መስጊድ・ምግብ ቤት・ድልድይ・መኪና・ደቂቃ・ሰዓት・ወረደ・ጠፋ ほか)"
           "をもとに作成(2026-10-27)。ቅርብ・ኋላ・እዚህ・እዚያ・ምሥራቅ・ሆቴል・ቤተ ክርስቲያን・አየር ማረፊያ・አደባባይ・ጣቢያ・ሚኒባስ・ባጃጅ、"
           "命令形(ሂድ・ቁም・ተመለስ・ውሰደኝ)と ወራጅ አለ は辞書で直接確認できず、一般的な形と活用の規則から作成した。")


def css(printable):
    base = g.css(printable)
    if printable:
        return base + """
  .grid2 { display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px; align-items: start; }
"""
    return base + """
  .lead { margin: 0; font-size: 0.88rem; max-width: 70ch; }
  .cards { display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 8px; }
  .card { background: var(--surface); border: 1px solid var(--border); border-radius: 6px; padding: 10px 14px;
    display: flex; flex-direction: column; gap: 1px; min-width: 0; }
  .card .ja { font-weight: 700; font-size: 0.9rem; }
  .card .gez { font-family: var(--f-ge); font-size: 1.35rem; line-height: 1.35; overflow-wrap: anywhere; }
  .card .kt { color: var(--accent); font-size: 0.88rem; }
  .card .rom { color: var(--ink-muted); font-size: 0.8rem; }
  h3.grp { margin: 6px 0 0; font-size: 0.95rem; display: flex; gap: 10px; align-items: baseline; }
  h3.grp .ge { color: var(--accent); font-size: 1.15rem; }

  .quiz { background: var(--surface); border: 1px solid var(--border); border-left: 4px solid var(--accent);
    border-radius: 6px; padding: 16px 20px; display: flex; flex-direction: column; gap: 14px; }
  .quiz .q { display: flex; flex-direction: column; gap: 2px; min-height: 4.6em; }
  .quiz .q .gez { font-family: var(--f-ge); font-size: 1.9rem; line-height: 1.35; }
  .quiz .q .who { font-size: 0.8rem; color: var(--ink-muted); }
  .quiz .btns { display: grid; grid-template-columns: repeat(5, minmax(0, 1fr)); gap: 8px; max-width: 520px; }
  .quiz .btns button { font: inherit; cursor: pointer; padding: 8px 4px; border-radius: 4px; color: var(--ink);
    border: 1px solid var(--border); background: var(--bg); display: flex; flex-direction: column; align-items: center; gap: 0; }
  .quiz .btns button .ar { font-size: 1.4rem; line-height: 1.2; }
  .quiz .btns button .lb { font-size: 0.75rem; color: var(--ink-muted); }
  .quiz .btns button:hover { border-color: var(--accent-soft); }
  .quiz button:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
  .quiz .btns button.ok { border-color: var(--accent); box-shadow: inset 0 0 0 1px var(--accent); }
  .quiz .btns button.ng { opacity: 0.45; }
  .quiz .res { font-size: 0.9rem; min-height: 3.2em; }
  .quiz .res .kt { color: var(--accent); }
  .quiz .bar { display: flex; flex-wrap: wrap; gap: 8px 16px; align-items: center; font-size: 0.85rem; color: var(--ink-muted); }
  .quiz .next { font: inherit; font-size: 0.85rem; cursor: pointer; padding: 5px 14px; border-radius: 4px;
    border: 1px solid var(--accent); background: var(--accent); color: var(--surface); }
  @media (max-width: 420px) { .quiz .btns { grid-template-columns: repeat(3, minmax(0, 1fr)); } }
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
    <div class="mark ge">አቅጣጫ</div>
    <div class="titles">
      <h1>アムハラ語 道案内フレーズ集</h1>
      <p>場所を尋ねる、道順を聞き取る、目印で位置を言う、タクシーやミニバスに乗る。道順の指示は話しかける相手(男性・女性・目上・複数)で形が変わるので、その形も並べた。</p>
    </div>
  </header>"""


def sec_h(ge, ja, extra=""):
    return f'<h2 class="sec"><span class="ge">{esc(ge)}</span>{esc(ja)}{extra}</h2>'


def notes_html():
    items = "\n".join(f"      <li>{ge_spans(n)}</li>" for n in NOTES)
    return f'  <div class="notes">\n    <h3>使うときの注意</h3>\n    <ul>\n{items}\n    </ul>\n  </div>'


def build_web():
    out = [head(False), '<div class="page">', masthead()]
    btns = "\n".join(
        f'      <button type="button" data-k="{k}" aria-pressed="{str(k == "m").lower()}">'
        f'<span class="lbl">{lbl}</span><span class="suf">{esc(e[1])}<span class="rom">{esc(e[2])}</span></span>'
        f'<span class="ex">{esc(e[3])}</span></button>'
        for (k, lbl), e in zip(FORMS, ENDINGS))
    out.append(f"""  <div class="ends-wrap">
    {sec_h("ለማን?", "道順の指示は相手で形が変わる")}
    <p>「曲がって」「行って」「止めて」は命令形で、相手によって語尾が変わる。下のボタンで相手を選ぶと、フレーズとクイズがその形に切り替わる。道を教えてもらうときは、自分に合った形で言われる。</p>
    <div class="ends" role="group" aria-label="話しかける相手">
{btns}
    </div>
  </div>
  <div id="list"></div>""")

    qbtns = "".join(f'<button type="button" data-a="{a}"><span class="ar" aria-hidden="true">{ar}</span>'
                    f'<span class="lb">{lb}</span></button>' for a, ar, lb in QUIZ_BUTTONS)
    out.append(f"""  <section class="scene">{sec_h("ፈተና", "道順クイズ")}
    <p class="lead">アムハラ語の指示を読んで(声に出して)、どちらへ進むかを選ぶ。上で選んだ相手の形で出題する。</p>
    <div class="quiz">
      <div class="q" aria-live="polite"><span class="gez" id="qge"></span><span class="who" id="qwho"></span></div>
      <div class="btns" role="group" aria-label="進む方向">{qbtns}</div>
      <div class="res" id="qres" aria-live="polite"></div>
      <div class="bar"><span id="qscore">0 問中 0 問正解</span><button type="button" class="next" id="qnext">次の問題</button></div>
    </div>
  </section>""")

    for ge, ja, items in WORDS:
        cards = "".join(f'<div class="card"><span class="ja">{esc(w)}</span><span class="gez">{esc(f)}</span>'
                        f'<span class="kt">{esc(k)}</span><span class="rom">{esc(r)}</span></div>' for w, f, r, k in items)
        out.append(f'  <section class="scene">{sec_h(ge, ja)}\n    <div class="cards">{cards}</div>\n  </section>')

    lines = "\n".join(
        f'      <div class="line"><span class="sp">{sp}</span><div><span class="gez">{esc(ge)}</span>'
        f'<span class="kt">{esc(kt)}</span><span class="tr">{esc(ja)}</span></div></div>'
        for sp, ge, kt, ja in DIALOGUE)
    out.append(f'  <section class="scene">{sec_h("ውይይት", "会話の例", "<span class=\"rom\" style=\"font-size:.8rem;color:var(--ink-muted)\">A = 男性の旅行者、B = 道を教える人、C = タクシーの運転手</span>")}\n'
               f'    <div class="dlg">\n{lines}\n    </div>\n  </section>')
    out.append(notes_html())
    out.append(f"  <footer>{ge_spans(SOURCES)}</footer>\n</div>")

    quiz = [{"a": a, "forms": f, "ja": ja} for a, f, ja in QUIZ]
    out.append(f"""<script>
  const SECTIONS = {json.dumps(SECTIONS, ensure_ascii=False)};
  const FORMS = {json.dumps(FORMS, ensure_ascii=False)};
  const QUIZ = {json.dumps(quiz, ensure_ascii=False)};
  const esc = s => String(s).replace(/[&<>"]/g, c => ({{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}}[c]));
  const geSpan = s => esc(s).replace(/([\\u1200-\\u139f\\u2d80-\\u2ddf]+(?:\\s[\\u1200-\\u139f]+)*)/g, '<span class="ge">$1</span>');
  const label = Object.fromEntries(FORMS);
  let who = "m";
  try {{ const v = localStorage.getItem("amh-dir-who"); if (v && FORMS.some(f => f[0] === v)) who = v; }} catch (e) {{}}

  function phrase(p) {{
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

  // クイズ: 同じ問題が続かないように選ぶ
  let cur = 0, answered = false, total = 0, right = 0;
  const qBtns = document.querySelectorAll(".quiz .btns button");
  function showQ() {{
    const q = QUIZ[cur];
    document.getElementById("qge").textContent = q.forms[who][0];
    document.getElementById("qwho").textContent = label[who] + "の形";
    document.getElementById("qres").innerHTML = "";
    qBtns.forEach(b => {{ b.className = ""; b.disabled = false; }});
    answered = false;
  }}
  function nextQ() {{
    let n; do {{ n = Math.floor(Math.random() * QUIZ.length); }} while (n === cur && QUIZ.length > 1);
    cur = n; showQ();
  }}
  qBtns.forEach(b => b.addEventListener("click", () => {{
    if (answered) return;
    answered = true; total++;
    const q = QUIZ[cur], ok = b.dataset.a === q.a;
    if (ok) right++;
    qBtns.forEach(x => {{ x.className = x.dataset.a === q.a ? "ok" : (x === b ? "ng" : ""); x.disabled = true; }});
    const [ge, rom, kana] = q.forms[who];
    document.getElementById("qres").innerHTML = `${{ok ? "正解。" : "ちがいます。"}}<span class="kt">${{esc(kana)}}</span> = ${{esc(q.ja)}}<br><span class="rom">${{esc(rom)}}</span>`;
    document.getElementById("qscore").textContent = `${{total}} 問中 ${{right}} 問正解`;
  }}));
  document.getElementById("qnext").addEventListener("click", nextQ);

  function render() {{
    document.getElementById("list").innerHTML = SECTIONS.map(s =>
      `<section class="scene"><h2 class="sec"><span class="ge">${{esc(s.ge)}}</span>${{esc(s.ja)}}</h2>
       <div class="list">${{s.phrases.map(phrase).join("")}}</div></section>`).join("");
    document.querySelectorAll(".ends button").forEach(b => b.setAttribute("aria-pressed", String(b.dataset.k === who)));
    showQ();
  }}
  document.querySelectorAll(".ends button").forEach(b => b.addEventListener("click", () => {{
    who = b.dataset.k;
    try {{ localStorage.setItem("amh-dir-who", who); }} catch (e) {{}}
    render();
  }}));
  render();
</script>""")
    return "\n".join(out) + "\n"


def build_print():
    out = [head(True), '<div class="page">', masthead()]
    ends = "\n".join(
        f'<div><span class="lbl">{lbl}</span><span class="suf">{esc(e[1])}</span> '
        f'<span class="rom">{esc(e[2])}</span><span class="ex">{esc(e[3])}</span></div>'
        for (k, lbl), e in zip(FORMS, ENDINGS))
    out.append(f'  <section>{sec_h("ለማን?", "道順の指示は相手で形が変わる")}\n  <div class="ends">\n{ends}\n  </div></section>')
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

    def words_table(items):
        rows = "".join(f'<tr><td class="ja">{esc(w)}</td><td><span class="gez">{esc(f)}</span></td>'
                       f'<td><span class="kt">{esc(k)}</span><span class="rom">{esc(r)}</span></td></tr>'
                       for w, f, r, k in items)
        return ('<table><colgroup><col style="width:32%"><col style="width:32%"><col></colgroup>'
                f'<thead><tr><th>日本語</th><th>フィデル</th><th>読み方</th></tr></thead><tbody>{rows}</tbody></table>')
    for ge, ja, items in WORDS:
        half = (len(items) + 1) // 2
        out.append(f'  <section style="break-inside:avoid">{sec_h(ge, ja)}'
                   f'<div class="grid2">{words_table(items[:half])}{words_table(items[half:])}</div></section>')

    rows = "\n".join(
        f'<tr><td style="width:2.2em;font-weight:700;color:var(--accent)">{sp}</td>'
        f'<td><span class="gez">{esc(ge)}</span><span class="kt">{esc(kt)}</span></td><td>{esc(ja)}</td></tr>'
        for sp, ge, kt, ja in DIALOGUE)
    out.append(f'  <section class="dlg">{sec_h("ውይይት", "会話の例(A = 男性の旅行者、B = 道を教える人、C = タクシーの運転手)")}\n'
               '  <table><colgroup><col style="width:2.2em"><col style="width:62%"><col></colgroup>'
               f'<tbody>\n{rows}\n</tbody></table></section>')
    out.append(notes_html())
    out.append(f"  <footer>{ge_spans(SOURCES)}</footer>\n</div>\n</body>\n</html>")
    return "\n".join(out) + "\n"


def build_md():
    md = [f"# {NAME}", "",
          "場所を尋ねる、道順を聞き取る、目印で位置を言う、タクシーやミニバスに乗る。フィデル / ローマ字 / カタカナ読みの順。", ""]
    if WEB_URL:
        md += [f"Web版: {WEB_URL}(相手別の形の切り替えと道順クイズつき)", ""]
    md += ["## 道順の指示は相手で形が変わる", "", "| 相手 | 語尾 | ローマ字 | 例 |", "|---|---|---|---|"]
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
    for ge, ja, items in WORDS:
        md += ["", f"## {ja}({ge})", "", "| 日本語 | フィデル | ローマ字 | カタカナ目安 |", "|---|---|---|---|"]
        md += [f"| {w} | {f} | {r} | {k} |" for w, f, r, k in items]
    md += ["", "## 会話の例(A = 男性の旅行者、B = 道を教える人、C = タクシーの運転手)", ""]
    md += [f"- **{sp}**: {ge}  \n  {kt} — {ja}" for sp, ge, kt, ja in DIALOGUE]
    md += ["", "## 使うときの注意", ""] + [f"- {n}" for n in NOTES]
    md += ["", "---", f"出典: {SOURCES}", ""]
    return "\n".join(md)


if __name__ == "__main__":
    (ROOT / f"{NAME}.html").write_text(build_web(), encoding="utf-8")
    (ROOT / f"{NAME}-print.html").write_text(build_print(), encoding="utf-8")
    (ROOT / f"{NAME}.md").write_text(build_md(), encoding="utf-8")
    print("ok")
