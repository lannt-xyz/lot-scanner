from sqlalchemy import Column, DateTime, Integer, String

from app.db.entities import Base
from app.db.entities.audit_mixin import AuditMixin
from app.utils.common import utcnow

class DeviceInformation(Base, AuditMixin):
    __tablename__ = "device_information"

    device_id = Column(String(255), primary_key=True, nullable=False)
    fingerprint = Column(String(255), nullable=False)
    scan_limitation = Column(Integer, nullable=True, default=0)
    scan_reseted_at = Column(DateTime, nullable=True)
