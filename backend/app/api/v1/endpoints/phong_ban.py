from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.api.v1.endpoints.crud_factory import create_crud_router
from app.models.generated import PhongBan

router = APIRouter(prefix="/phong_ban", tags=["phong_ban"])


@router.get("/danh_sach")
def list_phong_ban(
	q: Optional[str] = None,
	page: int = 1,
	page_size: int = 20,
	db: Session = Depends(get_db),
) -> dict:
	conditions = []
	params: dict = {}
	resolved_limit = max(page_size, 1)
	resolved_skip = max(page - 1, 0) * resolved_limit

	if q:
		conditions.append("(pb.ten_phong LIKE :q OR nv.ho_ten LIKE :q)")
		params["q"] = f"%{q}%"

	where_sql = f"WHERE {' AND '.join(conditions)}" if conditions else ""

	query = text(
		f"""
		SELECT
			pb.id,
			pb.ten_phong,
			pb.truong_phong_id,
			nv.ho_ten AS truong_phong
		FROM phong_ban pb
		LEFT JOIN nhanvien nv ON nv.id = pb.truong_phong_id
		{where_sql}
		ORDER BY pb.id DESC
		LIMIT :limit OFFSET :skip
		"""
	)

	total_query = text(
		f"""
		SELECT COUNT(*)
		FROM phong_ban pb
		LEFT JOIN nhanvien nv ON nv.id = pb.truong_phong_id
		{where_sql}
		"""
	)

	params_with_paging = {**params, "limit": resolved_limit, "skip": resolved_skip}
	rows = db.execute(query, params_with_paging).mappings().all()
	total = db.execute(total_query, params).scalar() or 0
	total_pages = (total + resolved_limit - 1) // resolved_limit if resolved_limit else 0

	return {
		"data": [dict(row) for row in rows],
		"total": total,
		"page": page,
		"page_size": resolved_limit,
		"total_pages": total_pages,
	}


crud_router = create_crud_router(PhongBan, prefix="", tags=["phong_ban"])
router.include_router(crud_router)
