from app.api.v1.endpoints.crud_factory import create_crud_router
from app.models.generated import NhanSuLichSu

router = create_crud_router(NhanSuLichSu, prefix='/nhan_su_lich_su', tags=['nhan_su_lich_su'])
