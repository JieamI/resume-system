from fastapi import APIRouter

from .endpoints import login, cv, dept, authority

api_router = APIRouter()
api_router.include_router(login.router, prefix = "/login", tags=["login"])
api_router.include_router(cv.router, prefix = "/cv", tags=["cv"])
api_router.include_router(dept.router, prefix = "/dept", tags=["dept"])
api_router.include_router(authority.router, prefix = "/authority", tags=["authority"])
