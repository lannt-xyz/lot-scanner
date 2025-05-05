from typing import Any
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

class BaseResponseModel(BaseModel):
    detail: Any = "Success"

    @staticmethod
    def ok() -> Any:
        return jsonable_encoder(BaseResponseModel())
