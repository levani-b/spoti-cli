from spotify_api import search_tracks, play_track

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

# menu options
menu_options = {
    'p': 'Play/Pause',
    'n': 'Next track',
    'b': 'Previous track',
    's': 'Search',
    'q': 'Quit',

}


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

def get_user_input():
    command = input("\nEnter command: ").lower().strip()
    return command[0] if command else ''

    
def search_mode(access_token):
    print(CLEAR)
    print(f"{CYAN}Search for a track:{RESET}")
    query = input("> ")
    
    tracks = search_tracks(access_token, query)
    
    if not tracks:
        print_colored("No tracks found", "yellow")
        return
    
    print(f"\n{GREEN}Results:{RESET}")
    displayed_tracks = tracks[:10]
    
    for i, track in enumerate(displayed_tracks, 1):
        name = track['name']
        artist = track['artists'][0]['name']
        album = track['album']['name']
        print(f"{i}. {name} - {artist} · {album}")

    while True:
        print(f"\n{YELLOW}Enter track number to play (or 0 to cancel):{RESET}")
        
        try:
            choice = int(input("> "))
            
            if choice == 0:
                return  
            
            if 1 <= choice <= len(displayed_tracks):
                selected = displayed_tracks[choice - 1]
                track_uri = selected['uri']
                play_track(access_token, track_uri)
                return 
            else:
                print_colored(f"Invalid! Enter 1-{len(displayed_tracks)} or 0 to cancel", "red")
              
        except ValueError:
            print_colored("Please enter a number!", "red")

def print_full_ui(track_data, menu_options):
    width = 40

    is_playing = track_data.get('is_playing', False)

    print("╔" + "═" * width + "╗")
    print("║" + "spoti-cli".center(width) + "║")
    print("╠" + "═" * width + "╣")

    if track_data:
        name = track_data["item"]["name"]
        artist = track_data["item"]["artists"][0]["name"]
        album = track_data["item"]["album"]["name"]
        
        print("║" + " " * width + "║")
        print("║" + "  Now Playing:".ljust(width) + "║")
        print("║" + f"  {'▶' if is_playing else '⏸'} {name}".ljust(width) + "║")
        print("║" + f"    {artist} · {album}".ljust(width) + "║")
        print("║" + " " * width + "║")

    else:
        print("║" + " " * width + "║")
        print("║" + "  No track playing".ljust(width) + "║")
        print("║" + " " * width + "║")
    
    print("╠" + "═" * width + "╣")

    for key, description in menu_options.items():
        text = f"  [{key.upper()}] {description}"
        print("║" + text.ljust(width) + "║")
    
    print("╚" + "═" * width + "╝")
