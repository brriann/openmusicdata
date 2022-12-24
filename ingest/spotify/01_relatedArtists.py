import config
import psycopg2
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# INITIALIZE

#settings
ARTIST_LIMIT = 1000

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

cur.execute('select id, spotifyid, name from artists limit %s',
    (ARTIST_LIMIT,))

artists = cur.fetchall()

print('len(artists)', len(artists))

# TODO
# if artists is None:

for idx, seedArtist in enumerate(artists):
    seedArtistPrimaryKey = seedArtist[0]
    seedArtistSpotifyId = seedArtist[1]
    seedArtistName = seedArtist[2]

    cur.execute('select id from queriesrelatedartist where seedartistid = %s',
    (seedArtistPrimaryKey,))

    existingQueryRelatedArtist = cur.fetchone()
    if existingQueryRelatedArtist is not None:
        print('existingQueryRelatedArtist for: ', seedArtistName)
        continue
    print('RUNNING RELATED_ARTISTS ON:', seedArtistName)
    # set counters
    artistsSaved = 0
    artistRelationsSaved = 0

    # get spotify related artists
    relatedArtists = sp.artist_related_artists(seedArtistSpotifyId)

    for idx, artist in enumerate(relatedArtists['artists']):
        print(artist['id'], artist['name'])
        
        # check for existence of artist by spotifyId
        cur.execute('select id from artists where spotifyId = %s',
            (artist['id'],))
        existingArtist = cur.fetchone()
        
        if existingArtist is None:
            print('inserting artist', artist['name'])
            cur.execute('insert into artists (spotifyId, name) values(%s, %s) returning id',
                (artist['id'], artist['name']))
            
            relatedArtistPrimaryKey = cur.fetchone()[0]
            artistsSaved += 1
        else:
            print('artist existed: ', artist['name'])
            relatedArtistPrimaryKey = existingArtist[0]
        # check for existence of artistrelation by source and target ids
        # TODO, if existingArtist was None, there will not be an artistrelation...
        cur.execute('select id from artistrelations where sourceartistid = %s and targetartistid = %s',
            (seedArtistPrimaryKey, relatedArtistPrimaryKey))
        
        existingArtistRelation = cur.fetchone()
        if existingArtistRelation is None:
            print('inserting artistrelation', seedArtistPrimaryKey, relatedArtistPrimaryKey)
            cur.execute('insert into artistrelations (sourceartistid, targetartistid) values (%s, %s) returning id',
                (seedArtistPrimaryKey, relatedArtistPrimaryKey))
            artistRelationsSaved += 1
    
    print('artistRelationsSaved', artistRelationsSaved)
    print('artistsSaved', artistsSaved)

    # - - save queriesrelatedartist
    cur.execute('insert into queriesrelatedartist (seedArtistId, artistsSaved, relationsSaved) values(%s, %s, %s)',
        (seedArtistPrimaryKey, artistsSaved, artistRelationsSaved))

conn.commit()
cur.close()
