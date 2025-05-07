from sqlalchemy import Column, String

from app.db.entities import Base
from app.db.entities.audit_mixin import AuditMixin

class UserDevice(Base, AuditMixin):
    __tablename__ = "user_device"

    user_id = Column(String(255), primary_key=True, nullable=False)
    device_id = Column(String(255), primary_key=True, nullable=False)
