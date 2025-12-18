from fastapi import FastAPI
from manim_generation_pipeline.stages.stage1_scenes import generate_scenes
from manim_generation_pipeline.stages.stage2_manim import generate_manim
from manim_generation_pipeline.stages.stage3_script import generate_script
from manim_generation_pipeline.stages.stage4_tts import tts_generate
from manim_generation_pipeline.stages.stage5_stitch import stitch

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
    # tts_generate(script)
    # stitch()

    return {"status": "pipeline complete"}
