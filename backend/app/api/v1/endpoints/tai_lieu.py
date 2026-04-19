from app.api.v1.endpoints.crud_factory import create_crud_router
from app.models.generated import TaiLieu

router = create_crud_router(TaiLieu, prefix='/tai_lieu', tags=['tai_lieu'])
