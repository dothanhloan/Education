from app.api.v1.endpoints.crud_factory import create_crud_router
from app.models.generated import LichTrinh

router = create_crud_router(LichTrinh, prefix='/lich_trinh', tags=['lich_trinh'])
