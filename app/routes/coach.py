from typing import Optional  # Added missing import
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from bson import ObjectId, errors as bson_errors

from app.models import ChatSession
from app.services.coach import GeminiCoachService

# Instantiate our router and the underlying AI streaming client
router = APIRouter(prefix="/api/coach", tags=["Coach Apex Conversational Interface"])
coach_service = GeminiCoachService()

# =====================================================================
# INCOMING REQUEST SCHEMAS
# =====================================================================
class CreateChatRequest(BaseModel):
    user_id: str = Field(..., description="The unique database ID of the user starting the chat")
    session_name: Optional[str] = Field("Active Coaching Discussion", description="Optional label for the thread")


class ChatMessageRequest(BaseModel):
    message: str = Field(..., description="The messy user message sent to the coach")


# =====================================================================
# ROUTE HANDLERS
# =====================================================================

@router.post("/sessions", status_code=status.HTTP_201_CREATED)
async def create_new_chat_session(payload: CreateChatRequest):
    """
    Spins up a new empty conversation thread in MongoDB for a user.
    Returns the session document containing the unique session ID.
    """
    try:
        new_session = ChatSession(
            user_id=payload.user_id,
            session_name=payload.session_name,
            messages=[]
        )
        await new_session.insert()
        return new_session
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Could not initialize conversation thread: {str(e)}"
        )


@router.post("/sessions/{session_id}/stream")
async def stream_coach_chat(session_id: str, payload: ChatMessageRequest):
    """
    Accepts an incoming statement, pulls historical thread context from MongoDB,
    and returns a live text streaming HTTP chunk connection.
    """
    # 1. Validation Check: Verify session_id is a syntactically correct 24-character hex string
    try:
        ObjectId(session_id)
    except (bson_errors.InvalidId, TypeError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The provided session_id parameter format is malformed or invalid."
        )

    # 2. Look up the session in the database
    session = await ChatSession.get(session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The requested coaching conversation thread does not exist."
        )

    # 3. Return an active HTTP StreamingResponse wrapping our generator service layer
    return StreamingResponse(
        coach_service.stream_coach_response(chat_session=session, user_message=payload.message),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )