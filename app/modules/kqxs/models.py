from pydantic import BaseModel


class PrizeStructure(BaseModel):
  name: str
  amount: int
  length: int
