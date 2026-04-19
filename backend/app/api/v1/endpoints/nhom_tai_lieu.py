from app.api.v1.endpoints.crud_factory import create_crud_router
from app.models.generated import NhomTaiLieu

router = create_crud_router(NhomTaiLieu, prefix='/nhom_tai_lieu', tags=['nhom_tai_lieu'])
