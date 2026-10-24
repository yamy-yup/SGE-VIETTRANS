# Design: SGE Viettrans (xanh - đỏ - trắng, ban ngày)

Nguồn: ảnh mẫu do chủ công ty chốt (24/10/2026). Trang một cột, nền trắng, ảnh chụp bãi xe làm bằng chứng đầu tiên.

## Màu
- `--blue` #184e94: thanh tiện ích, nền khối liên hệ, số bước
- `--navy` #0f2f63: chữ tiêu đề, chân trang
- `--red` #d52b2c (hover #b21f20): mọi nút hành động, ô biểu tượng, bước cuối
- `--mist` #eef3fa: nền dịch vụ và phiếu báo giá
- `--ink` #16233b, `--muted` #4a5875: chữ thân; `--line` #d3ddec: đường kẻ

## Chữ
- Tiêu đề: Montserrat 700-800 (self-host `assets/fonts/montserrat.woff`), chữ hoa có giãn cho menu và nhãn nút
- Thân: Be Vietnam Pro 400/500; h2 `clamp(1.75rem, 1.15rem + 2.2vw, 2.8rem)`, h1 hero tối đa 6rem

## Thành phần
- Nút: viên thuốc, đỏ đặc (chính), trắng (trên ảnh), viền xanh (phụ); bóng mềm có độ lệch
- Ô cam kết: ô vuông đỏ 56 px, biểu tượng nét 1.7 trắng
- Dải ưu đãi: ảnh phủ xanh, người nhô lên trên dải; từ 1100 px chữ đè lên ảnh, dưới đó chữ nằm trong khối xanh bên dưới
- Hero: ảnh tràn ngang, chữ trên bầu trời; dưới 760 px ảnh nằm dưới khối chữ
- Chuyển động: chỉ ảnh hero lắng xuống và chữ hero hiện lên khi tải trang; tôn trọng giảm chuyển động
