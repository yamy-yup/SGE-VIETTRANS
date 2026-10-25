# Dựng toàn bộ trang con: dịch vụ, bảng giá, khu vực, blog, sitemap.
# Chạy từ thư mục gốc web: python3 _tools/build.py
import sys, os, re, datetime, hashlib
sys.path.insert(0, os.path.dirname(__file__))
from engine import *
from content_services import SERVICES
from content_areas import AREAS, INTRO, WHY, NOTE
from content_blog import POSTS

TODAY = datetime.date.today().isoformat()
INC_IDX = {'chuyen-nha-tron-goi': 1, 'chuyen-van-phong': 1, 'cho-thue-xe-tai': 0, 'boc-xep': 0, 'kho-bai-luu-tru': 1, 'chuyen-nha-lien-tinh': 1, 'chuyen-kho-xuong': 1}
from content_routes import ROUTES
ROUTE_LIST = [(slug(r), r, km, d) for r, km, d in ROUTES]
POST_BY = {p['slug']: p for p in POSTS}
AREA_LIST = [(slug(a), a, k, d) for a, k, d in AREAS]


def lower1(s): return s[0].lower() + s[1:]


def steps_li(steps):
    return ''.join(f'<li><b>{a}</b>{b}</li>' for a, b in steps)


def img(p, src, alt, w, h, cls='fig', lazy=True, caption=''):
    srcset = ''
    if src == 'assets/hero.jpg':
        srcset = f' srcset="{p}assets/hero-s.jpg 1100w, {p}assets/hero.jpg 2000w" sizes="(max-width: 1000px) 100vw, 60vw"'
    cap = f'<figcaption>{caption}</figcaption>' if caption else ''
    return (f'<figure class="{cls}"><img src="{p}{src}"{srcset} width="{w}" height="{h}" alt="{esc(alt)}"'
            f'{" loading=\"lazy\"" if lazy else ""} decoding="async">{cap}</figure>')


def fill(html, p, d=None, sv=None):
    html = html.replace('{p}', p)
    if d is not None:
        html = html.replace('{steps_li}', steps_li(d['steps']))
        html = html.replace('{steps_img}', img(p, f'assets/blog/quy-trinh-{sv}.jpg', f'Quy trình {lower1(d["name"])} của SGE Viettrans', 1200, 600))
        html = html.replace('{routes}', route_chips(p))
        html = html.replace('{truck_img}', img(p, 'assets/blog/chon-xe.jpg', 'Bảng chọn xe van, xe tải nhỏ, xe tải lớn theo lượng đồ', 1200, 580))
    def rep(m):
        n = m.group(1)
        alt = {'lich-chuan-bi': 'Lịch chuẩn bị chuyển nhà theo 4 mốc thời gian', 'dong-goi-de-vo': 'Bốn bước đóng gói đồ dễ vỡ',
               'gio-cam-xe-tai': 'Biểu đồ giờ cấm xe tải nội thành TP.HCM theo tải trọng', 'chon-xe': 'Bảng chọn xe tải theo lượng đồ',
               'checklist-van-phong': 'Năm bước chuyển văn phòng', 'tu-lanh-may-giat': 'Cách vận chuyển tủ lạnh, máy giặt, máy lạnh', 'lien-tinh': 'Bốn việc cần nhớ khi chuyển nhà liên tỉnh'}[n]
        hh = {'lich-chuan-bi': 560, 'dong-goi-de-vo': 600, 'gio-cam-xe-tai': 560, 'chon-xe': 580, 'checklist-van-phong': 560, 'tu-lanh-may-giat': 600, 'lien-tinh': 520}[n]
        return img(p, f'assets/blog/{n}.jpg', alt, 1200, hh)
    return re.sub(r'\{img:([a-z0-9-]+)\}', rep, html)


def area_chips(p, sv, cur=None):
    def chip(s, a):
        if s == cur:
            return f'<li><span aria-current="page">{a}</span></li>'
        return f'<li><a href="{p}{sv}/{s}.html">{a}</a></li>'
    h = ''.join(chip(s, a) for s, a, k, d in AREA_LIST if k != 'lan')
    n = ''.join(chip(s, a) for s, a, k, d in AREA_LIST if k == 'lan')
    return f'<h3>TP. Hồ Chí Minh</h3><ul class="areas">{h}</ul><h3>Bình Dương, Long An, Biên Hòa</h3><ul class="areas">{n}</ul>'


def route_chips(p, cur=None):
    def chip(s, r):
        if s == cur:
            return f'<li><span aria-current="page">TP.HCM – {r}</span></li>'
        return f'<li><a href="{p}chuyen-nha-lien-tinh/{s}.html">TP.HCM – {r}</a></li>'
    return '<ul class="areas">' + ''.join(chip(s, r) for s, r, km, d in ROUTE_LIST) + '</ul>'


def related_posts(p, slugs, limit=3, exclude=None):
    out = sorted([q for q in POSTS if q['slug'] != exclude and any(s in q['svc'] for s in slugs)],
                 key=lambda q: min(slugs.index(s) if s in slugs else 9 for s in q['svc']))[:limit]
    if len(out) < limit:
        out += [q for q in POSTS if q not in out and q['slug'] != exclude][:limit - len(out)]
    return '<ul class="rel">' + ''.join(
        f'<li><a href="{p}blog/{q["slug"]}.html"><img src="{p}assets/blog/cover-{q["slug"]}.jpg" width="1200" height="630" alt="" loading="lazy"><span>{q["h1"]}</span></a></li>'
        for q in out) + '</ul>'


def toc(sections):
    return '<nav class="toc-box" aria-label="Mục lục"><b>Nội dung chính</b><ol>' + ''.join(
        f'<li><a href="#m{i+1}">{h}</a></li>' for i, (h, _) in enumerate(sections)) + '</ol></nav>'


# ---------------- Trang dịch vụ ----------------
def build_services():
    for sv, name in SV:
        d = SERVICES[sv]; p = ''
        lt = sv == 'chuyen-nha-lien-tinh'
        secs = d['sections'] + [('Câu hỏi thường gặp', None)] + ([] if lt else [('Khu vực phục vụ', None)])
        body_secs = ''
        for i, (h, html) in enumerate(d['sections']):
            body_secs += f'<section id="m{i+1}"><h2>{h}</h2>{fill(html, p, d, sv)}</section>\n'
        n = len(d['sections'])
        faq = [(q, a.replace('{p}', p)) for q, a in d['faq']]
        body_secs += f'<section id="m{n+1}"><h2>Câu hỏi thường gặp về {lower1(name)}</h2>{faq_html(faq)}</section>\n'
        if not lt: body_secs += f'<section id="m{n+2}" class="area-sec"><h2>{name} theo khu vực</h2><p>Chọn khu vực của bạn để xem chi tiết dịch vụ {lower1(name)} tại đó.</p>{area_chips(p, sv)}</section>'
        im = d['img']
        rel = ''.join(f'<li><a href="{s}.html">{nm}</a></li>' for s, nm in SV if s != sv)
        extra = (f'<a class="more" href="{d["price"]}.html">Xem {dict(PR)[d["price"]].lower()}</a>' if d['price'] else '')
        body = f'''<section class="page-head"><div class="wrap">{crumb_html([("index.html", "Trang chủ"), ("dich-vu.html", "Dịch vụ"), (sv + ".html", name)], p)}
<h1>{d["h1"]}</h1><p class="lead">{d["lead"]}</p>
<div class="head-act"><a class="btn" href="tel:{PHONE}">Gọi {PHONE_TXT}</a><a class="btn btn-ghost" href="index.html?dv={urllib.parse.quote(name)}#phieu">Lập phiếu báo giá</a></div></div></section>
<section class="detail"><div class="wrap grid">
  <article class="prose">
    {img(p, im[0], im[1], im[2], im[3], 'fig fig-wide' if im[2]/im[3] < 2.5 else 'fig', lazy=False)}
    {toc(secs)}
    {body_secs}
  </article>
  <div class="side">
  {aside_cta(p, "Nhận báo giá " + lower1(name), name, extra)}
  <div class="side-box"><h2>Dịch vụ khác</h2><ul class="side-links">{rel}</ul></div>
  <div class="side-box"><h2>Bài viết hữu ích</h2>{related_posts(p, [sv])}</div>
  </div>
</div></section>'''
        ld = [breadcrumb_ld([("", "Trang chủ"), ("dich-vu.html", "Dịch vụ"), (sv + ".html", name)]),
              {"@type": "Service", "name": name, "serviceType": name, "provider": {"@id": BASE + "#org"},
               "areaServed": (["TP. Hồ Chí Minh"] + [r for _, r, _, _ in ROUTE_LIST]) if lt else ["TP. Hồ Chí Minh", "Bình Dương", "Long An", "Biên Hòa"], "description": d['desc'], "url": BASE + sv + '.html'},
              faq_ld(faq)]
        page(sv + '.html', d['title'], d['desc'], body, cur=sv, ld=ld, og_image=im[0], priority='0.9')


# ---------------- Trang khu vực ----------------
def build_areas():
    for sv, name in SV:
        if sv == 'chuyen-nha-lien-tinh':
            continue
        d = SERVICES[sv]
        inc = re.search(r'<ul>.*?</ul>', d['sections'][INC_IDX[sv]][1], re.S).group(0)
        for i, (s, a, kind, desc) in enumerate(AREA_LIST):
            p = '../'
            k = int(hashlib.md5((sv + s).encode()).hexdigest(), 16)
            svc = lower1(name)
            intro = INTRO[k % len(INTRO)].format(svc=svc, area=a)
            why = WHY[(k // 7) % len(WHY)]
            note = NOTE[kind].format(area=a, p=p)
            region = '' if kind == 'lan' else ', TP. Hồ Chí Minh'
            faq = [
                (f'Giá {svc} ở {a} tính như thế nào?', f'Giá phụ thuộc vào khối lượng đồ, quãng đường, số tầng, thang máy và đường vào nhà. SGE Viettrans báo giá rõ trước khi làm. Bạn có thể xem <a href="{p}bang-gia.html">bảng giá</a> hoặc gọi {PHONE_TXT}.'),
                (f'{a} có bị cấm giờ xe tải không?', NOTE[kind].format(area=a, p=p) if kind != 'lan' else f'Tuyến {a} đi vào nội thành TP. Hồ Chí Minh phải theo giờ cấm xe tải của thành phố. Chúng tôi xếp giờ xe chạy phù hợp với cả hai đầu tuyến.'),
                (f'Tôi cần cung cấp gì để được báo giá {svc} {a}?', 'Địa chỉ đi và đến, danh sách đồ hoặc hàng hóa, số tầng, có thang máy không và ngày giờ dự kiến. Gửi kèm ảnh qua Zalo sẽ giúp báo giá sát hơn.'),
            ]
            if kind == 'lan':
                faq.append((f'Có nhận {svc} từ {a} về TP. Hồ Chí Minh và ngược lại không?', f'Có. SGE Viettrans nhận cả chiều từ {a} về TP. Hồ Chí Minh và từ TP. Hồ Chí Minh đi {a}.'))
            body = f'''<section class="page-head"><div class="wrap">{crumb_html([("index.html", "Trang chủ"), ("dich-vu.html", "Dịch vụ"), (sv + ".html", name), (f"{sv}/{s}.html", a)], p)}
<h1>{name} {a}</h1><p class="lead">{intro} Tư vấn và báo giá 24/7: <a href="tel:{PHONE}">{PHONE_TXT}</a>.</p></div></section>
<section class="detail"><div class="wrap grid">
  <article class="prose">
    <section><h2>{name} tại {a}{region}</h2><p>{desc}</p><p>{note}</p>
    {"" if kind == "lan" else '<p class="pg-note">Từ 01/07/2025 TP. Hồ Chí Minh không còn cấp quận, huyện. Chúng tôi dùng tên cũ cho dễ tìm và nhận đơn ở tất cả các phường thuộc khu vực này.</p>'}</section>
    <section><h2>{name} {a} gồm những gì</h2>{inc}</section>
    <section><h2>Vì sao chọn SGE Viettrans</h2><ul>{"".join(f"<li>{w}</li>" for w in why)}</ul></section>
    <section><h2>Quy trình {svc} tại {a}</h2>{img(p, f"assets/blog/quy-trinh-{sv}.jpg", f"Quy trình {svc} của SGE Viettrans", 1200, 600)}<ol class="mini-steps">{steps_li(d["steps"])}</ol></section>
    <section><h2>Câu hỏi thường gặp về {svc} {a}</h2>{faq_html(faq)}</section>
    <section class="area-sec"><h2>{name} ở khu vực khác</h2>{area_chips(p, sv, s)}</section>
  </article>
  <div class="side">
  {aside_cta(p, f"Báo giá {svc} {a}", name, f'<a class="more" href="{p}{sv}.html">Về dịch vụ {svc}</a>')}
  <div class="side-box"><h2>Bài viết hữu ích</h2>{related_posts(p, [sv], 2)}</div>
  </div>
</div></section>'''
            title = f'{name} {a} – Báo giá nhanh 24/7 | SGE Viettrans'
            if len(title) > 65:
                title = f'{name} {a} | SGE Viettrans'
            dsc = f'{name} tại {a}{region}: nhân viên đồng phục, xe tải thùng SGE, báo giá rõ trước khi làm. Tư vấn 24/7, gọi {PHONE_TXT}.'
            ld = [breadcrumb_ld([("", "Trang chủ"), ("dich-vu.html", "Dịch vụ"), (sv + ".html", name), (f"{sv}/{s}.html", a)]),
                  {"@type": "Service", "name": f"{name} {a}", "serviceType": name, "provider": {"@id": BASE + "#org"},
                   "areaServed": a, "url": f"{BASE}{sv}/{s}.html"}, faq_ld(faq)]
            page(f'{sv}/{s}.html', title, dsc, body, cur=sv, ld=ld, priority='0.6')


# ---------------- Tuyến liên tỉnh ----------------
def build_routes():
    sv, name = 'chuyen-nha-lien-tinh', 'Chuyển nhà liên tỉnh'
    d = SERVICES[sv]; p = '../'
    inc = re.search(r'<ul>.*?</ul>', d['sections'][1][1], re.S).group(0)
    for s, r, km, desc in ROUTE_LIST:
        faq = [
            (f'Chuyển nhà TP.HCM đi {r} giá bao nhiêu?', f'Giá phụ thuộc quãng đường ({km}), khối lượng đồ và dịch vụ đi kèm như đóng gói, tháo lắp. SGE Viettrans báo giá trọn chuyến trước khi đi, gọi {PHONE_TXT}.'),
            (f'Có nhận chuyển nhà từ {r} về TP. Hồ Chí Minh không?', f'Có. Chúng tôi nhận cả chiều TP. Hồ Chí Minh đi {r} và {r} về TP. Hồ Chí Minh.'),
            (f'Chuyển nhà đi {r} mất bao lâu?', 'Phụ thuộc lịch xe và khối lượng đồ. Khi đặt lịch, chúng tôi báo rõ ngày đi và ngày giao dự kiến.'),
            ('Tôi cần chuẩn bị gì?', 'Danh sách đồ, địa chỉ hai đầu, tầng và đường vào nhà, ngày mong muốn. Giấy tờ, tiền, trang sức nên mang theo người.'),
        ]
        body = f'''<section class="page-head"><div class="wrap">{crumb_html([("index.html", "Trang chủ"), ("dich-vu.html", "Dịch vụ"), (sv + ".html", name), (f"{sv}/{s}.html", "TP.HCM – " + r)], p)}
<h1>Chuyển nhà TP.HCM đi {r}</h1><p class="lead">Chuyển nhà, chở đồ từ TP. Hồ Chí Minh đi {r} và ngược lại: đóng gói kỹ cho đường dài, xe tải thùng, báo giá trọn chuyến trước khi đi. Gọi <a href="tel:{PHONE}">{PHONE_TXT}</a>.</p></div></section>
<section class="detail"><div class="wrap grid">
  <article class="prose">
    <section><h2>Tuyến TP. Hồ Chí Minh – {r}</h2><p>Quãng đường {km} (tham khảo). {desc}</p></section>
    <section><h2>Dịch vụ chuyển nhà đi {r} gồm những gì</h2>{inc}</section>
    <section><h2>Kinh nghiệm chuyển nhà đi {r}</h2>{img(p, "assets/blog/lien-tinh.jpg", "Bốn việc cần nhớ khi chuyển nhà liên tỉnh", 1200, 520)}
    <p>Đọc thêm <a href="{p}blog/kinh-nghiem-chuyen-nha-lien-tinh.html">kinh nghiệm chuyển nhà liên tỉnh, Bắc Nam</a>.</p></section>
    <section><h2>Quy trình</h2><ol class="mini-steps">{steps_li(d["steps"])}</ol></section>
    <section><h2>Câu hỏi thường gặp về chuyển nhà đi {r}</h2>{faq_html(faq)}</section>
    <section class="area-sec"><h2>Các tuyến khác</h2>{route_chips(p, s)}</section>
  </article>
  <div class="side">
  {aside_cta(p, f"Báo giá chuyển nhà đi {r}", name, f'<a class="more" href="{p}{sv}.html">Về dịch vụ chuyển nhà liên tỉnh</a>')}
  <div class="side-box"><h2>Bài viết hữu ích</h2>{related_posts(p, [sv, "chuyen-nha-tron-goi"], 3)}</div>
  </div>
</div></section>'''
        ld = [breadcrumb_ld([("", "Trang chủ"), ("dich-vu.html", "Dịch vụ"), (sv + ".html", name), (f"{sv}/{s}.html", "TP.HCM – " + r)]),
              {"@type": "Service", "name": f"Chuyển nhà TP.HCM đi {r}", "serviceType": name, "provider": {"@id": BASE + "#org"}, "areaServed": ["TP. Hồ Chí Minh", r], "url": f"{BASE}{sv}/{s}.html"},
              faq_ld(faq)]
        page(f'{sv}/{s}.html', f'Chuyển nhà TPHCM đi {r} trọn gói | SGE Viettrans',
             f'Chuyển nhà, chở đồ TP.HCM đi {r} và ngược lại: đóng gói kỹ, xe tải thùng, báo giá trọn chuyến. Tư vấn 24/7, gọi {PHONE_TXT}.',
             body, cur=sv, ld=ld, priority='0.7')


# ---------------- Trang chủ: đồng bộ menu và chân trang ----------------
def sync_index():
    s = open(ROOT + 'index.html', encoding='utf8').read()
    a = s.index('<nav class="nav"'); b = s.index('</nav>', a) + 6
    n = nav('', '').replace('href="index.html#', 'href="#')
    s = s[:a] + n + s[b:]
    a = s.index('<footer>'); b = s.index('</footer>') + 9
    s = s[:a] + footer('').replace('href="index.html#', 'href="#') + s[b:]
    open(ROOT + 'index.html', 'w', encoding='utf8').write(s)


def build_404():
    body = f'''<section class="page-head"><div class="wrap"><h1>Không tìm thấy trang</h1>
<p class="lead">Trang bạn tìm có thể đã đổi địa chỉ. Hãy quay về trang chủ, xem các dịch vụ hoặc gọi ngay {PHONE_TXT} để được hỗ trợ.</p>
<div class="head-act"><a class="btn" href="index.html">Về trang chủ</a><a class="btn btn-ghost" href="dich-vu.html">Xem dịch vụ</a><a class="btn btn-ghost" href="tel:{PHONE}">Gọi {PHONE_TXT}</a></div></div></section>'''
    doc = page('404.html', 'Không tìm thấy trang | SGE Viettrans', 'Trang không tồn tại.', body)
    PAGES.pop()
    doc = doc.replace('<head>', '<head>\n<base href="/SGE-VIETTRANS/">', 1).replace('content="index, follow, max-image-preview:large"', 'content="noindex"')
    open(ROOT + '404.html', 'w', encoding='utf8').write(doc)


# ---------------- Bảng giá ----------------
PRD = {
 'bang-gia-xe-tai': dict(lead='Bảng giá thuê xe tải chở hàng, chuyển đồ tại TP. Hồ Chí Minh: xe van, xe tải nhỏ, xe tải lớn mang thương hiệu SGE, có tài xế.',
   items=['Xe van', 'Xe tải nhỏ', 'Xe tải lớn'], basis='Quãng đường và thời gian thuê', svc='cho-thue-xe-tai',
   note='Giá thuê xe chưa gồm nhân công bốc xếp nếu bạn không chọn thêm dịch vụ này.',
   factors=['Loại xe và tải trọng.', 'Quãng đường: trong quận, liên quận hay đi tỉnh.', 'Thời gian thuê và thời gian chờ.', 'Khung giờ chạy, nhất là khi xe lớn phải chạy đêm trong nội thành.'],
   faq=[('Giá thuê xe có gồm tài xế không?', 'Có, xe cho thuê có tài xế của SGE Viettrans.'), ('Có phát sinh phí khi chờ bốc hàng lâu không?', 'Thời gian chờ được tính vào báo giá. Hãy mô tả đầy đủ công việc để chúng tôi báo giá trọn chuyến, tránh phát sinh.')]),
 'bang-gia-boc-xep': dict(lead='Bảng giá nhân công bốc xếp đồ gia dụng, đồ văn phòng, hàng hóa và đồ nặng tại TP. Hồ Chí Minh.',
   items=['Bốc xếp đồ gia dụng', 'Bốc xếp văn phòng', 'Bốc xếp hàng hóa, hàng nặng'], basis='Khối lượng đồ và số người', svc='boc-xep',
   note='Giá tính theo khối lượng đồ, số tầng và có thang máy hay không.',
   factors=['Khối lượng và loại hàng.', 'Số người cần.', 'Số tầng, có thang máy hay không.', 'Khoảng cách từ chỗ để đồ ra xe.'],
   faq=[('Có thuê nhân công theo giờ được không?', 'Hãy mô tả công việc, chúng tôi sẽ báo giá theo cách tính phù hợp nhất với bạn.'), ('Nhân công có mang theo dụng cụ không?', 'Nhân viên có găng tay bảo hộ và dụng cụ bốc xếp cơ bản. Đồ đặc biệt nặng hãy báo trước để chuẩn bị thêm.')]),
 'bang-gia-thao-lap': dict(lead='Bảng giá tháo lắp nội thất khi chuyển nhà, chuyển văn phòng: giường, tủ quần áo, bàn ghế, điều hòa, tivi.',
   items=['Giường', 'Tủ quần áo', 'Bàn, ghế', 'Điều hòa', 'Tivi'], basis='Từng món', svc='chuyen-nha-tron-goi',
   note='Giá tùy kích thước và độ phức tạp của từng món đồ.',
   factors=['Số lượng và kích thước từng món.', 'Đồ lắp ráp phức tạp, nhiều chi tiết.', 'Điều hòa cần thợ điện lạnh thu gas và lắp lại.', 'Có cần lắp lại ở nơi mới hay không.'],
   faq=[('Tháo lắp có nằm trong gói chuyển nhà trọn gói không?', 'Có. Với <a href="{p}chuyen-nha-tron-goi.html">chuyển nhà trọn gói</a>, tháo lắp nội thất là một phần của dịch vụ.'), ('Có tháo lắp điều hòa không?', 'Có nhận. Điều hòa cần thu gas trước khi tháo và lắp lại đúng kỹ thuật, hãy báo trước số lượng.')]),
}


def build_prices():
    for s, n in PR:
        d = PRD[s]; p = ''
        name_svc = dict(SV)[d['svc']]
        tr = ''.join(f'<tr><td>{x}</td><td>{d["basis"]}</td><td>Liên hệ</td></tr>' for x in d['items'])
        faq = [(q, a.replace('{p}', p)) for q, a in d['faq']] + [('Vì sao bảng giá ghi "Liên hệ"?', 'Mỗi công việc có khối lượng và điều kiện khác nhau, nên chúng tôi báo giá cụ thể sau khi nghe bạn mô tả, thay vì một con số chung dễ phát sinh.')]
        body = f'''<section class="page-head"><div class="wrap">{crumb_html([("index.html", "Trang chủ"), ("bang-gia.html", "Bảng giá"), (s + ".html", n)], p)}
<h1>{n} SGE Viettrans</h1><p class="lead">{d["lead"]} Báo giá rõ trước khi làm.</p></div></section>
<section class="detail"><div class="wrap grid">
  <article class="prose">
    <section><h2>{n}</h2>
    <!-- TODO: điền giá thật vào cột "Giá" (thay chữ "Liên hệ") khi chủ công ty chốt bảng giá. Không tự bịa giá. -->
    <div class="tbl"><table><thead><tr><th scope="col">Hạng mục</th><th scope="col">Tính giá theo</th><th scope="col">Giá</th></tr></thead><tbody>{tr}</tbody></table></div>
    <p class="pg-note">{d["note"]}</p></section>
    <section><h2>Giá được tính dựa trên những gì</h2><ul>{"".join(f"<li>{x}</li>" for x in d["factors"])}</ul>
    <p>Đọc thêm: <a href="blog/chi-phi-chuyen-nha.html">Chi phí chuyển nhà phụ thuộc vào những gì</a>.</p></section>
    <section><h2>Câu hỏi thường gặp</h2>{faq_html(faq)}</section>
  </article>
  <div class="side">
  {aside_cta(p, "Báo giá chính xác", name_svc, f'<a class="more" href="{d["svc"]}.html">Dịch vụ {lower1(name_svc)}</a><a class="more" href="bang-gia.html">Các bảng giá khác</a>')}
  </div>
</div></section>'''
        ld = [breadcrumb_ld([("", "Trang chủ"), ("bang-gia.html", "Bảng giá"), (s + ".html", n)]), faq_ld(faq)]
        page(s + '.html', f'{n} TPHCM | SGE Viettrans', f'{d["lead"]} Gọi {PHONE_TXT} để được báo giá.', body, cur=s, ld=ld, priority='0.7')


def build_lists():
    rows = ''.join(f'''<li><a class="row-img" href="{s}.html">{img("", SERVICES[s]["img"][0], SERVICES[s]["img"][1], SERVICES[s]["img"][2], SERVICES[s]["img"][3], "fig")}</a>
<div><h2><a href="{s}.html">{n}</a></h2><p>{SERVICES[s]["lead"]}</p><a class="go" href="{s}.html">Xem chi tiết {lower1(n)}</a></div></li>''' for s, n in SV)
    body = f'''<section class="page-head"><div class="wrap">{crumb_html([("index.html", "Trang chủ"), ("dich-vu.html", "Dịch vụ")], "")}
<h1>Dịch vụ vận chuyển của SGE Viettrans</h1><p class="lead">Chuyển nhà trọn gói, chuyển văn phòng, cho thuê xe tải, bốc xếp và kho bãi lưu trữ tại TP. Hồ Chí Minh, Bình Dương, Long An, Biên Hòa. Báo giá rõ trước khi làm, tư vấn 24/7.</p></div></section>
<section class="list-page"><div class="wrap"><ul class="svc-cards">{rows}</ul></div></section>'''
    page('dich-vu.html', 'Dịch vụ chuyển nhà, chuyển văn phòng, thuê xe tải TPHCM | SGE Viettrans',
         'Các dịch vụ của SGE Viettrans: chuyển nhà trọn gói, chuyển văn phòng, cho thuê xe tải, bốc xếp, kho bãi lưu trữ tại TP.HCM và khu vực lân cận.',
         body, cur='dich-vu', ld=[breadcrumb_ld([("", "Trang chủ"), ("dich-vu.html", "Dịch vụ")])], priority='0.9')
    rows = ''.join(f'<li><h2><a href="{s}.html">{n}</a></h2><p>{PRD[s]["lead"]}</p><a class="go" href="{s}.html">Xem bảng giá</a></li>' for s, n in PR)
    body = f'''<section class="page-head"><div class="wrap">{crumb_html([("index.html", "Trang chủ"), ("bang-gia.html", "Bảng giá")], "")}
<h1>Bảng giá dịch vụ SGE Viettrans</h1><p class="lead">Giá phụ thuộc khối lượng, quãng đường, tầng và thang máy, nên chúng tôi báo giá cụ thể sau khi nghe bạn mô tả. Báo giá rõ trước khi làm, không phát sinh mập mờ.</p></div></section>
<section class="list-page"><div class="wrap"><ul class="rows">{rows}</ul></div></section>'''
    page('bang-gia.html', 'Bảng giá chuyển nhà, thuê xe tải, bốc xếp TPHCM | SGE Viettrans',
         'Bảng giá xe tải, nhân công bốc xếp và tháo lắp nội thất của SGE Viettrans tại TP.HCM. Báo giá rõ trước khi làm, gọi 0368 757 303.',
         body, cur='bang-gia', ld=[breadcrumb_ld([("", "Trang chủ"), ("bang-gia.html", "Bảng giá")])], priority='0.8')


# ---------------- Blog ----------------
def build_blog():
    cards = ''.join(f'''<li class="card"><a href="blog/{q["slug"]}.html"><img src="assets/blog/cover-{q["slug"]}.jpg" width="1200" height="630" alt="{esc(q["h1"])}" loading="lazy"></a>
<div class="card-in"><span class="tag">{q["cat"]}</span><h2><a href="blog/{q["slug"]}.html">{q["h1"]}</a></h2><p>{q["desc"]}</p></div></li>''' for q in POSTS)
    cats = sorted(set(q['cat'] for q in POSTS))
    filt = '<div class="filters" role="group" aria-label="Lọc theo chủ đề"><button type="button" class="on" data-cat="">Tất cả</button>' + ''.join(
        f'<button type="button" data-cat="{c}">{c}</button>' for c in cats) + '</div>'
    body = f'''<section class="page-head"><div class="wrap">{crumb_html([("index.html", "Trang chủ"), ("blog.html", "Blog")], "")}
<h1>Blog SGE Viettrans: kinh nghiệm chuyển nhà, chuyển văn phòng</h1><p class="lead">Mẹo đóng gói, chọn xe, giờ cấm xe tải và mọi điều cần biết để chuyển nhà, chuyển văn phòng nhẹ nhàng hơn.</p></div></section>
<section class="list-page"><div class="wrap">{filt}<ul class="cards" id="cards">{cards}</ul></div></section>
<script>document.addEventListener('click',function(e){{var b=e.target.closest('.filters button');if(!b)return;
document.querySelectorAll('.filters button').forEach(function(x){{x.classList.toggle('on',x===b)}});var c=b.getAttribute('data-cat');
document.querySelectorAll('#cards .card').forEach(function(li){{li.hidden=!!c&&li.querySelector('.tag').textContent!==c}})}});</script>'''
    ld = [breadcrumb_ld([("", "Trang chủ"), ("blog.html", "Blog")]),
          {"@type": "Blog", "name": "Blog SGE Viettrans", "url": BASE + "blog.html",
           "blogPost": [{"@type": "BlogPosting", "headline": q['h1'], "url": f"{BASE}blog/{q['slug']}.html"} for q in POSTS]}]
    page('blog.html', 'Blog kinh nghiệm chuyển nhà, chuyển văn phòng | SGE Viettrans',
         'Kinh nghiệm chuyển nhà, đóng gói đồ dễ vỡ, chọn xe tải, giờ cấm xe tải TP.HCM, chuyển văn phòng và thuê kho từ SGE Viettrans.',
         body, cur='blog', ld=ld, og_image='assets/blog/cover-chuan-bi-truoc-ngay-chuyen-nha.jpg', priority='0.8')
    for q in POSTS:
        p = '../'
        dt = datetime.date.fromisoformat(q['date']).strftime('%d/%m/%Y')
        words = len(re.sub('<[^>]+>', ' ', q['body']).split())
        svc_links = ''.join(f'<li><a href="{p}{s}.html">{dict(SV)[s]}</a></li>' for s in q['svc'])
        body = f'''<section class="page-head"><div class="wrap">{crumb_html([("index.html", "Trang chủ"), ("blog.html", "Blog"), (f"blog/{q['slug']}.html", q["h1"])], p)}
<h1>{q["h1"]}</h1><p class="meta"><span class="tag">{q["cat"]}</span> <time datetime="{q["date"]}">{dt}</time> · {max(2, round(words/200))} phút đọc · SGE Viettrans</p></div></section>
<section class="detail"><div class="wrap grid">
  <article class="prose">
    {img(p, f"assets/blog/cover-{q['slug']}.jpg", q["h1"], 1200, 630, "fig fig-wide", lazy=False)}
    {fill(q["body"], p)}
    <div class="post-cta"><h2>Cần hỗ trợ chuyển nhà, chuyển đồ?</h2><p>SGE Viettrans tư vấn và báo giá 24/7, báo giá rõ trước khi làm.</p>
    <div class="head-act"><a class="btn" href="tel:{PHONE}">Gọi {PHONE_TXT}</a><a class="btn btn-ghost" href="{ZALO}" target="_blank" rel="noopener">Nhắn Zalo</a></div></div>
  </article>
  <div class="side">
  <div class="side-box"><h2>Dịch vụ liên quan</h2><ul class="side-links">{svc_links}</ul></div>
  <div class="side-box"><h2>Bài viết khác</h2>{related_posts(p, q["svc"], 3, q["slug"])}</div>
  </div>
</div></section>'''
        ld = [breadcrumb_ld([("", "Trang chủ"), ("blog.html", "Blog"), (f"blog/{q['slug']}.html", q["h1"])]),
              {"@type": "BlogPosting", "headline": q['h1'], "description": q['desc'], "datePublished": q['date'], "dateModified": q['date'],
               "image": f"{BASE}assets/blog/cover-{q['slug']}.jpg", "author": {"@type": "Organization", "name": "SGE Viettrans", "url": BASE},
               "publisher": {"@id": BASE + "#org"}, "mainEntityOfPage": f"{BASE}blog/{q['slug']}.html", "inLanguage": "vi"}]
        page(f'blog/{q["slug"]}.html', q['title'] + ' | SGE Viettrans' if len(q['title']) < 52 else q['title'], q['desc'], body,
             cur='blog', ld=ld, og_image=f'assets/blog/cover-{q["slug"]}.jpg', og_type='article', priority='0.7')


if __name__ == '__main__':
    build_services(); build_prices(); build_lists(); build_blog(); build_areas(); build_routes(); build_404(); sync_index()
    write_sitemap(TODAY)
    print(len(PAGES) + 1, 'URL trong sitemap')
