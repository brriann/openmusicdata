import config
import spotipy
import pdb
from spotipy.oauth2 import SpotifyClientCredentials

def getData():
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=config.clientId,
                                                            client_secret=config.clientSecret))

    # results = sp.search(q='weezer', limit=20)
    # for idx, track in enumerate(results['tracks']['items']):
    #     print(idx, track['name'])

    pdb.set_trace()
    seedArtistId = "6V4bkdqHvsJ2lqkIl4qnG7" # Nicolas Jaar

    relatedArtists = sp.artist_related_artists(seedArtistId)
    for idx, artist in enumerate(relatedArtists['artists']):
        if idx < 3:
            artistName = artist['name']
            print(idx, artistName, artist['id'])
            artistTracks = sp.artist_top_tracks(artist['id'])
            for trackIdx, track in enumerate(artistTracks['tracks']):
                if trackIdx < 3:
                    print(">>", idx, track['id'], track['name'], f'({artistName})')
        
        subRelatedArtists = sp.artist_related_artists(artist['id'])
        for subIdx, subArtist in enumerate(subRelatedArtists['artists']):
            if subIdx < 3:
                subArtistName = subArtist['name']
                print('>>>>', subIdx, subArtistName, subArtist['id'])
                subArtistTracks = sp.artist_top_tracks(subArtist['id'])
                for subTrackIdx, subTrack in enumerate(subArtistTracks['tracks']):
                    if subTrackIdx < 3:
                        print(">>>>>>", subTrackIdx, subTrack['id'], subTrack['name'], f'({subArtistName})')
