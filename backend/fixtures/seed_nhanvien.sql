USE hrm_ics;

INSERT INTO nhanvien (
  ho_ten,
  email,
  mat_khau,
  so_dien_thoai,
  gioi_tinh,
  ngay_sinh,
  phong_ban_id,
  chuc_vu,
  luong_co_ban,
  trang_thai_lam_viec,
  vai_tro,
  ngay_vao_lam,
  avatar_url
) VALUES
(
  'Admin ICS',
  'admin@ics.local',
  'admin123',
  '0900000000',
  'Nam',
  '1990-01-01',
  NULL,
  'Admin',
  0.00,
  'Đang làm',
  'Admin',
  '2025-01-01',
  NULL
),
(
  'Nhan Vien Demo',
  'nhanvien@ics.local',
  '12345678',
  '0911111111',
  'Nữ',
  '1996-06-15',
  NULL,
  'Nhân viên',
  0.00,
  'Đang làm',
  'Nhân viên',
  '2025-01-01',
  NULL
);
