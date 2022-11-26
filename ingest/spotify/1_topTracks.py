
# INITIALIZE
# - postgres / psycopg2
# - spotipy
# - set parameters, eg iteration count (api calls made, artists queried, tracks saved?)


# SEED DATA
# - insert seed artist into artists table (if no count)


# ITERATE
# - for artist
# - if no queriestoptracks for seedArtistId
# - - get spotify top tracks
# - - save tracks (upsert behavior?)
# - - save queriestoptracks
# - - set new seedArtist (simply traverse artists table?)
