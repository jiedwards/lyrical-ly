import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import spotipy.util as util

from private_info import spotify_client_id, spotify_secret, spotify_username


def get_youtube_client():
    """ Log Into Youtube, Copied from Youtube Data API """
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_secret.json"

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
                                           redirect_uri="http://google.com/", scope='playlist-modify-public')
    except:
        os.remove(f".cache-{spotify_username}")
        token = util.prompt_for_user_token(spotify_username, client_id=spotify_client_id,
                                           client_secret=spotify_secret,
                                           redirect_uri="http://google.com/", scope='playlist-modify-public')
    return token


class GenerateSpotifyPlaylist:

    def __init__(self):
        self.auth = get_spotify_token()
        self.youtube_client = get_youtube_client()


if __name__ == '__main__':
    GenerateSpotifyPlaylist()
