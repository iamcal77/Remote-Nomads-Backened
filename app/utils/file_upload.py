from pathlib import Path
from uuid import uuid4
from fastapi import UploadFile

BASE_DIR = Path("/app/app")  # points to inner app folder

def save_file(file: UploadFile, folder: str = "cvs") -> str:
    ext = Path(file.filename).suffix
    filename = f"{uuid4().hex}{ext}"

    # Save under BASE_DIR/static/<folder>/
    folder_path = BASE_DIR / "static" / folder
    folder_path.mkdir(parents=True, exist_ok=True)

    file_path = folder_path / filename

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    # Return path relative to BASE_DIR for storing in DB
    return f"static/{folder}/{filename}"
