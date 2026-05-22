from typing import List, Optional
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from app.models import WorkoutLog
from app.services.parser import GeminiParserService, ExtractedWorkoutAnalysis

router = APIRouter(prefix="/api/workouts", tags=["Workout Metrics Logging Engine"])
parser_service = GeminiParserService()

# =====================================================================
# INCOMING REQUEST SCHEMAS
# =====================================================================
class LogWorkoutRequest(BaseModel):
    user_id: str = Field(..., description="The unique database identity string of the athlete")
    raw_input_text: str = Field(
        ..., 
        description="Messy fitness journal input string e.g., 'did 3x5 squats at 225, 5km run in 25m'",
        examples=["Benched 3x10 at 135lbs, then hit 40lb curls. Felt pretty energetic!"]
    )


# =====================================================================
# ROUTE HANDLERS
# =====================================================================

@router.post("/log", response_model=WorkoutLog, status_code=status.HTTP_201_CREATED)
async def parse_and_record_workout(payload: LogWorkoutRequest):
    """
    Accepts messy natural text entries, orchestrates Gemini to break them into 
    strict data models, and saves the verified result directly to MongoDB.
    """
    if not payload.raw_input_text.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The workout text log input cannot be empty."
        )

    try:
        # 1. Dispatch the unstructured payload to our standalone Gemini parser
        analysis: ExtractedWorkoutAnalysis = await parser_service.parse_unstructured_workout(
            raw_text=payload.raw_input_text
        )
        
        # 2. Instantiate our persistent Beanie Document utilizing the structured metadata
        workout_document = WorkoutLog(
            user_id=payload.user_id,
            raw_input_text=payload.raw_input_text,
            exercises=analysis.exercises,
            energy_rating=analysis.energy_rating,
            coach_notes=analysis.coach_notes
        )
        
        # 3. Commit asynchronously directly to MongoDB
        await workout_document.insert()
        return workout_document

    except RuntimeError as re:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"AI parsing execution breakdown: {str(re)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Could not commit metrics tracking data: {str(e)}"
        )


@router.get("/user/{user_id}", response_model=List[WorkoutLog])
async def get_user_workout_history(user_id: str, limit: int = 20):
    """
    Retrieves the workout history collection for a specific athlete, 
    sorted chronologically (most recent entries first).
    """
    try:
        # Query MongoDB using Beanie's built-in asynchronous lookup chains
        history = await WorkoutLog.find(WorkoutLog.user_id == user_id)\
                                  .sort(-WorkoutLog.workout_date)\
                                  .limit(limit)\
                                  .to_list()
        return history
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to query workout collection matrix: {str(e)}"
        )