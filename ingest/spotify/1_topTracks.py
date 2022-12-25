import config
import psycopg2
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# INITIALIZE

# settings
ARTIST_LIMIT = 100

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

cur.execute('select id, spotifyid, name from artists where highlighted = true limit %s',
    (ARTIST_LIMIT,))

artists = cur.fetchall()

print('len(artists)', len(artists))

for idx, seedArtist in enumerate(artists):
    seedArtistPrimaryKey = seedArtist[0]
    seedArtistSpotifyId = seedArtist[1]
    seedArtistName = seedArtist[2]

    cur.execute('select id from queriestoptracks where seedartistid = %s',
        (seedArtistPrimaryKey,))

    existingQueryTopTracks = cur.fetchone()
    if existingQueryTopTracks is not None:
        print('existingQueryTopTracks for: ', seedArtistName)
        continue
    print('RUNNING TOP_TRACKS ON:', seedArtistName)
    # set counters
    tracksSaved = 0

    # get spotify top tracks
    topTracks = sp.artist_top_tracks(seedArtistSpotifyId)
    
    for idx, track in enumerate(topTracks['tracks']):
        print(track['id'], track['name'])

        # check for existence of track by spotifyId
        cur.execute('select id from tracks where spotifyId = %s',
            (track['id'],))
        existingTrack = cur.fetchone()

        if existingTrack is None:
            print('inserting track', track['name'])
            cur.execute('insert into tracks (spotifyId, artistId, name) values (%s, %s, %s) returning id',
                (track['id'], seedArtistPrimaryKey, track['name']))
            tracksSaved += 1
            
        else:
            print('track existed: ', track['name'])

    print('tracksSaved', tracksSaved)

    # save queriestoptracks
    cur.execute('insert into queriestoptracks (seedArtistId, tracksSaved) values (%s, %s)',
        (seedArtistPrimaryKey, tracksSaved))

conn.commit()
cur.close()
