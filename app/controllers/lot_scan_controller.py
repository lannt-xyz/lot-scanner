from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from app.services.image_service import ImageService

router = APIRouter()

@router.post("/ocr")
def ocr_image(image: UploadFile = File(...)):
    image_service = ImageService()
    result = image_service.image_to_lot_info(image)
    return JSONResponse(content=result)
    
    
