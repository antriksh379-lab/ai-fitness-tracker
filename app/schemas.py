from pydantic import BaseModel
from typing import List, Optional

# --- Parsing Inputs ---
class UserTextInput(BaseModel):
    raw_text: str

# --- Parsed Output Mappings ---
class FoodItem(BaseModel):
    itemName: str
    calories: int
    proteinGrams: int

class ExerciseItem(BaseModel):
    exerciseName: str
    sets: int
    reps: int
    weightLbs: int

class WorkoutData(BaseModel):
    routineName: str
    exercises: List[ExerciseItem]

class IngestionPayload(BaseModel):
    logType: str  # 'food', 'workout', or 'both'
    foodData: Optional[List[FoodItem]] = None
    workoutData: Optional[WorkoutData] = None

# --- Conversational Coach Contracts ---
class ChatMessage(BaseModel):
    role: str  # 'user' or 'model'
    text: str

class CoachRequest(BaseModel):
    message: str
    chatHistory: List[ChatMessage]