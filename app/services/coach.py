from datetime import datetime, timezone
from typing import AsyncGenerator
import asyncio
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
        Loads database conversation state, maps a manual system instructions matrix,
        and streams token arrays sequentially using true asynchronous SDK streaming.
        """
        
        # 1. Establish elite fitness persona boundaries
        system_prompt = (
            "You are 'Coach Apex', an elite, empathetic, yet highly candid fitness and nutrition coach. "
            "Your goal is to guide the user toward their athletic goals with evidence-based principles. "
            "Be encouraging but down-to-earth. Do not use corporate fluff. Speak like a helpful expert peer. "
            "Keep answers concise, direct, and focused on actionable metrics. Never give medical diagnoses."
        )

        # 2. Build explicit content historical array blocks manually
        contents_payload = []
        
        # Hydrate array with past MongoDB conversations and force strict role compliance
        if chat_session.messages:
            for msg in chat_session.messages:
                # Fallback safety validation to ignore corrupt or empty historical elements
                if not msg.content or not msg.content.strip():
                    continue
                sdk_role = "user" if msg.role in ["user", "human"] else "model"
                contents_payload.append(
                    types.Content(
                        role=sdk_role,
                        parts=[types.Part.from_text(text=msg.content)]
                    )
                )
            
        # 3. Append the incoming prompt to the very end of the array sequence
        contents_payload.append(
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=user_message)]
            )
        )

        # 4. Commit user prompt message locally to historical memory
        new_user_msg = ChatMessage(role="user", content=user_message, timestamp=get_utc_now())
        chat_session.messages.append(new_user_msg)
        
        ai_response_chunks = []

        try:
            # 5. 🟢 CRITICAL FIXED LINE: Call the true async engine stream wrapper ('aio.models') with await
            response_stream = await self.client.aio.models.generate_content_stream(
                model=self.model_name,
                contents=contents_payload,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    temperature=0.7
                )
            )

            # 6. 🟢 CRITICAL FIXED LINE: Use 'async for' to consume the asynchronous network generator
            async for chunk in response_stream:
                if chunk.text:
                    ai_response_chunks.append(chunk.text)
                    # Prepend 'data: ' and append double newlines to force-flush the streaming network buffer
                    yield f"data: {chunk.text}\n\n"

            # 7. Stitch components and update database collection
            full_ai_response = "".join(ai_response_chunks)
            new_ai_msg = ChatMessage(role="model", content=full_ai_response, timestamp=get_utc_now())
            
            chat_session.messages.append(new_ai_msg)
            chat_session.last_updated = get_utc_now()
            
            await chat_session.save()

        except Exception as e:
            print(f"❌ Error during active Coach Apex core model generation stream: {e}")
            yield f"data: [Coach Apex connectivity breakdown occurred: {str(e)}]\n\n"