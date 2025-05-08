from pydantic import BaseModel
from typing import Optional

class AdRewardPayloadModel(BaseModel):
    user_id: Optional[str]
    custom_data: Optional[str]
    reward_type: Optional[str]
    reward_amount: Optional[int]
    trans_id: Optional[str]
    signature: Optional[str]
