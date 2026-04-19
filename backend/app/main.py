import logging

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.api.v1.router import api_router
from app.db.session import engine

app = FastAPI(title="ICS HRMS")
logger = logging.getLogger("uvicorn.error")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")


@app.get("/")
def health_check():
    return {"status": "ok"}


@app.get("/health/db")
def db_health_check():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
    return {"status": "ok"}


@app.get("/api/nhanvien")
def list_nhanvien():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT * FROM nhanvien"))
            rows = [dict(row) for row in result.mappings().all()]
        return {"data": rows}
    except Exception as exc:
        logger.exception("Failed to fetch nhanvien")
        raise HTTPException(status_code=500, detail=str(exc))
