import json
import subprocess
from pathlib import Path
from utils.llm import call_llm
from utils.json_safe import extract_json
from utils.timestamps_extractor import extract_timestamps
import re

def normalize_video_names(scene_ids):
    video_dir = Path("media/videos/animation/480p15")
    videos = sorted(video_dir.glob("*.mp4"))

    if len(videos) != len(scene_ids):
        raise ValueError(
            f"Scene count mismatch: {len(scene_ids)} scenes, {len(videos)} videos"
        )

    for scene_id, video in zip(scene_ids, videos):
        target = video_dir / f"{scene_id}.mp4"
        print(f"🔁 Renaming {video.name} → {target.name}")
        video.rename(target)



def generate_manim(scenes):
    scenes_json = json.dumps(scenes)
    scenes_category = scenes["category"]

    prompt_path = f"app/prompts/{scenes_category.lower()}_manim.txt"
    prompt = Path(prompt_path).read_text()
    prompt = prompt.format(scenes_json=scenes_json)

    output = call_llm(prompt)
    print("RAW LLM OUTPUT:\n", output)

    data = extract_json(output)
    manim_code = data["manim_code"]

    Path("outputs/animation.py").write_text(manim_code)

    # 🔹 Stage 2.5 — timestamps (independent of video naming)
    timestamps = extract_timestamps(manim_code)
    Path("outputs/timestamps.json").write_text(
        json.dumps(timestamps, indent=2)
    )

    # 🔹 SOURCE OF TRUTH: input scenes order
    scene_ids = [f"scene_{i+1}" for i in range(len(scenes["scenes"]))]

    # 🔹 Clean old renders
    clean_manim_output()

    # 🔹 Render
    subprocess.run(
        ["manim", "-pql", "outputs/animation.py"],
        check=True
    )

    # 🔹 Normalize filenames by order
    normalize_video_names(scene_ids)

    return {
        "manim_code": manim_code,
        "timestamps": timestamps,
        "scene_ids": scene_ids
    }

def clean_manim_output():
    video_dir = Path("media/videos/animation/480p15")
    video_dir.mkdir(parents=True, exist_ok=True)

    for f in video_dir.glob("*.mp4"):
        f.unlink()
