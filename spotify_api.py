import requests
import os
from dotenv import load_dotenv


load_dotenv()

SPOTIFY_API_BASE = "https://api.spotify.com/v1"

def get_current_track(token):
    current_track_url = f'{SPOTIFY_API_BASE}/me/player/currently-playing'

    headers = {
        'Authorization':f'Bearer {token}',
         "Content-Type": "application/json" 
    }

    try:
        response = requests.get(current_track_url, headers=headers)
        response.raise_for_status()

        if response.status_code == 204 or not response.content:
            print("No track currently playing")
            return None
        
        return response.json()
        
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
    except requests.exceptions.RequestException as err:
        print(f"Other error occurred: {err}")
    

def play_track(access_token, track_uri):
    play_track_url = f"{SPOTIFY_API_BASE}/me/player/play"

    headers = {
    'Authorization':f'Bearer {access_token}',
        "Content-Type": "application/json" 
    }

    data_to_send = {
        "uris": [track_uri]
    }

    try:
        response = requests.put(play_track_url, headers=headers, json = data_to_send)
        response.raise_for_status()

        if response.status_code == 204:
            print("Track playing")
            return True

        return response.json()

    except requests.exceptions.HTTPError as err:
        if response.status_code == 404:
            print("No active device found. Open Spotify on any device.")
        elif response.status_code == 403:
            print("Forbidden: requires Premium and user-modify-playback-state scope")
        else:
            print(f"HTTP error occurred: {err}")
        return False
    except requests.exceptions.RequestException as err:
        print(f"Other error occurred: {err}")
        return False

def pause_playback(access_token):
    pause_url = f"{SPOTIFY_API_BASE}/me/player/pause"

    headers = {
        'Authorization':f'Bearer {access_token}',
        "Content-Type": "application/json" 
    }

    try:
        response = requests.put(pause_url, headers=headers)
        response.raise_for_status()

        if response.status_code == 204:
            print("Playback paused")
            return True

        if response.content and response.headers.get("Content-Type", "").startswith("application/json"):
            return response.json()
        return True
    except requests.exceptions.HTTPError as err:
        if response.status_code == 404:
            print("No active device found. Open Spotify on any device.")
        elif response.status_code == 403:
            print("Forbidden: requires Premium and user-modify-playback-state scope")
        else:
            print(f"HTTP error occurred: {err}")
        return False
    except requests.exceptions.RequestException as err:
        print(f"Other error occurred: {err}")
        return False

def resume_playback(access_token):
    resume_url = f"{SPOTIFY_API_BASE}/me/player/play"

    headers = {
        'Authorization': f'Bearer {access_token}',
        "Content-Type": "application/json"
    }

    try:
        response = requests.put(resume_url, headers=headers)
        response.raise_for_status()

        if response.status_code == 204:
            print("Playback resumed")
            return True

        if response.content and response.headers.get("Content-Type", "").startswith("application/json"):
            return response.json()
        return True
    
    except requests.exceptions.HTTPError as err:
        if response.status_code == 404:
            print("No active device found. Open Spotify on any device.")
        elif response.status_code == 403:
            print("Forbidden: requires Premium and user-modify-playback-state scope")
        else:
            print(f"HTTP error occurred: {err}")
        return False
    except requests.exceptions.RequestException as err:
        print(f"Other error occurred: {err}")
        return False

def skip_to_next(access_token):
    skipt_to_next_url = f"{SPOTIFY_API_BASE}/me/player/next"
    headers = {
        'Authorization': f'Bearer {access_token}',
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(skipt_to_next_url, headers=headers)
        response.raise_for_status()

        if response.status_code == 204:
            print("Playback resumed")
            return True

        if response.content and response.headers.get("Content-Type", "").startswith("application/json"):
            return response.json()
        return True
    
    except requests.exceptions.HTTPError as err:
        if response.status_code == 404:
            print("No active device found. Open Spotify on any device.")
        elif response.status_code == 403:
            print("Forbidden: requires Premium and user-modify-playback-state scope")
        else:
            print(f"HTTP error occurred: {err}")
        return False
    except requests.exceptions.RequestException as err:
        print(f"Other error occurred: {err}")
        return False

def skip_to_previous(access_token):
    skip_to_previous_url = f"{SPOTIFY_API_BASE}/me/player/previous"
    headers = {
        'Authorization': f'Bearer {access_token}',
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(skip_to_previous_url, headers=headers)
        response.raise_for_status()

        if response.status_code == 204:
            print("Playback resumed")
            return True

        if response.content and response.headers.get("Content-Type", "").startswith("application/json"):
            return response.json()
        return True
    
    except requests.exceptions.HTTPError as err:
        if response.status_code == 404:
            print("No active device found. Open Spotify on any device.")
        elif response.status_code == 403:
            print("Forbidden: requires Premium and user-modify-playback-state scope")
        else:
            print(f"HTTP error occurred: {err}")
        return False
    except requests.exceptions.RequestException as err:
        print(f"Other error occurred: {err}")
        return False

def search_tracks(access_token, query, limit=20):
    search_url = f"{SPOTIFY_API_BASE}/search"
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        "Content-Type": "application/json"
    }
    
    params = {
        'q': query,
        'type': 'track',
        'limit': limit
    }
    
    try:
        response = requests.get(search_url, headers=headers, params=params)
        response.raise_for_status()
        
        data = response.json()
        tracks = data.get('tracks', {}).get('items', [])
        if not tracks:
            print(f"No results found for '{query}'")
        return tracks

    except requests.exceptions.HTTPError as err:
        print(f"Search failed: {err}")
        return []
    except requests.exceptions.RequestException as err:
        print(f"Search error: {err}")
        return []