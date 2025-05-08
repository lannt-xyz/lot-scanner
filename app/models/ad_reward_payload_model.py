from pydantic import BaseModel
from typing import Optional

class AdRewardPayloadModel(BaseModel):
    ad_network: Optional[str] = None
    ad_unit: Optional[str] = None
    custom_data: Optional[str] = None
    reward_amount: Optional[int] = None
    reward_item: Optional[str] = None
    timestamp: Optional[int] = None
    transaction_id: Optional[str] = None
    user_id: Optional[str] = None
    signature: Optional[str] = None
    key_id: Optional[int] = None
