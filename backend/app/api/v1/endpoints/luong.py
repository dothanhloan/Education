from app.api.v1.endpoints.crud_factory import create_crud_router
from app.models.generated import Luong

router = create_crud_router(Luong, prefix='/luong', tags=['luong'])
