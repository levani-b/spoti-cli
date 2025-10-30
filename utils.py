import subprocess
import time
import requests
from io import BytesIO


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

def download_album_art(url):
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return BytesIO(response.content)
    except:
        return None


def truncate_text(text, max_len):
    return text[:max_len-3] + '...' if len(text) > max_len else text