import os
from dotenv import load_dotenv
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import requests
import base64
import json
from datetime import datetime, timedelta


def generate_auth_url():
    load_dotenv()

    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI")

    scope = (
    "user-read-playback-state "
    "user-modify-playback-state "
    "user-read-currently-playing "
    "playlist-read-private "
    "playlist-read-collaborative "
    "user-library-read"
    )

    auth_url = (
        f"https://accounts.spotify.com/authorize?"
        f"client_id={client_id}&"
        f"response_type=code&"
        f"redirect_uri={redirect_uri}&"
        f"scope={scope}"
    )

    return auth_url


def start_callback_server():
    class CallBackHandler(BaseHTTPRequestHandler):
        auth_code = None

        def do_GET(self):
            parsed_url = urlparse(self.path)
            query_string = parsed_url.query
            query_parameters = parse_qs(query_string)

            CallBackHandler.auth_code = query_parameters.get('code', [''])[0]

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"Success! You can close this window.")

    port = os.getenv("SPOTIFY_AUTH_PORT")
    server = HTTPServer(('127.0.0.1', 8888),CallBackHandler)
    server.handle_request()
    return CallBackHandler.auth_code
    


def exchange_code_for_token(code):
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI")
    
    url = "https://accounts.spotify.com/api/token"

    credentials = f"{client_id}:{client_secret}"
    b64_credentials = base64.b64encode(credentials.encode()).decode()
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {b64_credentials}"
    }

    body = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': redirect_uri
    }

    response = requests.post(url, data=body, headers=headers)
    response.raise_for_status()
    return response.json()

def save_tokens(tokens):
    now_ts = int(datetime.now().timestamp())
    expires_in = tokens.get('expires_in')
    expires_at = None
    if isinstance(expires_in, (int, float)):
        expires_at = now_ts + int(expires_in) - 60

    data = {
        'access_token': tokens.get('access_token'),
        'refresh_token': tokens.get('refresh_token'),
        'token_type': tokens.get('token_type'),
        'scope': tokens.get('scope')
    }
    if expires_in is not None:
        data['expires_in'] = int(expires_in)
    if expires_at is not None:
        data['expires_at'] = expires_at

    with open('tokens.json', 'w') as file:
        json.dump(data, file, indent=4)
        print("Created tokens.json successfully")
    

def load_tokens():
    try:
        with open('tokens.json', 'r') as file:
            data = json.load(file)
            if not isinstance(data, dict):
                return None
            return data
    except FileNotFoundError:
        return None
    except json.JSONDecodeError:
        return None

def refresh_access_token(refresh_token):
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")

    url = "https://accounts.spotify.com/api/token"
    credentials = f"{client_id}:{client_secret}"
    b64_credentials = base64.b64encode(credentials.encode()).decode()
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {b64_credentials}"
    }
    body = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token
    }

    response = requests.post(url, data=body, headers=headers)
    response.raise_for_status()
    data = response.json()

    if 'refresh_token' not in data or not data.get('refresh_token'):
        data['refresh_token'] = refresh_token

    save_tokens(data)
    return data
