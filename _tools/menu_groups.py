# Menu 5 nhóm dịch vụ (mega menu) cho mọi trang. Chạy lại được nhiều lần (idempotent).
import os, re, glob
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'

GROUPS = [
    ('Chuyển dọn', 'dich-vu.html#chuyen-don', [
        ('Chuyển nhà trọn gói', 'chuyen-nha-tron-goi.html'),
        ('Chuyển văn phòng', 'chuyen-van-phong.html'),
        ('Chuyển kho xưởng', 'chuyen-kho-xuong.html'),
        ('Chuyển nhà liên tỉnh', 'chuyen-nha-lien-tinh.html')]),
    ('Xe tải', 'cho-thue-xe-tai.html', [
        ('Thuê xe tải 500kg', 'thue-xe-tai-500kg.html'),
        ('Thuê xe tải 1 đến 1,5 tấn', 'thue-xe-tai-1-tan.html'),
        ('Thuê xe tải 1,9 tấn', 'thue-xe-tai-1-9-tan.html'),
        ('Thuê xe tải 2,5 tấn', 'thue-xe-tai-2-5-tan.html')]),
    ('Bốc xếp', 'boc-xep.html', [
        ('Bốc xếp hàng xe tải', 'boc-xep-hang-xe-tai.html'),
        ('Bốc xếp kho', 'boc-xep-kho.html'),
        ('Bốc xếp container', 'boc-xep-container.html')]),
    ('Lắp đặt', 'lap-dat.html', [
        ('Tháo lắp nội thất', 'thao-lap-noi-that.html'),
        ('Tháo lắp máy lạnh', 'thao-lap-may-lanh.html'),
        ('Lắp đặt điện nước', 'lap-dat-dien-nuoc.html')]),
    ('Lưu trữ', 'kho-bai-luu-tru.html', [
        ('Kho cho gia đình', 'kho-bai-luu-tru.html#luu-tru-gia-dinh'),
        ('Kho cho văn phòng, doanh nghiệp', 'kho-bai-luu-tru.html#luu-tru-doanh-nghiep')]),
]

def mega(prefix, current):
    out = ['<ul class="dd-menu mega">']
    for title, href, subs in GROUPS:
        cur = ' aria-current="page"' if href == current else ''
        out.append(f'<li class="dd-g"><a class="dd-h" href="{prefix}{href}"{cur}>{title}</a><ul>')
        for t, h in subs:
            c = ' aria-current="page"' if h == current else ''
            out.append(f'<li><a href="{prefix}{h}"{c}>{t}</a></li>')
        out.append('</ul></li>')
    out.append('</ul>')
    return ''.join(out)

def footer_list(prefix):
    items = [('Chuyển nhà trọn gói','chuyen-nha-tron-goi.html'),('Chuyển văn phòng','chuyen-van-phong.html'),
             ('Chuyển nhà liên tỉnh','chuyen-nha-lien-tinh.html'),('Chuyển kho xưởng','chuyen-kho-xuong.html'),
             ('Cho thuê xe tải','cho-thue-xe-tai.html'),('Bốc xếp','boc-xep.html'),
             ('Lắp đặt','lap-dat.html'),('Kho bãi lưu trữ','kho-bai-luu-tru.html')]
    return '<ul>' + ''.join(f'<li><a href="{prefix}{h}">{t}</a></li>' for t, h in items) + '</ul>'

def process(path):
    rel = os.path.relpath(path, ROOT)
    prefix = '../' if '/' in rel else ''
    s = open(path, encoding='utf8').read(); o = s
    cur = os.path.basename(rel) if prefix == '' else None
    # 1. menu Dịch vụ (ul.dd-menu chứa link chuyen-nha-tron-goi)
    s = re.sub(r'<ul class="dd-menu(?: mega)?">(?:(?!</ul></div>|</ul>\s*</div>).)*?chuyen-nha-tron-goi\.html.*?</ul>(?=\s*</div>)',
               lambda m: mega(prefix, cur), s, count=1, flags=re.S) if 'chuyen-nha-tron-goi.html' in s else s
    # 2. footer Dịch vụ
    s = re.sub(r'(<h3>Dịch vụ</h3>\s*)<ul>.*?</ul>', lambda m: m.group(1) + footer_list(prefix), s, count=1, flags=re.S)
    if s != o:
        open(path, 'w', encoding='utf8').write(s); return True
    return False

if __name__ == '__main__':
    n = 0
    for p in glob.glob(ROOT + '**/*.html', recursive=True):
        if '/_tools/' in p or '/node_modules/' in p: continue
        if process(p): n += 1
    print('cập nhật', n, 'trang')
