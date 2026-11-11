# Tạo các trang con (xe tải theo tải trọng, bốc xếp, lắp đặt) từ khung của cho-thue-xe-tai.html.
# Chạy: python3 _tools/build_subpages.py   (chạy lại được, sẽ ghi đè các trang con này)
import os, re, json, html, urllib.parse
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE) + '/'
import sys
sys.path.insert(0, HERE)
import menu_groups

BASE = 'https://sgeviettrans.vn/'
TEL = '0368 757 303'
VARS = json.load(open(HERE + '/variants.json', encoding='utf8'))
TPL = open(ROOT + 'cho-thue-xe-tai.html', encoding='utf8').read()
TODAY = '2026-11-11'


def esc(t):
    return html.escape(t, quote=False)


def picture(key, alt, sizes='(max-width: 1000px) 100vw, 760px', lazy=True):
    v = VARS['assets/%s.jpg' % key]
    srcset = ', '.join('%s %dw' % (p, w) for w, p in v['webp'])
    ld = ' loading="lazy"' if lazy else ''
    return ('<figure class="fig"><picture><source type="image/webp" srcset="%s" sizes="%s">'
            '<img src="%s" width="%d" height="%d" alt="%s"%s decoding="async"></picture></figure>'
            % (srcset, sizes, v['jpg'], v['w'], v['h'], html.escape(alt), ld))


def table(head, rows, cls='tbl'):
    th = ''.join('<th scope="col">%s</th>' % esc(h) for h in head)
    body = ''
    for r in rows:
        tds = ''
        for i, c in enumerate(r):
            tds += '<td>%s</td>' % c
        body += '<tr>%s</tr>' % tds
    return '<div class="%s"><table><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>' % (cls, th, body)


def ul(items):
    return '<ul>' + ''.join('<li>%s</li>' % i for i in items) + '</ul>'


def ol(items):
    return '<ol class="mini-steps">' + ''.join('<li><b>%s</b>%s</li>' % (a, b) for a, b in items) + '</ol>'


def faq_html(faqs):
    return '<div class="faq-list">' + ''.join(
        '<details><summary>%s</summary><p>%s</p></details>' % (esc(q), esc(a)) for q, a in faqs) + '</div>'


PRICE_RULE_FORBIDDEN = re.compile(r'rẻ nhất|giảm \d+%|priceRange')

# ---------------------------------------------------------------------------
# Dữ liệu các trang
# ---------------------------------------------------------------------------
TRUCK_ROWS = {
    '500kg': [('Xe 500kg', 'Phòng trọ, ít đồ', '300K', '13K/km', '70K/giờ'),
              ('Xe 750kg', 'Phòng trọ lớn, cửa hàng nhỏ', '350K', '14K/km', '70K/giờ')],
    '1-tan': [('Xe 1,25 đến 1,5 tấn', 'Căn hộ 1 phòng ngủ, văn phòng nhỏ', '400K', '16K/km', '100K/giờ')],
    '1-9-tan': [('Xe 1,9 tấn', 'Căn hộ 2 phòng ngủ', '500K', '20K/km', '120K/giờ')],
    '2-5-tan': [('Xe 2,5 tấn', 'Nhà phố, văn phòng vừa', '700K', '30K/km', '150K/giờ')],
}
TRUCK_HEAD = ['Loại xe, phù hợp với', 'Chỉ từ (10km đầu)', 'Km tiếp theo, phí chờ']
TRUCK_NOTE = ('Giá tham khảo cho nội thành TP.HCM, có tài xế. Quãng đường dài, chạy đêm hoặc ngày lễ được báo giá riêng. '
              'Giá thuê xe chưa gồm nhân công bốc xếp nếu bạn không chọn thêm dịch vụ này. Gọi %s để nhận báo giá chính xác.' % TEL)

OTHER_TRUCKS = [('Thuê xe tải 500kg', 'thue-xe-tai-500kg.html'), ('Thuê xe tải 1 đến 1,5 tấn', 'thue-xe-tai-1-tan.html'),
                ('Thuê xe tải 1,9 tấn', 'thue-xe-tai-1-9-tan.html'), ('Thuê xe tải 2,5 tấn', 'thue-xe-tai-2-5-tan.html')]


def truck_page(key, slug, short, price_from, title, meta, h1, lead, img, img_alt, intro, who, tips, compare, faqs, steps_extra=''):
    rows = [['%s<small>%s</small>' % (esc(a), esc(b)), esc(c), '%s, chờ %s' % (esc(d), esc(e))] for a, b, c, d, e in TRUCK_ROWS[key]]
    secs = [
        ('Xe %s phù hợp với ai' % short, intro + ul(who)),
        ('Bảng giá thuê xe %s' % short,
         '<p>Thuê xe tải chỉ từ 300K, xe %s chỉ từ %s trong 10km đầu. Đây là giá tham khảo.</p>' % (short, price_from)
         + table(TRUCK_HEAD, rows, 'tbl t2') + '<p class="pg-note">%s</p>' % esc(TRUCK_NOTE)
         + '<p>Xem đầy đủ các loại xe tại <a href="bang-gia-xe-tai.html">bảng giá thuê xe tải</a>.</p>'),
        ('Lưu ý khi thuê xe %s' % short, ul(tips)
         + '<p>Giờ cấm tải trong nội thành ảnh hưởng đến lịch chạy, xem thêm <a href="blog/gio-cam-xe-tai-tphcm.html">giờ cấm xe tải TP.HCM</a>.</p>'),
        ('Quy trình thuê xe %s' % short, ol([
            ('Cho biết hàng hóa', 'Loại hàng, khối lượng ước tính.'),
            ('Điểm đi, điểm đến', 'Địa chỉ và quãng đường.'),
            ('Chốt xe và giá', 'Tư vấn xe phù hợp, báo giá trước khi chạy.'),
            ('Xe đến đúng hẹn', 'Xe tải thùng SGE có tài xế đến nhận hàng, có thể kèm nhân công bốc xếp.')])),
        ('Khi nào nên chọn xe khác', '<p>%s</p>' % esc(compare)
         + '<p>Xem các tải trọng khác: ' + ', '.join('<a href="%s">%s</a>' % (h, t) for t, h in OTHER_TRUCKS if h != slug + '.html')
         + '. Cách chọn chi tiết ở bài <a href="blog/chon-xe-tai-phu-hop.html">chọn xe tải phù hợp khi chuyển nhà</a>.</p>'),
    ]
    return dict(slug=slug, title=title, meta=meta, h1=h1, lead=lead, img=(img, img_alt), crumb_parent=('Cho thuê xe tải', 'cho-thue-xe-tai.html'),
                service='Cho thuê xe tải %s' % short, dv='Cho thuê xe tải', secs=secs, faqs=faqs,
                aside_title='Nhận báo giá thuê xe %s' % short, aside_more=('Xem bảng giá xe tải', 'bang-gia-xe-tai.html'),
                side_links=OTHER_TRUCKS + [('Cho thuê xe tải', 'cho-thue-xe-tai.html'), ('Bốc xếp', 'boc-xep.html')],
                og='truck', area=None)


PAGES = []

PAGES.append(truck_page(
    '500kg', 'thue-xe-tai-500kg', '500kg', '300K',
    'Thuê xe tải 500kg TPHCM chỉ từ 300K | SGE Viettrans',
    'Thuê xe tải 500kg TPHCM chỉ từ 300K, có tài xế. Xe 750kg từ 350K. Hợp chuyển phòng trọ, đồ ít, giao hàng nhỏ. Giá tham khảo, gọi 0368 757 303 để báo giá.',
    'Thuê xe tải 500kg tại TP. Hồ Chí Minh',
    'Chuyển phòng trọ, chở ít đồ hay giao hàng nhỏ: thuê xe tải 500kg có tài xế chỉ từ 300K, chạy linh hoạt trong nội thành, báo giá trước khi chạy.',
    'xe-tai-cho-may-giat', 'Nhân viên SGE Viettrans xếp đồ lên xe tải nhỏ để chuyển phòng trọ',
    '<p>Xe tải 500kg là lựa chọn nhỏ gọn và tiết kiệm nhất của SGE Viettrans, đủ cho việc chuyển đồ ít hoặc giao hàng trong nội thành. Nếu đồ nhiều hơn một chút, xe 750kg chỉ từ 350K sẽ dư dả hơn.</p>',
    ['Chuyển phòng trọ, phòng ký túc xá, đồ chỉ gồm giường, tủ nhỏ và vài thùng.', 'Chở một vài món đồ lẻ: máy giặt, tủ lạnh nhỏ, xe máy điện.',
     'Cửa hàng nhỏ giao hàng hoặc lấy hàng định kỳ trong nội thành.', 'Đường hẻm nhỏ mà xe lớn khó vào.'],
    ['Báo trước số tầng và có thang máy hay không để chúng tôi sắp người phù hợp.', 'Đồ cồng kềnh như tủ quần áo lớn, giường hộp nên báo trước kích thước.',
     'Quãng đường trên 10km tính thêm khoảng 13K mỗi km với xe 500kg.', 'Thời gian chờ bốc hàng tính theo giờ, mô tả đủ công việc để chốt giá trọn chuyến.'],
    'Nếu bạn chuyển nhà có nhiều đồ, có tủ lạnh, máy giặt và nhiều thùng, xe 1,25 đến 1,5 tấn sẽ đỡ phải chạy nhiều chuyến. Trường hợp muốn SGE lo đóng gói và tháo lắp, hãy xem chuyển nhà trọn gói chỉ từ 800K.',
    [('Thuê xe tải 500kg giá bao nhiêu?', 'Thuê xe tải 500kg chỉ từ 300K cho 10km đầu, từ km thứ 11 tính thêm khoảng 13K mỗi km. Đây là giá tham khảo, báo giá chính xác theo quãng đường và thời gian thuê khi gọi %s.' % TEL),
     ('Xe 500kg chở được những gì?', 'Phù hợp chuyển phòng trọ, đồ ít và giao hàng nhỏ. Bạn nên mô tả đồ qua Zalo %s để được tư vấn xe 500kg hay 750kg.' % TEL),
     ('Xe có kèm tài xế không?', 'Có, xe cho thuê có tài xế của SGE Viettrans. Bạn không cần tự lái.'),
     ('Có thuê thêm người bốc xếp được không?', 'Có. Nhân công bốc xếp chỉ từ 350K mỗi người mỗi lượt nội thành, tính riêng khỏi giá thuê xe.')]))

PAGES.append(truck_page(
    '1-tan', 'thue-xe-tai-1-tan', '1 đến 1,5 tấn', '400K',
    'Thuê xe tải 1 tấn, 1,5 tấn TPHCM chỉ từ 400K | SGE',
    'Thuê xe tải 1 tấn đến 1,5 tấn TPHCM chỉ từ 400K, có tài xế, hợp chuyển căn hộ và văn phòng nhỏ. Giá tham khảo, báo giá chính xác gọi 0368 757 303.',
    'Thuê xe tải 1 tấn đến 1,5 tấn tại TP. Hồ Chí Minh',
    'Xe tải 1,25 đến 1,5 tấn là cỡ xe phổ biến cho chuyển căn hộ và văn phòng nhỏ. Thuê xe có tài xế chỉ từ 400K, báo giá rõ trước khi chạy.',
    'xe-tai-cho-may-giat', 'Nhân viên SGE Viettrans xếp máy giặt và đồ gia dụng lên xe tải thùng',
    '<p>Xe tải 1,25 đến 1,5 tấn (thường gọi chung là xe 1 tấn) là cỡ xe được thuê nhiều nhất khi chuyển nhà trong thành phố. Thùng xe đủ cho đồ của một căn hộ 1 phòng ngủ trong một chuyến.</p>',
    ['Chuyển căn hộ 1 phòng ngủ hoặc nhà nhỏ, đồ gồm giường, tủ, tủ lạnh, máy giặt và nhiều thùng.', 'Văn phòng nhỏ khoảng vài bàn làm việc, tủ hồ sơ và máy móc.',
     'Cửa hàng chở hàng số lượng vừa theo chuyến hoặc theo giờ.', 'Chở hàng đi các tỉnh gần như Bình Dương, Đồng Nai, Long An.'],
    ['Cho biết số lượng đồ lớn như tủ lạnh, máy giặt, tủ quần áo để sắp xếp người khiêng.', 'Quãng đường trên 10km tính thêm khoảng 16K mỗi km, thời gian chờ khoảng 100K mỗi giờ.',
     'Nhà trong hẻm nhỏ xe không vào được cần báo trước để bố trí người chuyển ra điểm đậu xe.', 'Chạy khung giờ cấm tải cần được hẹn từ trước.'],
    'Nếu đồ nhiều như nhà phố hoặc căn hộ 2 phòng ngủ, hãy cân nhắc xe 1,9 tấn chỉ từ 500K để đỡ phải chạy hai chuyến. Với đồ ít, xe 500kg chỉ từ 300K tiết kiệm hơn.',
    [('Thuê xe tải 1 tấn giá bao nhiêu?', 'Xe 1,25 đến 1,5 tấn chỉ từ 400K cho 10km đầu, từ km thứ 11 tính thêm khoảng 16K mỗi km, phí chờ khoảng 100K mỗi giờ. Đây là giá tham khảo, gọi %s để báo giá chính xác.' % TEL),
     ('Xe 1 tấn có chở được đồ căn hộ không?', 'Thường đủ cho căn hộ 1 phòng ngủ trong một chuyến. Hãy mô tả đồ qua Zalo %s để chúng tôi tư vấn đúng cỡ xe.' % TEL),
     ('Xe 1 tấn khác xe 1,25 và 1,5 tấn thế nào?', 'Trong bảng giá của SGE Viettrans, xe 1,25 đến 1,5 tấn dùng chung một mức giá chỉ từ 400K. Khi gọi, bạn cho biết lượng đồ để chúng tôi chọn xe sát nhất.'),
     ('Có thuê thêm nhân công bốc xếp được không?', 'Có. Nhân công bốc xếp chỉ từ 350K mỗi người mỗi lượt nội thành, tính riêng khỏi giá thuê xe.')]))

PAGES.append(truck_page(
    '1-9-tan', 'thue-xe-tai-1-9-tan', '1,9 tấn', '500K',
    'Thuê xe tải 1,9 tấn TPHCM chỉ từ 500K | SGE Viettrans',
    'Thuê xe tải 1,9 tấn TPHCM chỉ từ 500K, có tài xế, hợp chuyển căn hộ 2 phòng ngủ, hàng cửa hàng. Giá tham khảo, báo giá chính xác gọi 0368 757 303.',
    'Thuê xe tải 1,9 tấn tại TP. Hồ Chí Minh',
    'Chuyển căn hộ 2 phòng ngủ hay chở hàng số lượng vừa: thuê xe tải 1,9 tấn có tài xế chỉ từ 500K, đủ thùng để không phải chạy hai chuyến.',
    'truck', 'Xe tải thùng SGE Viettrans cho thuê chở hàng và chuyển nhà',
    '<p>Xe tải 1,9 tấn có thùng rộng hơn xe 1 tấn, phù hợp khi đồ nhiều nhưng chưa cần xe cỡ lớn. Đây là lựa chọn cân bằng giữa chi phí và sức chứa.</p>',
    ['Chuyển căn hộ 2 phòng ngủ, đồ nhiều, có tủ lạnh, máy giặt, giường lớn.', 'Chuyển nhà nhỏ trong hẻm vừa, đỡ phải chạy hai chuyến bằng xe nhỏ.',
     'Cửa hàng, kho nhỏ cần chở hàng số lượng vừa.', 'Chở hàng liên tỉnh quãng ngắn trong ngày.'],
    ['Quãng đường trên 10km tính thêm khoảng 20K mỗi km, thời gian chờ khoảng 120K mỗi giờ.', 'Xe cỡ này phải tuân thủ khung giờ cấm tải trong nội thành, nên chốt giờ chạy từ trước.',
     'Hẻm nhỏ xe không vào được thì cần người chuyển đồ ra điểm đậu xe, hãy báo trước.', 'Cho biết đồ cồng kềnh để chúng tôi chuẩn bị dụng cụ tháo lắp.'],
    'Nếu đồ còn ít, xe 1,25 đến 1,5 tấn chỉ từ 400K sẽ tiết kiệm hơn. Nếu là nhà phố nhiều tầng hoặc văn phòng vừa, xe 2,5 tấn chỉ từ 700K sẽ dư dả.',
    [('Thuê xe tải 1,9 tấn giá bao nhiêu?', 'Xe 1,9 tấn chỉ từ 500K cho 10km đầu, từ km thứ 11 tính thêm khoảng 20K mỗi km, phí chờ khoảng 120K mỗi giờ. Đây là giá tham khảo, gọi %s để báo giá chính xác.' % TEL),
     ('Xe 1,9 tấn chở được căn hộ 2 phòng ngủ không?', 'Thường phù hợp với căn hộ 2 phòng ngủ. Hãy mô tả đồ qua Zalo %s để chúng tôi xác nhận cỡ xe và số người cần.' % TEL),
     ('Xe 1,9 tấn có bị cấm giờ cao điểm không?', 'Xe tải bị hạn chế theo khung giờ và tuyến đường trong nội thành. Chúng tôi sắp xếp giờ chạy phù hợp khi nhận lịch của bạn.'),
     ('Có thuê thêm nhân công bốc xếp được không?', 'Có. Nhân công bốc xếp chỉ từ 350K mỗi người mỗi lượt nội thành, tính riêng khỏi giá thuê xe.')]))

PAGES.append(truck_page(
    '2-5-tan', 'thue-xe-tai-2-5-tan', '2,5 tấn', '700K',
    'Thuê xe tải 2,5 tấn TPHCM chỉ từ 700K | SGE Viettrans',
    'Thuê xe tải 2,5 tấn TPHCM chỉ từ 700K, có tài xế, hợp chuyển nhà phố, văn phòng vừa, hàng số lượng lớn. Giá tham khảo, báo giá chính xác gọi 0368 757 303.',
    'Thuê xe tải 2,5 tấn tại TP. Hồ Chí Minh',
    'Nhà phố nhiều tầng, văn phòng vừa hay hàng số lượng lớn: thuê xe tải 2,5 tấn có tài xế chỉ từ 700K, chở gọn trong một chuyến.',
    'truck', 'Xe tải thùng SGE Viettrans màu trắng, xanh, đỏ cho thuê chở hàng',
    '<p>Xe tải 2,5 tấn là cỡ xe lớn nhất trong bảng giá thuê xe theo chuyến của SGE Viettrans, dành cho đồ nhiều và hàng nặng cần chở gọn trong một lần.</p>',
    ['Chuyển nhà phố nhiều tầng, đồ đạc nhiều và nặng.', 'Chuyển văn phòng vừa với nhiều bàn ghế, tủ hồ sơ, máy móc.',
     'Chở hàng số lượng lớn cho cửa hàng, kho, công trình.', 'Chở hàng liên tỉnh bằng một chuyến.'],
    ['Quãng đường trên 10km tính thêm khoảng 30K mỗi km, thời gian chờ khoảng 150K mỗi giờ.', 'Xe lớn bị hạn chế giờ chạy trong nội thành, nên chốt giờ từ trước để tránh phát sinh.',
     'Kiểm tra đường vào, chiều cao cổng, chỗ đậu xe và báo cho chúng tôi trước.', 'Nên kết hợp nhân công bốc xếp khi đồ nặng hoặc nhà nhiều tầng.'],
    'Nếu đồ không nhiều, thuê xe 1,9 tấn chỉ từ 500K hoặc 1,25 đến 1,5 tấn chỉ từ 400K sẽ tiết kiệm hơn. Hàng nặng hơn hoặc hàng rời lớn hơn mức này sẽ được báo giá theo khảo sát.',
    [('Thuê xe tải 2,5 tấn giá bao nhiêu?', 'Xe 2,5 tấn chỉ từ 700K cho 10km đầu, từ km thứ 11 tính thêm khoảng 30K mỗi km, phí chờ khoảng 150K mỗi giờ. Đây là giá tham khảo, gọi %s để báo giá chính xác.' % TEL),
     ('Xe 2,5 tấn hợp với việc gì?', 'Phù hợp nhà phố, văn phòng vừa và hàng số lượng lớn. Hãy mô tả khối lượng hàng qua Zalo %s để chúng tôi tư vấn đúng cỡ xe.' % TEL),
     ('Chạy đêm hoặc ngày lễ có tính thêm phí không?', 'Quãng đường dài, chạy đêm hoặc ngày lễ được báo giá riêng. Hãy báo trước giờ chạy khi gọi.'),
     ('Có thuê thêm nhân công bốc xếp được không?', 'Có. Nhân công bốc xếp chỉ từ 350K mỗi người mỗi lượt nội thành, tính riêng khỏi giá thuê xe.')]))

# --- Bốc xếp ---------------------------------------------------------------
BX_NOTE = 'Giá tham khảo, tùy khối lượng, loại hàng và điều kiện nơi làm việc. Ngoài giờ, ngày lễ, hàng đặc thù được báo giá theo khảo sát. Gọi %s để nhận báo giá chính xác.' % TEL
BX_OTHERS = [('Bốc xếp hàng xe tải', 'boc-xep-hang-xe-tai.html'), ('Bốc xếp kho', 'boc-xep-kho.html'), ('Bốc xếp container', 'boc-xep-container.html')]

PAGES.append(dict(
    slug='boc-xep-hang-xe-tai',
    title='Bốc xếp hàng xe tải TPHCM, xe 2 tấn từ 150K | SGE',
    meta='Bốc xếp hàng lên xuống xe tải TPHCM: xe 2 tấn từ 150K, xe 5 tấn từ 295K, xe 10 tấn từ 590K. Giá tham khảo, báo giá chính xác gọi 0368 757 303.',
    h1='Bốc xếp hàng lên xuống xe tải tại TP. Hồ Chí Minh',
    lead='Hàng về kho, hàng ra xe, xe tải đến là có người bốc. Nhân công SGE Viettrans bốc xếp theo xe từ xe 2 tấn đến 20 tấn, giá niêm yết rõ theo từng cỡ xe.',
    img=('xe-tai-cho-may-giat', 'Nhân viên SGE Viettrans bốc xếp hàng và đồ gia dụng lên xe tải'),
    crumb_parent=('Bốc xếp', 'boc-xep.html'), service='Bốc xếp hàng xe tải', dv='Bốc xếp',
    secs=[
        ('Bốc xếp hàng xe tải gồm những gì', '<p>Dịch vụ dành cho chủ hàng, cửa hàng, kho và doanh nghiệp cần bốc hàng lên hoặc xuống xe nhanh gọn, tính giá theo xe nên dễ dự trù chi phí.</p>'
         + ul(['Bốc hàng từ kho, cửa hàng lên xe và ngược lại.', 'Bốc thủ công hoặc kết hợp xe nâng khi hàng nặng.', 'Xếp hàng gọn trên xe để hạn chế xô lệch khi di chuyển.', 'Phục vụ xe từ 2 tấn đến 20 tấn, đầu kéo rơ-moóc.'])),
        ('Bảng giá bốc xếp hàng theo xe tải', '<p>Giá bốc lên hoặc xuống hàng cho mỗi xe.</p>'
         + table(['Loại xe', 'Chỉ từ'], [[esc(a), esc(b)] for a, b in [('Xe 2 tấn', '150K'), ('Xe 3,5 tấn', '190K'), ('Xe 5 tấn', '295K'), ('Xe 8 tấn', '495K'), ('Xe 10 tấn', '590K'), ('Xe 15 tấn', '995K'), ('Xe 20 tấn', '1,495 triệu'), ('Đầu kéo rơ-moóc thùng 12 m', '1,49 triệu')]], 'tbl t2')
         + '<p class="pg-note">%s</p>' % esc(BX_NOTE) + '<p>Hàng bốc thủ công tính theo tấn chỉ từ 200K mỗi tấn. Xem thêm <a href="bang-gia-boc-xep.html">bảng giá nhân công bốc xếp</a>.</p>'),
        ('Giá phụ thuộc vào những gì', ul(['Cỡ xe và khối lượng hàng.', 'Loại hàng: hàng rời, hàng đóng thùng, hàng dễ vỡ, hàng nặng.', 'Khoảng cách từ chỗ để hàng ra xe, số tầng và có thang máy hay không.', 'Khung giờ làm việc: ban đêm, ngày lễ báo giá riêng.'])),
        ('Quy trình bốc xếp', ol([('Cho biết hàng và xe', 'Loại hàng, khối lượng, cỡ xe.'), ('Báo giá', 'Báo giá theo xe hoặc theo tấn trước khi làm.'),
                                 ('Nhân công đến đúng giờ', 'Đồng phục, găng tay bảo hộ, dụng cụ cơ bản.'), ('Bốc xếp và kiểm đếm', 'Bốc, xếp gọn và đối chiếu hàng cùng bạn.')])),
    ],
    faqs=[('Bốc xếp hàng xe tải giá bao nhiêu?', 'Bốc xếp theo xe chỉ từ 150K cho xe 2 tấn, 295K cho xe 5 tấn, 590K cho xe 10 tấn. Đây là giá tham khảo, giá chính xác phụ thuộc loại hàng và điều kiện thực tế. Gọi %s để báo giá.' % TEL),
          ('Bốc xếp theo xe hay theo tấn có lợi hơn?', 'Hàng đầy xe thì tính theo xe thường dễ dự trù hơn. Hàng ít, nhiều loại thì tính theo tấn hoặc theo giờ. Gọi %s để chúng tôi tư vấn cách tính phù hợp.' % TEL),
          ('Có bốc xếp ngoài giờ, ngày lễ không?', 'Có nhận, nhưng được báo giá riêng. Hãy báo trước giờ làm khi gọi.'),
          ('Nhân công có mang dụng cụ không?', 'Nhân viên có găng tay bảo hộ và dụng cụ bốc xếp cơ bản. Hàng đặc biệt nặng hãy báo trước để chuẩn bị thêm.')],
    aside_title='Nhận báo giá bốc xếp hàng xe tải', aside_more=('Xem bảng giá bốc xếp', 'bang-gia-boc-xep.html'),
    side_links=BX_OTHERS + [('Bốc xếp', 'boc-xep.html'), ('Cho thuê xe tải', 'cho-thue-xe-tai.html')], og='truck'))

PAGES.append(dict(
    slug='boc-xep-kho',
    title='Bốc xếp kho hàng TPHCM, từ 100K mỗi tấn | SGE Viettrans',
    meta='Bốc xếp kho, xưởng TPHCM: trong kho từ 100K/tấn, hàng nhẹ từ 18K/m3, xe nâng từ 150K mỗi lần. Giá tham khảo, báo giá chính xác gọi 0368 757 303.',
    h1='Bốc xếp kho, nhà xưởng tại TP. Hồ Chí Minh',
    lead='Nhập hàng, xuất hàng, sắp xếp lại kho: nhân công SGE Viettrans bốc xếp trong kho tính theo tấn hoặc mét khối, có xe nâng khi hàng nặng, báo giá rõ trước khi làm.',
    img=('boc-xep-ong-nhua', 'Nhân viên SGE Viettrans bốc xếp, di dời ống nhựa và vật liệu tại công trình'),
    crumb_parent=('Bốc xếp', 'boc-xep.html'), service='Bốc xếp kho, nhà xưởng', dv='Bốc xếp',
    secs=[
        ('Bốc xếp kho gồm những việc gì', '<p>Dịch vụ cho kho hàng, cửa hàng và nhà xưởng cần người bốc xếp theo đợt hoặc định kỳ.</p>'
         + ul(['Bốc hàng nhập kho, xuất kho lên xuống xe.', 'Chuyển hàng trong kho, sắp xếp lại vị trí để hàng.', 'Bốc thủ công hoặc dùng xe nâng cho hàng nặng.', 'Hàng nhẹ cồng kềnh tính theo mét khối.'])),
        ('Bảng giá bốc xếp kho theo tấn', '<p>Dành cho hàng kho xưởng, hàng hóa số lượng lớn.</p>'
         + table(['Hạng mục', 'Tính giá theo', 'Chỉ từ'], [[esc(a), esc(b), esc(c)] for a, b, c in [
             ('Bốc thủ công hàng thông thường', 'Tấn', '200K'), ('Bốc trong kho, chuyển hàng', 'Tấn', '100K'), ('Bốc trong kho, hàng nhẹ', 'Mét khối', '18K'),
             ('Tối thiểu mỗi lần bốc', 'Lần', '30K'), ('Xe nâng', 'Mỗi lần nâng', '150K')]])
         + '<p class="pg-note">Giá chưa gồm phát sinh ngoài giờ, ngày lễ. %s</p>' % esc(BX_NOTE)),
        ('Thuê nhân công kho theo giờ, theo ca', '<p>Việc ít và không đều, bạn có thể thuê theo giờ hoặc theo ca:</p>'
         + table(['Hạng mục', 'Tính giá theo', 'Chỉ từ'], [[esc(a), esc(b), esc(c)] for a, b, c in [('Bốc xếp theo giờ', 'Mỗi người, mỗi giờ', '100K'), ('Bốc xếp theo ca', 'Mỗi người, ca 8 giờ', '400K đến 600K')]], 'tbl t2')),
        ('Khi nào nên thuê xe nâng', ul(['Hàng nặng, kiện lớn, hàng đóng pallet.', 'Kho cao, cần nâng hàng lên kệ.', 'Cần bốc nhanh nhiều hàng trong thời gian ngắn.']) + '<p>Hãy cho biết trọng lượng kiện hàng để chúng tôi chọn phương án phù hợp. Muốn dọn cả kho sang chỗ mới, xem <a href="chuyen-kho-xuong.html">chuyển kho xưởng</a>.</p>'),
    ],
    faqs=[('Bốc xếp kho giá bao nhiêu?', 'Bốc trong kho chỉ từ 100K mỗi tấn, hàng nhẹ từ 18K mỗi mét khối, tối thiểu 30K mỗi lần bốc. Bốc thủ công hàng thông thường chỉ từ 200K mỗi tấn. Đây là giá tham khảo, gọi %s để báo giá chính xác.' % TEL),
          ('Thuê xe nâng bốc hàng giá bao nhiêu?', 'Xe nâng chỉ từ 150K mỗi lần nâng. Giá chính xác phụ thuộc trọng lượng và số lần nâng, gọi %s để báo giá.' % TEL),
          ('Có thuê nhân công kho theo ca không?', 'Có. Bốc xếp theo ca 8 giờ từ 400K đến 600K mỗi người, theo giờ từ 100K mỗi người.'),
          ('Có nhận bốc xếp kho định kỳ không?', 'Có. Doanh nghiệp cần bốc xếp thường xuyên hãy gọi %s để thỏa thuận lịch và mức giá phù hợp.' % TEL)],
    aside_title='Nhận báo giá bốc xếp kho', aside_more=('Xem bảng giá bốc xếp', 'bang-gia-boc-xep.html'),
    side_links=BX_OTHERS + [('Bốc xếp', 'boc-xep.html'), ('Chuyển kho xưởng', 'chuyen-kho-xuong.html'), ('Kho bãi lưu trữ', 'kho-bai-luu-tru.html')], og='truck'))

PAGES.append(dict(
    slug='boc-xep-container',
    title='Bốc xếp container TPHCM, rút cont từ 400K | SGE Viettrans',
    meta='Bốc xếp, rút hàng container 20 feet, 40 feet TPHCM bằng xe nâng: cont 20ft từ 400K, 40ft từ 700K. Giá tham khảo, báo giá chính xác gọi 0368 757 303.',
    h1='Bốc xếp, rút hàng container tại TP. Hồ Chí Minh',
    lead='Container về kho, cần rút hàng gấp: SGE Viettrans bốc xếp và rút hàng container 20 feet, 40 feet bằng xe nâng, tính giá rõ theo container và trọng lượng.',
    img=None,
    crumb_parent=('Bốc xếp', 'boc-xep.html'), service='Bốc xếp container', dv='Bốc xếp',
    secs=[
        ('Dịch vụ bốc xếp container gồm những gì', ul(['Rút hàng từ container 20 feet, 40 feet ra kho, ra xe.', 'Bốc hàng lên container, xếp gọn tận dụng thùng.', 'Dùng xe nâng cho hàng đóng pallet, kiện nặng.', 'Phối hợp với xe tải để chở hàng về kho hoặc đến nơi nhận.'])
         + '<p>Việc đóng hàng vào container và các yêu cầu đặc thù được báo giá sau khi khảo sát.</p>'),
        ('Bảng giá rút container bằng xe nâng', table(['Hạng mục', 'Tính giá theo', 'Chỉ từ'], [[esc(a), esc(b), esc(c)] for a, b, c in [
            ('Rút container 20 feet bằng xe nâng', 'Mỗi container', '400K'), ('Rút container 40 feet bằng xe nâng', 'Mỗi container', '700K')]], 'tbl t2')),
        ('Bảng giá bốc xếp theo container', '<p>Giá bốc lên hoặc xuống hàng cho mỗi container.</p>'
         + table(['Loại container', 'Chỉ từ'], [[esc(a), esc(b)] for a, b in [('Container 20 feet nhẹ (dưới 10 tấn)', '690K'), ('Container 20 feet nặng (trên 10 tấn)', '1,195 triệu'),
                                                                               ('Container 40 feet nhẹ (dưới 10 tấn)', '1,55 triệu'), ('Container 40 feet nặng (trên 10 tấn)', '2,195 triệu')]], 'tbl t2')
         + '<p class="pg-note">%s</p>' % esc(BX_NOTE)),
        ('Cần chuẩn bị gì trước khi rút container', ul(['Loại container (20 hay 40 feet) và trọng lượng hàng ước tính.', 'Loại hàng: rời, đóng thùng, đóng pallet, hàng nặng.', 'Địa điểm rút hàng: kho, bãi, nhà xưởng; xe nâng và xe container vào được không.', 'Giờ cần rút hàng, nhất là khi có hạn trả cont.'])
         + '<p>Cần chở hàng sau khi rút, xem <a href="cho-thue-xe-tai.html">cho thuê xe tải</a>.</p>'),
    ],
    faqs=[('Rút container giá bao nhiêu?', 'Rút container 20 feet bằng xe nâng chỉ từ 400K, container 40 feet chỉ từ 700K mỗi container. Đây là giá tham khảo, gọi %s để báo giá chính xác theo loại hàng và địa điểm.' % TEL),
          ('Bốc xếp container nặng tính giá thế nào?', 'Container 20 feet dưới 10 tấn chỉ từ 690K, trên 10 tấn chỉ từ 1,195 triệu. Container 40 feet dưới 10 tấn chỉ từ 1,55 triệu, trên 10 tấn chỉ từ 2,195 triệu. Giá tham khảo, báo giá chính xác khi gọi %s.' % TEL),
          ('Có nhận rút container ngoài giờ, cuối tuần không?', 'Có nhận, được báo giá riêng cho ngoài giờ và ngày lễ. Hãy báo trước giờ cần rút hàng khi gọi.'),
          ('Cần cung cấp thông tin gì để báo giá?', 'Loại container, trọng lượng hàng, loại hàng, địa điểm và giờ rút. Ảnh chụp hàng hoặc mặt bằng gửi qua Zalo %s giúp báo giá nhanh hơn.' % TEL)],
    aside_title='Nhận báo giá bốc xếp container', aside_more=('Xem bảng giá bốc xếp', 'bang-gia-boc-xep.html'),
    side_links=BX_OTHERS + [('Bốc xếp', 'boc-xep.html'), ('Cho thuê xe tải', 'cho-thue-xe-tai.html')], og='truck'))

# --- Lắp đặt ---------------------------------------------------------------
LD_OTHERS = [('Tháo lắp nội thất', 'thao-lap-noi-that.html'), ('Tháo lắp máy lạnh', 'thao-lap-may-lanh.html'), ('Lắp đặt điện nước', 'lap-dat-dien-nuoc.html')]
NT_ROWS = [('Giường đơn', 'Rộng khoảng 1m', '300K'), ('Giường đôi', 'Rộng 1m6 đến 1m8', '350K'), ('Giường hộp, giường ngăn kéo', 'Có ngăn chứa đồ', '650K'),
           ('Tủ quần áo 2 cánh', '', '450K'), ('Tủ quần áo 3 cánh', '', '600K'), ('Tủ quần áo 4 cánh', '', '800K'), ('Tủ quần áo 5 đến 6 cánh', 'Giá từ, tùy kích thước', '900K'),
           ('Tủ kệ, tủ kính', 'Có bọc lót chống va đập', '350K'), ('Bàn làm việc', '', '250K'), ('Bộ sofa', 'Giá từ, tùy loại', '300K'),
           ('Ti vi treo tường', 'Tháo và lắp lại', '250K'), ('Quạt trần, quạt treo tường', '', '50K'), ('Giường tầng, tủ bếp, tủ ngoại cỡ', 'Báo giá theo khảo sát', 'Báo giá')]

PAGES.append(dict(
    slug='thao-lap-noi-that',
    title='Tháo lắp nội thất TPHCM: giường, tủ, sofa từ 300K | SGE',
    meta='Tháo lắp nội thất khi chuyển nhà TPHCM: giường đơn từ 300K, tủ 2 cánh từ 450K, bàn từ 250K. Giá tham khảo, báo giá chính xác gọi 0368 757 303.',
    h1='Tháo lắp nội thất khi chuyển nhà, chuyển văn phòng',
    lead='Giường, tủ, bàn, sofa tháo ra gọn để chuyển và lắp lại như cũ ở chỗ mới. Nhân viên SGE Viettrans có dụng cụ, giá tính theo từng món, báo rõ trước khi làm.',
    img=('thao-giuong', 'Nhân viên SGE Viettrans dùng máy khoan tháo giường khi chuyển nhà'),
    crumb_parent=('Lắp đặt', 'lap-dat.html'), service='Tháo lắp nội thất', dv='Chuyển nhà trọn gói',
    secs=[
        ('Tháo lắp nội thất gồm những gì', '<p>Đồ lớn không tháo thì khó qua cửa, dễ trầy xước và tốn chỗ trên xe. Dịch vụ gồm tháo, bọc lót, vận chuyển và lắp lại tại nơi mới.</p>'
         + ul(['Tháo và lắp giường, tủ quần áo, tủ kệ, bàn làm việc, sofa.', 'Tháo lắp ti vi treo tường, quạt trần, quạt treo tường.', 'Bọc lót chống va đập cho tủ kính, tủ kệ.', 'Đánh số, gom ốc vít để lắp lại đúng vị trí.'])),
        ('Bảng giá tháo lắp nội thất', '<p>Giá tham khảo cho một lần tháo và lắp lại tại nhà mới, tính theo từng món.</p>'
         + table(['Hạng mục', 'Quy cách', 'Chỉ từ (tháo + lắp)'], [[esc(a), esc(b), esc(c)] for a, b, c in NT_ROWS])
         + '<p class="pg-note">Giá cho đồ gỗ công nghiệp thông thường. Đồ gỗ tự nhiên, kích thước lớn, kết cấu phức tạp hoặc tầng cao không thang máy được báo giá sau khi xem ảnh hoặc khảo sát. Gọi %s để báo giá chính xác.</p>' % TEL
         + '<p>Xem thêm <a href="bang-gia-thao-lap.html">bảng giá tháo lắp</a>.</p>'),
        ('Giá tháo lắp nội thất tính dựa trên gì', ul(['Số lượng và kích thước từng món.', 'Đồ lắp ráp phức tạp, nhiều chi tiết.', 'Có cần lắp lại ở nơi mới hay chỉ tháo.', 'Tầng cao, có thang máy hay không.'])),
        ('Nằm trong chuyển nhà trọn gói', '<p>Với <a href="chuyen-nha-tron-goi.html">chuyển nhà trọn gói chỉ từ 800K</a>, tháo lắp nội thất là một phần của dịch vụ. Chỉ cần tháo lắp riêng, bạn vẫn đặt được theo bảng trên.</p>'),
    ],
    faqs=[('Tháo lắp giường đôi giá bao nhiêu?', 'Tháo và lắp lại giường đôi chỉ từ 350K. Đây là giá tham khảo cho đồ gỗ công nghiệp thông thường, báo giá chính xác sau khi xem ảnh hoặc khảo sát.'),
          ('Tháo lắp tủ quần áo giá bao nhiêu?', 'Tủ 2 cánh chỉ từ 450K, tủ 3 cánh chỉ từ 600K, tủ 4 cánh chỉ từ 800K, tủ 5 đến 6 cánh từ 900K. Giá tham khảo, gọi %s để báo giá chính xác.' % TEL),
          ('Tháo lắp có nằm trong gói chuyển nhà trọn gói không?', 'Có. Với chuyển nhà trọn gói, tháo lắp nội thất là một phần của dịch vụ.'),
          ('Đồ gỗ tự nhiên có tháo lắp được không?', 'Được, nhưng kết cấu thường phức tạp và nặng nên được báo giá sau khi xem ảnh hoặc khảo sát. Gửi ảnh qua Zalo %s để báo giá nhanh.' % TEL)],
    aside_title='Nhận báo giá tháo lắp nội thất', aside_more=('Xem bảng giá tháo lắp', 'bang-gia-thao-lap.html'),
    side_links=LD_OTHERS + [('Lắp đặt', 'lap-dat.html'), ('Chuyển nhà trọn gói', 'chuyen-nha-tron-goi.html')], og='thao-giuong'))

PAGES.append(dict(
    slug='thao-lap-may-lanh',
    title='Tháo lắp máy lạnh TPHCM trọn bộ chỉ từ 600K | SGE Viettrans',
    meta='Tháo lắp máy lạnh khi chuyển nhà TPHCM: tháo từ 220K, lắp từ 380K, trọn bộ từ 600K (treo tường 1 đến 2HP). Giá tham khảo, báo giá gọi 0368 757 303.',
    h1='Tháo lắp, di dời máy lạnh khi chuyển nhà',
    lead='Chuyển nhà là phải dời máy lạnh. SGE Viettrans tháo dàn lạnh, dàn nóng, chở đến nhà mới và lắp lại. Tháo và lắp trọn bộ máy treo tường chỉ từ 600K.',
    img=('thao-may-lanh', 'Nhân viên SGE Viettrans tháo máy lạnh treo tường, áo đồng phục có hotline 0368 757 303'),
    crumb_parent=('Lắp đặt', 'lap-dat.html'), service='Tháo lắp máy lạnh', dv='Chuyển nhà trọn gói',
    secs=[
        ('Dịch vụ tháo lắp máy lạnh gồm những gì', ul(['Tháo dàn lạnh, dàn nóng, ống đồng, dây điện.', 'Vận chuyển dàn nóng và dàn lạnh cùng đợt chuyển nhà.', 'Lắp lại, kiểm tra máy chạy ở nơi mới.', 'Báo rõ vật tư phát sinh (ống đồng, gas, giá đỡ nếu cần thay mới) trước khi thi công.'])
         + picture('dan-nong-may-lanh', 'Nhân viên SGE Viettrans vận chuyển dàn nóng máy lạnh Daikin sau khi tháo')),
        ('Bảng giá tháo lắp máy lạnh', '<p>Áp dụng cho máy lạnh treo tường công suất 1HP đến 2HP, tính mỗi bộ.</p>'
         + table(['Hạng mục', 'Chỉ từ'], [[esc(a), esc(b)] for a, b in [('Tháo máy lạnh', '220K'), ('Lắp máy lạnh', '380K'), ('Tháo và lắp trọn bộ', '600K')]], 'tbl t2')
         + '<p class="pg-note">Giá chưa gồm vật tư phát sinh (ống đồng, gas, giá đỡ nếu cần thay mới), vật tư được báo rõ trước khi thi công. Máy âm trần, máy tủ đứng báo giá theo khảo sát. Gọi %s để báo giá chính xác.</p>' % TEL),
        ('Nên tháo lắp máy lạnh cùng lúc chuyển nhà', '<p>Đặt cùng lúc với chuyển nhà giúp lịch gọn, một đội phối hợp từ tháo đến lắp, máy lạnh không phải nằm chờ ở nhà cũ. Với <a href="chuyen-nha-tron-goi.html">chuyển nhà trọn gói chỉ từ 800K</a>, bạn chọn thêm hạng mục này khi đặt lịch.</p>'),
        ('Chuẩn bị trước khi tháo máy lạnh', ul(['Cho biết số lượng máy, công suất và loại máy (treo tường, âm trần, tủ đứng).', 'Chụp ảnh vị trí dàn nóng, nhất là khi ở ban công, tầng cao.', 'Chọn vị trí lắp ở nhà mới và cho biết đã có sẵn đường ống, đường điện chưa.', 'Hẹn lịch tháo gần ngày chuyển để nhà cũ ít phải chịu nóng.'])),
    ],
    faqs=[('Tháo lắp máy lạnh giá bao nhiêu?', 'Tháo máy lạnh chỉ từ 220K, lắp chỉ từ 380K, tháo và lắp trọn bộ chỉ từ 600K cho máy treo tường 1 đến 2HP, chưa gồm vật tư phát sinh. Giá tham khảo, gọi %s để báo giá chính xác.' % TEL),
          ('Máy lạnh âm trần, tủ đứng có tháo lắp được không?', 'Có nhận, nhưng được báo giá theo khảo sát do kết cấu và công suất khác nhau. Gửi ảnh qua Zalo %s để báo giá nhanh.' % TEL),
          ('Vật tư phát sinh gồm những gì?', 'Thường là ống đồng, gas, giá đỡ nếu cần thay mới. Vật tư được báo rõ trước khi thi công, bạn đồng ý rồi mới làm.'),
          ('Có tháo lắp máy lạnh cùng chuyển nhà trọn gói không?', 'Có. Bạn cho biết số máy khi đặt lịch chuyển nhà, chúng tôi sắp xếp tháo, chở và lắp lại trong cùng đợt.')],
    aside_title='Nhận báo giá tháo lắp máy lạnh', aside_more=('Xem bảng giá tháo lắp', 'bang-gia-thao-lap.html'),
    side_links=LD_OTHERS + [('Lắp đặt', 'lap-dat.html'), ('Chuyển nhà trọn gói', 'chuyen-nha-tron-goi.html')], og='thao-may-lanh'))

PAGES.append(dict(
    slug='lap-dat-dien-nuoc',
    title='Lắp đặt điện nước cho nhà, văn phòng TPHCM | SGE',
    meta='Khảo sát, tư vấn bố trí và thi công đường điện, đường nước cho nhà mới, văn phòng, cửa hàng TPHCM. Báo giá sau khi khảo sát, gọi 0368 757 303.',
    h1='Lắp đặt, bố trí đường điện nước cho nhà và văn phòng',
    lead='Chuyển vào nơi mới cần đường điện, đường nước đúng chỗ đặt máy móc, thiết bị. SGE Viettrans khảo sát trực tiếp, tư vấn bố trí và báo giá sau khi xem hiện trạng.',
    img=None,
    crumb_parent=('Lắp đặt', 'lap-dat.html'), service='Lắp đặt điện nước', dv='Chuyển văn phòng', robots='noindex, follow',
    secs=[
        ('Khi nào cần lắp đặt điện nước', ul(['Chuyển vào nhà mới, văn phòng mới cần bố trí lại ổ điện, đường điện cho thiết bị.', 'Cần đi lại đường nước cho máy giặt, bếp, khu vệ sinh theo vị trí đặt đồ mới.',
                                              'Văn phòng, cửa hàng cần bố trí điện cho máy móc, máy lạnh, thiết bị văn phòng.', 'Muốn tư vấn bố trí đường điện, đường nước trước khi sắp xếp nội thất.'])),
        ('Vì sao báo giá sau khi khảo sát', '<p>Mỗi công trình một khác: kết cấu tường, đường ống có sẵn, công suất thiết bị, vị trí đặt máy. Vì vậy SGE Viettrans không niêm yết giá chung mà cử người đến xem hiện trạng, tư vấn phương án rồi báo giá một lần.</p>'
         + ul(['Khảo sát tại chỗ để nắm hiện trạng và yêu cầu.', 'Đề xuất phương án bố trí, nêu rõ vật tư cần dùng.', 'Báo giá trọn gói, chốt trước khi thi công.', 'Thi công đúng lịch hẹn, kiểm tra vận hành cùng bạn.'])),
        ('Đặt lịch khảo sát', '<p>Gọi %s hoặc nhắn Zalo, cho biết loại công trình, địa chỉ, nhu cầu và ảnh hiện trạng nếu có. Chúng tôi hẹn lịch khảo sát và báo giá sau khi xem trực tiếp.</p>' % TEL
         + '<p>Cần dọn nhà hoặc văn phòng cùng lúc, xem <a href="chuyen-nha-tron-goi.html">chuyển nhà trọn gói</a> và <a href="chuyen-van-phong.html">chuyển văn phòng</a>.</p>'),
    ],
    faqs=[('Lắp đặt điện nước giá bao nhiêu?', 'Giá phụ thuộc hiện trạng và yêu cầu nên được báo sau khi khảo sát trực tiếp. Gọi %s hoặc nhắn Zalo để đặt lịch khảo sát.' % TEL),
          ('Có cần gửi ảnh hiện trạng trước không?', 'Không bắt buộc, nhưng ảnh hoặc video hiện trạng giúp chúng tôi chuẩn bị phương án trước khi đến khảo sát.'),
          ('Khảo sát có mất phí không?', 'Hãy gọi %s để xác nhận chính sách khảo sát cho công trình của bạn.' % TEL)],
    aside_title='Đặt lịch khảo sát điện nước', aside_more=('Xem trang Lắp đặt', 'lap-dat.html'),
    side_links=LD_OTHERS + [('Lắp đặt', 'lap-dat.html'), ('Chuyển văn phòng', 'chuyen-van-phong.html')], og='truck'))

PAGES.append(dict(
    slug='lap-dat',
    title='Dịch vụ lắp đặt TPHCM: nội thất, máy lạnh, điện nước | SGE',
    meta='Dịch vụ lắp đặt SGE Viettrans TPHCM: tháo lắp nội thất từ 300K, máy lạnh trọn bộ từ 600K, điện nước báo giá sau khảo sát. Gọi 0368 757 303 để được tư vấn.',
    h1='Dịch vụ lắp đặt tại TP. Hồ Chí Minh',
    lead='Tháo lắp nội thất, tháo lắp máy lạnh, lắp đặt điện nước: ba việc thường đi kèm chuyển nhà, chuyển văn phòng, do cùng một đội SGE Viettrans phối hợp.',
    img=('lap-kinh-thang-nhom', 'Hai nhân viên SGE Viettrans tháo lắp vách kính mặt tiền bằng thang nhôm'),
    crumb_parent=None, service='Dịch vụ lắp đặt', dv='Chuyển nhà trọn gói',
    secs=[
        ('Chọn dịch vụ lắp đặt', '<p>Chọn việc bạn cần, mỗi dịch vụ có trang riêng với giá và quy trình chi tiết.</p>'
         + table(['Dịch vụ', 'Giá'], [
             ['<a href="thao-lap-noi-that.html">Tháo lắp nội thất</a><small>Giường, tủ, bàn, sofa, ti vi</small>', 'Chỉ từ 300K'],
             ['<a href="thao-lap-may-lanh.html">Tháo lắp máy lạnh</a><small>Máy treo tường 1 đến 2HP, trọn bộ chỉ từ 600K</small>', 'Chỉ từ 220K'],
             ['<a href="lap-dat-dien-nuoc.html">Lắp đặt điện nước</a><small>Khảo sát, tư vấn bố trí, thi công</small>', 'Báo giá sau khảo sát']], 'tbl t2')
         + '<p class="pg-note">Giá tham khảo, tùy số lượng và điều kiện thực tế. Gọi %s để báo giá chính xác.</p>' % TEL),
        ('Vì sao đặt lắp đặt cùng chuyển nhà', ul(['Một đội phối hợp từ tháo, vận chuyển đến lắp lại, ít phải hẹn nhiều bên.', 'Lịch gọn, ít thời gian nhà cũ và nhà mới ở trạng thái dang dở.', 'Báo giá một lần, rõ từng hạng mục.', 'Đồ được bọc lót, tháo đánh số để lắp lại đúng vị trí.'])
         + '<p>Xem <a href="chuyen-nha-tron-goi.html">chuyển nhà trọn gói chỉ từ 800K</a> và <a href="chuyen-van-phong.html">chuyển văn phòng</a>.</p>'),
        ('Quy trình đặt dịch vụ lắp đặt', ol([('Gọi hoặc nhắn Zalo', 'Mô tả đồ, số máy lạnh hoặc yêu cầu điện nước.'), ('Xem ảnh hoặc khảo sát', 'Đồ phức tạp hoặc điện nước được khảo sát trực tiếp.'),
                                              ('Báo giá một lần', 'Giá từng hạng mục, vật tư phát sinh nếu có.'), ('Thi công và kiểm tra', 'Tháo, lắp, chạy thử cùng bạn.')])),
    ],
    faqs=[('Dịch vụ lắp đặt của SGE Viettrans gồm những gì?', 'Tháo lắp nội thất, tháo lắp máy lạnh và lắp đặt điện nước. Tháo lắp nội thất chỉ từ 300K, tháo và lắp trọn bộ máy lạnh treo tường chỉ từ 600K, điện nước báo giá sau khảo sát.'),
          ('Có đặt riêng lắp đặt, không chuyển nhà được không?', 'Được. Bạn chỉ cần tháo lắp hoặc lắp đặt riêng vẫn đặt được. Gọi %s để hẹn lịch.' % TEL),
          ('Giá lắp đặt có phải giá cuối cùng không?', 'Đây là giá tham khảo. Đồ lớn, kết cấu phức tạp, máy lạnh âm trần hoặc điện nước được báo giá sau khi xem ảnh hoặc khảo sát.')],
    aside_title='Nhận báo giá lắp đặt', aside_more=('Xem bảng giá tháo lắp', 'bang-gia-thao-lap.html'),
    side_links=LD_OTHERS + [('Chuyển nhà trọn gói', 'chuyen-nha-tron-goi.html'), ('Chuyển văn phòng', 'chuyen-van-phong.html')], og='thao-giuong'))


# ---------------------------------------------------------------------------
# Dựng trang
# ---------------------------------------------------------------------------
def build(p):
    slug = p['slug']; url = BASE + slug + '.html'
    robots = p.get('robots', 'index, follow, max-image-preview:large')
    if robots.startswith('noindex') and 'max-image' not in robots:
        robots = 'noindex, follow'
    og_img = BASE + VARS['assets/%s.jpg' % p['og']]['jpg']
    head_end = TPL.index('<script type="application/ld+json">')
    head = TPL[:head_end]
    rep = [
        (r'<title>.*?</title>', '<title>%s</title>' % esc(p['title'])),
        (r'<meta name="description" content=".*?">', '<meta name="description" content="%s">' % html.escape(p['meta'])),
        (r'<link rel="canonical" href=".*?">', '<link rel="canonical" href="%s">' % url),
        (r'<meta name="robots" content=".*?">', '<meta name="robots" content="%s">' % robots),
        (r'<meta property="og:title" content=".*?">', '<meta property="og:title" content="%s">' % html.escape(p['title'])),
        (r'<meta property="og:description" content=".*?">', '<meta property="og:description" content="%s">' % html.escape(p['meta'])),
        (r'<meta property="og:url" content=".*?">', '<meta property="og:url" content="%s">' % url),
        (r'<meta property="og:image" content=".*?">', '<meta property="og:image" content="%s">' % og_img),
    ]
    for a, b in rep:
        head, n = re.subn(a, lambda m, b=b: b, head, count=1, flags=re.S)
        assert n == 1, a
    # JSON-LD
    old = json.loads(re.search(r'<script type="application/ld\+json">\s*(.*?)\s*</script>', TPL, re.S).group(1))
    org = old['@graph'][0]
    crumbs = [('Trang chủ', BASE), ('Dịch vụ', BASE + 'dich-vu.html')]
    if p['crumb_parent']:
        crumbs.append((p['crumb_parent'][0], BASE + p['crumb_parent'][1]))
    crumbs.append((p['h1'] if False else p['service'], url))
    graph = [org,
             {'@type': 'BreadcrumbList', 'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': u} for i, (n, u) in enumerate(crumbs)]},
             {'@type': 'Service', 'name': p['service'], 'serviceType': p['service'], 'provider': {'@id': BASE + '#org'},
              'areaServed': org['areaServed'], 'description': p['meta'], 'url': url},
             {'@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in p['faqs']]}]
    ld = json.dumps({'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False, indent=1)
    head += '<script type="application/ld+json">\n%s\n</script>\n' % ld
    # body trước <main>
    b0 = TPL.index('</head>')
    b1 = TPL.index('<main id="noi-dung">')
    mid = TPL[b0:b1]
    mid = re.sub(r'<ul class="dd-menu mega">.*?</ul>(?=\s*</div>)', lambda m: menu_groups.mega('', slug + '.html'), mid, count=1, flags=re.S)
    tail = TPL[TPL.index('</main>'):]
    # main
    crumb_html = '<a href="index.html">Trang chủ</a> <span aria-hidden="true">/</span> <a href="dich-vu.html">Dịch vụ</a> <span aria-hidden="true">/</span> '
    if p['crumb_parent']:
        crumb_html += '<a href="%s">%s</a> <span aria-hidden="true">/</span> ' % (p['crumb_parent'][1], esc(p['crumb_parent'][0]))
    crumb_html += '<span>%s</span>' % esc(p['service'])
    dvq = 'index.html?dv=%s#phieu' % urllib.parse.quote(p['dv'])
    # sections
    secs = list(p['secs']) + [('Câu hỏi thường gặp', faq_html(p['faqs']))]
    toc = '<nav class="toc-box" aria-label="Mục lục"><b>Nội dung chính</b><ol>' + ''.join('<li><a href="#m%d">%s</a></li>' % (i + 1, esc(t)) for i, (t, _) in enumerate(secs)) + '</ol></nav>'
    body = ''
    for i, (t, c) in enumerate(secs):
        body += '<section id="m%d"><h2>%s</h2>%s</section>\n' % (i + 1, esc(t), c)
    fig = picture(*p['img'], lazy=False) + '\n    ' if p['img'] else ''
    side = ''.join('<li><a href="%s">%s</a></li>' % (h, esc(t)) for t, h in p['side_links'] if h != slug + '.html')
    main = ('<main id="noi-dung">\n<section class="page-head"><div class="wrap"><nav class="crumb" aria-label="Đường dẫn">%s</nav>\n'
            '<h1>%s</h1><p class="lead">%s</p>\n'
            '<div class="head-act"><a class="btn" href="tel:0368757303">Gọi %s</a><a class="btn btn-ghost" href="%s">Lập phiếu báo giá</a></div></div></section>\n'
            '<section class="detail"><div class="wrap grid">\n  <article class="prose">\n    %s%s\n    %s\n  </article>\n'
            '  <div class="side">\n  <aside class="aside" aria-label="Liên hệ">\n    <h2>%s</h2>\n    <p>Tư vấn và báo giá 24/7, gọi là có người nghe máy.</p>\n'
            '    <a class="call" href="tel:0368757303">%s</a>\n    <a class="btn" href="%s">Lập phiếu báo giá</a>\n'
            '    <a class="btn btn-ghost" href="https://zalo.me/0368757303" target="_blank" rel="noopener">Nhắn Zalo</a>\n    <a class="more" href="%s">%s</a>\n  </aside>\n'
            '  <div class="side-box"><h2>Dịch vụ liên quan</h2><ul class="side-links">%s</ul></div>\n  </div>\n</div></section>\n')
    main = main % (crumb_html, esc(p['h1']), esc(p['lead']), TEL, dvq, fig, toc, body.rstrip(), esc(p['aside_title']), TEL, dvq, p['aside_more'][1], esc(p['aside_more'][0]), side)
    out = head + mid + main + tail
    assert not PRICE_RULE_FORBIDDEN.search(out), slug
    open(ROOT + slug + '.html', 'w', encoding='utf8').write(out)
    return slug


if __name__ == '__main__':
    for p in PAGES:
        print('tạo', build(p))
