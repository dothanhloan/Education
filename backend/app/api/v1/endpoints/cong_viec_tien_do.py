from app.api.v1.endpoints.crud_factory import create_crud_router
from app.models.generated import CongViecTienDo

router = create_crud_router(CongViecTienDo, prefix='/cong_viec_tien_do', tags=['cong_viec_tien_do'])
