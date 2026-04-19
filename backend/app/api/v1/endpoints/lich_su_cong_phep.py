from app.api.v1.endpoints.crud_factory import create_crud_router
from app.models.generated import LichSuCongPhep

router = create_crud_router(LichSuCongPhep, prefix='/lich_su_cong_phep', tags=['lich_su_cong_phep'])
