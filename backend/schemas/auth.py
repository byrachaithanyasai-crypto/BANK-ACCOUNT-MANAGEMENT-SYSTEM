from pydantic import BaseModel
from typing import Optional

class UserResponse(BaseModel):
    username: str
    role: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user: Optional[UserResponse] = None

class LoginRequest(BaseModel):
    username: str
    password: str
