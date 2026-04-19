from app.api.v1.endpoints.crud_factory import create_crud_router
from app.models.generated import ThongBao

router = create_crud_router(ThongBao, prefix='/thong_bao', tags=['thong_bao'])
