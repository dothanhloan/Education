from app.api.v1.endpoints.crud_factory import create_crud_router
from app.models.generated import CongViecLichSu

router = create_crud_router(CongViecLichSu, prefix='/cong_viec_lich_su', tags=['cong_viec_lich_su'])
