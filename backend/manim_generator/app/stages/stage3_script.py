import json
from utils.llm import call_llm
from pathlib import Path

def generate_script(scenes, timestamps, persona, level):
    prompt = Path("app/prompts/script_writer.txt").read_text()
    prompt = prompt.format(
        scenes=json.dumps(scenes),
        timestamps=json.dumps(timestamps),
        persona=persona,
        level=level
    )

    output = call_llm(prompt)
    script = json.loads(output)

    Path("outputs/script.json").write_text(json.dumps(script, indent=2))
    return script
