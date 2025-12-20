from fastapi import FastAPI
from api.sad_talker_video import router as sad_talker_router
from api.qa import router as qa
from api.tts import router as tts_router
from api.flashcards import router as flashcards
from api.quiz import router as quiz
from api.play.teach_ai import router as teach_ai
from api.roadmap import router as roadmap_router
# from api.manim_generator import router as manim_generator
from api.play.find_mistake import router as find_mistake
from api.play.complete_missing_link import router as complete_missing_link
from api.manim_generator import router as manim_generator


app = FastAPI(title="Bloop!")

app.include_router(sad_talker_router)
app.include_router(qa)
app.include_router(tts_router)
app.include_router(flashcards)
app.include_router(quiz)
app.include_router(teach_ai)
app.include_router(roadmap_router)
# app.include_router(manim_generator)
app.include_router(find_mistake)
app.include_router(complete_missing_link)

app.include_router(manim_generator)

@app.get("/")
def health():
    return {
        "status": "ok"
    }


