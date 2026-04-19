from app.api.v1.endpoints.crud_factory import create_crud_router
from app.models.generated import ChamCong

router = create_crud_router(ChamCong, prefix='/cham_cong', tags=['cham_cong'])
