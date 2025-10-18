# ANSI escape codes
CLEAR = "\033[2J\033[H"

# Colors
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
WHITE = "\033[97m"
RESET = "\033[0m"

# Text styles
BOLD = "\033[1m"
DIM = "\033[2m"
UNDERLINE = "\033[4m"

# Cursor control
HIDE_CURSOR = "\033[?25l"
SHOW_CURSOR = "\033[?25h"

def clear_screen():
    print(CLEAR, end='')

def print_colored(text, color):
    colors = {
        'red': RED,
        'green': GREEN,
        'yellow': YELLOW,
        'blue': BLUE,
        'magenta': MAGENTA,
        'cyan': CYAN,
        'white': WHITE
    }
    
    color_code = colors.get(color.lower(), WHITE)
    print(f"{color_code}{text}{RESET}")
   

def print_styled(text, style):
    styles = {
        'bold': BOLD,
        'underline': UNDERLINE,
        'dim': DIM
    }
    
    style_code = styles.get(style.lower(), '')
    print(f'{style_code}{text}{RESET}')


def move_cursor(row, col):
    print(f"\033[{row};{col}H", end='')


def hide_cursor():
    print(HIDE_CURSOR, end='')


def show_cursor():
    print(SHOW_CURSOR, end='')


def print_track_info(track_data):
    album_name = track_data["item"]["album"]["name"]
    track_name = track_data["item"]["name"]
    artist_name = track_data["item"]["artists"][0]["name"]

    print('\nNow Playing:')
    print(f"> {track_name}")
    print(f'{artist_name} -> {album_name}')


def print_menu(options):
    print("\n" + "─" * 40)
    for key, description in options.items():
        print(f"[{key.upper()}] {description}")
    print("─" * 40)