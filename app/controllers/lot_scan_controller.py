from fastapi import APIRouter, Depends, UploadFile, File
from fastapi.responses import JSONResponse
from sqlmodel import Session

from app.context import ApplicationContext, get_application_context
from app.db import SessionDep
from app.db.entities import scan_history
from app.db.services.device_information_service import DeviceInfoService
from app.db.services.scan_history_service import ScanHistoryService
from app.models.device_info import DeviceInfo
from app.modules.services.image_service import ImageService

router = APIRouter()

@router.post("/ocr")
def ocr_image(
    image: UploadFile = File(...),
    context: ApplicationContext = Depends(get_application_context()),
):
    db: Session = context.db
    device_info: DeviceInfo = context.device_info

    image_service = ImageService()
    upload_file, ocr_text, json_dict, corrected_text = image_service.image_to_lot_info(device_info.id, image)

    device_info_service = DeviceInfoService(db)
    device_info_service.save_if_not_exists(device_info)

    scan_history_service = ScanHistoryService(db)
    scan_history_service.save(device_info.id, upload_file, ocr_text, corrected_text)

    return JSONResponse(content=json_dict)
