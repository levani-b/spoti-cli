from spotify_auth import authenticate
from spotify_api import get_current_track,play_track,pause_playback, resume_playback, skip_to_next, skip_to_previous, search_tracks


def main():
    tokens = authenticate()
    access_token = tokens['access_token']

    # track = get_current_track(tokens['access_token'])
    
    # print(track)
    # play_track(tokens['access_token'], "spotify:track:4iV5W9uYEdYUVa79Axb7Rh")

    # pause_playback(access_token)
    # resume_playback(access_token)
    # skip_to_next(access_token)
    # skip_to_previous(access_token)
    tracks = search_tracks(access_token, 'the beatles')
    print(tracks)

if __name__ == "__main__":
    main()
