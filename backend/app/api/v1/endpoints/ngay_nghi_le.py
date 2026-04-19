from app.api.v1.endpoints.crud_factory import create_crud_router
from app.models.generated import NgayNghiLe

router = create_crud_router(NgayNghiLe, prefix='/ngay_nghi_le', tags=['ngay_nghi_le'])
