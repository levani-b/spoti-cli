from spotify_api import search_tracks, play_track
from utils import ms_to_min_sec, truncate_text
from PIL import Image, ImageEnhance
import re


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
    'p': '[P]lay/Pause',
    'n': '[N]ext',
    'b': '[B]ack',
    's': '[S]earch',
    'q': '[Q]uit',
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


# def move_cursor(row, col):
#     print(f"\033[{row};{col}H", end='')


# def hide_cursor():
#     print(HIDE_CURSOR, end='')


# def show_cursor():
#     print(SHOW_CURSOR, end='')


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


def draw_album(img_path):
    try:
        img = Image.open(img_path).convert("RGB")
    except:
        return []  
    
    MAX_WIDTH = 30
    MAX_HEIGHT = 20
    
    original_width, original_height = img.size
    aspect_ratio = original_width / original_height
    
    if aspect_ratio > (MAX_WIDTH / MAX_HEIGHT):
        new_width = MAX_WIDTH
        new_height = int(new_width / aspect_ratio)
    else:
        new_height = MAX_HEIGHT
        new_width = int(new_height * aspect_ratio)
    
    resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    enhancer = ImageEnhance.Sharpness(resized_img)
    resized_img = enhancer.enhance(1.5)
    
    pixels = resized_img.load()
    width, height = resized_img.size
    
    lines = []
    for y in range(0, height, 2):
        row = ""
        for x in range(width):
            top_r, top_g, top_b = pixels[x, y]
            
            if y + 1 < height:
                bottom_r, bottom_g, bottom_b = pixels[x, y + 1]
            else:
                bottom_r, bottom_g, bottom_b = top_r, top_g, top_b
            
            row += f"\033[38;2;{top_r};{top_g};{top_b}m\033[48;2;{bottom_r};{bottom_g};{bottom_b}m▀"
        
        row += RESET
        lines.append(row)
    
    return lines


def print_full_ui(track_data, album_art_lines=None):
    width = 50
    ansi_re = re.compile(r'\x1b\[[0-9;]*m')
    
    print("╔" + "═" * width + "╗")
    print("║" + "spoti-cli".center(width) + "║")
    print("╠" + "═" * width + "╣")
    
    if album_art_lines:
        for line in album_art_lines:
            visible = ansi_re.sub('', line)
            visible_len = len(visible)
            if visible_len > width:
                visible_len = width
            left_pad = max((width - visible_len) // 2, 0)
            right_pad = max(width - visible_len - left_pad, 0)
            print("║" + (" " * left_pad) + line + (" " * right_pad) + "║")
        print("╠" + "═" * width + "╣")
    
    if track_data:
        is_playing = track_data.get('is_playing', False)
        name = truncate_text(track_data["item"]["name"], width - 4)
        artist = track_data["item"]["artists"][0]["name"]

        used_space = 4 + len(artist) + 3
        remaining_space = width - used_space
        album = truncate_text(track_data["item"]["album"]["name"], remaining_space)

        # progress_ms = track_data["progress_ms"]
        # duration_ms = track_data["item"]["duration_ms"]

        # curr_progress = ms_to_min_sec(progress_ms)
        # duration = ms_to_min_sec(duration_ms)
        # progress = progress_ms / duration_ms

        # bar_width = width - 20  
        # filled = int(bar_width * progress)
        # bar = "█" * filled + "░" * (bar_width - filled)
        
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
    menu_text = "  [P]lay/Pause [N]ext [B]ack [S]earch [Q]uit"
    print("║" + menu_text.ljust(width) + "║")
    
    print("╚" + "═" * width + "╝")
    
    print("\nEnter command: ", end='', flush=True)