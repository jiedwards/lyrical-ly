# Youtube/Spotify Playlist and Genius Lyrics Generator

This project allows a user to extract all of their liked youtube music videos via the Google Cloud API, whilst simultaneously creating a spotify playlist containing those songs using the Spotify API. 
The application also has the ability to locate the lyrics using the Genius API and display them on the terminal. 

### Prerequisites

```
* Python
* Pip
* Developer API credentials (Spotify, Google, Genius)
* A premium Spotify account (I think)
* A Youtube account with liked music videos
```

## Getting Started

Before you execute this step, ensure that you have all the required developer credentials as mentioned in the prerequisites.

Begin by running the following script to install dependencies and insert necessary credentials:
```
python3 setup.py
```
Proceed to insert/replace the required information in the client_secret.json (application/resources directory) file, the template is available. 
Obtain your credentials by following this guide (https://developers.google.com/adwords/api/docs/guides/authentication) and selecting "other" for application type.

To run all of the scripts simultaneously: 
```
python3 application.py
```
Or if you prefer to execute them separately, feel free to run:
```
python3 generate_spotify_playlist.py
```
to extract all the liked youtube videos, and create a playlist.

Then 
```
python3 retrieve_genius_lyrics.py
```
to retrieve the lyrics for the song which is currently playing. 

## Demonstration

![Demonstration of the application](application/resources/demo.gif)

## Built With

* [Youtube Data API](https://developers.google.com/youtube/v3) - The API used to extract song information from Youtube 
* [Spotify API](https://developer.spotify.com/) - The API used to create playlists and find/play songs. 
* [Spotipy library](https://spotipy.readthedocs.io/en/2.9.0/#) - The library used to mostly interface with the Spotify API
* [Google Cloud API](https://console.developers.google.com/) - The API used to extract user information from Youtube. 
* [Genius API](https://docs.genius.com/) - The API used to retrieve song lyrics.

## Acknowledgments

* Inspiration: https://www.youtube.com/watch?v=7J_qcttfnJA
