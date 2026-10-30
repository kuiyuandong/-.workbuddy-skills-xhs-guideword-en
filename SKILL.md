---
name: xhs-guideword-en
description: >-
  This skill should be used when generating Xiaohongshu (小红书) image-text posts for
  English-language tour guide scripts (英文导游词) of Liaoning scenic spots, specifically the
  5-minute oral exam recitation version for the 2026 Liaoning tour guide English qualification
  exam. It produces a white-background recitation card set (6 cards + cover, Cambria serif
  English, zero badge/decoration) plus a clean full-text docx attachment and a publish-ready
  markdown package. Trigger when the user provides an English 导游词 (5-minute version) and
  asks to "生成英文图文 / 按白底格式做英文导游词 / 英文跟读卡".
agent_created: true
---

# 英文导游词小红书图文生成

## 用途

将用户**英文**口试导游词定稿（5 分钟讲解版）转化为小红书图文发布包：白底庄重简约跟读卡 6 张 + 白底封面 + 完整稿 docx 附件 + 发布包 md。专用于辽宁导游英语口试（机考）备考。

## 何时使用

- 收到英文导游词（5 分钟口试版，通常 300–400 词），要求"生成英文图文""按白底格式做英文导游词""英文跟读卡""制作英文发布包"。
- 区分：中文讲解稿走 `xhs-guideword-cn`；本 skill 只处理**英文**稿。

## 输入

- 英文导游词全文（5 分钟口试版）。若为 docx，用 Python `zipfile` 提取 `word/document.xml`（只读）。
- 史实红线与专名（如鸭绿江断桥 26 万=260,000 志愿军首批过江，禁写 2,600,000；友谊桥 1937 动工 1943 通车）。
- 辽宁文旅口号官方英文译法：`Sentient mountains and seas, vast and tranquil Liaoning`（山海有情，天辽地宁）。

## 工作流程

1. **史实二次核实**：WebSearch 核实关键史实（年份/数据/称号/英文译法），记入发布包"史实校核记录"。
2. 按段落切片成 6 张卡（CARDS 数据区）。每段 3 句左右，Cambria 衬线英文 42px 正文。
3. 运行 `scripts/gen_white_template.py` 生成 6 张白底卡 + 白底封面。
4. 运行 `scripts/build_docx_template.py` 生成完整稿 docx 附件（手写最小合法 docx，不依赖 python-docx）。
5. 写发布包 md（字段结构见 `references/publish_template.md`）。

## 视觉规范（白底庄重简约，强制）

| 元素 | 取值 | 说明 |
|------|------|------|
| 比例 | 3:4（1080×1440px） | 小红书图文最佳尺寸 |
| 背景 | 纯白 #ffffff | **零渐变、零角标、零橙点、零矢量装饰** |
| 英文标题 | Cambria Bold（cambriab.ttf）46px，黑 #1a1a1a | 卡标题 / 封面主标题 |
| 英文正文 | Cambria（cambria.ttc）42px，近黑 #161616 | 衬线庄重 |
| 序号 | 微软雅黑 30px，灰 #9a9a9a（如 CARD 01） | 顶部左 |
| 重音小字 | 微软雅黑 30px，灰 #888（中文前缀+英文重音） | 底部（如 重音：944.2 meters · 12 spans） |
| 封面 slogan | Cambria Bold 44–48px，黑，锚点式（如断桥"One Bridge · Two Nations · For Peace"） | 记忆锚点 |

详细函数见 `scripts/gen_white_template.py` 注释。**纯矢量文字卡，零实景图、零 AI 图，无需 AI 标识。**

## 合规红线（发布前必查）

- **时长铁律**：一切时长标注以口试 **5 分钟**为准；模板/外部素材误标"3 分钟/2 分半"属 bug 必改。描述栏写"全文约 X 词，朗读约 4–5 分钟，建议掐表控制在 4.5 分钟内留缓冲"。
- **史实**：WebSearch 核实；红色题材庄重，无轻佻 emoji、无贩卖焦虑。
- **极限词**："China's first panoramic painting"等历史事实陈述豁免；禁"最/唯一"营销绝对化。
- **鸭绿江红线**：断桥专版 vs 沿线游全景（5 站）严格区分，不可混用；群雕 26 人物=260,000 志愿军首批过江（禁二百六十万=2,600,000）；友谊桥 1937 动工 1943 通车（禁 built in 1937）。
- **站外引流**：正文零"公众号/私信/加微信/外链"；引流只走评论区置顶。
- **标题 ≤20 字**（矩阵前缀"辽宁导考｜" + "英文词"搜索词）；**描述栏 ≤950 字符**；标签 9 个左右精准搜索词。
- **自检清单**：逐项打勾后随发布包交付（见模板第六节）。

## 产出文件

- `封面_<景点>英文_白底.png` + `轮播_<景点>英文_白底1.png` … `白底6.png`（共 7 张）
- `<景点>英文导游词_口试定稿.docx`（完整稿附件）
- `XHS_<景点>英文_发布包.md`
- 落地路径：`Claw\小红书产出\<景点>\英文图文版\`

## 冷启动风控（红色题材）

红色教育题材初始流量池偏小、"自见不外放"属平台常态风控非账号违规。若遇冷启动走"申诉→失败隐藏重制"，重制须换封面+改 md5+间隔≥24h。
