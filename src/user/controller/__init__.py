from fastapi import APIRouter

from src.user.controller import user_controller

user_router = APIRouter()

user_router.include_router(user_controller.router, prefix="", tags=["user"])
