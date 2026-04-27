from fastapi import HTTPException
from pathlib import Path
from logger import logger


async def validate_and_save_file(file):
    try:
        # Path to save uploaded files inside the 'static/uploads' directory
        UPLOAD_DIR = Path(__file__).parent.parent / "static" / "uploads"
        UPLOAD_DIR.mkdir(parents=True, exist_ok=True)  # Ensure the folder exists

        file_size = file.size
        # max size of file is 10 MB
        if file_size > 10 * 1024 * 1024:
            raise HTTPException(status_code=413, detail="File size too large. Max size is 10 MB.")

        # File save path
        file_location = UPLOAD_DIR / file.filename

        # Save the file
        content = await file.read()
        with open(file_location, "wb") as f:
            f.write(content)
        return file_location
    except Exception:
        logger.error("Some Error occured while uploading file")
        return None
