from typing import Any
from pydantic import BaseModel

class BaseResponseModel(BaseModel):
    detail: Any = "Success"
