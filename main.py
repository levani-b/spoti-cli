from spotify_auth import authenticate
from spotify_api import get_current_track,play_track,pause_playback, resume_playback, skip_to_next, skip_to_previous, search_tracks
from terminal_ui import clear_screen, move_cursor, hide_cursor, show_cursor
import time


def main():
    clear_screen()
    # hide_cursor()

    # print("Line 1")
    # print("Line 2")
    # print("Line 3")

    # time.sleep(1)

    # # Go back and update line 2
    # move_cursor(2, 0)
    # print("Line 2 CHANGED!")

    # time.sleep(1)

    # # Update line 1
    # move_cursor(1, 0)
    # print("Line 1 CHANGED!")

    # time.sleep(2)
    # show_cursor()

if __name__ == "__main__":
    main()
