from app.api.v1.endpoints.crud_factory import create_crud_router
from app.models.generated import CongViecNguoiNhan

router = create_crud_router(CongViecNguoiNhan, prefix='/cong_viec_nguoi_nhan', tags=['cong_viec_nguoi_nhan'])
