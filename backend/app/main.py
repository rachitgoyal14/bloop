from fastapi import FastAPI
from api.sad_talker_video import router as sad_talker_router
from api.qa import router as qa
from api.tts import router as tts_router

app = FastAPI(title="Bloop!")

app.include_router(sad_talker_router)
app.include_router(qa)
app.include_router(tts_router)

@app.get("/")
def health():
    return {
        "status": "ok"
    }


