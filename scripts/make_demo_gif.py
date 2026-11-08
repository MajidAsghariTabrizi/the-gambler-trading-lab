import os, subprocess
from PIL import Image, ImageDraw, ImageFont
out = subprocess.run(['python', 'demo_offline.py'], capture_output=True, text=True, cwd=os.path.join(os.path.dirname(__file__), '..'))
lines = [l for l in (out.stdout or '').splitlines() if l.strip()][:8]
W, H = 960, 40 + 26 * len(lines) + 20
frames = []
try:
    font = ImageFont.truetype('consola.ttf', 20)
except Exception:
    try: font = ImageFont.truetype('arial.ttf', 20)
    except Exception: font = ImageFont.load_default()
for step in range(1, len(lines) + 1):
    im = Image.new('RGB', (W, H), (12, 12, 12))
    dr = ImageDraw.Draw(im)
    dr.text((20, 14), 'python demo_offline.py', fill=(120, 200, 120), font=font)
    for i, l in enumerate(lines[:step]):
        dr.text((20, 44 + i * 26), l[:118], fill=(220, 220, 220), font=font)
    frames.append(im)
dst = os.path.join(os.path.dirname(__file__), '..', 'assets')
os.makedirs(dst, exist_ok=True)
frames[0].save(os.path.join(dst, 'demo_terminal.gif'), save_all=True, append_images=frames[1:], duration=650, loop=0)
print('GIF frames', len(frames))