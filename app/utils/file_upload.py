from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

BASE_DIR = Path(__file__).resolve().parent.parent.parent

def save_file(file: UploadFile, folder: str = "uploads") -> str:
    ext = Path(file.filename).suffix
    filename = f"{uuid4().hex}{ext}"

    folder_path = BASE_DIR / "static" / folder
    folder_path.mkdir(parents=True, exist_ok=True)

    file_path = folder_path / filename

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    return f"static/{folder}/{filename}"
