from app.api.v1.endpoints.crud_factory import create_crud_router
from app.models.generated import NgayPhepNam

router = create_crud_router(NgayPhepNam, prefix='/ngay_phep_nam', tags=['ngay_phep_nam'])
