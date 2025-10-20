import requests
from dotenv import load_dotenv

load_dotenv()

SPOTIFY_API_BASE = "https://api.spotify.com/v1"

def _make_spotify_request(method, endpoint, access_token, data=None, params=None):
    url = f"{SPOTIFY_API_BASE}{endpoint}"
    headers = {
        'Authorization': f'Bearer {access_token}',
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.request(method, url, headers=headers, json=data, params=params)
        response.raise_for_status()
        
        if response.status_code == 204:
            return True, None
        
        if response.content and response.headers.get("Content-Type", "").startswith("application/json"):
            return True, response.json()
        
        return True, None
        
    except requests.exceptions.HTTPError as err:
        if response.status_code == 404:
            print("No active device found. Open Spotify on any device.")
        elif response.status_code == 403:
            print("Forbidden: requires Premium and user-modify-playback-state scope")
        else:
            print(f"HTTP error occurred: {err}")
        return False, None
    except requests.exceptions.RequestException as err:
        print(f"Other error occurred: {err}")
        return False, None

def get_current_track(token):
    success, data = _make_spotify_request('GET', '/me/player/currently-playing', token)
    
    if not success:
        return None
    
    if data is None: 
        return None
    
    return data
    

def play_track(access_token, track_uri):
    data_to_send = {"uris": [track_uri]}
    success, data = _make_spotify_request('PUT', '/me/player/play', access_token, data_to_send)
    
    if success and data is None:
        print("Track playing")
        return True
    
    return success

def pause_playback(access_token):
    success, data = _make_spotify_request('PUT', '/me/player/pause', access_token)
    
    if success and data is None:
        print("Playback paused")
        return True
    
    return success

def resume_playback(access_token):
    success, data = _make_spotify_request('PUT', '/me/player/play', access_token)
    
    if success and data is None: 
        print("Playback resumed")
        return True
    
    return success

def skip_to_next(access_token):
    success, data = _make_spotify_request('POST', '/me/player/next', access_token)
    
    if success and data is None:  
        print("Skipped to next track")
        return True
    
    return success

def skip_to_previous(access_token):
    success, data = _make_spotify_request('POST', '/me/player/previous', access_token)
    
    if success and data is None: 
        print("Skipped to previous track")
        return True
    
    return success

def search_tracks(access_token, query, limit=20):
    params = {
        'q': query,
        'type': 'track',
        'limit': limit
    }
    
    success, data = _make_spotify_request('GET', '/search', access_token, params=params)
    
    if not success:
        return []
    
    tracks = data.get('tracks', {}).get('items', []) if data else []
    if not tracks:
        print(f"No results found for '{query}'")
    
    return tracks

def toggle_playback(access_token):
    track = get_current_track(access_token)
    
    if not track:
        print("Nothing is playing")
        return
    
    is_playing = track.get('is_playing', False)
    
    if is_playing:
        pause_playback(access_token)
    else:
        resume_playback(access_token)