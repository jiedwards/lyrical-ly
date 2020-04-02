import json
import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import requests
import spotipy
import spotipy.util as util
import youtube_dl

from resources.private_info import spotify_client_id, spotify_secret, spotify_username, spotify_redirect, spotify_scope


def get_youtube_client():
    """ Log Into Youtube, Copied from Youtube Data API """
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "resources/client_secret.json"

    # Get credentials and create an API client
    scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_console()

    # from the Youtube DATA API
    youtube_client = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    return youtube_client


def get_spotify_token():
    try:
        token = util.prompt_for_user_token(spotify_username, client_id=spotify_client_id,
                                           client_secret=spotify_secret,
                                           redirect_uri=spotify_redirect, scope=spotify_scope)
    except:
        os.remove(f".cache-{spotify_username}")
        token = util.prompt_for_user_token(spotify_username, client_id=spotify_client_id,
                                           client_secret=spotify_secret,
                                           redirect_uri=spotify_redirect, scope=spotify_scope)
    return token


spotify_token = get_spotify_token()
spotifyObject = spotipy.Spotify(auth=spotify_token)


class GenerateSpotifyPlaylist:

    def __init__(self):
        self.auth = get_spotify_token()
        self.youtube_client = get_youtube_client()
        self.playlist_id = self.generate_playlist()
        self.all_song_info = {}

    def generate_playlist(self):
        youtube_playlist_name = "Youtube Videos"
        youtube_playlist_desciption = "A compilation of every video liked by me on youtube."
        all_user_playlists = spotifyObject.current_user_playlists(50)

        for playlist in all_user_playlists["items"]:
            if playlist["name"] == youtube_playlist_name:
                return playlist["id"]

        new_playlist = spotifyObject.user_playlist_create(spotify_username, youtube_playlist_name, True,
                                                      youtube_playlist_desciption)
        return new_playlist["id"]


if __name__ == '__main__':
    generatePlaylist = GenerateSpotifyPlaylist()
    generatePlaylist.generate_playlist()

