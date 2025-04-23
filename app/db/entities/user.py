from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseOAuthAccountTable, SQLAlchemyBaseUserTable
from sqlalchemy.orm import relationship

from app.db.entities import Base

class OAuthAccount(SQLAlchemyBaseOAuthAccountTable[int], Base):
    __tablename__ = "oauth_account"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id")) 

class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    oauth_accounts: Mapped[list[OAuthAccount]] = relationship("OAuthAccount", back_populates="user", lazy="joined")

# Add back_populates in OAuthAccount to complete the bidirectional relationship
OAuthAccount.user = relationship("User", back_populates="oauth_accounts")
