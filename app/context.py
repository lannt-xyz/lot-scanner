from typing import Optional
from fastapi import Depends
from pydantic import BaseModel, ConfigDict
from sqlmodel import Session

from app.db.entities.user import User
from app.error.unauthorized_exception import UnauthorizedException
from app.modules.auth import current_active_user

from app.db import get_session

class AuthenticatedUser(BaseModel):
    user_id: int
    email: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class ApplicationContext(BaseModel):
    user: AuthenticatedUser
    db: Session
    model_config = ConfigDict(arbitrary_types_allowed=True)

def get_application_context():
    def context_provider(
        db: Session = Depends(get_session),
        authenticated_user: User = Depends(current_active_user)
    ):
        if not authenticated_user:
            raise UnauthorizedException("Unauthorized.")

        user = AuthenticatedUser(
            user_id=authenticated_user.id,
            email=authenticated_user.email
        )
        return ApplicationContext(user=user, db=db)
    return context_provider
