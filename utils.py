import subprocess
import time


def ensure_spotify_running():
    try:
        subprocess.check_output(['pgrep', '-f', 'spotify'])
        print("Spotify is already running.")
    except subprocess.CalledProcessError:
        print("Spotify not running, starting it...")
        subprocess.Popen(['spotify'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(5)

def ms_to_min_sec(ms):
    minutes = ms // 60000
    seconds = (ms % 60000) // 1000
    return f"{minutes}:{seconds:02}"
