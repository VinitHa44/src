from datetime import datetime

class FileUpload:  
    def __init__(self, user_id: str, file_url: str, file_type: str, created_at: datetime = None, updated_at: datetime = None):
        self.user_id = user_id
        self.file_url = file_url
        self.file_type = file_type  # "product", "complaint"
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
