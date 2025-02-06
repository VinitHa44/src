from pydantic import BaseModel

class FileUploadResponse(BaseModel): 
    file_id: str  
    user_id: str
    file_url: str
    file_type: str
