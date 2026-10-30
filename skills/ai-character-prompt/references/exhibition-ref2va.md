# 单角色展览短片示例

这是本项目原创的短片练习，尚未执行生成。输入只有一张实际角色图，约 5 秒；角色向观众挥手，无对白，无 BGM。它保留所选图片的体型，不预设发色和服装。复杂动作、多人或音频参考应另行策划。

| 输入 | 标签 | 用途 |
| --- | --- | --- |
| 用户实际选中的角色图，第一图片槽 | `<Picture 1>` | 仅供人物身份、配色、服装、比例和画风参考 |

```text
subject_definitions:
<Subject 1> is the single anime character depicted in <Picture 1>. Preserve the selected version's face, hair shape and colors, eye colors, costume, accessories, distinctive silhouette, and body proportions. Any front, side, or rear views in that image describe one identity. They are design references and do not represent additional people.

summary:
[reference generation] Create an approximately five-second exhibition welcome clip featuring <Subject 1>. The character looks toward the viewer, blinks once, and gives a small friendly wave in one continuous shot. Use the reference for the character design while placing the character in a newly composed, quiet gallery interior.

retention_analysis:
<Subject 1> (appears in [Shot 1]): fully_preserved - retain the identity, selected body proportions, costume, accessories, and visual style defined by <Picture 1>. The neutral reference pose changes into the requested greeting action. The reference-sheet panels, captions, and color swatches are not part of the character and do not appear in the finished scene.

detailed_description:
The video follows the anime illustration style of the selected character reference. Soft, even indoor light keeps the face, clothing colors, and distinctive accessories easy to read.

[Shot 1] An eye-level medium-wide composition shows <Subject 1> standing alone slightly to the left of center in a quiet exhibition room. The camera includes the head, torso, and both hands, with enough empty space around the silhouette for the greeting to remain unobstructed. A pale wall and a low, unfurnished display plinth form a simple background. The environment has no readable signage, portraits, mirrors, or additional figures. The subject remains visually separated from the background throughout the shot.

At the opening, the character faces the camera with a relaxed, balanced posture. Both shoulders are level, the arms rest naturally, and the expression is calm and welcoming. The face, hairstyle, clothing structure, small accessories, and selected body proportions remain consistent with the identity shown in <Picture 1>. Preserve any distinctive visible design elements without treating another view of the same design as a second character.

During the first second, the character's eyes settle toward the lens and complete one natural blink. The head makes only a slight accompanying adjustment; the body stays in place. The camera begins a very gentle, short forward movement, keeping both hands inside the frame and avoiding a sudden change of viewing angle. Lighting stays steady, with soft shadows beneath the clothing folds.

Over the next two seconds, the character raises one hand to shoulder height with a smooth elbow bend. The palm turns toward the viewer. The hand makes two restrained side-to-side greeting motions while the other arm stays relaxed. Keep the hand attached to the same wrist, with a coherent silhouette and natural finger placement. Small fabric movements follow the arm motion, and loose hair or accessories respond subtly rather than changing shape or location.

During the remaining time, the waving motion eases to a stop. The raised hand lowers gently toward its resting position, and the character holds a soft smile toward the camera. The camera's forward motion also settles, ending on a stable view of the same person in the same room. The character does not speak, and the lips remain closed. The final moment retains a little stillness for the welcome gesture to feel complete, with no cut, fade, new action, or extra character arriving at the end.

overall_soundscape:
Quiet gallery room tone continues at a low level. A faint fabric rustle follows the raised arm and subsides when the character settles. There is no speech or singing.

non_diegetic_music:
N/A
```

语法依据：[MiniMax 官方 Ref2VA 规范](https://github.com/MiniMax-AI/MiniMax-H3/blob/main/.agents/skills/h3-prompt-writing/references/ref-en.txt)。正文场景、动作与镜头描述为本项目撰写，没有复制官方案例。实际生成前仍需检查图片内容、槽位顺序和工作流参数。
