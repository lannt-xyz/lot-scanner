from sqlalchemy import Column, Index, Integer, String, Text

from app.db.entities import Base

class ScanHistory(Base):
    __tablename__ = "scan_history"

    id = Column(Integer, primary_key=True, autoincrement=True)
    file_path = Column(String(255), nullable=False)
    ocr_text = Column(Text, nullable=False)
    corrected_text = Column(Text, nullable=False)
    device_id = Column(String(255), nullable=False)

    # Create an index for the device_id column
    __table_args__ = (
        Index("idx_device_id", "device_id"),
    )
