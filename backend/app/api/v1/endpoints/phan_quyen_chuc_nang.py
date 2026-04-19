from app.api.v1.endpoints.crud_factory import create_crud_router
from app.models.generated import PhanQuyenChucNang

router = create_crud_router(PhanQuyenChucNang, prefix='/phan_quyen_chuc_nang', tags=['phan_quyen_chuc_nang'])
