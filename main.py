import sys
import select
from spotify_auth import authenticate
from spotify_api import *
from ui import *
from utils import ensure_spotify_running, download_album_art
import time

def main():
    ensure_spotify_running()
    tokens = authenticate()
    if not tokens:
        sys.exit(1)
    
    access_token = tokens['access_token']
    print(CLEAR, end='')
    
    last_track_id = None
    
    while True:
        current = get_current_track(access_token)
        current_track_id = current['item']['id'] if current and current.get('item') else None
        
        if current_track_id != last_track_id:
            print(CLEAR, end="")
            
            album_art_lines = None
            if current and current.get('item'):
                try:
                    album_images = current["item"]["album"]["images"]
                    if album_images:
                        album_url = album_images[0]["url"]
                        img_data = download_album_art(album_url)
                        if img_data:
                            album_art_lines = draw_album(img_data)
                except:
                    pass
            
            print_full_ui(current, menu_options, album_art_lines)
            last_track_id = current_track_id
        
        if select.select([sys.stdin], [], [], 2)[0]:
            command = sys.stdin.readline().strip().lower()
            if command:
                cmd = command[0]
                
                if cmd == 'q':
                    break
                elif cmd == 'p':
                    toggle_playback(access_token)
                    last_track_id = None 
                elif cmd == 'n':
                    skip_to_next(access_token)
                    last_track_id = None
                elif cmd == 'b':
                    skip_to_previous(access_token)
                    last_track_id = None
                elif cmd == 's':
                    search_mode(access_token)
                    last_track_id = None


if __name__ == "__main__":
    main()