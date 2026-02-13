from fastapi import APIRouter

from app.api.v1 import employees, attendance, dashboard

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(employees.router, prefix="/employees", tags=["employees"])
api_router.include_router(attendance.router, prefix="/attendance", tags=["attendance"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
