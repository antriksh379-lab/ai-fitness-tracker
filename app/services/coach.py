from datetime import datetime, timezone
from typing import AsyncGenerator
from google import genai
from google.genai import types

from app.config import settings
from app.models import ChatSession, ChatMessage, get_utc_now


class GeminiCoachService:
    def __init__(self):
        # Initialize standard standalone Google GenAI driver
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.model_name = "gemini-2.5-flash"

    async def stream_coach_response(
        self, chat_session: ChatSession, user_message: str
    ) -> AsyncGenerator[str, None]:
        """
        Loads database conversation state, seeds Gemini's history matrix, 
        streams the response back chunk-by-chunk, and updates MongoDB.
        """
        
        # 1. Map MongoDB historical schemas into the required Google SDK Content layout
        sdk_history = []
        for msg in chat_session.messages:
            sdk_history.append(
                types.Content(
                    role=msg.role,
                    parts=[types.Part.from_text(text=msg.content)]
                )
            )

        # 2. Establish elite fitness persona boundaries
        system_prompt = (
            "You are 'Coach Apex', an elite, empathetic, yet highly candid fitness and nutrition coach. "
            "Your goal is to guide the user toward their athletic goals with evidence-based principles. "
            "Be encouraging but down-to-earth. Do not use corporate fluff. Speak like a helpful expert peer. "
            "Keep answers concise, direct, and focused on actionable metrics. Never give medical diagnoses."
        )

        # 3. Spin up an active, stateful SDK chat instance (Awaited correctly)
        sdk_chat = await self.client.aio.chats.create(
            model=self.model_name,
            history=sdk_history,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                temperature=0.7,  # Slight elevation allows fluid, human-like dialogue variance
            )
        )

        # 4. Record the user's incoming statement locally immediately (Timezone aware)
        new_user_msg = ChatMessage(role="user", content=user_message, timestamp=get_utc_now())
        chat_session.messages.append(new_user_msg)
        
        # Accumulator array to capture pieces of the streaming response
        ai_response_chunks = []

        try:
            # 5. Initiate the asynchronous streaming transport loop (Removed the extra 'await')
            async for chunk in sdk_chat.send_message_stream(user_message):
                if chunk.text:
                    ai_response_chunks.append(chunk.text)
                    yield chunk.text  # Immediately stream text chunks back to client

            # 6. Stitch response pieces together and commit to MongoDB
            full_ai_response = "".join(ai_response_chunks)
            new_ai_msg = ChatMessage(role="model", content=full_ai_response, timestamp=get_utc_now())
            
            chat_session.messages.append(new_ai_msg)
            chat_session.last_updated = get_utc_now()
            
            # Save the updated conversation session document to MongoDB via Beanie
            await chat_session.save()

        except Exception as e:
            print(f"❌ Error during active Coach Apex chat execution stream: {e}")
            yield " [Coach Apex connection anomaly detected. Please try re-transmitting.]"