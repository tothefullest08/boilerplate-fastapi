from typing import List, Union

from src.common.response import BaseResponse
from src.product.interface.product_dto import ProductDto


class GetProductsResponse(BaseResponse):
    data: List[ProductDto]


class GetProductResponse(BaseResponse):
    data: Union[ProductDto, None]
