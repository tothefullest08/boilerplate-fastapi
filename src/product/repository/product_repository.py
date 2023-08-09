from typing import List, Union

from sqlalchemy import or_
from sqlalchemy.orm import Session

from src.common.exception import InternalException, FailureType
from src.common.logger import Logger
from src.common.parser import parse_korean_initial_sound
from src.product.interface.product_request import ProductRequest, UpdateProductRequest
from src.product.model import ProductModel
from src.user.model.user_model import UserModel


class ProductRepository:
    def __init__(self, session_: Session, logger: Logger = Logger()):
        self.__session = session_
        self.__logger = logger

    def create_product(
        self, user_id: int, name_chosung: str, dto: ProductRequest
    ) -> ProductModel:
        try:
            product: ProductModel = ProductModel(
                user_id=user_id,
                category=dto.category,
                price=dto.price,
                raw_price=dto.raw_price,
                name=dto.name,
                name_chosung=name_chosung,
                description=dto.description,
                barcode=dto.barcode,
                size=dto.size,
                expiration_date=dto.expiration_date,
            )
            self.__session.add(product)
            self.__session.commit()

            return product

        except Exception as e:
            self.__session.rollback()
            self.__session.flush()

            self.__logger.error(f" 상품 생성 실패. dto: {dto}, e: {e}")
            raise InternalException(FailureType.CREATE_DATA_ERROR, "상품 생성 실패")

    def get_products(
        self,
        user_id: int,
        name: str = None,
        previous_id: int = None,
        paging_limit: int = 10,
    ) -> List[ProductModel]:
        try:
            filter_ = []
            if user_id:
                filter_.append(ProductModel.user_id == user_id)
            if name:
                chosung = parse_korean_initial_sound(name)
                filter_.append(
                    or_(
                        ProductModel.name.like(f"%{name}%"),
                        ProductModel.name_chosung.like(f"%{chosung}%"),
                    )
                )
            if previous_id:
                filter_.append(ProductModel.id < previous_id)

            return (
                self.__session.query(ProductModel)
                .filter(*filter_)
                .order_by(ProductModel.id.desc())
                .limit(paging_limit)
                .all()
            )
        except Exception as e:
            self.__logger.error(f"상품 목록 조회 실패, user_id: {user_id}, e: {e}")
            raise InternalException(FailureType.GET_DATA_ERROR, "상품 목록 조회 실패")

    def get_product(self, user_id: int, product_id: int) -> Union[UserModel, None]:
        try:
            return (
                self.__session.query(ProductModel)
                .filter(ProductModel.user_id == user_id, ProductModel.id == product_id)
                .first()
            )
        except Exception as e:
            self.__logger.error(
                f"상품 조회 실패, user_id: {user_id}, product_id: {product_id}, e: {e}"
            )
            raise InternalException(FailureType.GET_DATA_ERROR, "상품 조회 실패")

    def update_product(
        self, user_id: int, product_id: int, dto: UpdateProductRequest
    ) -> ProductModel:
        try:
            product: ProductModel = (
                self.__session.query(ProductModel)
                .filter(ProductModel.user_id == user_id, ProductModel.id == product_id)
                .first()
            )

            if dto.category:
                product.category = dto.category
            if dto.price:
                product.price = dto.price
            if dto.raw_price:
                product.raw_price = dto.raw_price
            if dto.name:
                product.name = dto.name
            if dto.description:
                product.description = dto.description
            if dto.barcode:
                product.barcode = dto.barcode
            if dto.size:
                product.size = dto.size
            if dto.expiration_date:
                product.expiration_date = dto.expiration_date

            self.__session.add(product)
            self.__session.commit()

            return product
        except Exception as e:
            self.__session.rollback()
            self.__session.flush()

            self.__logger.error(f" 상품 업데이트 실패. user_id: {user_id}, dto: {dto} e: {e}")
            raise InternalException(FailureType.UPDATE_DATA_ERROR, "상품 업데이트 실패")

    def delete_product(self, product_id: int) -> None:
        try:
            removed_count = (
                self.__session.query(ProductModel)
                .filter(ProductModel.id == product_id)
                .delete(synchronize_session="fetch")
            )
            if not removed_count:
                self.__session.flush()
                return 0

            self.__session.commit()

            return removed_count

        except Exception as e:
            self.__session.rollback()
            self.__session.flush()
            self.__logger.error(f" 상품 삭제 실패. user_id: {product_id}, e: {e}")
            raise InternalException(FailureType.DELETE_DATA_ERROR, "상품 삭제 실패")
