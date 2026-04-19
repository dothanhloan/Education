from app.api.v1.endpoints.crud_factory import create_crud_router
from app.models.generated import Quyen

router = create_crud_router(Quyen, prefix='/quyen', tags=['quyen'])
