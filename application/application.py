from generate_spotify_playlist import GenerateSpotifyPlaylist
import retrieve_genius_lyrics

if __name__ == '__main__':
    generatePlaylist = GenerateSpotifyPlaylist()
    generatePlaylist.add_song_to_playlist()
    generatePlaylist.start_playback()
    retrieve_genius_lyrics()