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

        artist = playback['item']['artists'][0]['name']
        song_title = playback['item']['name']
        self.request_song_info(song_title, artist)
        return artist, song_title

    # Method to request the song information from Genius' API
    def request_song_info(self, song_title, artist):
        search_url = 'https://api.genius.com/search'
        request_headers = {'Authorization': 'Bearer ' + genius_client_token}
        data = {'q': song_title + ' ' + artist}
        response = requests.get(search_url, data=data, headers=request_headers)
        json = response.json()
        for match in json['response']['hits']:
            if artist.lower() in match['result']['primary_artist']['name'].lower():
                remote_song_info = match
                break
        try:
            return self.extract_lyrics(remote_song_info)
        except UnboundLocalError:
            print("Song not found on genius")
            sys.exit()


if __name__ == '__main__':
    RetrieveSongLyrics()
