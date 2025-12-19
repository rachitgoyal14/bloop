from fastapi import FastAPI
from stages.stage1_scenes import generate_scenes
from stages.stage2_manim import generate_manim
from stages.stage3_script import generate_script
from stages.stage4_tts import tts_generate
from stages.stage5_stitch import stitch, mux_audio

app = FastAPI()

@app.post("/explain")
def explain(topic: str, level: str = "school", persona: str = "teacher"):
    scenes = generate_scenes(topic, level)
    manim_data = generate_manim(scenes)
    script = generate_script(
        scenes,
        manim_data["timestamps"],
        persona,
        level
    )
    tts_generate(script)
    mux_audio()
    stitch()

    return {"status": "pipeline complete"}
