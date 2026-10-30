# AI MUSE · AI 二次元拟人创作图鉴

一个给 AIGC 创作爱好者使用的离线角色展览与创作参考 Demo。收录 **14 位 AI 拟人角色、3 种体型、42 张多视图设定图**，配套带出处的社区资料、明确标识的二创设定、MiniMax H3 通用参考生成指引，以及提示词辅助 Skill。

## 打开展览

下载完整仓库后，用现代浏览器打开根目录的 **[index.html](index.html)**，或在 Windows 双击 **[打开展览.cmd](打开展览.cmd)**。不需要联网、Node.js、Python、账号或构建步骤。请保持整个目录一起移动；不要只复制 HTML 文件。

- 切换标准版、中间体型版、Q 版；搜索角色名、别名、颜色与风格关键词。
- 打开角色资料卡，阅读社区资料、本图视觉观察、本项目二创设定与逐条来源。
- 查看或下载原图；通过“用这个角色创作”把角色与体型带入创作工坊。
- 生成、编辑、复制或下载中文创作简报，再交给提示词 Skill 整理成 H3 提示词。
- 页面、图片、摘要和指南均在本地。只有主动点击外部来源链接才需要联网；页面不使用 CDN、远程字体、统计脚本或在线模型。

体型表示造型比例，不代表年龄。设定板展示的是同一角色的多个视角。创作时应说明不复刻拼版、文字与色卡；如有需要，另存单视角裁图，不覆盖原图。

## 角色与资料

| 角色 | 文字资料 | 角色 | 文字资料 |
| --- | --- | --- | --- |
| ChatGPT | [资料卡](docs/characters/chatgpt.md) | Kimi | [资料卡](docs/characters/kimi.md) |
| Claude | [资料卡](docs/characters/claude.md) | Llama | [资料卡](docs/characters/llama.md) |
| DeepSeek | [资料卡](docs/characters/deepseek.md) | MiniMax | [资料卡](docs/characters/minimax.md) |
| Gemini | [资料卡](docs/characters/gemini.md) | Mistral | [资料卡](docs/characters/mistral.md) |
| GLM / 智谱 | [资料卡](docs/characters/glm.md) | Qwen / 通义千问 | [资料卡](docs/characters/qwen.md) |
| Grok | [资料卡](docs/characters/grok.md) | Seed / 种子娘 | [资料卡](docs/characters/seed.md) |
| Hunyuan / 混元 | [资料卡](docs/characters/hunyuan.md) | Wenxin / 文心一言 | [资料卡](docs/characters/wenxin.md) |

研究日期为 **2026-10-30**，以中文社区和 bilibili 投稿、动态为主，辅以中文图鉴、作品索引及作者项目说明。来源汇总见 [sources.md](docs/sources.md)，检索过程与访问限制见 [A 组记录](research/research-a.md) 和 [B 组记录](research/research-b.md)。部分 B 站页面存在 412 或仅有搜索索引，已逐项标明；没有把搜索摘要当作完整原稿。

资料分三层：

1. **社区资料**：只说明某位作者或某个系列采用过的设定，并附证据范围。不同分支可以并存，不代表官方设定或全社区共识。
2. **本图视觉观察**：依据本仓库标准版图像记录可见元素；具体生成图与各体型可能有细节差异，以实际参考图为准。
3. **本项目二创设定**：为创作补充的职业、背景、性格、台词、关系与场景，均是本项目提案。展览中的称号和短句也属于此类。

角色设定属于拟人创作，不用于说明真实模型能力。社区来源记录了相关作品的创作表达，**不能直接证明当前图片的完整来源链或授权链**。

## AIGC 创作指引

- [完整创作指南](docs/creation-guide.md)：参考图整理、R2V 与 I2V 选择、MiniMax H3 流程与常见问题。
- [H3 工作流参考](docs/h3-workflow.md)：模式选择、参考绑定与通用参数检查。
- [提示词 Skill 指南](docs/prompt-skill-guide.md)：官方 Skill、仓库辅助 Skill 与 Prompt Rewriter 的区别。
- [ai-character-prompt / SKILL.md](skills/ai-character-prompt/SKILL.md)：可阅读、可分享的仓库内辅助技能。
- [离线 Ref2VA 示例](skills/ai-character-prompt/references/exhibition-ref2va.md)：原创单角色欢迎短片提示词，可按实际素材调整。

H3 教程依据公开上游资料编写，使用者需按所选版本准备模型和依赖，并自行验证生成结果。浏览器简报生成器仅拼接模板，不会识图、上传素材、调用模型或自动提交任务。

H3 Ref2VA 使用 `subject_definitions`、`summary`、`retention_analysis`、`detailed_description`、`overall_soundscape`、`non_diegetic_music` 六段式标记文本。它不是要求提交 JSON；I2V 等基础模式另有格式。外观与参考编号要依据实际输入，不凭文件名猜测。

## 致谢、来源与侵删

**特别感谢「Creeper-北极之光」为本项目提供初始形象图。**

本仓库中的 42 张图片，是项目维护者使用 GPT 参考 Creeper-北极之光提供的图片生成的，**不是将其提供的原图直接作为本仓库图片发布**。其提供的图片也可能参考了其他创作者的作品；这一更上游关系目前尚未完成考证，因此不将其表述为全部角色的首创者或唯一作者。

也感谢中文互联网、bilibili 及其他社区中参与这些 AI 拟人形象设计、二创、传播和资料整理的创作者。此次研究检索到了 ZipZipPipe、上善无形、这个刀子真甜等创作者的公开作品与声明；具体关联和证据范围见各角色资料。这里的研究署名不表示这些作者已确认参与当前图片的制作，也不表示已取得其对本项目的授权。

**侵删。** 如本仓库内容涉及您的作品或权益，请通过仓库 Issue 或直接联系项目维护者，提供涉及的文件、原始作品链接、署名及希望的处理方式。维护者会核实并及时更正、补充署名、调整展示或删除相关内容。无需提供无关个人身份材料。

**为这些形象做出贡献的创作者，欢迎联系我，在仓库中添加您的名字与贡献说明。** 可提供公开署名、作品链接、贡献类型（初始设计、二创、资料整理等）及适用的使用条件。请通过该仓库的 Issue 提交补充信息。

致谢与“侵删”不是授权替代品。原角色、品牌标识、上游作品与二创内容可能有不同的使用条件。本项目不对所有图片声明统一的 CC 或商业使用许可；有明示许可的具体分支应按其实际声明核对，不扩大到其他角色。例如调研发现的鲸鱼娘声明仅适用于其所述作品范围，详见 [DeepSeek 资料](docs/characters/deepseek.md)。本仓库没有附加一个覆盖全部图片和第三方内容的开源许可证。

## 文件结构与维护

```text
index.html / 打开展览.cmd   离线入口
assets/                    样式、交互代码、42 张衍生 WebP 预览
01_标准版/                 原始 PNG，原名原位置保留
02_中间体型版/             原始 PNG，原名原位置保留
03_Q版/                    原始 PNG，原名原位置保留
data/                      视觉观察、图片索引、工作流摘要、生成的页面数据
docs/characters/           14 份 Markdown 文字资料
docs/                      来源、使用说明与创作指南
research/                  研究输入、检索记录、公开元数据核验摘要
skills/ai-character-prompt/ 提示词辅助技能与离线示例
scripts/                   数据重建和完整性检查
```

页面以普通脚本加载本地数据，不使用 `fetch` 读取 JSON，便于 `file://` 直接打开。`data/gallery-data.json` 与 `.js` 由研究输入生成，修改角色资料请先编辑 `research/characters-*.json`，修改视觉观察请编辑 `data/visual-notes.json`，修改流程摘要请编辑 `data/workflow-guide.json`，然后重建。

普通浏览无需安装任何依赖。只有维护预览图时需要 Python 与 Pillow：

```powershell
python scripts/prepare_assets.py
python scripts/build_data.py
node scripts/verify.mjs
```

`prepare_assets.py` 生成衍生预览，`build_data.py` 生成页面数据与角色文字资料，`data/original-images.json` 用于验证分发图片的完整性。更多操作说明见[离线图鉴使用指南](docs/usage.md)。
