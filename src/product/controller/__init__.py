from fastapi import APIRouter

from src.product.controller import product_controller

product_v1_router = APIRouter()

product_v1_router.include_router(
    product_controller.router, prefix="/products", tags=["product"]
)
