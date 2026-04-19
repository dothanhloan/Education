from app.api.v1.endpoints.crud_factory import create_crud_router
from app.models.generated import CongViecDanhGia

router = create_crud_router(CongViecDanhGia, prefix='/cong_viec_danh_gia', tags=['cong_viec_danh_gia'])
