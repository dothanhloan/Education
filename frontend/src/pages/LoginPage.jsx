import React from "react";

function LoginPage({
	identifier,
	password,
	status,
	loading,
	onIdentifierChange,
	onPasswordChange,
	onSubmit,
}) {
	return (
		<div className="login-page">
			<section className="login-panel">
				<div className="brand">
					<span className="brand-badge">ICS</span>
					HRMS PORTAL
				</div>
				<div>
					<h1 className="login-title">Đăng nhập hệ thống</h1>
					<p className="login-subtitle">
						Quản lý nhân sự, công việc và tài liệu tập trung cho toàn bộ đội ngũ.
					</p>
				</div>
				<div className="login-card">
					<h2>Đăng nhập</h2>
					<p>Nhập email hoặc số điện thoại và mật khẩu của bạn.</p>
					<form onSubmit={onSubmit}>
						<div className="form-group">
							<label htmlFor="identifier">Email hoặc số điện thoại</label>
							<input
								id="identifier"
								type="text"
								placeholder="name@company.com"
								value={identifier}
								onChange={(event) => onIdentifierChange(event.target.value)}
							/>
						</div>
						<div className="form-group">
							<label htmlFor="password">Mật khẩu</label>
							<input
								id="password"
								type="password"
								placeholder="Nhập mật khẩu"
								value={password}
								onChange={(event) => onPasswordChange(event.target.value)}
							/>
						</div>
						{status.message ? (
							<div className={`alert ${status.type}`}>{status.message}</div>
						) : null}
						<div className="login-actions">
							<button type="submit" disabled={loading}>
								{loading ? "Đang xử lý..." : "Đăng nhập"}
							</button>
							<a className="helper-link" href="#">
								Quên mật khẩu?
							</a>
						</div>
					</form>
				</div>
			</section>
			<aside className="side-panel">
				<div>
					<h3>Quản trị quy trình nhanh gọn</h3>
					<p>
						Theo dõi chấm công, công việc và cập nhật báo cáo từ một giao diện thống nhất.
					</p>
				</div>
				<div>
					<p>Hỗ trợ: admin@ics.vn</p>
				</div>
			</aside>
		</div>
	);
}

export default LoginPage;
