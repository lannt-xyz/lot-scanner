from datetime import datetime
import hashlib
import hmac
from time import time
from typing import List
from sqlmodel import and_, select

from app.db.entities.ad_reward import AdReward
from app.models.ad_reward_response_model import AdRewardResponse
from app.utils.enums import AdRewardEnum
from config import settings
from app.db import SessionDep
from app.db.entities.code_master import CodeMaster

from app.models.select_option import SelectOption

class AdRewardService:
    def __init__(self, db: SessionDep):
        self.db = db
        pass

    def _generate_token(self, guest_id, timestamp):
        msg = f"{guest_id}:{timestamp}"
        return hmac.new(settings.ad_reward_token_secret.encode(), msg.encode(), hashlib.sha256).hexdigest()
    
    def generate_rewards_token(self, device_info) -> AdRewardResponse:
        guest_id = device_info.id
        # Get the current timestamp
        timestamp = int(time())
        token = self._generate_token(guest_id, timestamp)

        # Convert timestamp to datetime
        expired_at = datetime.fromtimestamp(timestamp + settings.ad_reward_expiration_time)

        ad_reward = AdReward(
            guest_id=guest_id,
            reward_token=token,
            ad_network=settings.ad_network,
            status=AdRewardEnum.issued.dbvalue,
            expired_at=expired_at,
        )
        self.db.add(ad_reward)
        self.db.commit()

        return AdRewardResponse(
            guest_id=guest_id,
            timestamp=timestamp,
            token=token,
            ad_network=settings.ad_network
        )
