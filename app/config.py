import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    """
    Application Configuration Gateway.
    Loads and validates keys from the environment or a local .env file.
    """
    # Core API Keys and Targets
    GEMINI_API_KEY: str = Field(..., validation_alias="GEMINI_API_KEY")
    
    # Target our asynchronous MongoDB cluster configuration vector
    MONGODB_URL: str = Field(..., validation_alias="MONGODB_URL")
    
    # Deployment tracking environment state marker
    ENVIRONMENT: str = Field("development", validation_alias="ENVIRONMENT")

    # Tell Pydantic how to handle file loading mechanics
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore" # Safely bypass external tracking keys present in environment
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Guard Check: Ensure we don't accidentally try to pass a SQL engine string to MongoDB
        if "postgresql://" in self.MONGODB_URL or "postgres://" in self.MONGODB_URL:
            print("\n❌ CRITICAL STRUCTURAL ERROR: MONGODB_URL contains a PostgreSQL connection schema prefix!")
            print(f"Current Value: {self.MONGODB_URL}")
            print("Please modify your .env file to point to a valid 'mongodb://' or 'mongodb+srv://' target connection vector.\n")
            raise ValueError("Invalid database wire protocol configured.")


# Instantiate a single cached configuration object for the runtime footprint
settings = Settings()