from pathlib import Path
from typing import Union
from fastapi import UploadFile

class FileService:
    @staticmethod
    def save_temp_file(file: UploadFile, temp_dir: Union[str, Path] = "temp") -> Path:
        """
        Save an uploaded file to a temporary directory.

        Args:
            file (UploadFile): The uploaded file to save.
            temp_dir (Union[str, Path]): The directory where the file will be saved. Defaults to "temp".

        Returns:
            Path: The path to the saved file.
        """
        # Ensure the temp directory exists
        temp_dir = Path(temp_dir)
        temp_dir.mkdir(parents=True, exist_ok=True)

        # Define the path for the temporary file
        temp_file_path = temp_dir / file.filename

        # Write the file content to the temporary file
        with temp_file_path.open("wb") as temp_file:
            temp_file.write(file.file.read())

        return temp_file_path

    @staticmethod
    def delete_temp_file(file_path: Union[str, Path]) -> None:
        """
        Delete a temporary file.

        Args:
            file_path (Union[str, Path]): The path to the file to delete.
        """
        file_path = Path(file_path)
        if file_path.exists():
            file_path.unlink()
