# Dữ liệu 25 khu vực. Đặc điểm chỉ ghi điều ai sống ở TP.HCM cũng biết; không bịa thời gian xe đến hay số liệu.
# kind: 'noi' = nội thành (áp dụng giờ cấm xe tải), 'ngoai' = ngoại thành, 'lan' = khu vực lân cận
AREAS = [
 ('Quận 1', 'noi', 'Quận 1 là trung tâm thành phố với nhiều cao ốc văn phòng, căn hộ chung cư và nhà phố mặt tiền. Đường đông xe, nhiều tuyến một chiều và chỗ đỗ xe hạn chế nên lịch xe cần sắp xếp khéo.'),
 ('Quận 3', 'noi', 'Quận 3 có nhiều nhà phố trong hẻm, biệt thự cũ và văn phòng nhỏ. Nhiều con hẻm hẹp, xe tải lớn khó vào, nên thường cần xe nhỏ hoặc trung chuyển bằng xe đẩy.'),
 ('Quận 4', 'noi', 'Quận 4 nằm giữa sông Sài Gòn và các con kênh, có nhiều chung cư mới ven sông bên cạnh khu nhà phố cũ. Chuyển đồ ở chung cư cần đăng ký thang máy với ban quản lý.'),
 ('Quận 5', 'noi', 'Quận 5 là khu Chợ Lớn với nhiều nhà phố vừa ở vừa buôn bán. Hàng hóa và đồ đạc thường nhiều, đường đông vào giờ cao điểm.'),
 ('Quận 6', 'noi', 'Quận 6 có chợ Bình Tây, nhiều nhà phố buôn bán và kho hàng nhỏ. Nhu cầu chở hàng cho cửa hàng, sạp chợ khá thường xuyên.'),
 ('Quận 7', 'noi', 'Quận 7 có khu Phú Mỹ Hưng, nhiều chung cư cao tầng và khu chế xuất Tân Thuận. Chuyển nhà ở đây phần lớn là căn hộ chung cư, cần hẹn thang máy và giờ chuyển với tòa nhà.'),
 ('Quận 8', 'noi', 'Quận 8 có nhiều kênh rạch, hẻm nhỏ và các chung cư mới dọc bờ kênh. Đường vào nhà trong hẻm cần được hỏi kỹ để chọn đúng cỡ xe.'),
 ('Quận 10', 'noi', 'Quận 10 đông dân với nhiều nhà phố, trường đại học và phòng trọ cho sinh viên. Chuyển phòng trọ, căn hộ nhỏ là nhu cầu phổ biến.'),
 ('Quận 11', 'noi', 'Quận 11 có nhiều nhà phố liền kề, cửa hàng và xưởng sản xuất nhỏ. Đồ đạc thường kèm máy móc, hàng hóa cần bốc xếp cẩn thận.'),
 ('Quận 12', 'ngoai', 'Quận 12 là cửa ngõ phía bắc thành phố, có nhiều khu dân cư mới, nhà trọ và xưởng sản xuất. Đường rộng hơn khu trung tâm, thuận tiện cho xe tải.'),
 ('Bình Thạnh', 'noi', 'Bình Thạnh giáp Quận 1, có nhiều chung cư cao tầng xen lẫn hẻm sâu và nhà phố. Mỗi địa chỉ một điều kiện riêng, nên khảo sát trước giúp báo giá sát hơn.'),
 ('Gò Vấp', 'noi', 'Gò Vấp đông dân, nhiều nhà trọ và hẻm nhỏ. Chuyển phòng trọ, nhà nhỏ trong hẻm thường dùng xe van hoặc xe tải nhỏ.'),
 ('Phú Nhuận', 'noi', 'Phú Nhuận nằm gần sân bay Tân Sơn Nhất, có nhiều nhà phố, căn hộ dịch vụ và văn phòng nhỏ. Đường đông vào giờ cao điểm.'),
 ('Tân Bình', 'noi', 'Tân Bình có sân bay Tân Sơn Nhất, khu công nghiệp Tân Bình cùng nhiều văn phòng, nhà phố. Nhu cầu chuyển văn phòng và chở hàng khá lớn.'),
 ('Tân Phú', 'noi', 'Tân Phú là khu dân cư đông với nhiều nhà phố, xưởng may và cửa hàng. Hẻm nhiều, cần chọn xe phù hợp đường vào.'),
 ('Bình Tân', 'ngoai', 'Bình Tân có khu công nghiệp Tân Tạo, nhiều khu dân cư và nhà trọ công nhân. Chuyển phòng trọ, chở hàng cho xưởng là nhu cầu thường gặp.'),
 ('Thủ Đức', 'ngoai', 'Thủ Đức có khu công nghệ cao, làng đại học, khu Thảo Điền và nhiều chung cư mới. Quãng đường đến các quận trung tâm khá xa, nên lịch chuyển cần tính kỹ.'),
 ('Bình Chánh', 'ngoai', 'Bình Chánh ở phía tây nam thành phố, có nhiều khu dân cư mới, nhà vườn và kho bãi. Đường rộng, phù hợp xe tải lớn.'),
 ('Hóc Môn', 'ngoai', 'Hóc Môn ở phía bắc, có nhà vườn, nhà xưởng và khu dân cư đang phát triển. Đồ đạc thường nhiều và cồng kềnh.'),
 ('Củ Chi', 'ngoai', 'Củ Chi ở xa trung tâm, đất rộng, nhiều nhà xưởng và khu công nghiệp. Quãng đường dài nên cần chọn xe đủ tải để chở một chuyến.'),
 ('Nhà Bè', 'ngoai', 'Nhà Bè ở phía nam, giáp Quận 7, có nhiều khu dân cư và chung cư mới. Thường chuyển đồ giữa Nhà Bè và các quận trung tâm.'),
 ('Cần Giờ', 'ngoai', 'Cần Giờ là huyện ven biển xa nhất của thành phố, đường đi qua phà Bình Khánh. Cần hẹn lịch sớm để sắp xếp xe và thời gian di chuyển.'),
 ('Bình Dương', 'lan', 'Bình Dương (nay thuộc TP. Hồ Chí Minh) có nhiều khu công nghiệp và khu dân cư ở Thủ Dầu Một, Dĩ An, Thuận An. Nhu cầu chuyển nhà, chuyển xưởng và chở hàng giữa Bình Dương và trung tâm thành phố rất lớn.'),
 ('Long An', 'lan', 'Long An (nay thuộc tỉnh Tây Ninh) là cửa ngõ miền Tây, giáp phía tây nam TP. Hồ Chí Minh, có nhiều khu công nghiệp. Tuyến chuyển đồ giữa Long An và thành phố cần tính quãng đường và giờ xe chạy.'),
 ('Biên Hòa', 'lan', 'Biên Hòa (Đồng Nai) là trung tâm công nghiệp lớn phía đông TP. Hồ Chí Minh. Tuyến Biên Hòa – TP.HCM thường dùng cho chuyển nhà, chuyển văn phòng và chở hàng xưởng.'),
]

# Các mẫu câu xoay vòng để mỗi trang có cách diễn đạt khác nhau.
INTRO = [
 'SGE Viettrans nhận {svc} tại {area}. Nhân viên mặc đồng phục, xe tải thùng mang thương hiệu SGE, chi phí báo rõ trước khi làm.',
 'Bạn đang tìm dịch vụ {svc} ở {area}? SGE Viettrans có đội ngũ đồng phục và xe tải thùng SGE, báo giá rõ ràng trước khi bắt đầu.',
 'Dịch vụ {svc} {area} của SGE Viettrans: đến đúng hẹn, làm cẩn thận, giá nói trước, tư vấn và báo giá 24/7.',
 'Cần {svc} ở {area}? Gọi SGE Viettrans để được tư vấn và báo giá ngay, chúng tôi sắp xếp người và xe theo đúng điều kiện nhà bạn.',
]
WHY = [
 ['Báo giá rõ trước khi làm, bạn đồng ý rồi mới bắt đầu.', 'Nhân viên mặc đồng phục, dễ nhận biết khi đến nhà bạn.', 'Xe tải thùng SGE, chọn cỡ xe theo khối lượng đồ.', 'Tư vấn và báo giá 24/7 qua hotline, Zalo.'],
 ['Một người phụ trách từ lúc nhận cuộc gọi đến khi bàn giao.', 'Đồ được bọc, đóng gói và bốc xếp cẩn thận, có đồ bảo hộ.', 'Lịch xe sắp xếp theo quy định giờ chạy xe tải.', 'Giá nói trước, không phát sinh mập mờ.'],
 ['Tư vấn đúng cỡ xe để bạn không trả tiền cho chỗ trống.', 'Nhân công quen việc với đồ nặng, cồng kềnh.', 'Đến đúng giờ hẹn, làm gọn trong ngày.', 'Liên hệ bất cứ lúc nào qua điện thoại, Zalo, Facebook.'],
]
NOTE = {
 'noi': '{area} thuộc khu vực nội thành, nơi áp dụng giờ cấm xe tải theo quy định của TP. Hồ Chí Minh. Chúng tôi xếp lịch xe trong khung giờ được phép và báo trước giờ đến cho bạn. Xem thêm <a href="{p}blog/gio-cam-xe-tai-tphcm.html">giờ cấm xe tải TP.HCM</a>.',
 'ngoai': '{area} có đường rộng hơn khu trung tâm nhưng quãng đường thường xa hơn. Chúng tôi tính trước lộ trình và thời gian di chuyển, kiểm tra quy định giờ chạy xe tải trên tuyến đi qua nội thành.',
 'lan': 'Tuyến {area} – TP. Hồ Chí Minh là tuyến liên tỉnh, chi phí phụ thuộc nhiều vào quãng đường. Chúng tôi báo giá trọn chuyến trước khi đi để bạn chủ động.',
}
