from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# --- User Schemas ---
class UserBase(BaseModel):
    full_name: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    risk_profile: Optional[str] = None

class User(UserBase):
    id: int
    risk_profile: str
    created_at: datetime

    class Config:
        from_attributes = True

# --- Auth Schemas ---
class Token(BaseModel):
    access_token: str
    token_type: str
    user_name: str

class TokenData(BaseModel):
    email: Optional[str] = None

# --- Dashboard Schemas ---
class PortfolioSummary(BaseModel):
    total_value: float
    ytd_return_pct: float
    risk_score: float
    rebalance_status: str
