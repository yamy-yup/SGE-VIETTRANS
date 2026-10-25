# Tạo ảnh nhiều kích thước (WebP + JPG dự phòng) cho trang web.
# Ảnh gốc chất lượng cao nằm trong _tools/masters/ (ảnh chụp) và _tools/_render/ (ảnh bìa, infographic).
import os, json, sys
from PIL import Image, ImageFilter
sys.path.insert(0, os.path.dirname(__file__))
from engine import ROOT

MANIFEST = ROOT + '_tools/variants.json'


def make(src_path, out_base, widths, jpg_w, q_webp=80, q_jpg=84):
    """out_base: đường dẫn trong web không có đuôi, ví dụ 'assets/hero'."""
    im = Image.open(src_path).convert('RGB')
    W, H = im.size
    webp = []
    for w in sorted(set(min(w, W) for w in widths)):
        h = round(H * w / W)
        r = im if w == W else im.resize((w, h), Image.LANCZOS)
        if w < W:
            r = r.filter(ImageFilter.UnsharpMask(radius=0.8, percent=40, threshold=2))
        p = f'{out_base}-{w}.webp'
        r.save(ROOT + p, 'WEBP', quality=q_webp, method=6)
        webp.append([w, p])
    jw = min(jpg_w, W); jh = round(H * jw / W)
    (im if jw == W else im.resize((jw, jh), Image.LANCZOS)).save(ROOT + out_base + '.jpg', quality=q_jpg, optimize=True, progressive=True)
    return {'w': jw, 'h': jh, 'ratio': [W, H], 'webp': webp, 'jpg': out_base + '.jpg'}


def load():
    try:
        return json.load(open(MANIFEST))
    except Exception:
        return {}


def save(m):
    json.dump(m, open(MANIFEST, 'w'), indent=1, ensure_ascii=False)


if __name__ == '__main__':
    m = load()
    m['assets/hero.jpg'] = make(ROOT + '_tools/masters/hero.jpg', 'assets/hero', [640, 1024, 1600, 2304], 1600)
    m['assets/band.jpg'] = make(ROOT + '_tools/masters/band.jpg', 'assets/band', [768, 1280, 2304], 1600)
    m['assets/truck.jpg'] = make(ROOT + '_tools/masters/truck.jpg', 'assets/truck', [534, 1068], 1068)
    save(m)
    print('ok', list(m))
