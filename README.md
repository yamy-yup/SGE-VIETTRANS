# SGE Viettrans - Website

Landing page một trang cho CÔNG TY TNHH THƯƠNG MẠI DỊCH VỤ VẬN TẢI SGE VIETTRANS.
HTML + CSS + JS thuần, không cần cài đặt hay build.

## Cấu trúc thư mục

```
sge-viettrans/
├── index.html
├── PRODUCT.md            (thông tin sản phẩm, dùng cho Claude khi chỉnh giao diện)
├── README.md
└── assets/
    ├── logo.jpg          (logo SGE Viettrans)
    ├── hero.jpg          (ảnh đầu trang, 2000 px ngang, từ ảnh mẫu đã bỏ chữ trên bầu trời)
    ├── hero-s.jpg        (cùng ảnh, 1100 px cho điện thoại)
    ├── truck.jpg         (xe tải thùng nhìn ngang, phần giới thiệu)
    ├── band.jpg          (dải ảnh phủ xanh, phần giảm 25%)
    ├── team.jpg          (đội ngũ trước xe tải)
    └── fonts/            (Montserrat, Be Vietnam Pro, kèm giấy phép OFL)
```

Các ảnh `hero`, `hero-s`, `truck`, `band`, `team` được cắt từ ảnh mẫu (ảnh minh họa dựng bằng AI, gốc chỉ rộng 768 px nên hơi mềm khi xem trên màn hình lớn). Khi có ảnh chụp thật của xe và nhân viên, thay đúng tên file và giữ tỉ lệ: hero 16:9 có bầu trời ở phần trên để đặt chữ.

## Đưa lên GitHub và bật website miễn phí

1. Đăng nhập GitHub, bấm **New repository**. Đặt tên, ví dụ `sge-viettrans`, chọn **Public**, bấm **Create repository**.
2. Bấm **uploading an existing file**, kéo thả `index.html`, `README.md` và thư mục `assets` (nếu có), bấm **Commit changes**.
3. Vào **Settings → Pages**. Ở mục **Build and deployment**, chọn **Deploy from a branch**, branch **main**, thư mục **/ (root)**, bấm **Save**.
4. Chờ khoảng 1-2 phút. Địa chỉ web sẽ có dạng `https://TEN-GITHUB.github.io/sge-viettrans/`.

## Cập nhật nội dung sau này

Mở `index.html` trên GitHub, bấm biểu tượng bút chì để sửa, rồi **Commit changes**. Web tự cập nhật sau ít phút.

## Những chỗ cần bổ sung (tìm chữ `TODO` trong index.html)

- Logo độ phân giải cao hơn (file hiện tại chỉ 160x160 px, hơi mờ trên màn hình lớn): thay `assets/logo.jpg`, nên dùng ảnh PNG nền trong suốt từ 512x512 px
- Ảnh chụp thật tại hiện trường và đội xe thay cho ảnh minh họa (xem danh sách ảnh ở trên)
- Link Zalo chính thức (hiện đang dùng `zalo.me/0368757303`)
- Link Facebook, TikTok, Zalo ở chân trang
- Ảnh chia sẻ (og:image) và địa chỉ web (og:url)
- Bảng giá từng dịch vụ
- Điều kiện và thời hạn chương trình giảm 25%
- Form báo giá hiện mở ứng dụng email. Muốn nhận thẳng về hộp thư không cần mở email, dùng Formspree hoặc Google Forms.

## Đổi màu thương hiệu

Sửa các biến ở đầu phần `<style>` trong `index.html` (`--blue` xanh dương, `--navy` xanh đậm cho chữ, `--red` đỏ SGE, `--mist` nền xanh nhạt).

## Phông chữ

Chữ tiêu đề dùng Montserrat, chữ thường dùng Be Vietnam Pro, đã đặt sẵn trong `assets/fonts/` (không gọi Google Fonts), giấy phép SIL OFL kèm theo trong cùng thư mục.

## Taste skill (thiết kế web)

Taste skill đã được chuyển sang kho skill riêng: https://github.com/yamy-yup/Skill-Claude (thư mục `skills/design-taste-frontend/`). Khi cần thiết kế hoặc chỉnh giao diện trang này, nhờ Claude đọc skill trong kho đó trước.

## Tên miền riêng

Khi có tên miền, vào **Settings → Pages → Custom domain** để gắn.
