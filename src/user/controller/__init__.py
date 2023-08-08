from fastapi import APIRouter

from src.user.controller import user_controller

user_v1_router = APIRouter()

user_v1_router.include_router(user_controller.router, prefix="/users", tags=["user"])
