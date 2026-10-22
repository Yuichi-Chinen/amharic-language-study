"""アムハラ語あいさつフレーズ集を生成する。

出力(アムハラ語フォルダ直下):
  アムハラ語あいさつフレーズ集.html        Web版(Artifact用。doctypeなしの断片)
  アムハラ語あいさつフレーズ集-print.html  印刷用(A4縦。Edgeヘッドレスで PDF 化)
  アムハラ語あいさつフレーズ集.md          テキスト版

カタカナは学習用の目安。ä→エ、ə→イ/ウ(前後の音で選ぶ)、二重子音→ッ で写している。
"""
import html
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
NAME = "アムハラ語あいさつフレーズ集"

# 相手によって形が変わるフレーズの4形(男性へ・女性へ・目上の人へ・複数の人へ)
FORMS = [("m", "男性へ"), ("f", "女性へ"), ("p", "目上の人へ"), ("pl", "複数の人へ")]

# 各フレーズ: ja(日本語), ge(フィデル), rom, kana, note
#   相手で形が変わるものは ge/rom/kana の代わりに forms={key: (ge, rom, kana)}
SECTIONS = [
    {"ge": "ሰላምታ", "ja": "いつでも使えるあいさつ", "phrases": [
        {"ja": "やあ / こんにちは", "ge": "ሰላム", "rom": "sälam", "kana": "セラム",
         "note": "もとの意味は「平和」。時間帯も相手も選ばない。ヘブル語の シャローム と同じ語根。"},
        {"ja": "こんにちは(丁寧)", "ge": "ጤና ይስጥልኝ", "rom": "ṭena yəsṭəlləñ", "kana": "テナ・イスティリニュ",
         "note": "「(神が)あなたに健康を与えますように」。初対面や目上の人に。"},
        {"ja": "元気? / 調子どう?", "ge": "ሰላም ነው?", "rom": "sälam näw?", "kana": "セラム・ネウ?",
         "note": "くだけた聞き方。答えも同じく ሰላም ነው(元気だよ)。"},
    ]},
    {"ge": "በቀኑ ሰዓት", "ja": "時間帯のあいさつ", "phrases": [
        {"ja": "おはようございます", "forms": {
            "m": ("እንደምን አደርክ?", "əndämən adärk?", "インデミン・アデルク?"),
            "f": ("እንደምን አደርሽ?", "əndämən adärš?", "インデミン・アデルシュ?"),
            "p": ("እንደምን አደሩ?", "əndämən adäru?", "インデミン・アデル?"),
            "pl": ("እንደምን አደራችሁ?", "əndämən adäraččəhu?", "インデミン・アデラッチュフ?")},
         "note": "直訳は「どのように夜を過ごしましたか」。"},
        {"ja": "こんにちは(昼〜夕方)", "forms": {
            "m": ("እንደምን ዋልክ?", "əndämən walk?", "インデミン・ワルク?"),
            "f": ("እንደምን ዋልሽ?", "əndämən walš?", "インデミン・ワルシュ?"),
            "p": ("እንደምን ዋሉ?", "əndämən walu?", "インデミン・ワル?"),
            "pl": ("እንደምን ዋላችሁ?", "əndämən walaččəhu?", "インデミン・ワラッチュフ?")},
         "note": "直訳は「どのように一日を過ごしましたか」。午後に会ったときに。"},
        {"ja": "こんばんは", "forms": {
            "m": ("እንደምን አመሸህ?", "əndämən amäššäh?", "インデミン・アメッシェフ?"),
            "f": ("እንደምን አመሸሽ?", "əndämən amäššäš?", "インデミン・アメッシェシュ?"),
            "p": ("እንደምን አመሹ?", "əndämən amäššu?", "インデミン・アメッシュ?"),
            "pl": ("እንደምን አመሻችሁ?", "əndämən amäššaččəhu?", "インデミン・アメッシャッチュフ?")},
         "note": "直訳は「どのように夕方を過ごしましたか」。"},
        {"ja": "おやすみなさい", "forms": {
            "m": ("ደህና እደር", "dähna ədär", "デフナ・イデル"),
            "f": ("ደህና እደሪ", "dähna ədäri", "デフナ・イデリ"),
            "p": ("ደህና ይደሩ", "dähna yədäru", "デフナ・イデル"),
            "pl": ("ደህና እደሩ", "dähna ədäru", "デフナ・イデル")},
         "note": "「無事に夜を過ごしてください」。"},
    ]},
    {"ge": "ጤንነት", "ja": "調子を聞く・答える", "phrases": [
        {"ja": "お元気ですか", "forms": {
            "m": ("እንደምን ነህ?", "əndämən näh?", "インデミン・ネフ?"),
            "f": ("እንደምን ነሽ?", "əndämən näš?", "インデミン・ネシュ?"),
            "p": ("እንደምን ነዎት?", "əndämən näwot?", "インデミン・ネウォト?"),
            "pl": ("እንደምን ናችሁ?", "əndämən naččəhu?", "インデミン・ナッチュフ?")},
         "note": "እንደምን の代わりに ደህና(デフナ)を使って「ደህና ነህ?(元気?)」とも聞く。"},
        {"ja": "元気です", "ge": "ደህና ነኝ", "rom": "dähna näñ", "kana": "デフナ・ネニュ",
         "note": "短く ደህና(デフナ)だけでもよい。"},
        {"ja": "おかげさまで", "ge": "እግዚአብሔር ይመስገን", "rom": "əgziʾabəḥer yəmmäsgän", "kana": "イグズィアブヘル・イメスゲン",
         "note": "「神に感謝」。調子を聞かれたらまずこう答える人が多い。"},
        {"ja": "あなたは?", "forms": {
            "m": ("አንተስ?", "antäs?", "アンテス?"),
            "f": ("አንቺስ?", "ančis?", "アンチス?"),
            "p": ("እርስዎስ?", "ərswos?", "イルスウォス?"),
            "pl": ("እናንተስ?", "ənnantäs?", "インナンテス?")},
         "note": "-ስ(-s)は「〜は?」と聞き返す語尾。"},
    ]},
    {"ge": "መተዋወቅ", "ja": "自己紹介", "phrases": [
        {"ja": "私の名前は〜です", "ge": "ስሜ … ነው", "rom": "səme … näw", "kana": "スメ … ネウ",
         "note": "例: ስሜ ኬንጂ ነው(スメ・ケンジ・ネウ)= 私はケンジです。"},
        {"ja": "お名前は?", "forms": {
            "m": ("ስምህ ማን ነው?", "səməh man näw?", "スミフ・マン・ネウ?"),
            "f": ("ስምሽ ማን ነው?", "səməš man näw?", "スミシュ・マン・ネウ?"),
            "p": ("ስምዎ ማን ነው?", "səmwo man näw?", "スムウォ・マン・ネウ?"),
            "pl": ("ስማችሁ ማን ነው?", "səmaččəhu man näw?", "スマッチュフ・マン・ネウ?")},
         "note": "ማን(マン)は「誰」。名前は「誰ですか」で聞く。"},
        {"ja": "私は日本人です", "ge": "እኔ ጃፓናዊ ነኝ", "rom": "əne ǰapanawi näñ", "kana": "イネ・ジャパナウィ・ネニュ",
         "note": "女性は ጃፓናዊት(ジャパナウィト)。"},
        {"ja": "はじめまして", "ge": "ስለተዋወቅን ደስ ብሎኛል", "rom": "səlätäwawäqən däss bəloñal", "kana": "スレテワウェクン・デス・ブロニャル",
         "note": "直訳は「知り合えてうれしいです」。返事は እኔም(イネム = 私も)。"},
    ]},
    {"ge": "ምስጋና", "ja": "お礼・おわび・返事", "phrases": [
        {"ja": "ありがとう", "ge": "አመሰግናለሁ", "rom": "amäsäggənallähu", "kana": "アメセギナレフ",
         "note": "相手を問わず使える。"},
        {"ja": "どういたしまして / 大丈夫", "ge": "ምንም አይደለም", "rom": "mənəm aydälläm", "kana": "ミニム・アイデッレム",
         "note": "直訳は「何でもない」。謝られたときの返事にも。"},
        {"ja": "すみません / ごめんなさい", "ge": "ይቅርታ", "rom": "yəqərta", "kana": "イキルタ",
         "note": "人を呼び止めるときにも使う。"},
        {"ja": "お願いします / どうか", "forms": {
            "m": ("እባክህ", "əbakəh", "イバキフ"),
            "f": ("እባክሽ", "əbakəš", "イバキシュ"),
            "p": ("እባክዎ", "əbakwo", "イバクウォ"),
            "pl": ("እባካችሁ", "əbakaččəhu", "イバカッチュフ")},
         "note": "頼みごとの前に添える。"},
        {"ja": "はい", "ge": "አዎ", "rom": "awo", "kana": "アウォ", "note": ""},
        {"ja": "わかりました / OK", "ge": "እሺ", "rom": "əšši", "kana": "イッシ",
         "note": "頼まれたことを引き受けるときの「はい」。"},
    ]},
    {"ge": "መቀበል እና መሰናበት", "ja": "迎える・別れる", "phrases": [
        {"ja": "ようこそ", "forms": {
            "m": ("እንኳን ደህና መጣህ", "ənkwan dähna mäṭṭah", "インクワン・デフナ・メッタフ"),
            "f": ("እንኳን ደህና መጣሽ", "ənkwan dähna mäṭṭaš", "インクワン・デフナ・メッタシュ"),
            "p": ("እንኳን ደህና መጡ", "ənkwan dähna mäṭṭu", "インクワン・デフナ・メットゥ"),
            "pl": ("እንኳን ደህና መጣችሁ", "ənkwan dähna mäṭṭaččəhu", "インクワン・デフナ・メッタッチュフ")},
         "note": "「無事に来てくれた」。空港や家の入口で言われる。"},
        {"ja": "さようなら", "forms": {
            "m": ("ደህና ሁን", "dähna hun", "デフナ・フン"),
            "f": ("ደህና ሁኚ", "dähna huñi", "デフナ・フニ"),
            "p": ("ደህና ይሁኑ", "dähna yəhunu", "デフナ・イフヌ"),
            "pl": ("ደህና ሁኑ", "dähna hunu", "デフナ・フヌ")},
         "note": "「元気でいてください」。"},
        {"ja": "またあとで", "ge": "በኋላ እንገናኝ", "rom": "bähwala ənnəgänaññ", "kana": "ベフワラ・インネゲナニュ",
         "note": "「後で会いましょう」。"},
        {"ja": "また明日", "ge": "ነገ እንገናኝ", "rom": "nägä ənnəgänaññ", "kana": "ネゲ・インネゲナニュ", "note": ""},
        {"ja": "バイバイ", "ge": "ቻው", "rom": "čaw", "kana": "チャウ",
         "note": "イタリア語 ciao から。友人どうしで。"},
    ]},
    {"ge": "በዓል", "ja": "お祝い", "phrases": [
        {"ja": "おめでとう", "forms": {
            "m": ("እንኳን ደስ አለህ", "ənkwan däss aläh", "インクワン・デス・アレフ"),
            "f": ("እንኳን ደስ አለሽ", "ənkwan däss aläš", "インクワン・デス・アレシュ"),
            "p": ("እንኳን ደስ አለዎት", "ənkwan däss aläwot", "インクワン・デス・アレウォト"),
            "pl": ("እንኳን ደስ አላችሁ", "ənkwan däss alaččəhu", "インクワン・デス・アラッチュフ")},
         "note": "結婚・合格・出産など個人のお祝いに。"},
        {"ja": "(祝日に)おめでとう", "forms": {
            "m": ("እንኳን አደረሰህ", "ənkwan adärräsäh", "インクワン・アデレセフ"),
            "f": ("እንኳን አደረሰሽ", "ənkwan adärräsäš", "インクワン・アデレセシュ"),
            "p": ("እንኳን አደረሰዎት", "ənkwan adärräsäwot", "インクワン・アデレセウォト"),
            "pl": ("እንኳን አደረሳችሁ", "ənkwan adärräsaččəhu", "インクワン・アデレサッチュフ")},
         "note": "「(神が)あなたをこの日まで導いた」。祝日の決まり文句。"},
        {"ja": "新年おめでとう", "ge": "መልካም አዲስ ዓመት", "rom": "mälkam addis amät", "kana": "メルカム・アッディス・アメト",
         "note": "エチオピア暦の元日は9月11日ごろ(閏年の前年は12日)。"},
        {"ja": "メリークリスマス", "ge": "መልካም ገና", "rom": "mälkam gäna", "kana": "メルカム・ゲナ",
         "note": "エチオピアのクリスマス(ገና)は1月7日ごろ。"},
    ]},
]

# 会話例: (話し手, フィデル, カタカナ, 日本語)
DIALOGUE = [
    ("A", "ሰላም! እንደምን ዋልክ?", "セラム! インデミン・ワルク?", "やあ! こんにちは。"),
    ("B", "ደህና ነኝ፣ እግዚአብሔር ይመስገን። አንተስ?", "デフナ・ネニュ、イグズィアブヘル・イメスゲン。アンテス?", "元気です、おかげさまで。あなたは?"),
    ("A", "ደህና ነኝ። ስሜ ኬንጂ ነው። ስምህ ማን ነው?", "デフナ・ネニュ。スメ・ケンジ・ネウ。スミフ・マン・ネウ?", "元気です。私はケンジです。お名前は?"),
    ("B", "ስሜ ዳዊት ነው።", "スメ・ダウィト・ネウ。", "ダウィトです。"),
    ("A", "ስለተዋወቅን ደስ ብሎኛል።", "スレテワウェクン・デス・ブロニャル。", "はじめまして。"),
    ("B", "እኔም። እንኳን ደህና መጣህ!", "イネム。インクワン・デフナ・メッタフ!", "こちらこそ。ようこそ!"),
    ("A", "አመሰግናለሁ። ቻው!", "アメセギナレフ。チャウ!", "ありがとう。じゃあね!"),
]

ENDINGS = [
    ("男性へ", "-ህ / -ክ", "-h / -k", "ነህ · አደርክ"),
    ("女性へ", "-ሽ", "-š", "ነሽ · አደርሽ"),
    ("目上の人へ", "-ዎ(ት) / -ኡ", "-wo(t) / -u", "ነዎት · አደሩ"),
    ("複数の人へ", "-ኣችሁ", "-aččəhu", "ናችሁ · አደራችሁ"),
]

NOTES = [
    "エチオピアのあいさつは長い。「元気?」「家族は?」「仕事は?」と何度も聞き合い、そのたびに「おかげさまで」と答えるのが普通。",
    "知らない大人や年上の人には「目上の人へ」の形を使う。迷ったらこれを選べば失礼にならない。",
    "握手は右手で。男性どうしは握手しながら肩を軽く当てることが多く、親しい人とは頬を左右に3回ほど寄せる。",
    "カタカナは目安。放出音(ጠ ጣ ቅ など)は日本語にない音なので、音源で確認すること。",
    "「目上の人へ」の形と「複数の人へ」の形は、地域や話し手によって入れ替わったり同じ形になったりする。",
]

SOURCES = "Wikivoyage「Amharic phrasebook」、Wikipedia「Amharic」をもとに作成(2026-10-22)。"


def esc(s):
    return html.escape(s, quote=True)


def css(printable):
    base = """
  :root {
    --bg: #EDEAE1; --surface: #F8F5ED; --surface-alt: #E2DDCD;
    --ink: #241F19; --ink-muted: #6E6455; --accent: #AC3527;
    --accent-soft: #DCC9AE; --border: #D6CFBC;
    --f-ge: "Noto Serif Ethiopic", "Nyala", serif;
    --f-body: "Noto Sans JP", "Hiragino Sans", "Yu Gothic", sans-serif;
    --f-rom: "Noto Serif", Georgia, serif;
  }
  * { box-sizing: border-box; }
  body { margin: 0; background: var(--bg); color: var(--ink); font-family: var(--f-body); line-height: 1.7; }
  .ge { font-family: var(--f-ge); }
  .rom { font-family: var(--f-rom); font-style: italic; }
  header.masthead { display: flex; flex-wrap: wrap; align-items: baseline; gap: 14px 28px;
    padding-bottom: 20px; border-bottom: 2px solid var(--accent); }
  .mark { font-weight: 700; color: var(--accent); line-height: 1.1; }
  .titles h1 { margin: 0 0 4px; text-wrap: balance; }
  .titles p { margin: 0; color: var(--ink-muted); max-width: 62ch; }
  h2.sec { margin: 0; display: flex; flex-wrap: wrap; align-items: baseline; gap: 4px 12px; text-wrap: balance; }
  h2.sec .ge { color: var(--accent); }
  .notes { background: var(--surface); border: 1px solid var(--border); border-left: 4px solid var(--accent);
    border-radius: 4px; padding: 14px 20px; }
  .notes h3 { margin: 0 0 8px; font-size: 0.95rem; }
  .notes ul { margin: 0; padding-left: 1.15em; display: flex; flex-direction: column; gap: 6px; font-size: 0.86rem; }
  footer { padding-top: 14px; border-top: 1px solid var(--border); font-size: 0.78rem; color: var(--ink-muted); }
"""
    if printable:
        return base + """
  @page { size: A4 portrait; margin: 14mm 13mm; }
  body { font-size: 9.6pt; line-height: 1.55; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
  .page { display: flex; flex-direction: column; gap: 14px; }
  .mark { font-size: 26pt; }
  .titles h1 { font-size: 15pt; }
  .titles p { font-size: 9pt; }
  section { break-inside: auto; display: flex; flex-direction: column; gap: 6px; }
  h2.sec { font-size: 12pt; break-after: avoid; }
  h2.sec .ge { font-size: 14pt; }
  table { border-collapse: collapse; width: 100%; table-layout: fixed; background: var(--surface); }
  th, td { border: 1px solid var(--border); padding: 4px 7px; text-align: left; vertical-align: top; }
  thead th { background: var(--surface-alt); font-size: 7.5pt; color: var(--ink-muted); letter-spacing: 0.05em; }
  body { background: #FFFFFF; }
  tbody, tr { break-inside: avoid; }
  td.ja { font-weight: 500; }
  td .gez { font-family: var(--f-ge); font-size: 11.5pt; }
  td .kt { color: var(--accent); display: block; line-height: 1.35; }
  td .rom { color: var(--ink-muted); font-size: 8pt; display: block; line-height: 1.35; }
  td.who { font-size: 7.5pt; color: var(--ink-muted); white-space: nowrap; }
  td.note { font-size: 8pt; color: var(--ink-muted); }
  .ends { display: grid; grid-template-columns: repeat(4, 1fr); gap: 6px; }
  .ends div { background: var(--surface); border: 1px solid var(--border); border-radius: 4px; padding: 6px 9px; }
  .ends .lbl { font-size: 8pt; color: var(--ink-muted); display: block; }
  .ends .suf { font-family: var(--f-ge); color: var(--accent); font-size: 12pt; }
  .ends .ex { font-family: var(--f-ge); font-size: 8.5pt; display: block; }
  .dlg { break-inside: avoid; }
  .notes { break-inside: avoid; }
"""
    dark = """--bg: #1B1712; --surface: #241F19; --surface-alt: #2D2721;
      --ink: #EEE6D6; --ink-muted: #A6987F; --accent: #E06A54;
      --accent-soft: #493F35; --border: #3A332B;"""
    return base + f"""
  @media (prefers-color-scheme: dark) {{
    :root:not([data-theme="light"]) {{ color-scheme: dark; {dark} }}
  }}
  :root[data-theme="dark"] {{ color-scheme: dark; {dark} }}
""" + """
  #list { display: flex; flex-direction: column; gap: 30px; }
  body { padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px));
    padding-block: clamp(20px, 4vw, 56px); }
  .page { max-width: 1000px; margin: 0 auto; display: flex; flex-direction: column; gap: 30px; }
  .mark { font-size: clamp(2.3rem, 6vw, 3.4rem); }
  .titles h1 { font-size: clamp(1.3rem, 2.6vw, 1.7rem); }
  .titles p { font-size: 0.9rem; }

  .ends-wrap { display: flex; flex-direction: column; gap: 10px; }
  .ends-wrap p { margin: 0; font-size: 0.88rem; max-width: 68ch; }
  .ends { display: grid; grid-template-columns: repeat(auto-fit, minmax(190px, 1fr)); gap: 8px; }
  .ends button { font: inherit; text-align: left; cursor: pointer; color: var(--ink);
    background: var(--surface); border: 1px solid var(--border); border-radius: 4px; padding: 10px 14px;
    display: flex; flex-direction: column; gap: 2px; }
  .ends button:hover { border-color: var(--accent-soft); }
  .ends button[aria-pressed="true"] { border-color: var(--accent); box-shadow: inset 0 0 0 1px var(--accent); }
  .ends button:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
  .ends .lbl { font-size: 0.78rem; color: var(--ink-muted); font-weight: 700; letter-spacing: 0.04em; }
  .ends .suf { font-family: var(--f-ge); color: var(--accent); font-size: 1.25rem; }
  .ends .suf .rom { font-size: 0.85rem; color: var(--ink-muted); margin-left: 6px; }
  .ends .ex { font-family: var(--f-ge); font-size: 0.85rem; }

  section.scene { display: flex; flex-direction: column; gap: 12px; }
  h2.sec { font-size: 1.15rem; }
  h2.sec .ge { font-size: 1.45rem; }
  .list { background: var(--surface); border: 1px solid var(--border); border-radius: 6px; }
  .ph { display: grid; grid-template-columns: minmax(9em, 13em) minmax(0, 1fr); gap: 4px 24px;
    padding: 14px 18px; border-bottom: 1px solid var(--border); }
  .ph:last-child { border-bottom: 0; }
  .ph .ja { font-weight: 700; font-size: 0.95rem; }
  .ph .ja .tag { display: inline-block; margin-top: 4px; font-size: 0.7rem; font-weight: 500; color: var(--accent);
    border: 1px solid var(--accent-soft); border-radius: 3px; padding: 0 6px; }
  .ph .body { min-width: 0; display: flex; flex-direction: column; gap: 2px; }
  .ph .gez { font-family: var(--f-ge); font-size: 1.55rem; line-height: 1.35; }
  .ph .kt { color: var(--accent); font-size: 0.95rem; }
  .ph .rom { color: var(--ink-muted); font-size: 0.85rem; margin-left: 10px; }
  .ph .note { font-size: 0.82rem; color: var(--ink-muted); margin-top: 4px; }
  .ph .note .ge { color: var(--ink); }
  .others { display: flex; flex-wrap: wrap; gap: 6px 14px; margin-top: 6px; font-size: 0.8rem; }
  .others span { color: var(--ink-muted); }
  .others b { font-weight: 500; color: var(--ink); font-family: var(--f-ge); }
  @media (max-width: 560px) { .ph { grid-template-columns: 1fr; } .ph .rom { display: block; margin-left: 0; } }

  .dlg { background: var(--surface); border: 1px solid var(--border); border-radius: 6px; padding: 8px 18px; }
  .line { display: grid; grid-template-columns: 2em minmax(0, 1fr); gap: 4px 12px; padding: 10px 0; border-bottom: 1px dashed var(--border); }
  .line:last-child { border-bottom: 0; }
  .line .sp { font-weight: 700; color: var(--accent); font-family: var(--f-rom); }
  .line .gez { font-family: var(--f-ge); font-size: 1.2rem; }
  .line .kt { font-size: 0.85rem; color: var(--accent); display: block; }
  .line .tr { font-size: 0.85rem; color: var(--ink-muted); display: block; }
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


def ge_spans(text):
    """備考内のゲエズ文字にフォントを当てる。"""
    out, buf, in_ge = [], "", False
    for ch in text:
        is_ge = "ሀ" <= ch <= "᎟" or "ⶀ" <= ch <= "⷟"
        if is_ge != in_ge and buf:
            out.append(f'<span class="ge">{esc(buf)}</span>' if in_ge else esc(buf))
            buf = ""
        in_ge = is_ge
        buf += ch
    if buf:
        out.append(f'<span class="ge">{esc(buf)}</span>' if in_ge else esc(buf))
    return "".join(out)


def masthead():
    return """  <header class="masthead">
    <div class="mark ge">ሰላምታ</div>
    <div class="titles">
      <h1>アムハラ語あいさつフレーズ集</h1>
      <p>朝・昼・夜のあいさつから自己紹介、お礼、別れ、お祝いまで。アムハラ語のあいさつは話しかける相手(男性・女性・目上・複数)で語尾が変わるので、その形も並べた。</p>
    </div>
  </header>"""


def notes_html():
    items = "\n".join(f"      <li>{ge_spans(n)}</li>" for n in NOTES)
    return f'  <div class="notes">\n    <h3>使うときの注意</h3>\n    <ul>\n{items}\n    </ul>\n  </div>'


def dialogue_html(printable):
    lines = "\n".join(
        f'      <div class="line"><span class="sp">{sp}</span><div><span class="gez">{esc(ge)}</span>'
        f'<span class="kt">{esc(kt)}</span><span class="tr">{esc(ja)}</span></div></div>'
        for sp, ge, kt, ja in DIALOGUE)
    if printable:
        rows = "\n".join(
            f'<tr><td style="width:2.2em;font-weight:700;color:var(--accent)">{sp}</td>'
            f'<td><span class="gez">{esc(ge)}</span><span class="kt">{esc(kt)}</span></td><td>{esc(ja)}</td></tr>'
            for sp, ge, kt, ja in DIALOGUE)
        return ('  <section class="dlg"><h2 class="sec"><span class="ge">ውይይት</span>会話の例</h2>\n'
                '  <table><colgroup><col style="width:2.2em"><col style="width:62%"><col></colgroup>'
                f'<tbody>\n{rows}\n</tbody></table></section>')
    return ('  <section class="scene"><h2 class="sec"><span class="ge">ውይይት</span>会話の例'
            '<span class="rom" style="font-size:.8rem;color:var(--ink-muted)">A が男性 B に話しかける場面</span></h2>\n'
            f'    <div class="dlg">\n{lines}\n    </div>\n  </section>')


def build_web():
    out = [head(False), '<div class="page">', masthead()]
    btns = "\n".join(
        f'      <button type="button" id="form-{k}" data-k="{k}" aria-pressed="{str(k == "m").lower()}">'
        f'<span class="lbl">{lbl}</span><span class="suf">{esc(e[1])}<span class="rom">{esc(e[2])}</span></span>'
        f'<span class="ex">{esc(e[3])}</span></button>'
        for (k, lbl), e in zip(FORMS, ENDINGS))
    out.append(f"""  <div class="ends-wrap">
    <h2 class="sec"><span class="ge">ለማን?</span>話しかける相手で語尾が変わる</h2>
    <p>あいさつの多くは「あなた」にあたる部分が語尾に入っていて、相手によって形が変わる。下のボタンで相手を選ぶと、すべてのフレーズがその形に切り替わる。</p>
    <div class="ends" role="group" aria-label="話しかける相手">
{btns}
    </div>
  </div>
  <div id="list"></div>""")
    out.append(dialogue_html(False))
    out.append(notes_html())
    out.append(f"  <footer>{esc(SOURCES)}</footer>\n</div>")
    data = json.dumps(SECTIONS, ensure_ascii=False)
    forms = json.dumps(FORMS, ensure_ascii=False)
    out.append(f"""<script>
  const SECTIONS = {data};
  const FORMS = {forms};
  const esc = s => String(s).replace(/[&<>"]/g, c => ({{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}}[c]));
  const geSpan = s => esc(s).replace(/([\\u1200-\\u139f\\u2d80-\\u2ddf]+(?:\\s[\\u1200-\\u139f]+)*)/g, '<span class="ge">$1</span>');
  let who = "m";
  try {{ const v = localStorage.getItem("amh-greet-who"); if (v && FORMS.some(f => f[0] === v)) who = v; }} catch (e) {{}}

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
    try {{ localStorage.setItem("amh-greet-who", who); }} catch (e) {{}}
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
    out.append('  <section><h2 class="sec"><span class="ge">ለማን?</span>話しかける相手で語尾が変わる</h2>\n'
               f'  <div class="ends">\n{ends}\n  </div></section>')
    for s in SECTIONS:
        bodies = []
        for p in s["phrases"]:
            # 相手で変わるフレーズは4行に分け、日本語と備考はまとめて1セルにする
            forms = [(lbl, *p["forms"][k]) for k, lbl in FORMS] if "forms" in p else [("", p["ge"], p["rom"], p["kana"])]
            span = f' rowspan="{len(forms)}"' if len(forms) > 1 else ""
            rows = []
            for i, (lbl, ge, rom, kana) in enumerate(forms):
                lead = (f'<td class="ja"{span}>{esc(p["ja"])}</td>' if i == 0 else "")
                tail = (f'<td class="note"{span}>{ge_spans(p["note"])}</td>' if i == 0 else "")
                rows.append(f'<tr>{lead}<td class="who">{lbl}</td><td><span class="gez">{esc(ge)}</span></td>'
                            f'<td><span class="kt">{esc(kana)}</span><span class="rom">{esc(rom)}</span></td>{tail}</tr>')
            bodies.append("<tbody>" + "".join(rows) + "</tbody>")
        out.append(f'  <section><h2 class="sec"><span class="ge">{esc(s["ge"])}</span>{esc(s["ja"])}</h2>\n'
                   '  <table><colgroup><col style="width:16%"><col style="width:9%"><col style="width:25%">'
                   '<col style="width:28%"><col></colgroup>\n'
                   '  <thead><tr><th>日本語</th><th>相手</th><th>フィデル</th><th>読み方</th><th>備考</th></tr></thead>\n'
                   f'  {chr(10).join(bodies)}\n  </table></section>')
    out.append(dialogue_html(True))
    out.append(notes_html())
    out.append(f"  <footer>{esc(SOURCES)}</footer>\n</div>\n</body>\n</html>")
    return "\n".join(out) + "\n"


def build_md():
    md = [f"# {NAME}", "",
          "朝・昼・夜のあいさつから自己紹介、お礼、別れ、お祝いまで。フィデル / ローマ字 / カタカナ読みの順。",
          "", "Web版: https://claude.ai/artifact/S4zgfvvbPq8sg4o4Qnkqnv", "",
          "## 話しかける相手で語尾が変わる", "",
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
    md += ["", "## 会話の例(A が男性 B に話しかける場面)", ""]
    md += [f"- **{sp}**: {ge}  \n  {kt} — {ja}" for sp, ge, kt, ja in DIALOGUE]
    md += ["", "## 使うときの注意", ""] + [f"- {n}" for n in NOTES]
    md += ["", "---", f"出典: {SOURCES}", ""]
    return "\n".join(md)


if __name__ == "__main__":
    (ROOT / f"{NAME}.html").write_text(build_web(), encoding="utf-8")
    (ROOT / f"{NAME}-print.html").write_text(build_print(), encoding="utf-8")
    (ROOT / f"{NAME}.md").write_text(build_md(), encoding="utf-8")
    print("ok")
