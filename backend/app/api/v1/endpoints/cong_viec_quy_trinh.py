from app.api.v1.endpoints.crud_factory import create_crud_router
from app.models.generated import CongViecQuyTrinh

router = create_crud_router(CongViecQuyTrinh, prefix='/cong_viec_quy_trinh', tags=['cong_viec_quy_trinh'])
