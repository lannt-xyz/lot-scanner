from datetime import datetime
from numpy import cov
from sqlalchemy import String
from sqlalchemy.orm import declared_attr, Mapped, mapped_column
from sqlalchemy.types import DateTime, TypeDecorator

from app.utils.common import convert_datetime_to_utc, utcnow

class UtcDatetime(TypeDecorator):
    impl = DateTime(timezone=True)
    python_type = datetime

    def process_bind_param(self, value, dialect):
        binding_value = convert_datetime_to_utc(value)
        return binding_value.replace(tzinfo=None) if binding_value else None

    def process_result_value(self, value, dialect):
        return convert_datetime_to_utc(value) if value else None
    
    def  process_literal_param(self, value, dialect):
        return f"'{value}'" if value else None

class AuditMixin:
    is_deleted: Mapped[bool] = mapped_column(default=False, nullable=False)

    created_by: Mapped[str] = mapped_column(String(20), nullable=False)

    @declared_attr
    def created_at(cls) -> Mapped[datetime]:
        return mapped_column(
            UtcDatetime,
            default=utcnow(),
            onupdate=utcnow(),
            nullable=False,
        )

    updated_by: Mapped[str] = mapped_column(String(20), nullable=False)

    @declared_attr
    def updated_at(cls) -> Mapped[datetime]:
        return mapped_column(
            UtcDatetime,
            default=utcnow(),
            onupdate=utcnow(),
            nullable=False,
        )
