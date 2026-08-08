from fastapi import FastAPI
from api.sad_talker_video import router as sad_talker_router

from api.qa import router as qa
from api.tts import router as tts_router
from api.flashcards import router as flashcards
from api.quiz import router as quiz
from api.play.teach_ai import router as teach_ai
from api.roadmap import router as roadmap_router
from api.play.find_mistake import router as find_mistake
from api.play.complete_missing_link import router as complete_missing_link
from api.manim_generator import router as manim_generator
from api.chat_history import router as chat_history_router
from core.database import engine, Base
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

app = FastAPI(title="Bloop!")

# Test database connection and create tables
@app.on_event("startup")
async def startup_event():
    try:
        # Test connection
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("✅ Database connection successful!")
            
        # Create tables
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created/verified!")
        
        # Verify tables exist
        with engine.connect() as connection:
            tables = ['chats', 'messages', 'documents', 'videos', 'roadmaps']
            for table in tables:
                try:
                    result = connection.execute(text(f"SELECT COUNT(*) FROM {table}"))
                    count = result.fetchone()[0]
                    print(f"✅ Table '{table}' verified - Row count: {count}")
                except Exception as e:
                    print(f"⚠️  Table '{table}' check failed: {e}")
                    
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        print("⚠️  Application will continue but database features may not work!")

app.include_router(sad_talker_router)
app.include_router(qa)
app.include_router(tts_router)
app.include_router(flashcards)
app.include_router(quiz)
app.include_router(teach_ai)
app.include_router(roadmap_router)
app.include_router(find_mistake)
app.include_router(complete_missing_link)
app.include_router(manim_generator)
app.include_router(chat_history_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow frontend origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def health():
    return {
        "status": "ok"
    }