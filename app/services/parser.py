import json
from typing import List, Optional
from pydantic import BaseModel, Field
from google import genai
from google.genai import types

from app.config import settings
from app.models import ExercisePerformance

# =====================================================================
# INTERMEDIATE EXTRACTION TARGET SCHEMA
# =====================================================================
class ExtractedWorkoutAnalysis(BaseModel):
    """
    The structured target layout Gemini must strictly fill out.
    """
    exercises: List[ExercisePerformance] = Field(
        description="A detailed breakdown of every single exercise, set, and rep mentioned by the user."
    )
    energy_rating: Optional[int] = Field(
        None, 
        ge=1, le=5, 
        description="An inferred rating from 1 to 5 of the user's energy or performance, if identifiable. 5 is peak energy."
    )
    coach_notes: str = Field(
        description="A direct, brief (1-2 sentences) peer-like athletic response validating their effort and noting any technical anomalies."
    )


# =====================================================================
# CORE GEMINI PARSING ENGINE WITH REDUNDANCY FAILOVER
# =====================================================================
class GeminiParserService:
    def __init__(self):
        # Initialize the official google-genai Client using our config key
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.model_name = "gemini-2.5-flash"

    async def parse_unstructured_workout(self, raw_text: str) -> ExtractedWorkoutAnalysis:
        """
        Ingests messy natural text and returns a strict, type-safe ExtractedWorkoutAnalysis object.
        Features automatic failover redundancy if the primary model experiences traffic spikes (503).
        """
        
        system_prompt = (
            "You are an expert sports scientist and elite fitness performance analyst. "
            "Your task is to dissect a user's natural, messy, or abbreviated workout journal entries "
            "and extract them into a clean, normalized structural data layout.\n\n"
            "Rules:\n"
            "- Normalize colloquial exercise terms (e.g., 'bench', 'flat bench' -> 'Barbell Bench Press').\n"
            "- Map reps and weights sequentially per set. If the user says '3x10 at 135', generate 3 items in the reps array [10, 10, 10] and 3 items in the weight_lbs array [135, 135, 135].\n"
            "- Preserve any implicit workout intensities (RPE scores 1-10) if mentioned."
        )

        user_content = f"Analyze the following workout entry and extract the details:\n\n\"\"\"\n{raw_text}\n\"\"\""
        
        # Share the exact structural extraction configuration payload across both attempts
        config_payload = types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0.1,  # Low temperature forces deterministic precision over creativity
            response_mime_type="application/json",
            response_schema=ExtractedWorkoutAnalysis,
        )

        try:
            # ⚡ PRIMARY EFFORT: Dispatch payload to the fast gemini-2.5-flash engine
            print(f"📡 Dispatching payload to primary model: {self.model_name}...")
            response = await self.client.aio.models.generate_content(
                model=self.model_name,
                contents=user_content,
                config=config_payload
            )
            
            if not response.text:
                raise ValueError("Primary model returned an empty text string.")
                
            return ExtractedWorkoutAnalysis.model_validate_json(response.text)

        except Exception as primary_error:
            # 🔄 AUTOMATIC FALLBACK: If primary hits a rate limit or 503, switch to gemini-1.5-flash
            print(f"⚠️ Primary AI engine busy or unavailable ({primary_error}). Activating failover routing...")
            
            try:
                backup_model = "gemini-1.5-flash"
                print(f"🔄 Attempting extraction with resilient backup engine: {backup_model}...")
                
                response = await self.client.aio.models.generate_content(
                    model=backup_model,
                    contents=user_content,
                    config=config_payload
                )
                
                if not response.text:
                    raise ValueError("Backup model returned an empty text string.")
                    
                print(f"🟢 Failover successfully resolved via backup engine: {backup_model}!")
                return ExtractedWorkoutAnalysis.model_validate_json(response.text)
                
            except Exception as backup_error:
                # Both endpoints down or credentials invalid
                print(f"❌ Both primary and secondary AI compilation models exhausted: {backup_error}")
                raise RuntimeError(f"All available parsing vectors are temporarily constrained: {str(backup_error)}")