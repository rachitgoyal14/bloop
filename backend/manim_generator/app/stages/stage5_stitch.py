import subprocess
import os
import glob


def get_duration(path):
    result = subprocess.run(
        [
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            path
        ],
        stdout=subprocess.PIPE,
        text=True,
        check=True
    )
    return float(result.stdout.strip())


def build_atempo_chain(factor):
    filters = []
    f = factor

    while f > 2.0:
        filters.append("atempo=2.0")
        f /= 2.0

    while f < 0.5:
        filters.append("atempo=0.5")
        f /= 0.5

    filters.append(f"atempo={f}")
    return ",".join(filters)


def mux_audio():
    os.makedirs("outputs/scenes_with_audio", exist_ok=True)

    video_files = sorted(glob.glob("media/videos/animation/480p15/*.mp4"))

    for video in video_files:
        scene_id = os.path.splitext(os.path.basename(video))[0]
        audio = f"outputs/audio/{scene_id}.wav"
        out = f"outputs/scenes_with_audio/{scene_id}.mp4"

        if not os.path.exists(audio):
            raise FileNotFoundError(f"Missing audio for {scene_id}")

        video_dur = get_duration(video)
        audio_dur = get_duration(audio)

        # Audio speed factor
        factor = audio_dur / video_dur
        atempo_filter = build_atempo_chain(factor)

        print(f"🎬 {scene_id}: video={video_dur:.2f}s audio={audio_dur:.2f}s factor={factor:.3f}")

        subprocess.run([
            "ffmpeg", "-y",
            "-i", video,
            "-i", audio,
            "-filter_complex", f"[1:a]{atempo_filter}[a]",
            "-map", "0:v",
            "-map", "[a]",
            "-c:v", "copy",
            "-c:a", "aac",
            "-shortest",
            out
        ], check=True)



def stitch():
    # Find all scene videos in the media directory
    video_files = sorted(
    glob.glob("outputs/scenes_with_audio/*.mp4")
    )

    
    if not video_files:
        print("No video files found!")
        return
    
    print(f"Found {len(video_files)} videos to stitch")
    for i, v in enumerate(video_files, 1):
        print(f"  {i}. {v}")
    
    # Create a temporary file list for FFmpeg concat
    with open("concat_list.txt", "w") as f:
        for video in video_files:
            # FFmpeg concat requires absolute paths or paths relative to the list file
            f.write(f"file '{os.path.abspath(video)}'\n")
    
    # Concatenate videos using FFmpeg
    subprocess.run([
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", "concat_list.txt",
        "-c", "copy",  # Copy streams without re-encoding (faster)
        "outputs/final.mp4"
    ], check=True)
    
    # Clean up temporary file
    os.remove("concat_list.txt")
    
    print("✅ Videos stitched successfully: outputs/final.mp4")


stitch()
