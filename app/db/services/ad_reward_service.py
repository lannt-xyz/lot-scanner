from datetime import datetime
import hashlib
import hmac
from time import time
from typing import List
from sqlmodel import and_, select

from app.db.entities.ad_reward import AdReward
from app.error.bad_request_exception import BadRequestException
from app.models.ad_reward_payload_model import AdRewardPayloadModel
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

    def _verify_signature(payload: AdRewardPayloadModel):
        params = payload.model_dump()
        # exclude the signature from the params
        params.pop("signature", None)

        message = '&'.join(f"{k}={params[k]}" for k in sorted(params))
        signature = hmac.new(
            settings.ad_reward_token_secret.encode(), message.encode(), hashlib.sha256
        ).hexdigest()
        return hmac.compare_digest(signature, payload.signature)

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

    def verify_admod_reward(self, ad_network: str, payload: AdRewardPayloadModel):
        if ad_network != settings.ad_network:
            raise BadRequestException('Invalid ad network')

        is_valid = self._verify_signature(payload, payload.signature)
        if not is_valid:
            raise BadRequestException('Invalid signature')
        
        # Check if the reward is already issued
        statement = select(
                AdReward
            ).where(and_(
                AdReward.guest_id == payload.user_id,
                AdReward.status == AdRewardEnum.issued.dbvalue,
                AdReward.ad_network == settings.ad_network,
                AdReward.reward_token == payload.custom_data,
            ))
        ad_reward = self.db.exec(statement).first()
        if not ad_reward:
            raise BadRequestException('Invalid reward token')

        # Check if the reward is expired, if so, update the status to expired
        if ad_reward.expired_at < datetime.now():
            ad_reward.status = AdRewardEnum.expired.dbvalue
            self.db.add(ad_reward)
            self.db.commit()
            raise BadRequestException('Reward token expired')

        # Update the reward status to claimed
        ad_reward.status = AdRewardEnum.claimed.dbvalue
        ad_reward.claimed_at = datetime.now()
        self.db.add(ad_reward)
        self.db.commit()
