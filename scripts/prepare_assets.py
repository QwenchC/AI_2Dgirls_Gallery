"""Create offline previews; never change the supplied PNG originals."""
from pathlib import Path
from PIL import Image
import json

ROOT = Path(__file__).resolve().parents[1]
VARIANTS = [('standard', '01_标准版', '标准版'), ('medium', '02_中间体型版', '中间体型版'), ('chibi', '03_Q版', 'Q版')]
NAMES = {'chatgpt':'ChatGPT', 'claude':'Claude', 'deepseek':'DeepSeek', 'gemini':'Gemini', 'glm':'GLM_智谱', 'grok':'Grok', 'hunyuan':'Hunyuan_混元', 'kimi':'Kimi', 'llama':'Llama', 'minimax':'MiniMax', 'mistral':'Mistral', 'qwen':'Qwen_通义千问', 'seed':'Seed_种子娘', 'wenxin':'Wenxin_文心一言'}

def main():
    folder = ROOT / 'assets' / 'previews'
    folder.mkdir(parents=True, exist_ok=True)
    index = {}
    for slug, name in NAMES.items():
        index[slug] = {}
        for key, directory, suffix in VARIANTS:
            original = ROOT / directory / f'{name}_{suffix}.png'
            target = folder / f'{slug}-{key}.webp'
            with Image.open(original) as im:
                im.thumbnail((900, 675))
                im.convert('RGB').save(target, 'WEBP', quality=87, method=6)
            index[slug][key] = {'original': original.relative_to(ROOT).as_posix(), 'preview': target.relative_to(ROOT).as_posix()}
    (ROOT / 'data' / 'image-index.json').write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'Prepared {len(NAMES) * len(VARIANTS)} previews without modifying originals.')

if __name__ == '__main__':
    main()
