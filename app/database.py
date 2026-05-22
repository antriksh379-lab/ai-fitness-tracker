from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.config import settings
from app.models import User, WorkoutLog, ChatSession

async def init_db():
    """
    Initializes the MongoDB connection pool and couples it with Beanie ODM.
    Called inside FastAPI's lifespan initialization event.
    """
    # 1. Create the asynchronous connection pool instance
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    
    try:
        # 2. Extract database name from the connection string path
        db_name = client.get_default_database().name
    except Exception:
        # Fallback if connection string doesn't explicitly name a database route string
        db_name = "ai_fitness"
    
    # 3. Register your Beanie Documents directly to the pool instance
    await init_beanie(
        database=client[db_name],
        document_models=[
            User,
            WorkoutLog,
            ChatSession
        ]
    )