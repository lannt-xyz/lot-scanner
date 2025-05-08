from fastapi import APIRouter, Body, Depends, Path

from app.context import ApplicationContext, get_application_context
from app.db.services.ticket_service import TicketService
from app.models.base_response_model import BaseResponseModel
from app.models.ticket_model import TicketModel

router = APIRouter()

@router.get("")
def get_tickets(
    context: ApplicationContext = Depends(get_application_context()),
):
    ticket_service = TicketService(context.db)
    tickets = ticket_service.get_tickets()
    return BaseResponseModel.ok(tickets)

@router.post("")
def save_ticket(
    ticket_model: TicketModel = Body(..., description="Ticket Model"),
    context: ApplicationContext = Depends(get_application_context()),
):
    ticket_service = TicketService(context.db)
    ticket = ticket_service.register_ticket(ticket_model)
    return BaseResponseModel.ok(ticket)

@router.get("/{ticket_id}")
def get_ticket(
    ticket_id: int = Path(..., description="Ticket ID"),
    context: ApplicationContext = Depends(get_application_context()),
):
    ticket_service = TicketService(context.db)
    ticket = ticket_service.get_ticket(ticket_id)
    return BaseResponseModel.ok(ticket)
