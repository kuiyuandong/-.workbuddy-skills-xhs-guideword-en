# -*- coding: utf-8 -*-
"""英文导游词小红书 · 白底跟读卡 + 封面 模板（2026-10-26，沉淀自 gen_white_cards.py / gen_liaoshen_white.py / gen_white_cover.py）

===== 使用说明 =====
1. 编辑下方【用户编辑区】：
   - OUT：成品输出目录（默认脚本同目录 output_sample；发布时改为
          Claw/小红书产出/<景点>/英文图文版/）
   - COVER：封面信息（英文主标题两行 / 中文名 / slogan 锚点）
   - CARDS：6 张卡数据列表（no/title/paras/stress）
2. 运行：python gen_white_template.py
3. 生成 6 张白底卡 + 1 张白底封面。纯白底 + Cambria 衬线英文，零角标零装饰。

视觉：对齐九一八/鸭绿江断桥/辽沈英文图文版（白底庄重简约家族）。
下方示例数据以「辽沈战役纪念馆」为参考实现，替换为你的景点即可。
"""
import os
from PIL import Image, ImageDraw, ImageFont

# ===================== 用户编辑区 =====================
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output_sample")
os.makedirs(OUT, exist_ok=True)

COVER = {
    "tag": "LIAONING TOUR GUIDE EXAM · 辽宁导游英语口试",
    "title_lines": ["Liaoshen Campaign", "Memorial Hall"],  # 封面主标题（两行）
    "cn": "辽沈战役纪念馆",
    "slogan": "One Campaign · One Painting · Countless Heroes",
    "sub": "English Recitation Script for the 5-Minute Oral Test",
    "foot": "跟读约 4 分钟 · 适配口试 5 分钟讲解",
}

CARDS = [
    {
        "no": "CARD 01", "title": "Welcome & Base Identity",
        "paras": [
            "Hello, friends and visitors! Welcome to the Liaoshen Campaign Memorial Hall in Jinzhou, Liaoning Province. I'm your guide today, and it's my great honor to explore this solemn red education base with you.",
            "This is an important National Patriotic Education Demonstration Base, built to preserve the history of the Liaoshen Campaign. Before we step inside, please keep three phrases in your mind: one campaign, one panoramic painting, countless heroes.",
            "Today I'll use these three keys to unfold this magnificent chapter of history.",
        ],
        "stress": "重音：Jinzhou · National Patriotic Education Base · three keys",
    },
    {
        "no": "CARD 02", "title": "The Campaign",
        "paras": [
            "The Liaoshen Campaign was the first of China's three decisive major campaigns of the Liberation War.",
            "It ran from September to November 1948.",
            "Its victory completely shifted the nationwide military balance and laid the foundation for the liberation of the whole country.",
        ],
        "stress": "重音：first of three · September–November 1948 · national balance",
    },
    {
        "no": "CARD 03", "title": "Five Exhibition Areas",
        "paras": [
            "The memorial hall holds five core exhibition areas: the Preface Hall, the War History Hall, the Mass Support Hall, the Martyrs Hall, and the Panoramic Painting Hall.",
            "Precious relics, historic photos, weapons and documents here retell every crucial moment of this campaign.",
        ],
        "stress": "重音：five halls · Preface · War History · Mass Support · Martyrs · Panoramic",
    },
    {
        "no": "CARD 04", "title": "Panoramic Painting",
        "paras": [
            "The landmark highlight here is the Panoramic Painting of the Battle of Jinzhou, China's first panoramic painting.",
            "With sound, lighting and modern display technology, it recreates the fierce battles of the Jinzhou assault.",
            "Standing within it, visitors feel transported back to the battlefield, witnessing the fearless spirit of our soldiers.",
        ],
        "stress": "重音：China's first panoramic painting · Battle of Jinzhou · immersive",
    },
    {
        "no": "CARD 05", "title": "Soldiers & People",
        "paras": [
            "During the bitter campaign, the Northeast People's Liberation Army endured freezing cold and severe supply shortages. They pressed forward with unshakable faith and extraordinary bravery.",
            "Local residents stood firmly behind the frontline, delivering grain, clothing and transport support.",
            "This victory belonged not only to soldiers, but also to ordinary people.",
        ],
        "stress": "重音：Northeast PLA · freezing cold · local residents · ordinary people",
    },
    {
        "no": "CARD 06", "title": "Reflection & Slogan",
        "paras": [
            "The dust of war has settled, and our mountains and rivers are peaceful again. This memorial hall is not merely a record of war. It is a lasting monument to loyalty and sacrifice.",
            "It reminds us that our peaceful life today is hard-won, bought with the blood and lives of heroes. The heroic spirit of the Liaoshen Campaign lives on, inspiring us to remember history, honor martyrs and cherish the peace we hold dear.",
            "At the end of our tour, let me share Liaoning's tourism slogan: 'Sentient mountains and seas, vast and tranquil Liaoning.' Thank you for listening. Wish you a safe and pleasant journey!",
        ],
        "stress": "重音：monument to sacrifice · peace hard-won · Liaoning slogan",
    },
]
# =================== 用户编辑区结束 ===================

W, H = 1080, 1440
FONT_DIR = r"C:\Windows\Fonts"
F_SERIF   = os.path.join(FONT_DIR, "cambria.ttc")
F_SERIF_B = os.path.join(FONT_DIR, "cambriab.ttf")
F_SANS    = os.path.join(FONT_DIR, "msyh.ttc")

def F(path, sz):
    return ImageFont.truetype(path, sz)

def wrap(draw, text, font, max_w):
    """word-aware 换行，保留原标点。"""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

MARGIN = 95
MAX_W = W - 2 * MARGIN

def make_card(card, idx):
    img = Image.new("RGB", (W, H), (255, 255, 255))
    d = ImageDraw.Draw(img)
    f_no    = F(F_SANS, 30)
    f_title = F(F_SERIF_B, 46)
    f_body  = F(F_SERIF, 42)
    f_stress= F(F_SANS, 30)

    d.text((MARGIN, 120), card["no"], font=f_no, fill=(154, 154, 154))
    d.text((MARGIN, 168), card["title"], font=f_title, fill=(26, 26, 26))

    y = 320
    for p in card["paras"]:
        lines = wrap(d, p, f_body, MAX_W)
        for ln in lines:
            d.text((MARGIN, y), ln, font=f_body, fill=(22, 22, 22))
            y += 54
        y += 16

    d.text((MARGIN, H - 110), card["stress"], font=f_stress, fill=(136, 136, 136))

    fname = f"轮播_{COVER['cn']}英文_白底{idx+1}.png"
    path = os.path.join(OUT, fname)
    img.save(path, "PNG")
    return y

def make_cover():
    img = Image.new("RGB", (W, H), (255, 255, 255))
    d = ImageDraw.Draw(img)
    f_tag    = F(F_SANS, 30)
    f_title  = F(F_SERIF_B, 72)
    f_cn     = F(F_SANS, 42)
    f_slogan = F(F_SERIF_B, 44)
    f_sub    = F(F_SERIF, 36)
    f_foot   = F(F_SANS, 30)

    def center(text, font, y, fill):
        tw = d.textlength(text, font=font)
        d.text(((W - tw) / 2, y), text, font=font, fill=fill)

    center(COVER["tag"], f_tag, 150, (154, 154, 154))
    ty = 340
    for line in COVER["title_lines"]:
        center(line, f_title, ty, (22, 22, 22)); ty += 92
    center(COVER["cn"], f_cn, ty + 8, (22, 22, 22))
    ty += 108
    d.line([(W/2 - 180, ty), (W/2 + 180, ty)], fill=(225, 225, 225), width=2)
    ty += 88
    center(COVER["slogan"], f_slogan, ty, (22, 22, 22))
    ty += 102
    center(COVER["sub"], f_sub, ty, (120, 120, 120))
    center(COVER["foot"], f_foot, 1300, (136, 136, 136))

    path = os.path.join(OUT, f"封面_{COVER['cn']}英文_白底.png")
    img.save(path, "PNG")
    print("生成白底封面 ->", path)

if __name__ == "__main__":
    total_words = 0
    for i, c in enumerate(CARDS):
        for p in c["paras"]:
            total_words += len(p.split())
        end_y = make_card(c, i)
        print(f"CARD {i+1} 生成, 末行 y={end_y} (安全线 {H-130})")
    make_cover()
    print(f"轮播总词数 ≈ {total_words} 词（正文，不含标题/重音）-> {OUT}")
