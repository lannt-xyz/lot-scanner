from app.db import SessionDep
from app.db.entities.code_master import CodeMaster

from app.db.entities.ticket import Ticket
from app.models.ticket_model import TicketModel

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
        ticket.prize_number = ticket_model.prize

        self.db.add(ticket)
        self.db.commit()
        self.db.refresh(ticket)
        return ticket
