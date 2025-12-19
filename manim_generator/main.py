from fastapi import FastAPI
from manim_generator.stages.stage1_scenes import generate_scenes
from manim_generator.stages.stage2_manim import generate_manim
from manim_generator.stages.stage3_script import generate_script
from manim_generator.stages.stage4_tts import tts_generate
from manim_generator.stages.stage5_stitch import stitch, mux_audio
from pydantic import BaseModel

app = FastAPI()

class ExplainRequest(BaseModel):
    topic: str
    level: str = "school"
    persona: str = "teacher"

@app.post("/explain")
def explain(request: ExplainRequest):
    scenes = generate_scenes(request.topic, request.level)
    manim_data = generate_manim(scenes)
    script = generate_script(
        scenes,
        manim_data["timestamps"],
        request.persona,
        request.level
    )
    tts_generate(script)
    mux_audio()
    stitch()

    return {"status": "pipeline complete"}
