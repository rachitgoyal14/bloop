import os


def find_sadtaker_video(folder:str):
    for file in os.listdir(folder):
        if file.endswith(".mp4"):
            return os.path.join(folder,file)
        
    return None

