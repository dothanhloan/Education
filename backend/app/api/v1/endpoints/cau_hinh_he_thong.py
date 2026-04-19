from app.api.v1.endpoints.crud_factory import create_crud_router
from app.models.generated import CauHinhHeThong

router = create_crud_router(CauHinhHeThong, prefix='/cau_hinh_he_thong', tags=['cau_hinh_he_thong'])
