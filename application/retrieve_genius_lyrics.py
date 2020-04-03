import sys

import requests
from bs4 import BeautifulSoup

from generate_spotify_playlist import spotify_object
from resources.private_info import genius_client_token


# Method to obtain user information from spotify for welcome message
def get_user_information():
    try:
        user = spotify_object.current_user()
        display_name = user['display_name']
        print()
        print("Welcome to Genius Lyrics, " + display_name + "!")
        print()
    except:
        raise NameError("User name not found.")
    return user


class RetrieveSongLyrics:

    def __init__(self):
        self.user = get_user_information()
        self.playback_information = self.get_playback_information()

    # Method to obtain current spotify playback information
    def get_playback_information(self):
        playback = spotify_object.currently_playing()
        if playback is None:
            raise TypeError("There is nothing currently playing. You have to play a song for this script to run.")
            sys.exit()

        artist_name = playback['item']['artists'][0]['name']
        song_title = playback['item']['name']
        return artist_name, song_title


if __name__ == '__main__':
    RetrieveSongLyrics()
