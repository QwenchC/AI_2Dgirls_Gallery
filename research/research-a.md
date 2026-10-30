# 七位角色的中文社区研究记录

核验日期：2026-10-30（Asia/Shanghai）。范围：ChatGPT、Claude、DeepSeek、Gemini、Grok、Kimi、Llama。

## 方法与边界

先搜索中文社区和 B 站，再沿作品简介中的署名寻找原作者、原始作品及后续创作。采用三层区分：作者明示／具体同人作品中的设定／本项目新增的创作建议。研究没有下载外部图像、音频、视频，也没有将整理站的图片复制进项目。`characters-a.json` 的 `projectSetting` 全部是本项目新写的虚构内容，不能表述成官方或社区一致设定。

检索覆盖约 30 组组合词，包括：

| 角色 | 主要检索词 | 结果范围 |
| --- | --- | --- |
| ChatGPT | ChatGPT 拟人 bilibili；GPT小龙娘 DeepSeek 大家庭；ChatGPT娘 性格 | 作者合集、后续 B 站小龙娘日常、社区评论 |
| Claude | Claude 拟人 bilibili；Claude娘 性格；Claude娘 大小姐 | B 站 LoRA 展示、群像署名、独立人格卡 |
| DeepSeek | DeepSeek 上善无形；大AI和小AI们；蓝色大肥鱼 起源；ZipZipPipe 素材来源与使用声明 | B 站原作者二创声明、后续同人、传播报道 |
| Gemini | Gemini娘 bilibili；Gemini娘 性格；Gemini娘 猫娘 | B 站猫娘翻唱标题及署名、社区评论 |
| Grok | Grok娘 bilibili；Grok娘 ZipZipPipe；Grok 娘 性格 | 作者合集、社区立绘档案、明示为二创的人格描述 |
| Kimi | Kimi 拟人 ZipZipPipe；Kimi娘 性格；Kimi娘 月之暗面 | B 站群像署名、立绘档案、繁体中文独立企划 |
| Llama | Llama 拟人 ZipZipPipe；Llama娘 性格；Llama娘 bilibili.com | 二手图鉴、逐图索引及独立企划，原始 B 站设定不足 |

## 可复核的 B 站证据

B 站普通网页部分返回 412。随后使用无需登录的公开接口 `https://api.bilibili.com/x/web-interface/view?bvid=...` 读取公开元数据，获得标题、UP 主、发布时间和简介；这是元数据核验，不是已观看视频。`bilibili-a-metadata.json` 保存七条元数据与自写摘要，不保存整段简介或视频内容。发布时间按北京时间转换，避免搜索缓存的时区偏差。

- [大AI和小AI们](https://www.bilibili.com/video/BV1tE9XBbErS/) — ZipZipPipe，2026-05-03。作者简介列出九位 AI，并说明大、小形象展示。鲸鱼娘另有上善无形来源及 CC BY-NC-SA 4.0 条件。
- [“亿万”身家的她们](https://www.bilibili.com/video/BV1bARXBYEZz/) — ZipZipPipe，2026-05-09。简介有愿意分享图片再创作的说明，但不应为全部角色推定统一标准许可证。
- [GPT小龙娘开始融入DeepSeek大家庭了（误）](https://www.bilibili.com/video/BV1EvKK6NEoi/) — 这个刀子真甜，2026-07-18。将女仆及龙女形象署为 ZipZipPipe。
- [gemini翻唱人是猫 猫娘收到谷歌命令](https://www.bilibili.com/video/BV1i6JR6AEuP/) — 桃莉鸭，2026-10-20。猫娘称呼与形象署名明确；歌曲及音源另有作者，不纳入图像授权推断。
- [只是一些Claude珂大小姐的anima lora showcase](https://www.bilibili.com/video/BV1wtaH6jEk8/) — Siling4040，2026-09-29。用于核验称呼存在，不核验 LoRA 训练素材。
- [好多鱼！哪条是大肥鱼？](https://www.bilibili.com/video/BV1jg866XEC8/) — 这个刀子真甜，2026-08-22。简介将 Kimi、Claude 形象署为 ZipZipPipe。
- [当全球AI娘聚在一起，会发生什么？](https://www.bilibili.com/video/BV1f7YM6BE1w/) — 土豆AX，2026-09-10。群像同人例证，形象署为 ZipZipPipe。

另通过 `x/polymer/web-dynamic/v1/detail?id=1231980045693616162` 核验 [ZipZipPipe 素材来源与使用声明](https://t.bilibili.com/1231980045693616162)，日期为 2026-08-02；声明限定鲸鱼娘分支。上善无形的 [动态入口](https://www.bilibili.com/opus/1231977657712771073) 可定位作者与日期，但正文未完整取得，因此不把这一步写成原始正文全部核验。

## 二手来源与不采用的推断

[AI 萌化百科](https://selinlee.github.io/ai-moe-atlas/zh/) 和 [ai-girls 清单](https://github.com/shuaizenge/ai-girls/blob/main/catalog.json) 帮助找到 [ZipZipPipe 的 Pixiv 合集](https://www.pixiv.net/artworks/148186519)；原作页本次不可完整读取。Llama 的第 14 张页码仅为清单线索，不标为独立看过原图。

[CrossPet](https://github.com/lokicorvus/crosspet) 主动说明 Grok 的部分性格由其项目二创；这类具体版本的署名比直接宣称“社区共识”更准确。[larcgpt 的人物企划](https://github.com/larcgpt/ai-model-musume/blob/main/settings.md) 是另一套独立设定，引用时保留企划归属，不合并为原设计者原设。

[游民星空社区观察](https://www.gamersky.com/news/202610/2222580.shtml) 仅用于了解前辈、猫系等角色解读。该文含不严谨的产品、厂商与能力概括，本项目没有把它们当作技术事实；也没有将它写的“公认”直接转述为跨社区共识。[17173 文章](https://news.17173.com/content/08212026/094421441.shtml) 仅用于记录白饭、摸鱼等传播梗，不代表其中模型日志传闻已复现。

未核实的内容包括：Creeper-北极之光每张初始参考图的具体上游、全部形象的原始发布时间、统一人格表、年龄、生日、身高、官方关系网以及逐张图像的完整授权状态。README 应保留用户已提供的直接贡献关系，并邀请原作者或贡献者补充可核验的原帖，不能因相似设计就断定其完整参考链。
