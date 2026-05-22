from contextlib import asynccontextmanager
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from app.database import init_db
from app.routes.coach import router as coach_router
from app.routes.workouts import router as workout_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Initializing backend connection services...")
    try:
        await init_db()
        print("📥 MongoDB connection established and Beanie models initialized.")
    except Exception as e:
        print(f"❌ Critical Error during database initialization: {e}")
        raise e
    yield
    print("🛑 Shutting down backend connection services...")


app = FastAPI(
    title="AI Fitness Coaching Backend",
    version="1.0.0",
    description="Asynchronous FastAPI Gateway leveraging MongoDB & Gemini AI Orchestration.",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register the audited routing blueprints
app.include_router(coach_router)
app.include_router(workout_router)

@app.get("/")
async def root():
    return {"status": "online", "environment": settings.ENVIRONMENT}

@app.get("/health")
async def health_check():
    return JSONResponse(status_code=200, content={"status": "operational"})