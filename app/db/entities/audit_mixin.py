from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import declared_attr, Mapped, mapped_column

from app.utils.common import utcnow

class AuditMixin:
    is_deleted: Mapped[bool] = mapped_column(default=False, nullable=False)
    created_by: Mapped[str] = mapped_column(String(255), default='guest', nullable=False)
    updated_by: Mapped[str] = mapped_column(String(255), default='guest', nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow(), onupdate=utcnow(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow(), onupdate=utcnow(), nullable=False)
