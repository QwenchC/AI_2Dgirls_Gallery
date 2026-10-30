# 中文社区调研记录 B

检索日期：2026-10-30（Asia/Shanghai）。覆盖 GLM、混元、MiniMax、Mistral、Qwen、Seed、文心，以及 Creeper-北极之光的公开出处。结构化结果见 [characters-b.json](characters-b.json)。

## 方法与证据边界

先逐角色检索中文名称、英文名称、娘／拟人／设定及 bilibili 限域词，再从中文角色索引和素材档案沿链接回到作者原帖。实际阅读了 B站动态、中文角色整理页和 GitHub 资料档案；部分 B站视频直接打开返回 HTTP 412，只能核对搜索引擎保存的标题、简介、日期和 UP 主信息。未声称完整观看这些视频。每条来源均在 JSON 的 `limits` 中注明读取方式与可支持的范围。

`community` 表示找到有关该角色的具体社区资料，不等于统一公认设定；`limited` 表示角色形象有线索，但完整背景和人格证据不足。本次不设置年龄、生日、身高或固定 CP。`projectSetting` 全部为本项目新编故事建议，不能作为原作者意见引用。

## 检索覆盖

| 角色 | 实际使用的主要检索词 | 结果 |
| --- | --- | --- |
| GLM | `site:bilibili.com GLM 智谱 拟人 娘`、`智谱娘`、`GLM ZipZipPipe` | 查到送鸡蛋、与鲸鱼娘互动的视频索引及狐耳形象资料页 |
| 混元 | `混元娘`、`混元 拟人 AI`、`site:bilibili.com 混元 ZipZipPipe` | 追到 ZipZipPipe 的 HY 娘设计自述 |
| MiniMax | `MiniMax 拟人`、`MiniMax娘`、`海螺娘 MiniMax` | 查到原作者群像、海螺娘称呼及造型档案 |
| Mistral | `Mistral 拟人`、`Mistral 娘`、`Mistral ZipZipPipe` | 查到作者群像、红帽金发分支；没有完整的一手性格表 |
| Qwen | `通义 娘 拟人`、`千问娘`、`鲸鱼娘 千问娘` | 查到代班剧情、造型档案及与 HY 娘呼应的设计自述 |
| Seed | `种子娘 AI`、`Seed 拟人 豆包`、`Seed ZipZipPipe` | 从非相关植物结果进一步追到作者的 Seed／豆包底模动态 |
| 文心 | `文心一言 娘`、`文心娘 轮椅`、`文心 ZipZipPipe` | 查到轮椅与书卷分支；未查实轮椅设计动机 |
| 初始参考图提供者 | `"Creeper-北极之光"`、`"Creeper" "北极之光" bilibili` | 未找到能唯一确认身份及本项目图像关系的公开结果 |

## 较强的一手线索

- [ZipZipPipe：是HY娘哦](https://www.bilibili.com/opus/1242184338245681157)，2026-08-30。可直接读取设计构思；富商之女、与千问呼应及企鹅轮廓均有作者文字支持。不是腾讯官方设定。
- [ZipZipPipe：AI娘第二批，有Seed（豆包底模）](https://www.bilibili.com/opus/1236803362705375305)，2026-08-15。可直接读取 Seed 的命名说明。发布日期不等于形象首创日期。
- [ZipZipPipe：7000粉贺图——小模型](https://www.bilibili.com/opus/1237178790069665792)，2026-08-16。作者直接点名 Mistral、MiniMax 等群像成员；没有给出完整性格表。
- [那就那就打断：智谱娘又送鸡蛋了](https://www.bilibili.com/video/BV1hLYR64EPH/)，2026-09-12。索引简介署名 ZipZipPipe、这个刀子真甜；原视频直接访问 412，因此只按索引记录。
- [追忆惘然_星梦：DeepSeek鲸鱼娘偷吃Token，还把工作外包给了Qwen？](https://www.bilibili.com/video/BV1u9us61EUf/)，2026-08-07。只把简介中的代班桥段当作这部同人作品的剧情。

## 用于追溯的整理入口

- [shuaizenge/ai-girls 素材档案](https://github.com/shuaizenge/ai-girls/blob/main/README.md)：有角色目录、原图与生成三视图区分、B站和 Pixiv 来源链。只用于定位原帖，未下载或复制其素材。
- [Gender Swap AI 中文角色图鉴](https://genderswapai.com/zh-CN/ai-gijinka)：各角色页提供造型摘要、作者署名和原帖入口。本次仅短篇转述识别特征，未复制其图片或设定全文。
- [各AI娘形象盘点](https://www.bilibili.com/video/BV14phK66Ejw/)，想看故事的lazy，2026-08-24：可读索引简介表示形象来自 ZipZipPipe，部分描述另指向 BV1Ey8B6QECx。后者未独立查实，不将其内容当已核实资料。

## 不采用或不扩大解释的结果

1. 搜到的同名代币、植物种子、混元生成拟人动物教程，都不是相关角色资料，已排除。
2. [larcgpt/ai-model-musume](https://github.com/larcgpt/ai-model-musume/blob/main/settings.md) 有中文详细角色企划，但多个外形与本馆参考图不同，属于另一套作者设定。未把其中舞台偶像、风衣特务等性格当成本馆分支的既定事实。
3. [游民星空的社区现象报道](https://www.gamersky.com/news/202610/2222580.shtml) 可作为传播背景线索，但文中有概括性评价、产品技术说法和调侃。本馆没有照搬为模型真实能力或统一人设。
4. 独立互动游戏、同人模组及小说的数值、身世、关系仅对各自作品成立，未合并为共同 canon。
5. 没有查实 Creeper-北极之光 的公开主页及上游参考链。按项目维护者提供的事实致谢即可：他提供了初始参考图；本仓库图片是维护者用 GPT 参考这些图生成的；更早来源待考。不把本次找到的作者原帖强行接在这条链上。

## 本馆图片核对

只读查看了七位角色的标准版 PNG，未改动原图。背景与场景建议沿用图中可见的衣饰和道具；网页资料中的不同版本保持区别。例如文心的医疗道具只按视觉元素记载，不推断疾病；Seed 与豆包玩偶的关系不自行写成血缘关系。
