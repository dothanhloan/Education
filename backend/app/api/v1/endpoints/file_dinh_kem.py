from app.api.v1.endpoints.crud_factory import create_crud_router
from app.models.generated import FileDinhKem

router = create_crud_router(FileDinhKem, prefix='/file_dinh_kem', tags=['file_dinh_kem'])
