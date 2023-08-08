import re
from typing import Union, List

from sqlalchemy.orm import Session
from src.common.exception import FailureType, InternalException
from src.common.logger import Logger
from src.common.parser import parse_korean_initial_sound
from src.product.interface.product_dto import ProductDto
from src.product.interface.product_request import ProductRequest, UpdateProductRequest
from src.product.model import ProductModel
from src.product.repository.product_repository import ProductRepository
from src.user.model.user_model import UserModel


class ProductService:
    def __init__(self, session_: Session, logger: Logger = Logger()):
        self.__product_repo = ProductRepository(session_=session_)
        self.__logger = logger

    def create_product(self, user_id: int, dto: ProductRequest):
        name_chosung = parse_korean_initial_sound(dto.name)
        self.__product_repo.create_product(
            user_id=user_id, name_chosung=name_chosung, dto=dto
        )

    def get_products(
        self, user_id: int, previous_id: int = None, paging_limit: int = 10
    ) -> List[ProductDto]:
        product_models: [ProductModel] = self.__product_repo.get_products(
            user_id=user_id, previous_id=previous_id, paging_limit=paging_limit
        )
        return [
            ProductDto(
                id=product_model.id,
                user_id=product_model.user_id,
                category=product_model.category,
                price=product_model.price,
                raw_price=product_model.raw_price,
                name=product_model.name,
                description=product_model.description,
                barcode=product_model.barcode,
                size=product_model.size,
                expiration_date=product_model.expiration_date,
            )
            for product_model in product_models
        ]

    def get_product(self, user_id: int, name: str = None) -> Union[UserModel, None]:
        return self.__product_repo.get_product(user_id=user_id, name=name)

    def update_product(self, user_id: int, dto: UpdateProductRequest):
        return self.__product_repo.update_product(user_id=user_id, dto=dto)

    def delete_product(self, user_id: int, product_id: int) -> None:
        product = self.__product_repo.get_product(
            user_id=user_id, product_id=product_id
        )
        if not product:
            raise InternalException(FailureType.INVALID_REQUEST_ERROR)

        return self.__product_repo.delete_product(product_id)
