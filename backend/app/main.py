from fastapi import FastAPI
from api.sad_talker_video import router as sad_talker_router

app = FastAPI(title="Bloom")

app.include_router(sad_talker_router)

@app.get("/")
def health():
    return {
        "status": "ok"
    }
