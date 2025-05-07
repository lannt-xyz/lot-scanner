from typing import Optional
from pydantic import BaseModel, ConfigDict

class TicketModel(BaseModel):
  kenh_xo_so: Optional[str]
  ngay_mo_thuong: Optional[str]
  so_du_thuong: Optional[str]

  model_config = ConfigDict(from_attributes=True)

class OcrResultModel(BaseModel):
  result: Optional[TicketModel]
  
  model_config = ConfigDict(from_attributes=True)
