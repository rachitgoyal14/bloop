from fastapi import FastAPI
from api.sad_talker_video import router as sad_talker_router
from api.qa import router as qa

app = FastAPI(title="Bloom")

app.include_router(sad_talker_router)
app.include_router(qa)

@app.get("/")
def health():
    return {
        "status": "ok"
    }


