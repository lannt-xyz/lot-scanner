
from fastapi_camelcase import CamelModel


class AdRewardResponse(CamelModel):
  guest_id: str
  timestamp: int
  token: str
  ad_network: str
