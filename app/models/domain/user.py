from typing import Literal
from datetime import datetime

class User:  
    def __init__(self, name: str, email: str, password_hash: str, role: Literal["admin", "buyer", "seller"], created_at: datetime = None, updated_at: datetime = None):
        self.name = name
        self.email = email
        self.password_hash = password_hash
        self.role = role
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
