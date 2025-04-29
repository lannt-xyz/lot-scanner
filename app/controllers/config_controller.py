from fastapi import APIRouter, Depends, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from sqlalchemy.orm import Session

from app.db import get_session
from app.db.services.code_master_service import CodeMasterService

router = APIRouter()

@router.get("/configurations")
def get_channels(
    group_code: str = Query(..., description="Group code to filter configurations"),
    db: Session = Depends(get_session),
):
    code_master_service = CodeMasterService(db)
    results = code_master_service.get_by_group_code(group_code)
    return JSONResponse(content=jsonable_encoder(results))
