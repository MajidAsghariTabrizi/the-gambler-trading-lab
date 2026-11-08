import os
try:
    from PIL import Image, ImageDraw, ImageFont
    W, H = 1280, 640
    bg = (13, 27, 42); fg = (227, 232, 238); accent = (42, 111, 151)
    im = Image.new('RGB', (W, H), bg)
    dr = ImageDraw.Draw(im)
    try:
        big = ImageFont.truetype('arial.ttf', 74)
        med = ImageFont.truetype('arial.ttf', 40)
        small = ImageFont.truetype('arial.ttf', 26)
    except Exception:
        big = med = small = ImageFont.load_default()
    dr.rectangle([0, 0, 16, H], fill=accent)
    dr.text((70, 120), 'THE GAMBLER', font=big, fill=fg)
    dr.text((70, 230), 'The Trading AI That Knows', font=med, fill=(144, 180, 206))
    dr.text((70, 285), 'When NOT to Trade.', font=med, fill=(144, 180, 206))
    dr.line([70, 400, 700, 400], fill=accent, width=3)
    dr.text((70, 430), '10,478 audited decision minutes. Zero trades. Every one justified.', font=small, fill=fg)
    dr.text((70, 470), 'Best signal +1.55 bps.  Round-trip cost 78.36 bps.', font=small, fill=fg)
    dr.text((70, 510), 'Evidence-graded. Fail-closed. Live trading OFF by design.', font=small, fill=(144, 180, 206))
    out = os.path.join(os.path.dirname(__file__), '..', 'assets')
    os.makedirs(out, exist_ok=True)
    im.save(os.path.join(out, 'social_preview_1280x640.png'))
    print('PIL_OK')
except ImportError:
    print('PIL_ABSENT')