from sqlalchemy import Column, Integer, String

from app.db.entities import Base
from app.db.entities.audit_mixin import AuditMixin

class ScanHistory(Base, AuditMixin):
    __tablename__ = "scan_history"

    id = Column(Integer, primary_key=True, autoincrement=True)
    file_path = Column(String(255), nullable=False)
    ocr_text = Column(String(255), nullable=False)
    corrected_text = Column(String(255), nullable=False)
    device_id = Column(String(255), nullable=False)
