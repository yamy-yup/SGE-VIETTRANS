# SGE Viettrans - Website

Landing page một trang cho CÔNG TY TNHH THƯƠNG MẠI DỊCH VỤ VẬN TẢI SGE VIETTRANS.
HTML + CSS + JS thuần, không cần cài đặt hay build.

## Cấu trúc thư mục

```
sge-viettrans/
├── index.html
├── README.md
└── assets/
    ├── logo.jpg          (logo SGE Viettrans, đã có)
    ├── hero.jpg          (ảnh đầu trang, máy tính, 2000 px ngang)
    ├── hero-m.jpg        (cùng ảnh, cắt cho điện thoại và máy tính bảng dọc)
    ├── fonts/            (Cormorant Garamond, Be Vietnam Pro)
    ├── field-1.jpg       (ảnh bốc xếp, chuyển đồ lên xe, dọc 4:5)
    ├── field-2.jpg       (ảnh tháo lắp tại chỗ, dọc 4:5)
    └── field-3.jpg       (ảnh xe tải thùng SGE, dọc 4:5)
```

Chưa có ảnh `field-*.jpg` thì mục "Công việc thực tế" tự ẩn, web vẫn chạy bình thường. Chép ảnh vào `assets/` là mục này tự hiện.

## Đưa lên GitHub và bật website miễn phí

1. Đăng nhập GitHub, bấm **New repository**. Đặt tên, ví dụ `sge-viettrans`, chọn **Public**, bấm **Create repository**.
2. Bấm **uploading an existing file**, kéo thả `index.html`, `README.md` và thư mục `assets` (nếu có), bấm **Commit changes**.
3. Vào **Settings → Pages**. Ở mục **Build and deployment**, chọn **Deploy from a branch**, branch **main**, thư mục **/ (root)**, bấm **Save**.
4. Chờ khoảng 1-2 phút. Địa chỉ web sẽ có dạng `https://TEN-GITHUB.github.io/sge-viettrans/`.

## Cập nhật nội dung sau này

Mở `index.html` trên GitHub, bấm biểu tượng bút chì để sửa, rồi **Commit changes**. Web tự cập nhật sau ít phút.

## Những chỗ cần bổ sung (tìm chữ `TODO` trong index.html)

- Logo độ phân giải cao hơn (file hiện tại chỉ 160x160 px, hơi mờ trên màn hình lớn): thay `assets/logo.jpg`, nên dùng ảnh PNG nền trong suốt từ 512x512 px
- Ảnh thực tế tại hiện trường: `assets/field-1.jpg` đến `field-3.jpg` (chưa có, mục "Công việc thực tế" đang ẩn). Ảnh đầu trang đã có (`hero.jpg`, `hero-m.jpg`). Muốn đổi ảnh đầu trang: giữ tỉ lệ ảnh gốc có phần mờ ở trên và dưới, chữ sẽ nằm trên các vùng mờ đó
- Link Zalo chính thức (hiện đang dùng `zalo.me/0368757303`)
- Link Facebook, TikTok, Zalo ở chân trang
- Ảnh chia sẻ (og:image) và địa chỉ web (og:url)
- Bảng giá từng dịch vụ
- Điều kiện và thời hạn chương trình giảm 25%
- Form báo giá hiện mở ứng dụng email. Muốn nhận thẳng về hộp thư không cần mở email, dùng Formspree hoặc Google Forms.

## Đổi màu thương hiệu

Sửa các biến ở đầu phần `<style>` trong `index.html` (`--ground`, `--s1` đến `--s3` là các tầng navy, `--gold`, `--ivory`).

## Phông chữ

Chữ tiêu đề dùng Cormorant Garamond, chữ thường dùng Be Vietnam Pro, đã đặt sẵn trong `assets/fonts/` (không gọi Google Fonts), giấy phép SIL OFL kèm theo trong cùng thư mục.

## Taste skill (thiết kế web)

Taste skill đã được chuyển sang kho skill riêng: https://github.com/yamy-yup/Skill-Claude (thư mục `skills/design-taste-frontend/`). Khi cần thiết kế hoặc chỉnh giao diện trang này, nhờ Claude đọc skill trong kho đó trước.

## Tên miền riêng

Khi có tên miền, vào **Settings → Pages → Custom domain** để gắn.
