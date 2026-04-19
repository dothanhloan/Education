from app.api.v1.endpoints.crud_factory import create_crud_router
from app.models.generated import QuyTrinhNguoiNhan

router = create_crud_router(QuyTrinhNguoiNhan, prefix='/quy_trinh_nguoi_nhan', tags=['quy_trinh_nguoi_nhan'])
