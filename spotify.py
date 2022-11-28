import pandas as pd

import spotifyconnect
import dbconnect


def startApplication():
    #playlist_list = displaySpotifyPlaylists()
    #print(playlist_list)
    #playlist_num = input("Enter playlist number: ").strip()
    #song_list = getSpotifyPlaylist(playlist_list[int(playlist_num)-1][1])

    #tracks = getSpotifyTracks('2022')
    #refreshTracks(tracks)

    artists = getSpotifyArtists('2022')
    refreshArtists(artists)


def displaySpotifyPlaylists():
    playlist_list = []
    try:
        print("List of Spotify Playlist")

        sp = spotifyconnect.getSpotifyConnection()
        playlists = sp.user_playlists('spotify')

        while playlists:
            for i, playlist in enumerate(playlists['items']):
                playlist_num = i + 1 + playlists['offset']
                playlist_list.append([playlist_num, playlist['uri'][17:], playlist['name']])
                #print("%4d %s" % (playlist_num, playlist['name']))

            if playlists['next']:
                playlists = sp.next(playlists)
            else:
                playlists = None

    except Exception as err:
        print(f"Unexpected error {displaySpotifyPlaylists.__name__}: {err}")
        playlist = []

    return playlist_list


def getSpotifyPlaylist(playlist_uri):
    try:
        sp = spotifyconnect.getSpotifyConnection()
        song_list = sp.playlist_items(playlist_uri)['items']
    except Exception as err:
        print(f"Unexpected error {getSpotifyPlaylist.__name__}: {err}")

    return song_list


def getSpotifyTracks(year):
    track_list = []
    try:
        sp = spotifyconnect.getSpotifyConnection()

        for i in range(0, 1000, 50):
            track_results = sp.search(q='year:'+year, type='track', limit=50, offset=i)
            for t in track_results['tracks']['items']:
                track = {"artist_id": t['artists'][0]['id'],
                         "artist_name": t['artists'][0]['name'],
                         "track_id": t['id'],
                         "track_name": t['name'],
                         "track_popularity": t['popularity']}
                track_list.append(track)

    except Exception as err:
        print(f"Unexpected error {getSpotifyTracks.__name__}: {err}")

    return track_list


def getSpotifyArtists(year):
    artist_list = []
    try:
        sp = spotifyconnect.getSpotifyConnection()
        artist_ids = getArtistIDsFromTrack()

        for id in artist_ids:
            a = sp.artist(id)
            artist = {"id": id,
                      "name": a['name'],
                      "genres": a['genres'],
                      "popularity": a['popularity'],
                      "followers": a['followers']['total']}
            artist_list.append(artist)

    except Exception as err:
        print(f"Unexpected error {getSpotifyArtists.__name__}: {err}")

    return artist_list


def getArtistIDsFromTrack():
    id_list = []
    try:
        database = dbconnect.getDBConnection()
        my_collection = database["track_info"]
        result = my_collection.find({}, {"artist_id": 1})

        for i in result:
            id_list.append(i["artist_id"])
        id_list = [*set(id_list)]

    except Exception as err:
        print(f"Unexpected error {getArtistIDsFromTrack.__name__}: {err}")

    return id_list


def refreshTracks(song_list):
    try:
        database = dbconnect.getDBConnection()
        my_collection = database["track_info"]
        my_collection.delete_many({})    # clear the content
        my_collection.insert_many(song_list)
    except Exception as err:
        print(f"Unexpected error {refreshTracks.__name__}: {err}")


def refreshArtists(artist_list):
    try:
        database = dbconnect.getDBConnection()
        my_collection = database["artist_info"]
        result = my_collection.find({}, {"id": 1})

        for artist in artist_list:
            for i in result:
                if artist["id"] == i["id"]:
                    my_collection.update_one({"id": i["id"]},
                                             {"$set": {"name": i[1], "genres": i[2], "popularity": i[3], "followers": i[4]}})
                    break
        else:
            my_collection.insert_one(artist)

        my_collection.insert_many(artist_list)
    except Exception as err:
        print(f"Unexpected error on {refreshArtists.__name__}: {err}")


startApplication()
