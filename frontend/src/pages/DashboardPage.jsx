import React from "react";

function DashboardPage() {
	return (
		<>
			<section className="home-hero">
				<div>
					<h2>Hôm nay bạn muốn làm gì?</h2>
					<p>Tổng hợp việc cần làm, lịch họp và thông báo cho nhân viên.</p>
					<div className="home-actions">
						<button type="button">Mở bảng điều khiển</button>
						<button type="button" className="ghost">
							Xem công việc hôm nay
						</button>
					</div>
				</div>
			</section>
			<section className="home-grid">
				<div className="home-card">
					<h3>Chấm công</h3>
					<p>Cập nhật trạng thái đến muộn, ra sớm và báo cáo nhanh.</p>
				</div>
				<div className="home-card">
					<h3>Công việc</h3>
					<p>Danh sách việc cần làm và tiến độ thực hiện trong tuần.</p>
				</div>
				<div className="home-card">
					<h3>Thông báo</h3>
					<p>Nhắc nhở và cập nhật mới từ phòng ban.</p>
				</div>
			</section>
		</>
	);
}

export default DashboardPage;
