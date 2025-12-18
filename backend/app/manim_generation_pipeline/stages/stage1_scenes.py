import json
from manim_generation_pipeline.utils.llm import call_llm
from pathlib import Path

def generate_scenes(topic: str, level: str):
    prompt = Path("app/prompts/scene_planner.txt").read_text()
    prompt = prompt.format(topic=topic, level=level)

    output = call_llm(prompt)
    scenes = json.loads(output)

    Path("outputs/scenes.json").write_text(json.dumps(scenes, indent=2))
    return scenes
