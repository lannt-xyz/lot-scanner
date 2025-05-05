from datetime import date
from typing import Optional

from fastapi_camelcase import CamelModel

class TicketModel(CamelModel):
  channel: str
  prize_date: date
  prize: str

class TicketResponseModel(CamelModel):
  id: int
  channel: str
  prize_date: date
  prize_number: str
  prize_amount: Optional[int]
  result: Optional[str]
