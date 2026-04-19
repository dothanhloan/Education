from app.api.v1.endpoints.crud_factory import create_crud_router
from app.models.generated import LuuKpi

router = create_crud_router(LuuKpi, prefix='/luu_kpi', tags=['luu_kpi'])
