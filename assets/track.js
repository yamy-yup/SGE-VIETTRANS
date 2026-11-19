/* Đo lường quảng cáo và chuyển đổi cho sgeviettrans.vn.
   Điền ID vào bảng C bên dưới. Để trống thì không tải công cụ nào của bên thứ ba,
   chỉ ghi sự kiện vào dataLayer.
   - GA4:      Measurement ID dạng G-XXXXXXXXXX
   - ADS:      Google Ads ID dạng AW-XXXXXXXXX
   - ADS_CALL / ADS_ZALO / ADS_LEAD: nhãn chuyển đổi (phần sau dấu / trong "AW-XXXX/nhan")
   - PIXEL:    Meta Pixel ID (dãy số) */
(function () {
  var C = { GA4: 'G-WM13QN6R5R', ADS: '', ADS_CALL: '', ADS_ZALO: '', ADS_LEAD: '', PIXEL: '' };

  window.dataLayer = window.dataLayer || [];
  function gtag() { window.dataLayer.push(arguments); }

  var first = C.GA4 || C.ADS;
  if (first) {
    var s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(first);
    document.head.appendChild(s);
    gtag('js', new Date());
    if (C.GA4) gtag('config', C.GA4);
    if (C.ADS) gtag('config', C.ADS);
  }

  if (C.PIXEL) {
    /* Đoạn mã Meta Pixel chuẩn */
    !function (f, b, e, v, n, t, s) {
      if (f.fbq) return; n = f.fbq = function () { n.callMethod ? n.callMethod.apply(n, arguments) : n.queue.push(arguments); };
      if (!f._fbq) f._fbq = n; n.push = n; n.loaded = !0; n.version = '2.0'; n.queue = []; t = b.createElement(e); t.async = !0;
      t.src = v; s = b.getElementsByTagName(e)[0]; s.parentNode.insertBefore(t, s);
    }(window, document, 'script', 'https://connect.facebook.net/en_US/fbevents.js');
    window.fbq('init', C.PIXEL);
    window.fbq('track', 'PageView');
  }

  var last = {};
  function track(name, params, adsKey, fbEvent) {
    var now = Date.now();
    if (last[name] && now - last[name] < 1500) return; /* chặn bấm đúp */
    last[name] = now;
    var p = params || {};
    p.page_path = location.pathname;
    window.dataLayer.push({ event: name, sge: p });
    if (C.GA4) gtag('event', name, p);
    if (C.ADS && C['ADS_' + adsKey]) gtag('event', 'conversion', { send_to: C.ADS + '/' + C['ADS_' + adsKey] });
    if (C.PIXEL && window.fbq) window.fbq('track', fbEvent);
  }

  document.addEventListener('click', function (e) {
    var a = e.target && e.target.closest ? e.target.closest('a[href]') : null;
    if (!a) return;
    var h = a.getAttribute('href') || '';
    if (/^tel:/i.test(h)) track('click_call', { link_url: h }, 'CALL', 'Contact');
    else if (/zalo\.me/i.test(h)) track('click_zalo', { link_url: h }, 'ZALO', 'Contact');
    else if (/^mailto:/i.test(h)) track('click_email', { link_url: h }, 'LEAD', 'Contact');
  }, true);

  /* Trang chủ gửi sự kiện này khi khách gửi phiếu báo giá hoặc sao chép nội dung phiếu để gửi Zalo */
  document.addEventListener('sge:lead', function (e) {
    var d = (e && e.detail) || {};
    track('generate_lead', { method: d.type || 'form', service: d.service || '' }, 'LEAD', 'Lead');
  });
})();
