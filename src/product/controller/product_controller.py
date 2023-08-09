from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from src.common.auth import get_current_user_id
from src.common.database import get_db
from src.common.exception import FailureType
from src.common.response import ErrorResponse, BaseResponse
from src.product.interface.product_request import ProductRequest, UpdateProductRequest
from src.product.interface.product_response import (
    GetProductsResponse,
    GetProductResponse,
)
from src.product.service.product_service import ProductService

router = APIRouter()


@router.post(
    path="",
    response_model=BaseResponse,
    responses={
        401: {
            "model": ErrorResponse,
            "description": f"{FailureType.UNAUTHORIZED_TOKEN_ERROR.error_type}",
        },
        400: {
            "model": ErrorResponse,
            "description": f"{FailureType.INPUT_PARAMETER_ERROR.error_type}"
            f"\n\n{FailureType.DATA_PROCESSING_ERROR.error_type}",
        },
    },
    description="상품 등록",
)
def create_product(
    request: ProductRequest,
    session: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    ProductService(session_=session).create_product(
        user_id=current_user_id, dto=request
    )

    return {
        "meta": {"code": 200, "message": "ok"},
        "data": None,
    }


@router.get(
    path="",
    response_model=GetProductsResponse,
    responses={
        401: {
            "model": ErrorResponse,
            "description": f"{FailureType.UNAUTHORIZED_TOKEN_ERROR.error_type}",
        },
        400: {
            "model": ErrorResponse,
            "description": f"{FailureType.GET_DATA_ERROR.error_type}",
        },
    },
    description="상품 목록 조회",
)
def get_products(
    name: str = Query(None),
    previous_id: int = Query(None),
    session: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    products = ProductService(session_=session).get_products(
        user_id=current_user_id, name=name, previous_id=previous_id
    )

    return {
        "meta": {"code": 200, "message": "ok"},
        "data": products,
    }


@router.get(
    path="/{product_id}",
    response_model=GetProductResponse,
    responses={
        401: {
            "model": ErrorResponse,
            "description": f"{FailureType.UNAUTHORIZED_TOKEN_ERROR.error_type}",
        },
        400: {
            "model": ErrorResponse,
            "description": f"{FailureType.GET_DATA_ERROR.error_type}",
        },
    },
    description="상품 상세 조회",
)
def get_product(
    product_id: int,
    session: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    product = ProductService(session_=session).get_product(
        user_id=current_user_id, product_id=product_id
    )

    return {
        "meta": {"code": 200, "message": "ok"},
        "data": product,
    }


@router.patch(
    path="/{product_id}",
    response_model=BaseResponse,
    responses={
        401: {
            "model": ErrorResponse,
            "description": f"{FailureType.UNAUTHORIZED_TOKEN_ERROR.error_type}",
        },
        400: {
            "model": ErrorResponse,
            "description": f"{FailureType.UPDATE_DATA_ERROR.error_type}",
        },
    },
    description="상품 업데이트",
)
def update_product(
    product_id: int,
    request: UpdateProductRequest,
    session: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    ProductService(session_=session).update_product(
        user_id=current_user_id, product_id=product_id, dto=request
    )

    return {
        "meta": {"code": 200, "message": "ok"},
        "data": None,
    }


@router.delete(
    path="/{product_id}",
    response_model=BaseResponse,
    responses={
        401: {
            "model": ErrorResponse,
            "description": f"{FailureType.UNAUTHORIZED_TOKEN_ERROR.error_type}",
        },
        400: {
            "model": ErrorResponse,
            "description": f"{FailureType.DELETE_DATA_ERROR.error_type}"
            f"\n\n{FailureType.NOT_FOUND_ERROR.error_type}",
        },
    },
    description="상품 삭제",
)
def delete_product(
    product_id: int,
    session: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    ProductService(session_=session).delete_product(
        user_id=current_user_id, product_id=product_id
    )

    return {
        "meta": {"code": 200, "message": "ok"},
        "data": None,
    }
