from datetime import datetime, timedelta

from src.product.interface.product_enum import ProductSizeEnum
from src.product.interface.product_request import ProductRequest, UpdateProductRequest
from src.product.repository.product_repository import ProductRepository
from src.product.service.product_service import ProductService


def test_create_product_should_create_product(test_session):
    # Given
    user_id = 1
    dto = ProductRequest(
        category="category",
        price=1,
        raw_price=2,
        name="name",
        description="description",
        barcode="barcode",
        size=ProductSizeEnum.SMALL,
        expiration_date=datetime.now(),
    )

    # When
    product_dto = ProductService(session_=test_session).create_product(
        user_id=user_id, dto=dto
    )

    # Then
    product = ProductRepository(session_=test_session).get_product(
        user_id=user_id, product_id=product_dto.id
    )
    assert product is not None


def test_get_products_should_return_product_dto_list(test_session):
    # Given
    user_id = 1
    dto = ProductRequest(
        category="category",
        price=1,
        raw_price=2,
        name="name",
        description="description",
        barcode="barcode",
        size=ProductSizeEnum.SMALL,
        expiration_date=datetime.now(),
    )
    product_ids = []
    for _ in range(10):
        product = ProductService(session_=test_session).create_product(
            user_id=user_id, dto=dto
        )
        product_ids.append(product.id)

    product_ids.sort(reverse=True)

    # When
    products = ProductService(session_=test_session).get_products(user_id=user_id)

    # Then
    assert len(products) == 10

    # When - previous_id & limit
    products = ProductService(session_=test_session).get_products(
        user_id=user_id, previous_id=product_ids[2], paging_limit=3
    )

    # Then - previous_id & limit
    assert len(products) == 3
    assert products[0].id == product_ids[3]


def test_get_products_should_return_product_dto_when_search_by_names(test_session):
    # Given
    for _ in range(3):
        product = ProductService(session_=test_session).create_product(
            user_id=1,
            dto=ProductRequest(
                category="category",
                price=1,
                raw_price=2,
                name=f"가나다abc하이{_}",
                description="description",
                barcode="barcode",
                size=ProductSizeEnum.SMALL,
                expiration_date=datetime.now(),
            ),
        )

    # When
    products = ProductService(session_=test_session).get_products(user_id=1, name="ㄴㄷ")

    # Then
    assert len(products) == 3

    # When
    products = ProductService(session_=test_session).get_products(user_id=1, name="ㅎㅇ")

    # Then
    assert len(products) == 3

    # When
    products = ProductService(session_=test_session).get_products(user_id=1, name="나")

    # Then
    assert len(products) == 3

    # When
    products = ProductService(session_=test_session).get_products(user_id=1, name="없음")

    # Then
    assert len(products) == 0


def test_update_product_should_update_product_accordingly(test_session):
    # Given
    product = ProductService(session_=test_session).create_product(
        user_id=1,
        dto=ProductRequest(
            category="category",
            price=1,
            raw_price=2,
            name="가나다abc하이",
            description="description",
            barcode="barcode",
            size=ProductSizeEnum.SMALL,
            expiration_date=datetime.now(),
        ),
    )

    # When
    dto = UpdateProductRequest(
        category="category2",
        price=10,
        raw_price=20,
        name="가나다abc하이2",
        description="description2",
        barcode="barcode2",
        size=ProductSizeEnum.LARGE,
        expiration_date=datetime.now() - timedelta(days=1),
    )
    ProductService(session_=test_session).update_product(
        user_id=1,
        product_id=product.id,
        dto=dto,
    )

    # Then
    product = ProductService(session_=test_session).get_product(
        user_id=1, product_id=product.id
    )
    assert product.category == dto.category
    assert product.price == dto.price
    assert product.raw_price == dto.raw_price
    assert product.name == dto.name
    assert product.description == dto.description
    assert product.barcode == dto.barcode
    assert product.size == dto.size
    assert product.expiration_date == dto.expiration_date


def test_delete_product_should_delete_product_accordingly(test_session):
    # Given
    product = ProductService(session_=test_session).create_product(
        user_id=1,
        dto=ProductRequest(
            category="category",
            price=1,
            raw_price=2,
            name="가나다abc하이",
            description="description",
            barcode="barcode",
            size=ProductSizeEnum.SMALL,
            expiration_date=datetime.now(),
        ),
    )

    # When
    ProductService(session_=test_session).delete_product(
        user_id=1,
        product_id=product.id,
    )

    # Then
    product = ProductRepository(session_=test_session).get_product(
        user_id=1, product_id=product.id
    )
    assert product is None
