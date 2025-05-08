from fastapi import APIRouter, Depends, Path
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


from app.context import ApplicationContext, get_application_context
from app.db.services.ad_reward_service import AdRewardService
from app.models.ad_reward_payload_model import AdRewardPayloadModel

router = APIRouter()

@router.get("/issue")
def request_rewards(
    context: ApplicationContext = Depends(get_application_context(device_info_required=True)),
):
    ad_reward_service = AdRewardService(context.db)
    results = ad_reward_service.generate_rewards_token(context.device_info)
    return JSONResponse(content=jsonable_encoder(results))

@router.get("/verify/{ad_provider}")
def verify_rewards(
    ad_provider: str = Path(..., description="Ad network to verify"),
    ad_payload: AdRewardPayloadModel = Depends(),
    context: ApplicationContext = Depends(get_application_context()),
):
    ad_reward_service = AdRewardService(context.db)
    results = ad_reward_service.verify_admod_reward(ad_provider, ad_payload)
    return JSONResponse(content=jsonable_encoder(results))
