from pathlib import Path

def tts_generate(script):
    Path("outputs/audio").mkdir(exist_ok=True)

    for scene in script:
        scene_id = scene["scene_id"]
        text = scene["script"]

        # Replace with ElevenLabs / Azure / XTTS
        with open(f"outputs/audio/scene_{scene_id}.wav", "wb") as f:
            f.write(b"FAKE_AUDIO")  # placeholder
