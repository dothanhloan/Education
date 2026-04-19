from typing import Any

import sqlalchemy as sa
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db


def _to_dict(obj: Any) -> dict:
    mapper = sa.inspect(obj).mapper
    return {attr.key: getattr(obj, attr.key) for attr in mapper.column_attrs}


def create_crud_router(model: Any, prefix: str, tags: list[str]) -> APIRouter:
    router = APIRouter(prefix=prefix, tags=tags)
    mapper = sa.inspect(model).mapper
    columns = {attr.key for attr in mapper.column_attrs}
    pk_cols = [col.key for col in mapper.primary_key]

    has_single_pk = len(pk_cols) == 1
    pk_col = pk_cols[0] if has_single_pk else None

    @router.get("/")
    def list_items(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
    ) -> list[dict]:
        items = db.query(model).offset(skip).limit(limit).all()
        return [_to_dict(item) for item in items]

    if has_single_pk:
        @router.get("/{item_id}")
        def get_item(item_id: int, db: Session = Depends(get_db)) -> dict:
            item = db.get(model, item_id)
            if not item:
                raise HTTPException(status_code=404, detail="Not found")
            return _to_dict(item)
    else:
        @router.post("/by-pk")
        def get_item_by_pk(payload: dict, db: Session = Depends(get_db)) -> dict:
            missing = [col for col in pk_cols if col not in payload]
            if missing:
                raise HTTPException(status_code=400, detail=f"Missing PK fields: {', '.join(missing)}")
            pk = tuple(payload[col] for col in pk_cols)
            item = db.get(model, pk)
            if not item:
                raise HTTPException(status_code=404, detail="Not found")
            return _to_dict(item)

    @router.post("/", status_code=201)
    def create_item(payload: dict, db: Session = Depends(get_db)) -> dict:
        data = {key: value for key, value in payload.items() if key in columns}
        item = model(**data)
        db.add(item)
        db.commit()
        db.refresh(item)
        return _to_dict(item)

    if has_single_pk:
        @router.put("/{item_id}")
        def update_item(item_id: int, payload: dict, db: Session = Depends(get_db)) -> dict:
            item = db.get(model, item_id)
            if not item:
                raise HTTPException(status_code=404, detail="Not found")
            for key, value in payload.items():
                if key in columns and key != pk_col:
                    setattr(item, key, value)
            db.commit()
            db.refresh(item)
            return _to_dict(item)
    else:
        @router.put("/by-pk")
        def update_item_by_pk(payload: dict, db: Session = Depends(get_db)) -> dict:
            missing = [col for col in pk_cols if col not in payload]
            if missing:
                raise HTTPException(status_code=400, detail=f"Missing PK fields: {', '.join(missing)}")
            pk = tuple(payload[col] for col in pk_cols)
            item = db.get(model, pk)
            if not item:
                raise HTTPException(status_code=404, detail="Not found")
            for key, value in payload.items():
                if key in columns and key not in pk_cols:
                    setattr(item, key, value)
            db.commit()
            db.refresh(item)
            return _to_dict(item)

    if has_single_pk:
        @router.delete("/{item_id}", status_code=204)
        def delete_item(item_id: int, db: Session = Depends(get_db)) -> None:
            item = db.get(model, item_id)
            if not item:
                raise HTTPException(status_code=404, detail="Not found")
            db.delete(item)
            db.commit()
            return None
    else:
        @router.post("/by-pk/delete", status_code=204)
        def delete_item_by_pk(payload: dict, db: Session = Depends(get_db)) -> None:
            missing = [col for col in pk_cols if col not in payload]
            if missing:
                raise HTTPException(status_code=400, detail=f"Missing PK fields: {', '.join(missing)}")
            pk = tuple(payload[col] for col in pk_cols)
            item = db.get(model, pk)
            if not item:
                raise HTTPException(status_code=404, detail="Not found")
            db.delete(item)
            db.commit()
            return None

    return router
