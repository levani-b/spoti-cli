import os
from dotenv import load_dotenv
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import requests
import base64

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