# -*- coding: utf-8 -*-
"""手写最小合法 docx（不依赖 python-docx）：英文导游词定稿，作为小红书笔记附件。
沉淀自 build_liaoshen_docx.py。

===== 使用说明 =====
1. 编辑下方【用户编辑区】：
   - OUT / DOCX：输出目录与文件名（发布时改为 Claw/小红书产出/<景点>/英文图文版/）
   - TITLE：文档首行标题
   - PARAS：英文全文段落列表（含空字符串表示空行）
2. 运行：python build_docx_template.py
3. 生成 <景点>英文导游词_口试定稿.docx，可直接作为小红书笔记附件挂载。
"""
import os, zipfile

# ===================== 用户编辑区 =====================
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output_sample")
DOCX = os.path.join(OUT, "辽沈战役纪念馆英文导游词_口试定稿.docx")
TITLE = "Liaoshen Campaign Memorial Hall - English Tour Guide Script (5 Minutes)"
PARAS = [
    "Hello, friends and visitors! Welcome to the Liaoshen Campaign Memorial Hall in Jinzhou, Liaoning Province. I'm your guide today, and it's my great honor to explore this solemn red education base with you.",
    "This is an important National Patriotic Education Demonstration Base, built to preserve the history of the Liaoshen Campaign. Before we step inside, please keep three phrases in your mind: one campaign, one panoramic painting, countless heroes. Today I'll use these three keys to unfold this magnificent chapter of history.",
    "The Liaoshen Campaign was the first of China's three decisive major campaigns of the Liberation War. It ran from September to November 1948. Its victory completely shifted the nationwide military balance and laid the foundation for the liberation of the whole country.",
    "The memorial hall holds five core exhibition areas: the Preface Hall, the War History Hall, the Mass Support Hall, the Martyrs Hall, and the Panoramic Painting Hall. Precious relics, historic photos, weapons and documents here retell every crucial moment of this campaign.",
    "The landmark highlight here is the Panoramic Painting of the Battle of Jinzhou, China's first panoramic painting. With sound, lighting and modern display technology, it recreates the fierce battles of the Jinzhou assault. Standing within it, visitors feel transported back to the battlefield, witnessing the fearless spirit of our soldiers.",
    "During the bitter campaign, the Northeast People's Liberation Army endured freezing cold and severe supply shortages. They pressed forward with unshakable faith and extraordinary bravery. Local residents stood firmly behind the frontline, delivering grain, clothing and transport support. This victory belonged not only to soldiers, but also to ordinary people.",
    "Here, we recall the heroic years of the Liaoshen Campaign and revisit the moving stories of the martyrs. We are filled with awe not only for the hardships endured, but also for the courage of those who came before us.",
    "The dust of war has settled, and our mountains and rivers are peaceful again. This memorial hall is not merely a record of war. It is a lasting monument to loyalty and sacrifice. It reminds us that our peaceful life today is hard-won, bought with the blood and lives of heroes.",
    "The heroic spirit of the Liaoshen Campaign lives on. It inspires us to remember history, honor martyrs and cherish the peace we hold dear.",
    "Our visit is drawing to a close. At the end of our tour, let me share the slogan of Liaoning cultural tourism: 'Sentient mountains and seas, vast and tranquil Liaoning.'",
    "Thank you for listening. Wish you a safe and pleasant journey!",
]
# =================== 用户编辑区结束 ===================

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

all_paras = [TITLE, ""] + PARAS
body = []
for p in all_paras:
    if p == "":
        body.append('<w:p/>')
    else:
        body.append(f'<w:p><w:r><w:t xml:space="preserve">{esc(p)}</w:t></w:r></w:p>')
document = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
    '<w:body>' + "".join(body) + '</w:body></w:document>'
)
content_types = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
    '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
    '<Default Extension="xml" ContentType="application/xml"/>'
    '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
    '</Types>'
)
rels = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
    '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
    '</Relationships>'
)

os.makedirs(OUT, exist_ok=True)
with zipfile.ZipFile(DOCX, "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("[Content_Types].xml", content_types)
    z.writestr("_rels/.rels", rels)
    z.writestr("word/document.xml", document)
print("生成 docx ->", DOCX, f"({len(all_paras)} 段)")
