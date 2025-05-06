from app.db import SessionDep
from app.db.entities.scan_history import ScanHistory
from app.models.device_info import DeviceInfo

class ScanHistoryService:
    def __init__(self, db: SessionDep):
        self.db = db
        pass

    def save(self, device_id: str, file_path: str, ocr_text: str, corrected_text: str) -> None:
        """
        Saves the scan history to the database.

        Args:
            device_id (str): The ID of the device.
            file_path (Path): The path to the scanned file.
            ocr_text (str): The text extracted from the image using OCR.
            corrected_text (str): The corrected text after processing.
        """

        file_path_str = str(file_path)

        # Assuming you have a ScanHistory model defined
        scan_history_model = ScanHistory()
        scan_history_model.file_path = file_path_str
        scan_history_model.ocr_text = ocr_text
        scan_history_model.corrected_text = corrected_text
        scan_history_model.device_id = device_id
        self.db.add(scan_history_model)
        self.db.commit()