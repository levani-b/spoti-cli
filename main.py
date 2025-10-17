from spotify_auth import authenticate
from spotify_api import get_current_track,play_track


def main():
    tokens = authenticate()
    access_token = tokens['access_token']

    track = get_current_track(tokens['access_token'])
    
    print(track)
    play_track(tokens['access_token'], "spotify:track:4iV5W9uYEdYUVa79Axb7Rh")

if __name__ == "__main__":
    main()
