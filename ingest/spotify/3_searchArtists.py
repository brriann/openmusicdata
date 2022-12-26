import config
import psycopg2
import csv
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# INITIALIZE
ARTISTS_FILE_NAME = '2022_12_25_seed_artists_todo.csv'

# postgres / psycopg2
conn = psycopg2.connect(
    dbname=config.dbName,
    user=config.dbUser,
    password=config.dbPassword,
    host="localhost",
    port=5432
    )

# spotipy
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=config.spotifyClientId,
                                                            client_secret=config.spotifyClientSecret))

cur = conn.cursor()

#import list of artist names


#for each artist
#   spotify search by name
#   try/catch insert into db (may fail with unique constraint)
#    