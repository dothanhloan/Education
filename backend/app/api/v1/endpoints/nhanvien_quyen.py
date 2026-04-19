from app.api.v1.endpoints.crud_factory import create_crud_router
from app.models.generated import NhanvienQuyen

router = create_crud_router(NhanvienQuyen, prefix='/nhanvien_quyen', tags=['nhanvien_quyen'])
