import config
import psycopg2
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# INITIALIZE

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

# set parameters, eg search depth (get related artists of a related artist of a ...)
# TODO
searchDepth = 2

# SEED DATA
# insert seed artist into artists table (if no count)
seedArtistSpotifyId = '5a0etAzO5V26gvlbmHzT9W'
seedArtistName = 'Nicolas Jaar'

cur = conn.cursor()

cur.execute('select id, spotifyId from artists where spotifyid = %s', 
    (seedArtistSpotifyId,))

existingSeedArtist = cur.fetchone()

if existingSeedArtist is None:
    cur.execute('insert into artists (spotifyId, name) values(%s, %s) returning id',
        (seedArtistSpotifyId, seedArtistName))

    seedArtistPrimaryKey = cur.fetchone()[0]
else:
    seedArtistPrimaryKey = existingSeedArtist[0]

print(seedArtistPrimaryKey)

cur.execute('select spotifyId from artists where id = %s', 
    (seedArtistPrimaryKey,))

seedArtistSpotifyId = cur.fetchone()[0]
print(seedArtistSpotifyId)


# ITERATE
# for artist
# if no relatedartistqueries for seedArtistId
# TODO

# set counters
artistsSaved = 0
artistRelationsSaved = 0

# get spotify related artists
relatedArtists = sp.artist_related_artists(seedArtistSpotifyId)

for idx, artist in enumerate(relatedArtists['artists']):
    print(artist['id'], artist['name'])

    relatedArtistPrimaryKey = 0
    artistExisted = False
    # check for existence of artist by spotifyId
    cur.execute('select id from artists where spotifyId = %s',
        (artist['id'],))

    # create if not exists
    existingArtist = cur.fetchone()
    if existingArtist is None:
        print('inserting artist', artist['id'], artist['name'])
        cur.execute('insert into artists (spotifyId, name) values(%s, %s) returning id',
            (artist['id'], artist['name']))
        relatedArtistPrimaryKey = cur.fetchone()[0]
        artistsSaved += 1
    else:
        artistExisted = True
        relatedArtistPrimaryKey = existingArtist[0]

    print('relatedArtistPrimaryKey', relatedArtistPrimaryKey)

    # check for existence of artistrelation by source and target ids
    cur.execute('select id from artistrelations where sourceartistid = %s and targetartistid = %s',
        (seedArtistPrimaryKey, relatedArtistPrimaryKey))
    
    existingArtistRelation = cur.fetchone()
    if existingArtistRelation is None:
        print('inserting artistrelation', seedArtistPrimaryKey, relatedArtistPrimaryKey)
        cur.execute('insert into artistrelations (sourceartistid, targetartistid) values (%s, %s) returning id',
            (seedArtistPrimaryKey, relatedArtistPrimaryKey))
        artistRelationsSaved += 1

conn.commit()
print('artistRelationsSaved', artistRelationsSaved)
print('artistsSaved', artistsSaved)

# - - save queriesrelatedartist
# - - set new seedArtist (simply traverse artists table? from relatedartists?)

cur.close()