"""
Connect to MongoDB

Submitted by:
Auradee Castro
Olivia Deguit
"""
import pickle
import pymongo as pymongo
import dbconnect
from colorama import Fore as fg, Back as bg, Style as ef, init

init(autoreset=True)


def getDBConnection():
    try:
        with open("config", "rb") as output_file:
            config = pickle.load(output_file)

        conn = "mongodb+srv://%s:%s@%s/?retryWrites=true&w=majority" % (config["db_username"],
                                                                        config["db_password"],
                                                                        config["db_host"])
        client = pymongo.MongoClient(conn)
        database = client["spotify"]

    except FileNotFoundError as err:
        print(f"{fg.RED}Missing config file: {err}")
    except Exception as err:
        print(f"{fg.RED}Unexpected error {getDBConnection.__name__}: {err}")
        database = None

    return database


def getSpotifyConfig():
    try:
        database = dbconnect.getDBConnection()
        config_col = database["config"]
        config = config_col.find({})

    except Exception as err:
        print(f"{fg.RED}Unexpected error {getSpotifyConfig.__name__}: {err}")
        config = None

    return config[0]["spotify"]

def refreshTracks(song_list):
    try:
        database = dbconnect.getDBConnection()
        track_info_col = database["track_info"]
        track_info_col.delete_many({})  # clear the content
        track_info_col.insert_many(song_list)

        print(f"{fg.GREEN}Successfully refreshed {len(song_list)} tracks_info collection")

    except Exception as err:
        print(f"{fg.RED}Unexpected error {refreshTracks.__name__}: {err}")


def refreshArtists(artist_list):
    try:
        database = dbconnect.getDBConnection()
        artist_info_col = database["artist_info"]
        artist_info_col.delete_many({})  # clear the content

        for artist in artist_list:

            artist_info_col.update_many({"id": artist["id"]},
                                        {"$set": {
                                            "name": artist["name"],
                                            "genres": artist["genres"],
                                            "popularity": artist["popularity"],
                                            "followers": artist["followers"],
                                            "tracks": artist["tracks"],
                                            "update_datetime": artist["update_datetime"]
                                        }},
                                        upsert=True)

        print(f"{fg.GREEN}Successfully added/updated {len(artist_list)} artist_info collection")

    except Exception as err:
        print(f"{fg.RED}Unexpected error on {refreshArtists.__name__}: {err}")


def getArtistIDsFromTrack():
    artist_id_list = []
    try:
        database = dbconnect.getDBConnection()
        track_info_col = database["track_info"]
        result = track_info_col.find({}, {"artist_id": 1})

        for t in result:
            artist_id_list.append(t["artist_id"])

        artist_id_list = [*set(artist_id_list)]

        print(f"{fg.GREEN}Successfully retrieved {len(artist_id_list)} artist IDs from track_info collection")

    except Exception as err:
        print(f"{fg.RED}Unexpected error {getArtistIDsFromTrack.__name__}: {err}")

    return artist_id_list


def searchByTrackName(keyword):
    try:
        database = dbconnect.getDBConnection()
        track_info_col = database["track_info"]
        track_list = track_info_col.find({"name": {"$regex": ".*"+keyword+".*", "$options": "i"}}, {"_id": 0})

        for i in track_list:
            print(i)

    except Exception as err:
        print(f"{fg.RED}Unexpected error {searchByTrackName.__name__}: {err}")
        track_list = []

    return track_list
