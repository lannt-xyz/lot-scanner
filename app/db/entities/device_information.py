from sqlalchemy import Column, String

from app.db.entities import Base
from app.db.entities.audit_mixin import AuditMixin

class DeviceInformation(Base, AuditMixin):
    __tablename__ = "device_information"

    device_id = Column(String(255), primary_key=True, nullable=False)
    fingerprint = Column(String(255), nullable=False)
