from datetime import date

from fastapi_camelcase import CamelModel

class TicketModel(CamelModel):
  channel: str
  prize_date: date
  prize: str
