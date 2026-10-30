# 提示词生成 Skill 指南

## 工具分工

| 工具 | 用途 |
| --- | --- |
| 官方 `h3-prompt-writing` | 指导智能体按 H3 模式编写提示词 |
| 本仓库 `ai-character-prompt` | 整理角色资料、体型、实际素材顺序与创作意图 |
| ComfyUI Prompt Rewriter | 可选的模型驱动提示词重写工具，依赖与用法以其项目文档为准 |

Skill 是供智能体阅读的指引，不是视频模型。图片由什么工具读取、是否联网，取决于创作者选择的服务与设置。本仓库页面仅生成文本简报。

## 官方入口

[MiniMax 官方 h3-prompt-writing](https://github.com/MiniMax-AI/MiniMax-H3/tree/main/.agents/skills/h3-prompt-writing) 将参考生成与基础模式分开处理。Ref2VA 对应 `references/ref-en.txt`；T2VA、I2VA、FL2VA、L2VA 对应 `references/base-en.txt`。可让支持读取文档的智能体按这些文件工作，或按上游提供的方式安装 Skill。[官方技能说明](https://github.com/MiniMax-AI/MiniMax-H3/blob/main/.agents/skills/h3-prompt-writing/SKILL.md)

需要节点自动扩写功能时，可查阅 [MiniMax-H3 Prompt Rewriter](https://github.com/pytraveler/MiniMax-H3-Prompt-Rewriter-ComfyUI)。它是独立工具，不是使用本图库或阅读辅助 Skill 的必要条件。

## 仓库辅助 Skill

打开 [SKILL.md](../skills/ai-character-prompt/SKILL.md)，向智能体提供实际角色图、体型、动作与成片要求。输出包括参考绑定表、提示词、中文检查说明。仓库还提供一个可离线阅读的 [单角色展览短片示例](../skills/ai-character-prompt/references/exhibition-ref2va.md)。

Ref2VA 使用以下六段式标记结构，不要求序列化为 JSON：

```text
subject_definitions:
summary:
retention_analysis:
detailed_description:
overall_soundscape:
non_diegetic_music:
```

正文使用英文；需要中文对白时保留原文并标注实际说话者。只提供一张图片时，不能凭空引用第二张图、视频或音频。更换素材顺序后，应同步检查所有标签。

## 图像与资料的取舍

- 外观依据实际图片，不根据品牌印象推断发色、服饰或体型。
- 三种体型分别使用，不把比例变化写成年龄变化。
- 多视图可以说明同一角色的不同角度；如需裁图，另存副本并保留辨识特征。
- 社区资料只支持对应作者表达过的内容，不自动代表全网共识。
- 本项目补充的职业、性格和背景作为创作建议使用，不虚构出处。
- 文本策划止于提示词交付，不自动上传素材或执行生成。

示例剧情由本项目编写，格式正确不等于效果保证。复杂音频复用、续写或模式转换，应继续阅读官方对应规范。
