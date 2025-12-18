import json
import subprocess
from pathlib import Path
from manim_generation_pipeline.utils.llm import call_llm
from manim_generation_pipeline.utils.json_safe import extract_json

def generate_manim(scenes):
    scenes_json = json.dumps(scenes)
    scenes_category = scenes['category']
    prompt_path = f"app/prompts/{scenes_category.lower()}_manim.txt"
    prompt = Path(prompt_path).read_text()
    prompt = prompt.format(scenes_json=scenes_json)

    output = call_llm(prompt)
    print("RAW LLM OUTPUT:\n", output)

    data = extract_json(output)  # ✅ SAFE

    Path("outputs/animation.py").write_text(data["manim_code"])
    Path("outputs/timestamps.json").write_text(
        json.dumps(data["timestamps"], indent=2)
    )

    subprocess.run(
        ["manim", "-pql", "outputs/animation.py"],
        check=True
    )

    return data
