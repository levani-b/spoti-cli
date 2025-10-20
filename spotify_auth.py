import os
from dotenv import load_dotenv
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlencode, urlparse, parse_qs
import requests
import base64
import json
from datetime import datetime

load_dotenv()

SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
TOKEN_EXPIRY_BUFFER = 60 

def _get_auth_headers():
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    credentials = f"{client_id}:{client_secret}"
    encoded = base64.b64encode(credentials.encode()).decode()
    return {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {encoded}"
    }


def generate_auth_url():
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI")
    scopes = [
    "user-read-playback-state",
    "user-modify-playback-state",
    "user-read-currently-playing",
    "playlist-read-private",
    "playlist-read-collaborative",
    "user-library-read",
]

    params = {
        "client_id": client_id,
        "response_type": "code",
        "redirect_uri": redirect_uri,
        "scope": " ".join(scopes),
    }

    return f"{SPOTIFY_AUTH_URL}?{urlencode(params)}"



def start_callback_server():
    class CallbackHandler(BaseHTTPRequestHandler):
        auth_code = None
        
        def do_GET(self):
            parsed_url = urlparse(self.path)
            query_params = parse_qs(parsed_url.query)
            CallbackHandler.auth_code = query_params.get('code', [''])[0]
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"Success! You can close this window.")
        
        def log_message(self, format, *args):
            pass
    
    port = int(os.getenv("SPOTIFY_AUTH_PORT", "8888"))
    server = HTTPServer(('127.0.0.1', port), CallbackHandler)
    server.handle_request()
    return CallbackHandler.auth_code
    

def exchange_code_for_token(code):
    redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI")
    
    headers = _get_auth_headers()
    body = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': redirect_uri
    }
    
    response = requests.post(SPOTIFY_TOKEN_URL, data=body, headers=headers)
    response.raise_for_status()
    return response.json()


def save_tokens(tokens):
    now_ts = int(datetime.now().timestamp())
    expires_in = tokens.get('expires_in')
    expires_at = None
    
    if isinstance(expires_in, (int, float)):
        expires_at = now_ts + int(expires_in) - TOKEN_EXPIRY_BUFFER
    
    token_data = {
        'access_token': tokens.get('access_token'),
        'refresh_token': tokens.get('refresh_token'),
        'token_type': tokens.get('token_type'),
        'scope': tokens.get('scope')
    }
    
    if expires_in is not None:
        token_data['expires_in'] = int(expires_in)
    if expires_at is not None:
        token_data['expires_at'] = expires_at
    
    with open('tokens.json', 'w') as f:
        json.dump(token_data, f, indent=4)
    
    print("Tokens saved successfully")


def load_tokens():
    try:
        with open('tokens.json', 'r') as f:
            token_data = json.load(f)
            if not isinstance(token_data, dict):
                return None
            return token_data
    except FileNotFoundError:
        print("No saved tokens found. Please authenticate.")
        return None
    except json.JSONDecodeError:
        print("Token file corrupted. Please re-authenticate.")
        return None


def is_token_expired(tokens):
    if not tokens or 'expires_at' not in tokens:
        return True
    now = int(datetime.now().timestamp())
    return now >= tokens['expires_at']


def refresh_access_token(refresh_token):
    headers = _get_auth_headers()
    body = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token
    }
    
    response = requests.post(SPOTIFY_TOKEN_URL, data=body, headers=headers)
    response.raise_for_status()
    
    token_data = response.json()
    
    if 'refresh_token' not in token_data or not token_data.get('refresh_token'):
        token_data['refresh_token'] = refresh_token
    
    save_tokens(token_data)
    return token_data


def authenticate():
    tokens = load_tokens()

    if tokens:
        if not is_token_expired(tokens):
            return tokens
        else:
            print("Token expired, refreshing...")
            try:
                return refresh_access_token(tokens['refresh_token'])
            except Exception as e:
                print(f"Failed to refresh token: {e}")
                print("Re-authenticating...")
    
    print("\nOpening browser for authentication...")
    url = generate_auth_url()
    print(f"Go to: {url}\n")
    
    code = start_callback_server()
    
    if not code:
        print("Authentication failed - no code received")
        return None
    
    try:
        tokens = exchange_code_for_token(code)
        save_tokens(tokens)
        print("Authentication successful!")
        return tokens
    except Exception as e:
        print(f"Authentication failed: {e}")
        return None
