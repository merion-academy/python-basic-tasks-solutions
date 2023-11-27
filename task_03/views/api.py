from fastapi import APIRouter

from .employees.api import router as employees_router

api_router = APIRouter(prefix="/api")
api_router.include_router(employees_router)
