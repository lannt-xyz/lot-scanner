from typing import Any
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel

class BaseResponseModel(BaseModel):
    detail: Any = "Success"

    @staticmethod
    def ok() -> JSONResponse:
        return JSONResponse(content=jsonable_encoder(BaseResponseModel()))

    @staticmethod
    def ok(data: BaseModel) -> JSONResponse:
        return JSONResponse(content=jsonable_encoder(data.model_dump()))

