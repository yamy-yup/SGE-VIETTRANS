# Bộ dựng trang tĩnh cho website SGE Viettrans.
# Thư mục bắt đầu bằng dấu gạch dưới không được GitHub Pages xuất bản.
import json, re, html, os, urllib.parse, unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
BASE = 'https://yamy-yup.github.io/SGE-VIETTRANS/'   # đổi khi có tên miền riêng
PHONE = '0368757303'
PHONE_TXT = '0368 757 303'
EMAIL = 'sgexpress.6868@gmail.com'
FB = 'https://www.facebook.com/share/1CRS1PLvNv/'
TT = 'https://www.tiktok.com/@sge6868'
ZALO = 'https://zalo.me/0368757303'

SV = [('chuyen-nha-tron-goi', 'Chuyển nhà trọn gói'), ('chuyen-van-phong', 'Chuyển văn phòng'),
      ('cho-thue-xe-tai', 'Cho thuê xe tải'), ('boc-xep', 'Bốc xếp'), ('kho-bai-luu-tru', 'Kho bãi lưu trữ')]
PR = [('bang-gia-xe-tai', 'Bảng giá xe tải'), ('bang-gia-boc-xep', 'Bảng giá nhân công bốc xếp'),
      ('bang-gia-thao-lap', 'Bảng giá tháo lắp nội thất')]

PAGES = []  # (path, lastmod-priority) cho sitemap

_index = open(ROOT + 'index.html', encoding='utf8').read()
SPRITE = _index[_index.index('<svg width="0"'):_index.index('</svg>\n', _index.index('<svg width="0"')) + 7]
TOPBAR = _index[_index.index('<div class="top">'):_index.index('<header class="bar">')]


def slug(t):
    t = t.replace('Đ', 'D').replace('đ', 'd')
    t = unicodedata.normalize('NFD', t)
    t = ''.join(c for c in t if unicodedata.category(c) != 'Mn')
    return re.sub(r'[^a-z0-9]+', '-', t.lower()).strip('-')


def esc(t):
    return html.escape(t, quote=True)


def rel(depth):
    return '../' * depth


def nav(p, cur=''):
    chev = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="m6 9 6 6 6-6"/></svg>'
    def cu(k): return ' aria-current="page"' if cur == k else ''
    sv = ''.join(f'<li><a href="{p}{s}.html"{cu(s)}>{n}</a></li>' for s, n in SV)
    pr = ''.join(f'<li><a href="{p}{s}.html"{cu(s)}>{n}</a></li>' for s, n in PR)
    svc_cur = ' aria-current="true"' if cur == 'dich-vu' or cur in [s for s, _ in SV] else ''
    pr_cur = ' aria-current="true"' if cur == 'bang-gia' or cur in [s for s, _ in PR] else ''
    blog_cur = ' aria-current="true"' if cur == 'blog' else ''
    return f'''<nav class="nav" id="nav" aria-label="Menu chính">
      <a href="{p}index.html#gioi-thieu">Giới thiệu</a>
      <div class="dd">
        <a href="{p}dich-vu.html"{svc_cur}>Dịch vụ</a>
        <button class="dd-btn" type="button" aria-expanded="false" aria-label="Mở danh sách dịch vụ">{chev}</button>
        <ul class="dd-menu">{sv}</ul>
      </div>
      <a href="{p}index.html#phieu">Báo giá</a>
      <div class="dd">
        <a href="{p}bang-gia.html"{pr_cur}>Bảng giá</a>
        <button class="dd-btn" type="button" aria-expanded="false" aria-label="Mở danh sách bảng giá">{chev}</button>
        <ul class="dd-menu">{pr}</ul>
      </div>
      <a href="{p}blog.html"{blog_cur}>Blog</a>
      <a href="{p}index.html#lien-he">Liên hệ</a>
      <a class="btn" href="tel:{PHONE}">Gọi ngay</a>
    </nav>'''


def header(p, cur):
    return f'''{SPRITE}<a class="skip" href="#noi-dung">Bỏ qua đến nội dung chính</a>

{TOPBAR}<header class="bar">
  <div class="wrap">
    <a class="brand" href="{p}index.html" aria-label="SGE Viettrans, về trang chủ">
      <img src="{p}assets/logo.jpg" width="56" height="56" alt="Logo SGE Viettrans">
    </a>
    <a class="btn bar-call" href="tel:{PHONE}">Gọi ngay</a>
    <button class="menu-btn" type="button" id="menu-btn" aria-expanded="false" aria-controls="nav" aria-label="Mở menu">
      <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>
    </button>
    {nav(p, cur)}
  </div>
</header>
'''


def soc(cls, p=''):
    def ic(n, z=''): return f'<svg{z} aria-hidden="true"><use href="#i-{n}"/></svg>'
    return f'''<ul class="soc{cls}">
        <li><a href="{ZALO}" target="_blank" rel="noopener" style="--c:#0068ff" aria-label="Zalo {PHONE_TXT}">{ic('zalo',' class="z"')}</a></li>
        <li><a href="mailto:{EMAIL}" style="--c:#d52b2c" aria-label="Email {EMAIL}">{ic('mail')}</a></li>
        <li><a href="{FB}" target="_blank" rel="noopener" style="--c:#0866ff" aria-label="Facebook SGE Viettrans">{ic('facebook')}</a></li>
        <li><a href="{TT}" target="_blank" rel="noopener" style="--c:#111" aria-label="TikTok SGE Viettrans">{ic('tiktok')}</a></li>
      </ul>'''


def footer(p):
    sv = ''.join(f'<li><a href="{p}{s}.html">{n}</a></li>' for s, n in SV)
    return f'''<footer>
  <div class="wrap">
    <div class="f-main">
      <div class="f-brand">
        <img src="{p}assets/logo.jpg" width="64" height="64" alt="" loading="lazy">
        <div><p>CÔNG TY TNHH THƯƠNG MẠI DỊCH VỤ VẬN TẢI SGE VIETTRANS. Số 1B, Đường 30, Khu phố 21, Phường An Khánh, TP. Hồ Chí Minh, Việt Nam.</p>
        {soc(' soc-foot')}
        </div>
      </div>
      <div>
        <h3>Dịch vụ</h3>
        <ul>{sv}</ul>
      </div>
      <div>
        <h3>Liên hệ</h3>
        <ul>
          <li><a href="tel:{PHONE}">{PHONE_TXT}</a></li>
          <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
          <li><a href="{ZALO}" target="_blank" rel="noopener">Zalo</a></li>
          <li><a href="{FB}" target="_blank" rel="noopener">Facebook</a></li>
          <li><a href="{TT}" target="_blank" rel="noopener">TikTok</a></li>
          <li><a href="{p}bang-gia.html">Bảng giá</a></li>
          <li><a href="{p}blog.html">Blog</a></li>
          <li><a href="{p}index.html#hoi-dap">Câu hỏi thường gặp</a></li>
        </ul>
      </div>
    </div>
    <div class="f-legal">
      <span>© <span id="year">2026</span> SGE Viettrans. Một chữ tín - Vạn niềm tin.</span>
      <a href="#top">Lên đầu trang</a>
    </div>
  </div>
</footer>'''


ORG = {
    "@type": "MovingCompany", "@id": BASE + "#org",
    "name": "Công ty TNHH Thương mại Dịch vụ Vận tải SGE Viettrans", "alternateName": "SGE Viettrans",
    "url": BASE, "logo": BASE + "assets/logo.jpg", "image": BASE + "assets/hero.jpg",
    "telephone": "+84368757303", "email": EMAIL, "slogan": "Một chữ tín - Vạn niềm tin",
    "address": {"@type": "PostalAddress", "streetAddress": "Số 1B, Đường 30, Khu phố 21", "addressLocality": "Phường An Khánh",
                "addressRegion": "TP. Hồ Chí Minh", "addressCountry": "VN"},
    "areaServed": ["TP. Hồ Chí Minh", "Bình Dương", "Long An", "Biên Hòa"],
    "sameAs": [FB, TT]
}


def breadcrumb_ld(items):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": BASE + u} for i, (u, n) in enumerate(items)]}


def crumb_html(items, p):
    out = []
    for i, (u, n) in enumerate(items):
        out.append(f'<span>{n}</span>' if i == len(items) - 1 else f'<a href="{p}{u}">{n}</a>')
    return '<nav class="crumb" aria-label="Đường dẫn">' + ' <span aria-hidden="true">/</span> '.join(out) + '</nav>'


def faq_html(qa):
    return '<div class="faq-list">' + ''.join(
        f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in qa) + '</div>'


def faq_ld(qa):
    strip = lambda s: re.sub('<[^>]+>', '', s)
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": strip(q), "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a in qa]}


def page(path, title, desc, body, cur='', ld=None, og_image='assets/hero.jpg', og_type='website', priority='0.6'):
    depth = path.count('/')
    p = rel(depth)
    url = BASE + ('' if path == 'index.html' else path)
    graph = [ORG] + (ld or [])
    ldjson = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1)
    doc = f'''<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="#184e94">
<meta property="og:type" content="{og_type}">
<meta property="og:locale" content="vi_VN">
<meta property="og:site_name" content="SGE Viettrans">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE}{og_image}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/jpeg" href="{p}assets/logo.jpg">
<link rel="preload" href="{p}assets/fonts/montserrat.woff" as="font" type="font/woff" crossorigin>
<link rel="preload" href="{p}assets/fonts/bevietnam-Regular.woff" as="font" type="font/woff" crossorigin>
<link rel="stylesheet" href="{p}assets/style.css">
<script type="application/ld+json">
{ldjson}
</script>
</head>
<body>
{header(p, cur)}
<main id="noi-dung">
{body}
</main>

{footer(p)}

<script src="{p}assets/site.js" defer></script>
</body>
</html>
'''
    os.makedirs(os.path.dirname(ROOT + path) or ROOT, exist_ok=True)
    open(ROOT + path, 'w', encoding='utf8').write(doc)
    PAGES.append((path, priority))
    return doc


def aside_cta(p, heading, svc_name, extra=''):
    q = p + 'index.html?dv=' + urllib.parse.quote(svc_name) + '#phieu'
    return f'''<aside class="aside" aria-label="Liên hệ">
    <h2>{heading}</h2>
    <p>Tư vấn và báo giá 24/7, gọi là có người nghe máy.</p>
    <a class="call" href="tel:{PHONE}">{PHONE_TXT}</a>
    <a class="btn" href="{q}">Lập phiếu báo giá</a>
    <a class="btn btn-ghost" href="{ZALO}" target="_blank" rel="noopener">Nhắn Zalo</a>
    {extra}
  </aside>'''


def write_sitemap(today):
    urls = ''.join(
        f'<url><loc>{BASE}{"" if p == "index.html" else p}</loc><lastmod>{today}</lastmod><priority>{pr}</priority></url>\n'
        for p, pr in [('index.html', '1.0')] + PAGES)
    open(ROOT + 'sitemap.xml', 'w', encoding='utf8').write(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + '</urlset>\n')
    open(ROOT + 'robots.txt', 'w', encoding='utf8').write(f'User-agent: *\nAllow: /\n\nSitemap: {BASE}sitemap.xml\n')
