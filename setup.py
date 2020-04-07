#!/usr/bin/env python3
import glob
import io
import os
import subprocess

print("Make sure you have your Spotify + Genius API credentials available before you proceed. \n")

path = "application/resources"
filename = 'private_info.py'
full_filename = os.path.join(path, filename)
files = glob.glob(os.path.join(path, filename))
if full_filename not in files:
    with io.open(full_filename, 'w', encoding='utf-8') as f:
        f.write('spotify_username = "{}"\n'.format(input("Enter your full Spotify username/id: ")))
        f.write('spotify_client_id = "{}"\n'.format(input(
            "Your Spotify developer client_id, obtain it from (https://developer.spotify.com/dashboard/login): ")))
        f.write('spotify_secret = "{}"\n'.format(input("Your Spotify developer client_secret, obtain it from ("
                                                       "https://developer.spotify.com/dashboard/login): ")))
        f.write('spotify_redirect = "http://google.com/"\n')
        f.write('spotify_scope = "playlist-modify-public, user-read-playback-state, user-modify-playback-state"\n')
        f.write('genius_client_id = "{}"\n'.format(input("Please enter your Genius Client ID (""https://genius.com"
                                                         "/api-clients): ")))
        f.write('genius_client_secret = "{}"\n'.format(input("Please enter your Genius secret ("
                                                             "https://genius.com/api-clients): ")))
        f.write('genius_client_token = "{}"\n'.format(
            input("Please enter your Genius token (https://genius.com/api-clients): ")))
        f.write('genius_redirect_uri = "http://www.example.com/"\n')
        print("If you've entered these credentials correctly and included the client_secret.json from Google file in "
              "the {} directory, you should be able to run the application as expected.".format(path))
else:
    print("The file already exists on your system. To execute this setup file, you must first delete the '{}' file in "
          "the {} directory.".format(filename, path))

print("Please enter your password below to install the required dependencies.")
subprocess.call(f'sudo pip3 install -r application/resources/project-requirements.txt', shell=True)
