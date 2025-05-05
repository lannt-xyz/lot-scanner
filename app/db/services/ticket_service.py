from sqlmodel import and_, select

from app.db import SessionDep
from app.db.entities.code_master import CodeMaster

from app.db.entities.ticket import Ticket
from app.models.ticket_model import TicketModel, TicketResponseModel

class TicketService:
    def __init__(self, db: SessionDep):
        self.db = db
        pass
    
    def register_ticket(self, ticket_model: TicketModel) -> Ticket:
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
        return ticket

    def get_ticket(self) -> Ticket:
        """
        Retrieves the ticket from the database.

        Returns:
            Ticket: The retrieved ticket object.
        """
        tickets = self.db.exec(
            select(
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
                and_(
                    Ticket.is_deleted.is_(False),
                )
            ).order_by(Ticket.created_at.desc())
        ).all()
        
        if not tickets or len(tickets) == 0:
            return None

        return [
            TicketResponseModel(**ticket._asdict())
            for ticket in tickets
        ]
