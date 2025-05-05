from fastapi import APIRouter, Body, Depends
from fastapi.responses import JSONResponse

from app.context import ApplicationContext, get_application_context
from app.db.services.quick_scan_service import QuickScanService
from app.models.base_response_model import BaseResponseModel
from app.models.ticket_model import TicketModel

router = APIRouter()

@router.post("")
def save_ticket(
    ticket_model: TicketModel = Body(..., description="Ticket Model"),
    context: ApplicationContext = Depends(get_application_context()),
):
    quick_scan_service = QuickScanService(context.db)
    ticket = quick_scan_service.scan(ticket_model)
    return JSONResponse(content=BaseResponseModel.of(ticket))
