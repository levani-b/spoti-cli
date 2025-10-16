from spotify_auth import authenticate
from datetime import datetime

def main():
    tokens = authenticate()
    
    if not tokens:
        print("Failed to authenticate. Exiting.")
        return
    
    access_token = tokens['access_token']

if __name__ == "__main__":
    main()
