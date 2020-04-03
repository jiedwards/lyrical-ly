import os

import googleapiclient.discovery
import googleapiclient.errors
import spotipy
import spotipy.util as util
import youtube_dl
from oauth2client import client, tools
from oauth2client.file import Storage

from resources.private_info import spotify_client_id, spotify_secret, spotify_username, spotify_redirect, spotify_scope


def get_youtube_client():
    """ Log Into Youtube, Copied from Youtube Data API """
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    absolute_path = os.path.dirname(os.path.abspath(__file__))
    client_secrets_file = os.path.join(absolute_path, 'resources/client_secret.json')
    scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

    credential_path = os.path.join(absolute_path, 'resources/google_credentials.json')
    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(client_secrets_file, scopes)
        credentials = tools.run_flow(flow, store)
    return googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials)


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


spotify_object = spotipy.Spotify(auth=get_spotify_token())
youtube_playlist_name = "Youtube Videos"


class GenerateSpotifyPlaylist:

    def __init__(self):
        self.auth = get_spotify_token()
        self.youtube_client = get_youtube_client()
        self.playlist_id = self.generate_playlist()
        self.all_song_info = {}

    def generate_playlist(self):
        youtube_playlist_desciption = "A compilation of every video liked by me on youtube."
        all_user_playlists = spotify_object.current_user_playlists(50)

        # To check whether a playlist already exists, before creating an entirely new one.
        for playlist in all_user_playlists["items"]:
            if playlist["name"] == youtube_playlist_name:
                return playlist["id"]

        new_playlist = spotify_object.user_playlist_create(spotify_username, youtube_playlist_name, True,
                                                           youtube_playlist_desciption)
        return new_playlist["id"]

    def get_liked_yt_videos(self):
        request = self.youtube_client.videos().list(
            maxResults=10,
            part="snippet,contentDetails,statistics",
            myRating="like"
        )
        response = request.execute()

        for video in response["items"]:
            if video["snippet"]["categoryId"] == '10':
                video_title = video["snippet"]["title"]
                youtube_url = "https://www.youtube.com/watch?v={}".format(video["id"])

                video = youtube_dl.YoutubeDL({}).extract_info(youtube_url, download=False)
                song_name = video["track"]
                artist = video["artist"]

                if song_name is not None and artist is not None:
                    self.all_song_info[video_title] = {
                        "youtube_url": youtube_url,
                        "song_name": song_name,
                        "artist": artist,

                        "spotify_uri": self.get_spotify_uri(song_name, artist)

                    }
                else:
                    print("The song '{}' cannot be processed as the required information is not uploaded to Youtube."
                          .format(video_title))
            else:
                pass

    def get_spotify_uri(self, song_name, artist):
        # Functionality to search for song
        search_query = 'artist: {}, track: {}'.format(artist, song_name)
        all_songs_found = spotify_object.search(search_query, 20, 0, 'track')
        songs = all_songs_found["tracks"]["items"]
        uri = songs[0]["uri"]
        return uri

    def add_song_to_playlist(self):
        self.get_liked_yt_videos()

        uris = [info["spotify_uri"]
                for song, info in self.all_song_info.items()]
        # replace essentially adds/updates the playlist
        return spotify_object.user_playlist_replace_tracks(spotify_username, self.playlist_id, uris)

    def start_playback(self):
        devices = spotify_object.devices()
        device_id = devices['devices'][0]['id']
        device_name = devices['devices'][0]['name']
        uri = "spotify:playlist:{}".format(self.playlist_id)
        spotify_object.start_playback(device_id, uri)
        print()
        print(">>>>>>>>>>>> Successfully started playing: '{}' on '{}' <<<<<<<<<<<<".format(youtube_playlist_name,
                                                                                 device_name))


if __name__ == '__main__':
    generatePlaylist = GenerateSpotifyPlaylist()
    generatePlaylist.add_song_to_playlist()
    generatePlaylist.start_playback()
