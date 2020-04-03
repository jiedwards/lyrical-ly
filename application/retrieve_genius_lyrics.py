from generate_spotify_playlist import spotify_object


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


if __name__ == '__main__':
    RetrieveSongLyrics()
