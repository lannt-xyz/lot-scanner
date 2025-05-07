from sqlmodel import select, and_

from app.db import SessionDep
from app.db.entities.device_information import DeviceInformation
from app.models.device_info import DeviceInfo

class DeviceInfoService:
    def __init__(self, db: SessionDep):
        self.db = db
        pass

    def save_if_not_exists(self, device_info: DeviceInfo) -> None:
        """
        Saves the device information to the database if it does not already exist.

        Args:
            device_info (DeviceInfo): The device information to save.
        """
        # Check if the device information already exists in the database
        existing_device = self.db.exec(select(
                DeviceInformation
            ).where(
                DeviceInformation.device_id == device_info.id,
            )).first()
        
        if not existing_device:
            # If it doesn't exist, add it to the database
            self.db.add(DeviceInformation(
                device_id=device_info.id,
                fingerprint=device_info.to_fingerprint(),
            ))
            self.db.commit()