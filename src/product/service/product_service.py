from typing import Union, List

from sqlalchemy.orm import Session

from src.common.exception import FailureType, InternalException
from src.common.logger import Logger
from src.common.parser import parse_korean_initial_sound
from src.product.interface.product_dto import ProductDto
from src.product.interface.product_request import ProductRequest, UpdateProductRequest
from src.product.model import ProductModel
from src.product.repository.product_repository import ProductRepository


class ProductService:
    def __init__(self, session_: Session, logger: Logger = Logger()):
        self.__product_repo = ProductRepository(session_=session_)
        self.__logger = logger

    def create_product(self, user_id: int, dto: ProductRequest) -> ProductDto:
        name_chosung = parse_korean_initial_sound(dto.name)
        product_model = self.__product_repo.create_product(
            user_id=user_id, name_chosung=name_chosung, dto=dto
        )

        return ProductDto(
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
            created_at=product_model.created_at,
            updated_at=product_model.updated_at,
        )

    def get_products(
        self,
        user_id: int,
        name: str = None,
        previous_id: int = None,
        paging_limit: int = 10,
    ) -> List[ProductDto]:
        product_models: [ProductModel] = self.__product_repo.get_products(
            user_id=user_id,
            name=name,
            previous_id=previous_id,
            paging_limit=paging_limit,
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
                created_at=product_model.created_at,
                updated_at=product_model.updated_at,
            )
            for product_model in product_models
        ]

    def get_product(
        self, user_id: int, product_id: int = None
    ) -> Union[ProductDto, None]:
        product_model = self.__product_repo.get_product(
            user_id=user_id, product_id=product_id
        )
        if not product_model:
            return None

        return ProductDto(
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
            created_at=product_model.created_at,
            updated_at=product_model.updated_at,
        )

    def update_product(
        self, user_id: int, product_id: int, dto: UpdateProductRequest
    ) -> None:
        return self.__product_repo.update_product(
            user_id=user_id, product_id=product_id, dto=dto
        )

    def delete_product(self, user_id: int, product_id: int) -> None:
        product = self.__product_repo.get_product(
            user_id=user_id, product_id=product_id
        )
        if not product:
            self.__logger.error(
                f"해당 상품은 존재하지 않음 , user_id: {user_id}, product_id: {product_id}"
            )
            raise InternalException(FailureType.NOT_FOUND_ERROR, "해당 상품은 존재하지 않음")

        return self.__product_repo.delete_product(product.id)
