from fastapi import APIRouter, Depends, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from sqlalchemy.orm import Session

from app.context import ApplicationContext, get_application_context
from app.db import get_session
from app.db.services.ad_reward_service import AdRewardService

router = APIRouter()

@router.get("/issue")
def request_rewards(
    context: ApplicationContext = Depends(get_application_context(device_info_required=True)),
):
    ad_reward_service = AdRewardService(context.db)
    results = ad_reward_service.generate_rewards_token(context.device_info)
    return JSONResponse(content=jsonable_encoder(results))
