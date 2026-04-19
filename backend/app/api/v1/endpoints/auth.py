from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.api.deps import get_db

router = APIRouter(prefix="/auth", tags=["auth"])


class LoginPayload(BaseModel):
    identifier: str
    password: str


@router.post("/login")
def login(payload: LoginPayload, db: Session = Depends(get_db)) -> dict:
    identifier = payload.identifier.strip()
    password = payload.password.strip()

    if not identifier or not password:
        raise HTTPException(status_code=400, detail="Missing credentials")

    query = text(
        """
        SELECT id, ho_ten, email, so_dien_thoai, vai_tro, chuc_vu, phong_ban_id
        FROM nhanvien
        WHERE (email = :identifier OR so_dien_thoai = :identifier)
          AND mat_khau = :password
        LIMIT 1
        """
    )

    result = db.execute(query, {"identifier": identifier, "password": password}).mappings().first()
    if not result:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    role = (result.get("vai_tro") or "").lower()
    home_route = "/admin" if "admin" in role else "/home"

    return {
        "user": dict(result),
        "home_route": home_route,
    }
