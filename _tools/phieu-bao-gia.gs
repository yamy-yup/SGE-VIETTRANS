/**
 * SGE Viettrans: nhận phiếu báo giá từ sgeviettrans.vn
 *
 * Cách cài (một lần):
 * 1. Đăng nhập lienhe@sgeviettrans.vn, tạo Google Sheet tên "Phiếu báo giá SGE Viettrans".
 * 2. Tiện ích mở rộng → Apps Script, dán toàn bộ file này, Lưu.
 * 3. Triển khai → Tùy chọn triển khai mới → Loại: Ứng dụng web.
 *    Thực thi với tư cách: Tôi. Người có quyền truy cập: Bất kỳ ai.
 * 4. Cấp quyền (Sheet + gửi email), sao chép URL ứng dụng web (…/exec)
 *    và dán vào FORM_ENDPOINT trong index.html.
 */
const NOTIFY = 'lienhe@sgeviettrans.vn';
const SHEET = 'Phiếu báo giá';
const HEAD = ['Thời gian', 'Dịch vụ', 'Họ tên', 'Số điện thoại', 'Địa chỉ đi', 'Địa chỉ đến',
  'Ngày dự kiến', 'Đồ cần chuyển', 'Ghi chú', 'Trang gửi', 'Trạng thái'];

function doPost(e) {
  const p = (e && e.parameter) || {};
  if (p.website) return out_({ ok: true });            // ô bẫy chống spam bot
  const phone = String(p.phone || '').replace(/[\s.\-]/g, '');
  const name = String(p.name || '').trim();
  if (!/^(0|\+84)\d{9}$/.test(phone) || name.length < 2) return out_({ ok: false, error: 'invalid' });

  const clip = (s, n) => String(s || '').slice(0, n || 1000);
  const safe = s => { s = clip(s); return /^[=+\-@]/.test(s) ? "'" + s : s; }; // chặn công thức

  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const lock = LockService.getScriptLock();
  lock.waitLock(10000);
  try {
    let sh = ss.getSheetByName(SHEET);
    if (!sh) {
      sh = ss.insertSheet(SHEET);
      sh.appendRow(HEAD);
      sh.setFrozenRows(1);
      sh.getRange(1, 1, 1, HEAD.length).setFontWeight('bold').setBackground('#184e94').setFontColor('#ffffff');
    }
    sh.appendRow([new Date(), safe(p.service), safe(name), "'" + phone, safe(p.from), safe(p.to),
      safe(p.date), safe(p.items), safe(p.note), safe(p.page), 'Mới']);
  } finally {
    lock.releaseLock();
  }

  MailApp.sendEmail({
    to: NOTIFY,
    subject: 'Phiếu báo giá mới: ' + clip(p.service, 60) + ' - ' + clip(name, 60) + ' - ' + phone,
    body: clip(p.summary, 4000) + '\n\nGọi lại khách: ' + phone + '\nXem tất cả phiếu: ' + ss.getUrl()
  });
  return out_({ ok: true });
}

function doGet() { return out_({ ok: true, service: 'sge-quote' }); }

function out_(o) {
  return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON);
}
