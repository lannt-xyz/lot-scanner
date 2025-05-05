from typing import Any
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

class BaseResponseModel(BaseModel):
    detail: Any = "Success"

    @staticmethod
    def ok() -> Any:
        return jsonable_encoder(BaseResponseModel())

    @staticmethod
    def of(data: Any) -> Any:
        return jsonable_encoder(BaseResponseModel(detail=data))
