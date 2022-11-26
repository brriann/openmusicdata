
# INITIALIZE
# - postgres / psycopg2
# - spotipy
# - set parameters, eg search depth (get related artists of a related artist of a ...)


# SEED DATA
# - insert seed artist into artists table (if no count)


# ITERATE
# - for artist
# - if no relatedartistqueries for seedArtistId
# - - get spotify related artists
# - - save artistrelations
# - - save queriesrelatedartist
# - - set new seedArtist (simply traverse artists table? from relatedartists?)