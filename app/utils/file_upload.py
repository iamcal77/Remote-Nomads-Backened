# app/utils/file_upload.py
import os
from fastapi import UploadFile
from uuid import uuid4

def save_file(file: UploadFile, folder: str = "uploads") -> str:
    ext = os.path.splitext(file.filename)[1]
    filename = f"{uuid4().hex}{ext}"
    folder_path = os.path.join("static", folder)
    os.makedirs(folder_path, exist_ok=True)
    file_path = os.path.join(folder_path, filename)

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    return file_path
