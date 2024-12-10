from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr

class TokenData(BaseModel):
    """Pydantic model for token data."""
    username: Optional[str] = None

class Token(BaseModel):
    """Pydantic model for token response."""
    access_token: str
    token_type: str

class UserBase(BaseModel):
    """Base Pydantic model for user data."""
    name: str
    age: int
    city: str
    salary: float

class UserInDB(UserBase):
    """Pydantic model for user in database."""
    id: int
    join_date: datetime

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class UserResponse(UserBase):
    """Pydantic model for user response."""
    id: int
    join_date: str

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    """Pydantic model for login data validation."""
    username: str
    password: str

class UserRegister(BaseModel):
    """Pydantic model for registration data validation."""
    username: str
    email: EmailStr
    password: str

class SocialLogin(BaseModel):
    """Pydantic model for social login data."""
    provider: str
    token: str
    
class AccountResponse(BaseModel):
    """Pydantic model for account response."""
    username: str
    email: str
    social_provider: Optional[str] = None

    class Config:
        from_attributes = True

class AccountUpdate(BaseModel):
    """Pydantic model for account update."""
    current_password: str
    new_username: Optional[str] = None
    new_email: Optional[EmailStr] = None
    new_password: Optional[str] = None

class AccountDelete(BaseModel):
    """Pydantic model for account deletion."""
    password: str
