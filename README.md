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
    ├── gallery-1.jpg     (ảnh xe tải, bốc xếp)
    ├── gallery-2.jpg     (ảnh tháo lắp)
    ├── gallery-3.jpg     (ảnh chuyển nhà)
    └── gallery-4.jpg     (ảnh đội ngũ)
```

Chưa có ảnh gallery thì web vẫn chạy: gallery hiện khung chờ. Thiếu logo thì header hiện chữ dự phòng.

## Đưa lên GitHub và bật website miễn phí

1. Đăng nhập GitHub, bấm **New repository**. Đặt tên, ví dụ `sge-viettrans`, chọn **Public**, bấm **Create repository**.
2. Bấm **uploading an existing file**, kéo thả `index.html`, `README.md` và thư mục `assets` (nếu có), bấm **Commit changes**.
3. Vào **Settings → Pages**. Ở mục **Build and deployment**, chọn **Deploy from a branch**, branch **main**, thư mục **/ (root)**, bấm **Save**.
4. Chờ khoảng 1-2 phút. Địa chỉ web sẽ có dạng `https://TEN-GITHUB.github.io/sge-viettrans/`.

## Cập nhật nội dung sau này

Mở `index.html` trên GitHub, bấm biểu tượng bút chì để sửa, rồi **Commit changes**. Web tự cập nhật sau ít phút.

## Những chỗ cần bổ sung (tìm chữ `TODO` trong index.html)

- Logo độ phân giải cao hơn (file hiện tại chỉ 160x160 px, hơi mờ trên màn hình lớn): thay `assets/logo.jpg`, nên dùng ảnh PNG nền trong suốt từ 512x512 px
- Ảnh thực tế: `assets/gallery-1.jpg` đến `gallery-4.jpg`
- Link Zalo chính thức (hiện đang dùng `zalo.me/0368757303`)
- Link Facebook, TikTok, Zalo ở chân trang
- Ảnh chia sẻ (og:image) và địa chỉ web (og:url)
- Bảng giá từng dịch vụ
- Điều kiện và thời hạn chương trình giảm 25%
- Form báo giá hiện mở ứng dụng email. Muốn nhận thẳng về hộp thư không cần mở email, dùng Formspree hoặc Google Forms.

## Đổi màu thương hiệu

Sửa các biến ở đầu phần `<style>` trong `index.html` (`--navy`, `--gold`, `--sky`, `--red`).

## Tên miền riêng

Khi có tên miền, vào **Settings → Pages → Custom domain** để gắn.
