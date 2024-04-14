from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import Optional


# User Validation
class UserBase(BaseModel):
    email: EmailStr = Field(..., title="user email address", example="example@email.com")
    
    
class UserCreate(UserBase):
    password: str = Field(..., title="user password", example="SOMEStrongPassword")
    

class User(UserBase):
    id: int
    is_active: bool
    is_verified: bool
    
    model_config = ConfigDict(
        from_attributes=True
    )
    
# OTP Validation
class OTPBase(BaseModel):
    code: str = Field(..., title="OTP code", examples="123456")
    
    
class OTPData(OTPBase):
    user_id: int
    code: Optional[str] = None
    
    model_config = ConfigDict(
        from_attributes=True
    )
    
# Validate User OTP
class OneTimePassword(BaseModel):
    code: str