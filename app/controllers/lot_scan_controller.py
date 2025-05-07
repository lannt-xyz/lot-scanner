from unittest import result
from fastapi import APIRouter, Depends, UploadFile, File
from fastapi.responses import JSONResponse
from pydantic import Json
from sqlmodel import Session

from app.context import ApplicationContext, get_application_context
from app.db.services.device_information_service import DeviceInfoService
from app.db.services.scan_counter_service import ScanCounterService
from app.db.services.scan_history_service import ScanHistoryService
from app.error.bad_request_exception import BadRequestException
from app.error.rate_limit_exception import RateLimitException
from app.models.base_response_model import BaseResponseModel
from app.models.device_info import DeviceInfo
from app.modules.services.image_service import ImageService

router = APIRouter()

@router.post("/ocr")
def ocr_image(
    image: UploadFile = File(...),
    context: ApplicationContext = Depends(get_application_context(device_info_required=True)),
):
    db: Session = context.db
    device_info: DeviceInfo = context.device_info

    scan_counter_service = ScanCounterService(db)
    is_scanable = scan_counter_service.is_scanable(device_info.id)
    if not is_scanable:
        raise RateLimitException("Rate limit exceeded. Please try again later.")

    image_service = ImageService()
    upload_file, ocr_text, ocr_result, corrected_text = image_service.image_to_lot_info(device_info.id, image)

    device_info_service = DeviceInfoService(db)
    device_info_service.save_if_not_exists(device_info)

    # Check if the JSON response contains a result
    # If the result is empty, raise an exception for ignoring scan history
    if ocr_result.result is not None:
        scan_history_service = ScanHistoryService(db)
        scan_history_service.save(device_info.id, upload_file, ocr_text, corrected_text)

    return BaseResponseModel.ok(ocr_result)
