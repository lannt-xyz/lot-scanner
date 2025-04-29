
from fastapi_camelcase import CamelModel


class SelectOption(CamelModel):
  key: str
  value: str
  display_order: int = 0
