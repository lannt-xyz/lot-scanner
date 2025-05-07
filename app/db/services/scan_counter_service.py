from sqlalchemy import func
from sqlmodel import select, and_

from config import settings

from app.db import SessionDep
from app.db.entities.device_information import DeviceInformation
from app.db.entities.scan_history import ScanHistory
from app.db.entities.user import User
from app.db.entities.user_device import UserDevice

class ScanCounterService:
    def __init__(self, db: SessionDep):
        self.db = db
        pass

    def is_scanable(self, device_id: str) -> bool:
        """
        Checks if the device can be scanned based on the scan count.

        Args:
            device_id (str): The ID of the device.

        Returns:
            bool: True if the device can be scanned, False otherwise.
        """
        # Check if the device ID is valid and owned by the user
        device_info = self._find_user_own_device_by_id(device_id)
        limit = 0
        if not device_info:
            # If the device ID is not found, it is considered a guest
            limit = settings.scan_limit_guest
        else:
            # If the device ID is found, it is considered a user
            limit = settings.scan_limit_user

        scan_count = self._count(device_id)
        if scan_count >= limit:
            return False
        return True

    def _count(self, device_id: str) -> int:
        """
        Counts the number of scans for a given device ID.

        Args:
            device_id (str): The ID of the device.

        Returns:
            int: The count of scans for the device.
        """
        scan_count = self.db.exec(
            select(
                func.count(ScanHistory.id)
            ).where(
                ScanHistory.device_id == device_id
            )
        ).one_or_none()
        if scan_count is None:
            return 0
        return scan_count

    def _find_user_own_device_by_id(self, device_id: str) -> DeviceInformation:
        device_info = self.db.exec(
            select(
                DeviceInformation
            ).join(UserDevice, and_(
                    UserDevice.device_id == DeviceInformation.device_id,
                    UserDevice.is_deleted.is_(False),
                )
            ).join(User, and_(
                    User.id == UserDevice.user_id,
                    User.is_deleted.is_(False),
                    User.is_active.is_(True),
                )
            ).where(
                and_(
                    DeviceInformation.device_id == device_id,
                    DeviceInformation.is_deleted.is_(False),
                )
            )
        ).first()
        return device_info

