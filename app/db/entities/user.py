import uuid
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseOAuthAccountTable, SQLAlchemyBaseUserTable

from app.db.entities import Base
from app.db.entities.audit_mixin import AuditMixin

class OAuthAccount(SQLAlchemyBaseOAuthAccountTable[str], Base, AuditMixin):
    __tablename__ = "oauth_account"
    id: Mapped[str] = mapped_column(String(255), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(ForeignKey("user.id"))

class User(SQLAlchemyBaseUserTable[str], Base, AuditMixin):
    __tablename__ = "user"
    id: Mapped[str] = mapped_column(String(255), primary_key=True, default=lambda: str(uuid.uuid4()))
    oauth_accounts: Mapped[list[OAuthAccount]] = relationship("OAuthAccount", back_populates="user", lazy="joined")

# Add back_populates in OAuthAccount to complete the bidirectional relationship
OAuthAccount.user = relationship("User", back_populates="oauth_accounts")
