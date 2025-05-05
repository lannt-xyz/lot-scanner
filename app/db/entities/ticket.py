from sqlalchemy import Column, Integer, String, DateTime, Boolean

from app.db.entities import Base
from app.db.entities.audit_mixin import AuditMixin

class Ticket(Base, AuditMixin):
    __tablename__ = "ticket"

    id = Column(Integer, primary_key=True, autoincrement=True)
    channel = Column(String(10))
    prize_date = Column(DateTime)
    prize_number = Column(String(6))
    result = Column(String(2)) # 0: none match, 1~9: match 1~9
    prize_amount = Column(Integer)
