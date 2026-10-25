# Dựng ảnh bìa bài viết và ảnh minh họa (infographic) bằng HTML, chụp bằng Playwright.
# Chạy: python3 _tools/images.py   (cần Node và Playwright)
import os, json, subprocess, sys
sys.path.insert(0, os.path.dirname(__file__))
from engine import ROOT
from content_blog import POSTS
from content_services import SERVICES

TMP = ROOT + '_tools/_render/'
OUT = ROOT + 'assets/blog/'
os.makedirs(TMP, exist_ok=True); os.makedirs(OUT, exist_ok=True)
FONT = ROOT + 'assets/fonts/'

CSS = f'''@font-face{{font-family:M;src:url(file://{FONT}montserrat.woff);font-weight:500 850}}
@font-face{{font-family:B;src:url(file://{FONT}bevietnam-Regular.woff);font-weight:400}}
@font-face{{font-family:B;src:url(file://{FONT}bevietnam-Medium.woff);font-weight:500}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:B,sans-serif;color:#16233b;-webkit-font-smoothing:antialiased}}
.blue{{--bg:#184e94}} h1,h2,h3,b{{font-family:M,sans-serif}}
svg{{fill:none;stroke:currentColor;stroke-width:3;stroke-linecap:round;stroke-linejoin:round}}'''

# Biểu tượng nét đơn giản, vẽ tay, viewBox 64
IC = {
 'calendar': '<rect x="10" y="14" width="44" height="40" rx="4"/><path d="M10 26h44M22 8v12M42 8v12M20 36l6 6 12-12"/>',
 'glass': '<path d="M20 8h24l-3 22a9 9 0 0 1-18 0zM32 39v13M22 56h20"/><path d="M48 40l6-6M50 48l8-2M44 50l2 8"/>',
 'clock': '<circle cx="32" cy="32" r="22"/><path d="M32 18v14l10 6"/>',
 'truck': '<path d="M6 18h32v26H6zM38 28h12l8 9v7H38z"/><circle cx="17" cy="47" r="5"/><circle cx="47" cy="47" r="5"/>',
 'office': '<path d="M12 56V10h26v46M38 24h14v32M8 56h48"/><path d="M19 18h4M27 18h4M19 28h4M27 28h4M19 38h4M27 38h4M44 32h2M44 42h2"/>',
 'fridge': '<rect x="16" y="6" width="32" height="52" rx="4"/><path d="M16 26h32M22 14v6M22 32v8"/>',
 'building': '<path d="M14 58V8h36v50M8 58h48"/><path d="M22 16h6M36 16h6M22 26h6M36 26h6M22 36h6M36 36h6M28 58V46h8v12"/>',
 'bag': '<path d="M16 22h32l-3 34H19zM24 22a8 8 0 0 1 16 0"/>',
 'box': '<path d="M8 20 32 8l24 12v26L32 58 8 46z"/><path d="M8 20l24 12 24-12M32 32v26"/>',
 'coin': '<circle cx="26" cy="30" r="16"/><path d="M26 22v16M21 26h8a3 3 0 0 1 0 6h-6a3 3 0 0 0 0 6h8"/><path d="M44 18a16 16 0 0 1 0 26"/>',
 'home': '<path d="M8 30 32 10l24 20M14 26v30h36V26"/><path d="M26 56V40h12v16"/><path d="M44 8v8"/>',
 'phone': '<rect x="18" y="6" width="28" height="52" rx="5"/><path d="M28 50h8M24 18l8 8 8-8M32 26v12"/>',
 'route': '<circle cx="14" cy="48" r="6"/><circle cx="50" cy="16" r="6"/><path d="M20 48h18a8 8 0 0 0 0-16H26a8 8 0 0 1 0-16h18"/>',
 'factory': '<path d="M6 56V30l14 8v-8l14 8v-8l14 8V12h10v44z"/><path d="M14 48h6M28 48h6M42 48h6"/>',
 'tape': '<path d="M8 22h48v32H8zM8 22l8-12h32l8 12M28 10v12M36 10v12M28 22v8M36 22v8"/>',
}
COVER_IC = {'chuan-bi-truoc-ngay-chuyen-nha': 'calendar', 'dong-goi-do-de-vo': 'glass', 'gio-cam-xe-tai-tphcm': 'clock',
            'chon-xe-tai-phu-hop': 'truck', 'chuyen-van-phong-gon-gang': 'office', 'van-chuyen-tu-lanh-may-giat': 'fridge',
            'chuyen-nha-chung-cu': 'building', 'chuyen-phong-tro-tiet-kiem': 'bag', 'co-nen-thue-kho-khi-chuyen-nha': 'box',
            'chi-phi-chuyen-nha': 'coin', 'xem-ngay-chuyen-nha': 'home', 'dong-thung-carton-dung-cach': 'tape',
            'chuyen-phong-tro-xem-ngay-cung': 'calendar', 'mua-thung-carton-chuyen-nha': 'box', 'boc-xep-duoi-xe-la-gi': 'truck',
            'thue-xe-tai-hay-ung-dung-giao-hang': 'phone', 'kinh-nghiem-chuyen-nha-lien-tinh': 'route', 'ke-hoach-chuyen-kho-xuong': 'factory'}
PHOTO = {'chuyen-nha-chung-cu': 'hero.jpg', 'chon-xe-tai-phu-hop': 'truck.jpg', 'chuyen-van-phong-gon-gang': 'band.jpg',
         'van-chuyen-tu-lanh-may-giat': 'band.jpg', 'kinh-nghiem-chuyen-nha-lien-tinh': 'truck.jpg', 'boc-xep-duoi-xe-la-gi': 'band.jpg'}


def svg(name, size=64):
    return f'<svg viewBox="0 0 64 64" width="{size}" height="{size}">{IC[name]}</svg>'


def cover(p):
    photo = PHOTO.get(p['slug'])
    right = (f'<div class="ph" style="background-image:url(file://{ROOT}assets/{photo})"></div>' if photo else
             f'<div class="icw"><div class="ring">{svg(COVER_IC[p["slug"]], 210)}</div></div>')
    return f'''<style>{CSS}
body{{width:1200px;height:630px;background:#184e94;display:flex;overflow:hidden;position:relative}}
.l{{width:{'620' if photo else '720'}px;padding:64px 0 56px 72px;display:flex;flex-direction:column;color:#fff;position:relative;z-index:2}}
.cat{{display:inline-block;align-self:flex-start;background:#d52b2c;font:700 20px/1 M;letter-spacing:.08em;text-transform:uppercase;padding:10px 16px;border-radius:4px}}
h1{{margin-top:34px;font-size:{'50' if len(p['h1'])>60 else '56'}px;line-height:1.12;font-weight:800;letter-spacing:-.01em}}
.ft{{margin-top:auto;display:flex;align-items:center;gap:16px;font:600 22px/1.2 M}}
.ft img{{width:58px;height:58px;border-radius:50%;background:#fff}}
.ft span{{opacity:.85;font:500 20px/1.2 B}}
.ph{{position:absolute;right:0;top:0;bottom:0;width:640px;background-size:cover;background-position:center}}
.ph::before{{content:"";position:absolute;inset:0;background:linear-gradient(90deg,#184e94 0,rgba(24,78,148,0) 35%)}}
.icw{{flex:1;display:grid;place-items:center}}
.ring{{width:380px;height:380px;border-radius:50%;background:#2563ae;display:grid;place-items:center;color:#fff;box-shadow:inset 0 0 0 14px #1d58a1}}
.bar{{position:absolute;left:0;bottom:0;height:10px;width:100%;background:#d52b2c}}</style>
<div class="l"><span class="cat">{p['cat']}</span><h1>{p['h1']}</h1>
<div class="ft"><img src="file://{ROOT}assets/logo.jpg"><div>SGE VIETTRANS<br><span>Hotline 0368 757 303</span></div></div></div>{right}<div class="bar"></div>'''


def frame(title, inner, h):
    return f'''<style>{CSS}
body{{width:1200px;height:{h}px;background:#fff;padding:56px 64px;position:relative}}
h2{{font-size:42px;font-weight:800;color:#0f2f63;line-height:1.15}}
.sub{{margin-top:10px;font-size:22px;color:#4a5875}}
.brand{{position:absolute;right:64px;top:56px;display:flex;align-items:center;gap:12px;font:700 18px/1.2 M;color:#184e94}}
.brand img{{width:46px;height:46px;border-radius:50%}}
.cols{{display:grid;gap:22px;margin-top:40px}}
.c{{background:#eef3fa;border-radius:12px;padding:28px 26px;position:relative}}
.n{{width:52px;height:52px;border-radius:50%;background:#184e94;color:#fff;display:grid;place-items:center;font:800 24px/1 M;margin-bottom:18px}}
.c.r .n{{background:#d52b2c}}
.c h3{{font-size:25px;color:#0f2f63;margin-bottom:12px;line-height:1.2}}
.c li{{list-style:none;font-size:20px;line-height:1.45;color:#16233b;padding-left:22px;position:relative;margin-bottom:8px}}
.c li::before{{content:"";position:absolute;left:0;top:11px;width:9px;height:9px;border-radius:50%;background:#d52b2c}}
.c p{{font-size:20px;line-height:1.45;color:#16233b}}
.ic{{color:#184e94;margin-bottom:14px}}
.foot{{position:absolute;left:64px;right:64px;bottom:34px;font-size:17px;color:#4a5875;display:flex;justify-content:space-between}}</style>
<div class="brand"><img src="file://{ROOT}assets/logo.jpg">SGE VIETTRANS</div>
<h2>{title}</h2>{inner}
<div class="foot"><span>SGE Viettrans · Hotline 0368 757 303</span><span>Một chữ tín - Vạn niềm tin</span></div>'''


def cols(items, n, red_last=True, icons=None):
    out = ''
    for i, (h, body) in enumerate(items):
        ic = f'<div class="ic">{svg(icons[i], 58)}</div>' if icons else f'<div class="n">{i+1}</div>'
        cls = ' r' if red_last and i == len(items) - 1 else ''
        b = ''.join(f'<li>{x}</li>' for x in body) if isinstance(body, list) else f'<p>{body}</p>'
        out += f'<div class="c{cls}">{ic}<h3>{h}</h3>{"<ul>"+b+"</ul>" if isinstance(body, list) else b}</div>'
    return f'<div class="cols" style="grid-template-columns:repeat({n},1fr)">{out}</div>'


def truck_hours():
    rows = [('Xe tải nhẹ (450 kg – dưới 2,5 tấn)', [(6, 9), (16, 20)]), ('Xe tải từ 2,5 tấn', [(6, 22)]), ('Xe van, bán tải dưới 950 kg', [])]
    r = ''
    for name, bans in rows:
        seg = ''.join(f'<i style="left:{a/24*100}%;width:{(b-a)/24*100}%"></i>' for a, b in bans)
        r += f'<div class="row"><div class="nm">{name}</div><div class="track">{seg}</div></div>'
    ticks = ''.join(f'<span style="left:{h/24*100}%">{h}h</span>' for h in (0, 6, 9, 12, 16, 20, 22, 24))
    return f'''<style>.row{{display:grid;grid-template-columns:330px 1fr;align-items:center;gap:24px;margin-top:30px}}
.nm{{font:700 22px/1.3 M;color:#0f2f63}}.track{{position:relative;height:54px;border-radius:10px;background:#2f7d4f}}
.track i{{position:absolute;top:0;bottom:0;background:#d52b2c}}.ticks{{position:relative;margin-left:354px;height:30px;margin-top:10px}}
.ticks span{{position:absolute;transform:translateX(-50%);font:600 18px/1 M;color:#4a5875}}
.lg{{display:flex;gap:36px;margin-top:34px;margin-left:354px;font-size:20px}}.lg b{{display:inline-block;width:22px;height:22px;border-radius:5px;vertical-align:-4px;margin-right:10px}}</style>
<p class="sub">Nội thành TP. Hồ Chí Minh, theo QĐ 23/2018/QĐ-UBND (tham khảo, có thể thay đổi)</p>
{r}<div class="ticks">{ticks}</div>
<div class="lg"><span><b style="background:#d52b2c"></b>Giờ cấm</span><span><b style="background:#2f7d4f"></b>Được chạy</span></div>'''


def jobs():
    J = []
    for p in POSTS:
        J.append(('cover-' + p['slug'], cover(p), 1200, 630))
    J.append(('lich-chuan-bi', frame('Lịch chuẩn bị chuyển nhà', cols([
        ('2 tuần trước', ['Chốt ngày, đặt lịch', 'Phân loại đồ', 'Đo nhà mới']),
        ('1 tuần trước', ['Đóng đồ ít dùng', 'Báo ban quản lý', 'Chuyển điện, nước, mạng']),
        ('1 ngày trước', ['Rã đông tủ lạnh', 'Túi đồ dùng ngay', 'Chụp ảnh nối dây']),
        ('Ngày chuyển', ['Có mặt từ đầu', 'Kiểm tra từng phòng', 'Chỉ chỗ đặt đồ lớn'])], 4), 560), 1200, 560))
    J.append(('dong-goi-de-vo', frame('Đóng gói đồ dễ vỡ trong 4 bước', cols([
        ('Thùng nhỏ, chắc', 'Dán đáy chữ thập, lót giấy vò dưới đáy.'),
        ('Bọc từng món', 'Đĩa xếp đứng, ly nhét giấy trong lòng.'),
        ('Chèn kín', 'Lắc nhẹ không còn tiếng va chạm.'),
        ('Ghi nhãn', '"DỄ VỠ", mũi tên chiều đứng, tên phòng.')], 4, icons=['box', 'glass', 'tape', 'home']), 600), 1200, 600))
    J.append(('gio-cam-xe-tai', frame('Giờ cấm xe tải nội thành TP.HCM', truck_hours(), 560), 1200, 560))
    J.append(('chon-xe', frame('Chọn xe tải theo lượng đồ', cols([
        ('Xe van', ['Phòng trọ, ít đồ', 'Không cấm giờ nội thành', 'Vào hẻm dễ']),
        ('Xe tải nhỏ', ['Căn hộ 1–2 phòng ngủ', 'Nhà nhỏ, cửa hàng nhỏ', 'Chạy 9h–16h, sau 20h']),
        ('Xe tải lớn', ['Nhà phố, văn phòng', 'Hàng hóa số lượng lớn', 'Nội thành chạy sau 22h'])], 3, red_last=False,
        icons=['truck', 'truck', 'truck']) + '<p class="sub" style="margin-top:22px">Ước lượng tham khảo. Gửi danh sách đồ để được tư vấn đúng cỡ xe.</p>', 580), 1200, 580))
    J.append(('checklist-van-phong', frame('Chuyển văn phòng trong 5 bước', cols([
        ('Chọn ngày', 'Cuối tuần, có người phụ trách.'), ('Hỏi tòa nhà', 'Giờ chuyển, thang máy, đỗ xe.'),
        ('Lập sơ đồ', 'Danh sách đồ, đánh số bàn.'), ('Đóng gói', 'Hồ sơ theo phòng ban, sao lưu dữ liệu.'),
        ('Ổn định', 'Lắp mạng, IT trước, kiểm tra thùng.')], 5), 560), 1200, 560))
    J.append(('tu-lanh-may-giat', frame('Vận chuyển đồ điện lạnh đúng cách', cols([
        ('Tủ lạnh', ['Rã đông, lau khô', 'Chở ở tư thế đứng', 'Chờ vài giờ mới cắm điện']),
        ('Máy giặt', ['Xả hết nước', 'Lắp ốc khóa lồng giặt', 'Bọc kín đầu ống']),
        ('Máy lạnh', ['Thu gas trước khi tháo', 'Bọc kín ống đồng', 'Thợ chuyên môn lắp lại'])], 3, red_last=False,
        icons=['fridge', 'box', 'clock']), 600), 1200, 600))
    J.append(('lien-tinh', frame('Chuyển nhà liên tỉnh: 4 việc cần nhớ', cols([
        ('Giảm đồ', 'Bán, cho đồ dễ mua lại; chỉ mang đồ giá trị.'),
        ('Đóng gói kỹ', 'Thùng 5 lớp, chèn kín, bọc góc nội thất.'),
        ('Mang theo người', 'Giấy tờ, tiền, trang sức, laptop, thuốc.'),
        ('Chốt lịch hai đầu', 'Ngày đi, ngày giao, người nhận, đường vào.')], 4, icons=['home', 'box', 'bag', 'calendar']), 520), 1200, 520))
    for s, d in SERVICES.items():
        J.append(('quy-trinh-' + s, frame(f'Quy trình {d["name"].lower()}', cols(d['steps'], 5), 600), 1200, 600))
    return J


if __name__ == '__main__':
    J = jobs()
    spec = []
    for name, html, w, h in J:
        hp = TMP + name + '.html'
        open(hp, 'w', encoding='utf8').write('<!doctype html><meta charset="utf-8">' + html)
        spec.append({'html': hp, 'png': TMP + name + '.png', 'jpg': OUT + name + '.jpg', 'w': w, 'h': h})
    json.dump(spec, open(TMP + 'spec.json', 'w'))
    js = '''const {chromium}=require('playwright');const s=require(process.argv[2]);
(async()=>{const b=await chromium.launch({args:['--no-sandbox','--allow-file-access-from-files']});
for(const j of s){const p=await b.newPage({viewport:{width:j.w,height:j.h},deviceScaleFactor:1});
await p.goto('file://'+j.html);await p.waitForTimeout(250);await p.screenshot({path:j.png});await p.close();}
await b.close();})();'''
    open(TMP + 'r.js', 'w').write(js)
    subprocess.run(['node', TMP + 'r.js', TMP + 'spec.json'], check=True)
    from PIL import Image
    for j in spec:
        Image.open(j['png']).convert('RGB').save(j['jpg'], quality=84, optimize=True, progressive=True)
    print(len(spec), 'images')
