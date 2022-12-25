import config
import psycopg2
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# INITIALIZE

# settings
TRACK_LIMIT = 100

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

cur.execute('select id, spotifyid, name from tracks limit %s',
    (TRACK_LIMIT,))

tracks = cur.fetchall()

for idx, seedTrack in enumerate(tracks):
    seedTrackPrimaryKey = seedTrack[0]
    seedTrackSpotifyId = seedTrack[1]
    seedTrackName = seedTrack[2]

    cur.execute('select id from queriestrackanalysis where seedtrackid = %s',
        (seedTrackPrimaryKey,))