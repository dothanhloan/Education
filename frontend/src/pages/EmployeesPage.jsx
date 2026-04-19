import React, { useEffect } from "react";

function EmployeesPage({
	employeeRows,
	employeeTotal,
	employeeQuery,
	employeeStatus,
	employeeLoading,
	employeePage,
	employeePageSize,
	employeeTotalPages,
	employeeFormOpen,
	employeeEditingId,
	employeeForm,
	deleteTarget,
	setEmployeeQuery,
	setEmployeeFormOpen,
	setEmployeeForm,
	setEmployeePageSize,
	resetEmployeeForm,
	fetchEmployees,
	openCreateEmployee,
	openEditEmployee,
	submitEmployeeForm,
	deleteEmployee,
	confirmDeleteEmployee,
	setDeleteTarget,
}) {
	useEffect(() => {
		fetchEmployees(1);
	}, []);

	return (
		<section className="admin-section">
			<div className="admin-section-header">
				<div>
					<h2>Danh sách nhân viên</h2>
					<p>Tổng số: {employeeTotal} nhân viên</p>
				</div>
				<div className="admin-actions">
					<input
						type="search"
						placeholder="Tìm theo tên, email, số điện thoại"
						value={employeeQuery}
						onChange={(event) => setEmployeeQuery(event.target.value)}
					/>
					<button type="button" onClick={() => fetchEmployees(1)}>
						Tìm kiếm
					</button>
					<button type="button" onClick={openCreateEmployee}>
						Thêm nhân viên
					</button>
				</div>
			</div>
			{employeeFormOpen ? (
				<div className="modal-backdrop">
					<div className="modal">
						<div className="modal-header">
							<h3>
								{employeeEditingId ? "Cập nhật nhân viên" : "Thêm nhân viên"}
							</h3>
							<button
								type="button"
								className="ghost"
								onClick={() => {
									setEmployeeFormOpen(false);
									resetEmployeeForm();
								}}
							>
								Đóng
							</button>
						</div>
						<div className="form-grid">
							<div className="form-group">
								<label>Họ tên *</label>
								<input
									value={employeeForm.ho_ten}
									onChange={(event) =>
										setEmployeeForm({
											...employeeForm,
											ho_ten: event.target.value,
										})
									}
								/>
							</div>
							<div className="form-group">
								<label>Email *</label>
								<input
									type="email"
									value={employeeForm.email}
									onChange={(event) =>
										setEmployeeForm({
											...employeeForm,
											email: event.target.value,
										})
									}
								/>
							</div>
							<div className="form-group">
								<label>{employeeEditingId ? "Mật khẩu" : "Mật khẩu *"}</label>
								<input
									type="password"
									value={employeeForm.mat_khau}
									onChange={(event) =>
										setEmployeeForm({
											...employeeForm,
											mat_khau: event.target.value,
										})
									}
								/>
							</div>
							<div className="form-group">
								<label>Số điện thoại</label>
								<input
									value={employeeForm.so_dien_thoai}
									onChange={(event) =>
										setEmployeeForm({
											...employeeForm,
											so_dien_thoai: event.target.value,
										})
									}
								/>
							</div>
							<div className="form-group">
								<label>Chức vụ</label>
								<input
									value={employeeForm.chuc_vu}
									onChange={(event) =>
										setEmployeeForm({
											...employeeForm,
											chuc_vu: event.target.value,
										})
									}
								/>
							</div>
							<div className="form-group">
								<label>Phòng ban ID</label>
								<input
									value={employeeForm.phong_ban_id}
									onChange={(event) =>
										setEmployeeForm({
											...employeeForm,
											phong_ban_id: event.target.value,
										})
									}
								/>
							</div>
							<div className="form-group">
								<label>Trạng thái</label>
								<select
									value={employeeForm.trang_thai_lam_viec}
									onChange={(event) =>
										setEmployeeForm({
											...employeeForm,
											trang_thai_lam_viec: event.target.value,
										})
									}
								>
									<option value="Dang lam">Đang làm</option>
									<option value="Tam nghi">Tạm nghỉ</option>
									<option value="Nghi viec">Nghỉ việc</option>
								</select>
							</div>
							<div className="form-group">
								<label>Vai trò</label>
								<select
									value={employeeForm.vai_tro}
									onChange={(event) =>
										setEmployeeForm({
											...employeeForm,
											vai_tro: event.target.value,
										})
									}
								>
									<option value="Admin">Admin</option>
									<option value="Quan ly">Quản lý</option>
									<option value="Nhan vien">Nhân viên</option>
								</select>
							</div>
						</div>
						<div className="form-actions">
							<button type="button" onClick={submitEmployeeForm}>
								{employeeEditingId ? "Lưu cập nhật" : "Lưu nhân viên"}
							</button>
							<button
								type="button"
								className="ghost"
								onClick={() => {
									setEmployeeFormOpen(false);
									resetEmployeeForm();
								}}
							>
								Hủy
							</button>
						</div>
					</div>
				</div>
			) : null}
			{employeeStatus.message ? (
				<div className={`alert ${employeeStatus.type}`}>
					{employeeStatus.message}
				</div>
			) : null}
			<div className="admin-table">
				<table>
					<thead>
						<tr>
							<th>ID</th>
							<th>Họ tên</th>
							<th>Email</th>
							<th>Phòng ban</th>
							<th>Chức vụ</th>
							<th>Trạng thái</th>
							<th>Thao tác</th>
						</tr>
					</thead>
					<tbody>
						{employeeLoading ? (
							<tr>
								<td colSpan="6">Đang tải dữ liệu...</td>
							</tr>
						) : (
							employeeRows.map((row) => (
								<tr key={row.id}>
									<td>{row.id}</td>
									<td>{row.ho_ten}</td>
									<td>{row.email}</td>
									<td>{row.phong_ban_id ?? "-"}</td>
									<td>{row.chuc_vu || "-"}</td>
									<td>{row.trang_thai_lam_viec || "-"}</td>
									<td>
										<div className="row-actions">
											<button type="button" onClick={() => openEditEmployee(row)}>
												Sửa
											</button>
											<button
												type="button"
												className="ghost"
												onClick={() => deleteEmployee(row)}
											>
												Xóa
											</button>
										</div>
									</td>
								</tr>
							))
						)}
						{!employeeLoading && employeeRows.length === 0 ? (
							<tr>
								<td colSpan="7">Không có dữ liệu</td>
							</tr>
						) : null}
					</tbody>
				</table>
			</div>
			<div className="pagination">
				<button
					type="button"
					disabled={employeePage <= 1 || employeeLoading}
					onClick={() => fetchEmployees(employeePage - 1)}
				>
					Trang trước
				</button>
				<span>
					Trang {employeePage} / {employeeTotalPages || 1}
				</span>
				<button
					type="button"
					disabled={employeePage >= employeeTotalPages || employeeLoading}
					onClick={() => fetchEmployees(employeePage + 1)}
				>
					Trang sau
				</button>
				<select
					value={employeePageSize}
					onChange={(event) => {
						setEmployeePageSize(Number(event.target.value));
						fetchEmployees(1);
					}}
				>
					<option value={10}>10 / trang</option>
					<option value={20}>20 / trang</option>
					<option value={50}>50 / trang</option>
				</select>
			</div>
			{deleteTarget ? (
				<div className="modal-backdrop">
					<div className="modal confirm">
						<h3>Xác nhận nghỉ việc</h3>
						<p>
							Bạn có chắc muốn chuyển nhân viên {deleteTarget.ho_ten} sang trạng
							thái nghỉ việc?
						</p>
						<div className="form-actions">
							<button type="button" onClick={confirmDeleteEmployee}>
								Xác nhận
							</button>
							<button
								type="button"
								className="ghost"
								onClick={() => setDeleteTarget(null)}
							>
								Hủy
							</button>
						</div>
					</div>
				</div>
			) : null}
		</section>
	);
}

export default EmployeesPage;
