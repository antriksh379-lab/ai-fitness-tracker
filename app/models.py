from datetime import datetime, timezone
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from beanie import Document, Indexed

# Function to generate uniform timezone-aware UTC timestamps
def get_utc_now() -> datetime:
    return datetime.now(timezone.utc)

# =====================================================================
# 1. EMBEDDED SUB-MODELS (Helper structures nested inside Documents)
# =====================================================================

class UserBiometrics(BaseModel):
    age: int
    height_cm: float
    weight_kg: float
    fitness_level: str = "beginner"  # e.g., beginner, intermediate, advanced
    primary_goal: str               # e.g., hypertrophy, fat_loss, endurance
    injuries_or_limitations: List[str] = []


class ExercisePerformance(BaseModel):
    name: str = Field(..., description="Name of the exercise e.g., Barbell Bench Press")
    sets: int
    reps: List[int] = Field(default=[], description="Reps completed per set")
    weight_lbs: Optional[List[float]] = Field(default=None, description="Weights used per set if applicable")
    duration_seconds: Optional[int] = None
    rpe: Optional[int] = Field(None, description="Rate of Perceived Exertion (1-10)")


# =====================================================================
# 2. MAIN DATABASE COLLECTIONS (Beanie Documents)
# =====================================================================

class User(Document):
    email: Indexed(str, unique=True)
    full_name: str
    hashed_password: str
    biometrics: Optional[UserBiometrics] = None
    created_at: datetime = Field(default_factory=get_utc_now)

    class Settings:
        name = "users"


class WorkoutLog(Document):
    user_id: Indexed(str)
    raw_input_text: str
    workout_date: datetime = Field(default_factory=get_utc_now)
    
    exercises: List[ExercisePerformance] = []
    energy_rating: Optional[int] = Field(None, description="User energy score 1-5")
    coach_notes: Optional[str] = Field(None, description="Immediate callout or advice from the AI parser")

    class Settings:
        name = "workout_logs"


class ChatMessage(BaseModel):
    role: str  # "user" or "model"
    content: str
    timestamp: datetime = Field(default_factory=get_utc_now)


class ChatSession(Document):
    user_id: Indexed(str)
    session_name: str = "Active Coaching Discussion"
    started_at: datetime = Field(default_factory=get_utc_now)
    last_updated: datetime = Field(default_factory=get_utc_now)
    messages: List[ChatMessage] = []

    class Settings:
        name = "chat_sessions"