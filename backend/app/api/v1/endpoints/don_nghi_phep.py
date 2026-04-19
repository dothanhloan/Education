from app.api.v1.endpoints.crud_factory import create_crud_router
from app.models.generated import DonNghiPhep

router = create_crud_router(DonNghiPhep, prefix='/don_nghi_phep', tags=['don_nghi_phep'])
