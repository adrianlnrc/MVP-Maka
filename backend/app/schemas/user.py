from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserPublic(BaseModel):
    id: str
    email: EmailStr
    full_name: str
    is_active: bool
    is_verified: bool
    subscription_status: str
    subscription_expires_at: datetime | None
    created_at: datetime

    model_config = {"from_attributes": True}


class UserUpdate(BaseModel):
    full_name: str | None = None


class UserStats(BaseModel):
    total_days_completed: int
    streak_days: int
    longest_streak: int
    current_day: int | None
