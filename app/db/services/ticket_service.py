from typing import List, Optional
from sqlmodel import select

from app.db import SessionDep
from app.db.entities.code_master import CodeMaster

from app.db.entities.ticket import Ticket
from app.models.ticket_model import TicketModel, TicketResponseModel
from app.utils.common import get_ticket_result
from app.utils.constants import TICKET_NO_RESULT, TICKET_RESULT_DATA

class TicketService:
    def __init__(self, db: SessionDep):
        self.db = db
        pass

    def _remap_result(self, ticket: Ticket) -> TicketResponseModel:
        result = TicketResponseModel(**ticket._asdict())
        ticket_result = result.result
        if ticket_result:
            result.result = get_ticket_result(ticket_result)['message']
            result.prize_amount = get_ticket_result(ticket_result)['amount']
        else:
            result.result = TICKET_NO_RESULT

        return result

    def register_ticket(self, ticket_model: TicketModel) -> TicketResponseModel:
        """
        Registers a new ticket in the database.

        Args:
            ticket (TicketModel): The ticket object to be registered.

        Returns:
            Ticket: The registered ticket object.
        """
        ticket = Ticket()
        ticket.channel = ticket_model.channel
        ticket.prize_date = ticket_model.prize_date
        ticket.prize_number = ticket_model.prize_number

        self.db.add(ticket)
        self.db.commit()
        self.db.refresh(ticket)

        return TicketResponseModel(**ticket.__dict__)

    def get_ticket_statement(self, ticket_id: Optional[int] = None) -> select:
        statement = select(
                Ticket.id,
                Ticket.channel,
                Ticket.prize_date,
                Ticket.prize_number,
                Ticket.prize_amount,
                Ticket.result,
                Ticket.is_deleted,
                Ticket.created_at,
                Ticket.updated_at,
                Ticket.created_by,
                Ticket.updated_by,
            ).where(
                Ticket.is_deleted.is_(False),
            ).order_by(Ticket.created_at.desc())

        if ticket_id:
            statement = statement.where(Ticket.id == ticket_id)

        return statement

    def get_tickets(self) -> List[TicketResponseModel]:
        """
        Retrieves the tickets from the database.

        Returns:
            Ticket: The retrieved ticket object.
        """
        statement = self.get_ticket_statement()
        tickets = self.db.exec(statement).all()
        if not tickets or len(tickets) == 0:
            return []

        return [
            self._remap_result(ticket)
            for ticket in tickets
        ]

    def get_ticket(self, ticket_id: int) -> TicketResponseModel:
        """
        Retrieves a ticket by its ID from the database.

        Args:
            ticket_id (int): The ID of the ticket to be retrieved.

        Returns:
            Ticket: The retrieved ticket object.
        """
        statement = self.get_ticket_statement(ticket_id)
        ticket = self.db.exec(statement).first()
        if not ticket:
            return None

        return self._remap_result(ticket)
