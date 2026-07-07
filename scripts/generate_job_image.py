"""
求人画像生成スクリプト (Pillow)
出力: outputs/job_posting.png (1080x1920)
"""

from PIL import Image, ImageDraw, ImageFont
import os

# ── パス設定 ──────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_PATH = os.path.join(BASE_DIR, "outputs", "job_posting.png")
FONT_DIR = r"C:\Windows\Fonts"

# ── カラーパレット ─────────────────────────────────────────
C_BG         = "#F4FBF7"      # ページ背景
C_HEADER_TOP = "#1B4332"      # ヘッダー上部（濃い緑）
C_HEADER_BOT = "#2D6A4F"      # ヘッダー下部
C_ACCENT     = "#40916C"      # セクションタイトル帯
C_ACCENT2    = "#52B788"      # バッジ・アクセント
C_BADGE_BG   = "#D8F3DC"      # バッジ背景
C_BADGE_TXT  = "#1B4332"      # バッジ文字
C_SECTION_BG = "#FFFFFF"      # セクション背景
C_BULLET     = "#74C69D"      # 箇条書きドット
C_TEXT_DARK  = "#1B2E23"      # 本文（濃い）
C_TEXT_MID   = "#374B3E"      # 本文（中間）
C_FOOTER_BG  = "#1B4332"      # フッター背景
C_WHITE      = "#FFFFFF"

# ── フォント ──────────────────────────────────────────────
def load_font(name: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)

FONT_TITLE_L  = load_font("NotoSansJP-VF.ttf", 48)
FONT_TITLE_M  = load_font("NotoSansJP-VF.ttf", 38)
FONT_TITLE_S  = load_font("NotoSansJP-VF.ttf", 30)
FONT_BODY_L   = load_font("NotoSansJP-VF.ttf", 26)
FONT_BODY_M   = load_font("NotoSansJP-VF.ttf", 23)
FONT_BODY_S   = load_font("NotoSansJP-VF.ttf", 20)
FONT_BADGE    = load_font("BIZ-UDGothicB.ttc",  24)
FONT_CAPTION  = load_font("NotoSansJP-VF.ttf", 19)

# ── 画像サイズ ────────────────────────────────────────────
W, H = 1080, 1920
img = Image.new("RGB", (W, H), C_BG)
d   = ImageDraw.Draw(img)

# ── ヘルパー ──────────────────────────────────────────────
def rect(x0, y0, x1, y1, fill, radius=0):
    if radius:
        d.rounded_rectangle([x0, y0, x1, y1], radius=radius, fill=fill)
    else:
        d.rectangle([x0, y0, x1, y1], fill=fill)

def text_center(txt, font, color, cx, y):
    bb = d.textbbox((0, 0), txt, font=font)
    tw = bb[2] - bb[0]
    d.text((cx - tw // 2, y), txt, font=font, fill=color)
    return bb[3] - bb[1]

def wrap_text(txt: str, font, max_w: int) -> list[str]:
    lines, line = [], ""
    for ch in txt:
        test = line + ch
        bb = d.textbbox((0, 0), test, font=font)
        if bb[2] - bb[0] > max_w and line:
            lines.append(line)
            line = ch
        else:
            line = test
    if line:
        lines.append(line)
    return lines

def draw_wrapped(txt, font, color, x, y, max_w, line_h=None):
    lines = wrap_text(txt, font, max_w)
    fh = d.textbbox((0, 0), "あ", font=font)[3] + 4
    if line_h is None:
        line_h = fh + 4
    for ln in lines:
        d.text((x, y), ln, font=font, fill=color)
        y += line_h
    return y

def section_header(label: str, y: int) -> int:
    rect(0, y, W, y + 58, C_ACCENT)
    rect(0, y, 8, y + 58, C_ACCENT2)
    text_center(label, FONT_TITLE_S, C_WHITE, W // 2, y + 12)
    return y + 58

def bullet_item(txt, x, y, font=FONT_BODY_M, max_w=900):
    DOT_R = 8
    rect(x, y + 10, x + DOT_R * 2, y + 10 + DOT_R * 2, C_BULLET, radius=DOT_R)
    y = draw_wrapped(txt, font, C_TEXT_MID, x + DOT_R * 2 + 14, y, max_w)
    return y + 4

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ① ヘッダー
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
rect(0, 0, W, 300, C_HEADER_TOP)
rect(0, 240, W, 300, C_HEADER_BOT)

# アイコン帯
for i, emoji_like in enumerate(["🌿", "✨", "💻"]):
    pass  # Pillow は絵文字非対応のためスキップ

# キャッチコピー
text_center("手順どおりに進めるだけ", FONT_BODY_L, "#B7E4C7", W // 2, 28)

# メインタイトル（2行）
text_center("完全在宅の", FONT_TITLE_L, C_WHITE, W // 2, 82)
text_center("AIクリエイター", FONT_TITLE_L, "#95D5B2", W // 2, 138)

# サブキャッチ
text_center("未経験OK  ·  月収 30万〜45万円 目安", FONT_TITLE_S, "#B7E4C7", W // 2, 208)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ② 3バッジ行
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
badges = [("月収 30〜45万円", "#40916C", C_WHITE),
          ("完全在宅", C_BADGE_BG, C_BADGE_TXT),
          ("未経験OK", C_BADGE_BG, C_BADGE_TXT)]
bx, by = 54, 318
bw, bh = 308, 62
gap = 27
for label, bg, fg in badges:
    rect(bx, by, bx + bw, by + bh, bg, radius=31)
    text_center(label, FONT_BADGE, fg, bx + bw // 2, by + 14)
    bx += bw + gap

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ③ リード文
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
rect(0, 400, W, 530, C_SECTION_BG)
lead = ("静かにコツコツ進める作業が好きな方へ。\n"
        "完全在宅でできるAIクリエイターを募集します。\n"
        "作業はひとつずつ覚えられる内容なので安心してください。")
y = 418
for line in lead.split("\n"):
    y = draw_wrapped(line, FONT_BODY_M, C_TEXT_DARK, 54, y, 972)
    y += 2

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ④ 仕事内容
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
y = section_header("仕事内容", 542)
rect(0, y, W, y + 250, C_SECTION_BG)
y += 18
jobs = [
    "AIツールを使った文章案・画像案の作成補助",
    "投稿文、広告文、企画案のたたき台作成",
    "生成された内容のチェック・修正・整理",
    "テンプレートに沿ったデータ入力や管理",
    "オンラインでの進捗共有・簡単な連絡対応",
]
for item in jobs:
    y = bullet_item(item, 60, y)
    y += 2

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ⑤ こんな方に向いています
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
y = section_header("こんな方に向いています", y + 10)
rect(0, y, W, y + 260, C_SECTION_BG)
y += 18
fits = [
    "落ち着いて作業する方が得意な方",
    "完全在宅で働きたい方",
    "指示や手順を見ながら正確に進めるのが好きな方",
    "AIを学びながら収入につなげたい方",
    "副業として少しずつ始めたい方",
    "未経験OKの仕事からPC作業を始めたい方",
]
for item in fits:
    y = bullet_item(item, 60, y)
    y += 2

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ⑥ 安心ポイント
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
y = section_header("安心して始められるポイント", y + 10)
rect(0, y, W, y + 230, C_SECTION_BG)
y += 18
points = [
    "作業手順があるので迷いにくい",
    "最初はシンプルな補助業務からスタート",
    "分からないことはオンラインで相談可能",
    "完全在宅なので出勤不要",
    "副業OK・生活に合わせて調整しやすい",
]
for item in points:
    y = bullet_item(item, 60, y)
    y += 2

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ⑦ 募集概要テーブル
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
y = section_header("募集概要", y + 10)
rect(0, y, W, y + 310, C_SECTION_BG)
y += 22
overview = [
    ("職　種", "AIクリエイター"),
    ("勤務地", "完全在宅・出勤不要"),
    ("経　験", "未経験OK（PC基本操作のみ）"),
    ("稼　働", "週3日〜・1日2時間程度から相談可"),
    ("報　酬", "月収 30万円〜45万円 目安"),
    ("働き方", "副業OK・オンライン連絡で完結"),
]
row_h = 48
for label, value in overview:
    rect(54, y, 230, y + row_h - 4, C_BADGE_BG, radius=6)
    d.text((64, y + 10), label, font=FONT_BODY_S, fill=C_BADGE_TXT)
    d.text((248, y + 10), value, font=FONT_BODY_M, fill=C_TEXT_DARK)
    y += row_h

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ⑧ フッター（CTA）
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
footer_top = max(y + 30, H - 200)
rect(0, footer_top, W, H, C_FOOTER_BG)
text_center("まずは条件確認だけでも大丈夫です", FONT_BODY_L, "#B7E4C7", W // 2, footer_top + 28)
text_center("応募・詳細確認は 公式LINE から", FONT_TITLE_S, C_WHITE, W // 2, footer_top + 72)

# LINE ボタン風
btn_y = footer_top + 128
rect(W // 2 - 260, btn_y, W // 2 + 260, btn_y + 56, "#06C755", radius=28)
text_center("▶  公式LINE から応募する", FONT_BADGE, C_WHITE, W // 2, btn_y + 14)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 保存
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
img.save(OUTPUT_PATH, "PNG", optimize=True)
print(f"保存完了: {OUTPUT_PATH}")
print(f"サイズ: {W}x{H} px")
