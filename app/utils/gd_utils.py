import io
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from fastapi import HTTPException, UploadFile

GDRIVE_CREDENTIALS_FILE = "book-api-449304-a2301d1293f4.json"
SCOPES = ["https://www.googleapis.com/auth/drive.file"]
FOLDER_ID = "1o5YxUCI0ws85Lkj2gbHOtvZE07MK0RpO"

credentials = service_account.Credentials.from_service_account_file(
    GDRIVE_CREDENTIALS_FILE, scopes=SCOPES
)
drive_service = build("drive", "v3", credentials=credentials)


async def upload_to_google_drive(file: UploadFile):
    try:
        file_metadata = {"name": file.filename, "parents": [FOLDER_ID]}
        file_content = io.BytesIO(await file.read())  # Read file before passing

        media = MediaIoBaseUpload(file_content, mimetype=file.content_type)
        file_drive = (
            drive_service.files()
            .create(body=file_metadata, media_body=media, fields="id, webViewLink")
            .execute()
        )
        return file_drive
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Google Drive upload failed: {str(e)}")

