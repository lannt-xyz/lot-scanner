from fastapi import APIRouter, Body, Depends, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from sqlalchemy.orm import Session

from app.context import ApplicationContext, get_application_context
from app.db import get_session
from app.db.services.code_master_service import CodeMasterService
from app.db.services.ticket_service import TicketService
from app.models.base_response_model import BaseResponseModel
from app.models.ticket_model import TicketModel

router = APIRouter()

@router.post("")
def save_ticket(
    ticket_model: TicketModel = Body(..., description="Ticket Model"),
    context: ApplicationContext = Depends(get_application_context()),
):
    ticket_service = TicketService(context.db)
    ticket_service.register_ticket(ticket_model)
    return JSONResponse(content=BaseResponseModel.ok())
