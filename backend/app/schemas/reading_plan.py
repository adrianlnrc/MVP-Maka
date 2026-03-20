from pydantic import BaseModel


class ReadingPlanDayOut(BaseModel):
    id: int
    day_number: int
    title: str
    story_ids: list[str]
    bible_passages: list[str]
    reflection_prompt: str

    model_config = {"from_attributes": True}


class ReadingPlanOut(BaseModel):
    id: int
    name: str
    description: str
    total_days: int
    is_default: bool

    model_config = {"from_attributes": True}


class UserProgressOut(BaseModel):
    current_day: int
    streak_days: int
    longest_streak: int
    total_days_completed: int
    plan: ReadingPlanOut

    model_config = {"from_attributes": True}


class CompleteDayRequest(BaseModel):
    day_number: int
    notes: str | None = None
