from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from sqlalchemy import func, update
from sqlmodel import select, and_
from yaml import scan

from config import settings

from app.db import SessionDep
from app.db.entities.device_information import DeviceInformation
from app.db.entities.scan_history import ScanHistory
from app.db.entities.user import User
from app.db.entities.user_device import UserDevice

class UserDeviceModel(BaseModel):
    device_id: str
    scan_limitation: Optional[int] = 0
    scan_reseted_at: Optional[datetime] = None
    user_id: Optional[str] = None
    model_config = {
        "from_attributes": True,
    }

class ScanCounterService:
    def __init__(self, db: SessionDep):
        self.db = db
        pass

    def decrease_limitation(self, device_id: str) -> None:
        """
        Increases the scan count for the device.

        Args:
            device_id (str): The ID of the device.
        """
        # Check if the device ID is valid and owned by the user
        device_info = self._find_device_by_id(device_id)
        if device_info is None:
            return

        statement = (
            update(
                DeviceInformation
            ).values(
                scan_limitation=DeviceInformation.scan_limitation - 1
            ).where(
                and_(
                    DeviceInformation.device_id == device_info.device_id,
                    DeviceInformation.is_deleted.is_(False),
                )
            )
        )
        self.db.exec(statement)
        self.db.commit()

    def is_scanable(self, device_id: str) -> bool:
        """
        Checks if the device can be scanned based on the scan count.

        Args:
            device_id (str): The ID of the device.

        Returns:
            bool: True if the device can be scanned, False otherwise.
        """
        # Check if the device ID is valid and owned by the user
        device_info = self._find_device_by_id(device_id)
        if device_info is None:
            return True

        # check if scan_reseted_at is in the previous day, then reset the scan count
        device_info = self._reset_scan_limitation(device_info)

        # Check if the scan limitation is not None and greater than 0 then True else False
        return not (device_info.scan_limitation is None or device_info.scan_limitation <= 0)

    def _reset_scan_limitation(self, device_info: UserDeviceModel) -> UserDeviceModel:
        current_datetime = datetime.now()
        scan_reseted_at = device_info.scan_reseted_at or current_datetime
        is_previous_day = scan_reseted_at.date() < current_datetime.date()
        if is_previous_day or device_info.scan_limitation is None:
            # Reset the scan count if the reset time has passed
            if device_info.user_id is None:
                device_info.scan_limitation = settings.scan_limit_guest
            else:
                device_info.scan_limitation = settings.scan_limit_user
            device_info.scan_reseted_at = current_datetime

            # Update the scan limitation in the database
            statement = (
                update(
                    DeviceInformation
                ).values(
                    scan_limitation=device_info.scan_limitation,
                    scan_reseted_at=device_info.scan_reseted_at,
                ).where(
                    and_(
                        DeviceInformation.device_id == device_info.device_id,
                        DeviceInformation.is_deleted.is_(False),
                    )
                )
            )
            self.db.exec(statement)
            self.db.commit()

        return device_info

    def _find_device_by_id(self, device_id: str) -> UserDeviceModel:
        device_info = self.db.exec(
            select(
                DeviceInformation.device_id,
                DeviceInformation.scan_limitation,
                DeviceInformation.scan_reseted_at,
                User.id.label("user_id"),
            ).join(UserDevice, and_(
                    UserDevice.device_id == DeviceInformation.device_id,
                    UserDevice.is_deleted.is_(False),
                ), isouter=True
            ).join(User, and_(
                    User.id == UserDevice.user_id,
                    User.is_deleted.is_(False),
                    User.is_active.is_(True),
                ), isouter=True
            ).where(
                and_(
                    DeviceInformation.device_id == device_id,
                    DeviceInformation.is_deleted.is_(False),
                )
            )
        ).first()
        
        if device_info is None:
            return None

        return UserDeviceModel.model_validate({
            **device_info._asdict(),
        })
