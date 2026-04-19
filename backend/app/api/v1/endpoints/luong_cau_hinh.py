from app.api.v1.endpoints.crud_factory import create_crud_router
from app.models.generated import LuongCauHinh

router = create_crud_router(LuongCauHinh, prefix='/luong_cau_hinh', tags=['luong_cau_hinh'])
