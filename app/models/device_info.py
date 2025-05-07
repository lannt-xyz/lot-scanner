import hashlib
from pydantic import BaseModel

class DeviceInfo():
    id: str
    model: str
    os_version: str
    user_agent: str

    def __init__(self, id: str, model: str, os_version: str, user_agent: str):
        self.id = id
        self.model = model
        self.os_version = os_version
        self.user_agent = user_agent

    def is_empty(self) -> bool:
        """
        Checks if the device information is empty.
        
        Returns:
            bool: True if any of the fields are empty, False otherwise.
        """
        return not (self.id and self.model and self.os_version and self.user_agent)

    def to_fingerprint(self) -> str:
        """
        Generates a fingerprint based on the device information.
        
        Returns:
            str: A unique fingerprint for the device.
        """
        raw = f"{self.id}_{self.model}_{self.os_version}_{self.user_agent}"

        # Encode the raw string to bytes and hash it
        fingerprint = hashlib.sha256(raw.encode()).hexdigest()

        return str(fingerprint)
