from generate_spotify_playlist import GenerateSpotifyPlaylist
from retrieve_genius_lyrics import RetrieveSongLyrics

if __name__ == '__main__':
    generatePlaylist = GenerateSpotifyPlaylist()
    generatePlaylist.add_song_to_playlist()
    generatePlaylist.start_playback()
    RetrieveSongLyrics()