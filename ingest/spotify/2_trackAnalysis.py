import config
import psycopg2
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# INITIALIZE

# settings
TRACK_LIMIT = 250

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

cur.execute('''
    select t.id, t.spotifyid, t.name
    from tracks t
    left join queriestrackanalysis qta
    on t.id = qta.seedtrackid
    where qta.id is null
    limit %s''',
    (TRACK_LIMIT,))

tracks = cur.fetchall()

for idx, seedTrack in enumerate(tracks):
    seedTrackPrimaryKey = seedTrack[0]
    seedTrackSpotifyId = seedTrack[1]
    seedTrackName = seedTrack[2]

    # INFO: removed need for check QTA with left join / qta.id is nul in select statement
    # cur.execute('select id from queriestrackanalysis where seedtrackid = %s',
    #     (seedTrackPrimaryKey,))

    print('RUNNING TRACK_ANALYSIS ON:', seedTrackName)

    trackAnalysis = sp.audio_analysis(seedTrackSpotifyId)

    # print(trackAnalysis)

    key = trackAnalysis['track']['key']
    bpm = trackAnalysis['track']['tempo']

    print ('key', key)
    print('bpm', bpm)

    cur.execute('''
        update tracks
        set key = %s, bpm = %s
        where id = %s''',
        (key, bpm, seedTrackPrimaryKey))
    
    cur.execute('''insert into queriestrackanalysis (seedtrackid) values (%s)''',
        (seedTrackPrimaryKey,))

conn.commit()
cur.close()
    