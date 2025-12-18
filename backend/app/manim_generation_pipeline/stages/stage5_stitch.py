import subprocess
import os
import glob


def stitch():
    # Find all scene videos in the media directory
    video_files = sorted(glob.glob("media/videos/animation/480p15/*.mp4", recursive=True))
    
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
