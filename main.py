import sys
from spotify_auth import authenticate
from spotify_api import *
from ui import *
from utils import ensure_spotify_running
import time


def main():
    ensure_spotify_running()
    tokens = authenticate()
    if not tokens:
        sys.exit(1)
    access_token = tokens['access_token']

    print(CLEAR, end='')
    while True:
        print(CLEAR, end = "")

        current = get_current_track(access_token)
        print_full_ui(current, menu_options)


        command = get_user_input()
        if command == 'q':
            break
        elif command == 'p':
            toggle_playback(access_token)
        elif command == 'n':
            skip_to_next(access_token)
        elif command == 'b':
            skip_to_previous(access_token)
        elif command == 's':
            search_mode(access_token)
        time.sleep(0.2)


if __name__ == "__main__":
    main()
