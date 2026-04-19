import React, { useEffect } from "react";

function DepartmentsPage({
	departmentRows,
	departmentTotal,
	departmentQuery,
	departmentStatus,
	departmentLoading,
	departmentPage,
	departmentPageSize,
	departmentTotalPages,
	setDepartmentQuery,
	setDepartmentPageSize,
	fetchDepartments,
}) {
	useEffect(() => {
		fetchDepartments(1);
	}, []);

	return (
		<section className="admin-section">
			<div className="admin-section-header">
				<div>
					<h2>Danh sách phòng ban</h2>
					<p>Tổng số: {departmentTotal} phòng ban</p>
				</div>
				<div className="admin-actions">
					<input
						type="search"
						placeholder="Tìm theo tên phòng ban hoặc trưởng phòng"
						value={departmentQuery}
						onChange={(event) => setDepartmentQuery(event.target.value)}
					/>
					<button type="button" onClick={() => fetchDepartments(1)}>
						Tìm kiếm
					</button>
				</div>
			</div>
			{departmentStatus.message ? (
				<div className={`alert ${departmentStatus.type}`}>
					{departmentStatus.message}
				</div>
			) : null}
			<div className="admin-table">
				<table>
					<thead>
						<tr>
							<th>Mã</th>
							<th>Tên phòng ban</th>
							<th>Mô tả</th>
							<th>Trưởng bộ phận</th>
							<th>Trạng thái</th>
						</tr>
					</thead>
					<tbody>
						{departmentLoading ? (
							<tr>
								<td colSpan="5">Đang tải dữ liệu...</td>
							</tr>
						) : (
							departmentRows.map((row) => (
								<tr key={row.id}>
									<td>{row.id}</td>
									<td>{row.ten_phong}</td>
									<td>-</td>
									<td>{row.truong_phong || "-"}</td>
									<td>Hoạt động</td>
								</tr>
							))
						)}
						{!departmentLoading && departmentRows.length === 0 ? (
							<tr>
								<td colSpan="5">Không có dữ liệu</td>
							</tr>
						) : null}
					</tbody>
				</table>
			</div>
			<div className="pagination">
				<button
					type="button"
					disabled={departmentPage <= 1 || departmentLoading}
					onClick={() => fetchDepartments(departmentPage - 1)}
				>
					Trang trước
				</button>
				<span>
					Trang {departmentPage} / {departmentTotalPages || 1}
				</span>
				<button
					type="button"
					disabled={departmentPage >= departmentTotalPages || departmentLoading}
					onClick={() => fetchDepartments(departmentPage + 1)}
				>
					Trang sau
				</button>
				<select
					value={departmentPageSize}
					onChange={(event) => {
						setDepartmentPageSize(Number(event.target.value));
						fetchDepartments(1);
					}}
				>
					<option value={10}>10 / trang</option>
					<option value={20}>20 / trang</option>
					<option value={50}>50 / trang</option>
				</select>
			</div>
		</section>
	);
}

export default DepartmentsPage;
