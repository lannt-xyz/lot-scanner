from typing import Optional
from fastapi import Depends, Request
from httpx import get
from pydantic import BaseModel, ConfigDict
from sqlmodel import Session

from app.db.entities.user import User
from app.error.bad_request_exception import BadRequestException
from app.error.unauthorized_exception import UnauthorizedException
from app.models import device_info
from app.models.device_info import DeviceInfo
from app.modules.auth import current_active_user

from app.db import SessionDep, get_session

class AuthenticatedUser():
    user_id: int
    email: Optional[str] = None

class ApplicationContext():
    # user: Optional[AuthenticatedUser] = None # change to require
    db: Session
    device_info: DeviceInfo

    def __init__(self, db: Session, device_info: DeviceInfo = None):
        self.db = db
        self.device_info = device_info
        pass


def get_device_info(request: Request) -> DeviceInfo:
    id = request.headers.get("X-Device-Id")
    model = request.headers.get("X-Device-Model")
    os_version = request.headers.get("X-Device-OS-Version")
    user_agent = request.headers.get("X-Device-User-Agent")
    
    if not id or not model or not os_version or not user_agent:
        raise BadRequestException("Missing device information in headers.")
    
    return DeviceInfo(
        id=id,
        model=model,
        os_version=os_version,
        user_agent=user_agent
    )


def get_application_context():
    def context_provider(
        db: Session = Depends(get_session),
        device_info: DeviceInfo = Depends(get_device_info),
        # authenticated_user: User = Depends(current_active_user)
    ):
        # if not authenticated_user:
        #     raise UnauthorizedException("Unauthorized.")

        # user = AuthenticatedUser(
        #     user_id=authenticated_user.id,
        #     email=authenticated_user.email
        # )
        # return ApplicationContext(user=user, db=db)
        return ApplicationContext(db=db, device_info=device_info)
    return context_provider

