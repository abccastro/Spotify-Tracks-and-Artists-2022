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
    """
    The function that get MongoDB connection
    :return: database connection
    """
    try:
        with open("dbconfig", "rb") as output_file:
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
    """
    The function that gets Spotify configuration
    :return map: Spotify's client ID and client secret
    """
    try:
        database = dbconnect.getDBConnection()
        config_col = database["config"]
        config = config_col.find({})

    except Exception as err:
        print(f"{fg.RED}Unexpected error {getSpotifyConfig.__name__}: {err}")
        config = None

    return config[0]["spotify"]


def refreshArtists(artist_list):
    """
    The function that updates artist info if exists,=. Otherwise, the record is inserted.
    :param list artist_list: List of artists with tracks
    """
    try:
        database = dbconnect.getDBConnection()
        artist_info_col = database["artist_info"]

        deactivated_artists = list(getDeactivatedArtists())

        for artist in artist_list:

            is_activated = True
            for d_artist in deactivated_artists:
                if artist["id"] == d_artist["id"]:
                    print(f"\tInactive Artist ID {artist['id']}. No changes done.")
                    is_activated = False
                    break

            if is_activated:
                artist_info_col.update_one({"id": artist["id"]},
                                           {"$set": {
                                               "name": artist["name"],
                                               "genres": artist["genres"],
                                               "popularity": artist["popularity"],
                                               "followers": artist["followers"],
                                               "tracks": artist["tracks"],
                                               "status": "A",
                                               "update_datetime": artist["update_datetime"]
                                           }},
                                           upsert=True)

        print(f"{fg.GREEN}Successfully updated the records")

    except Exception as err:
        print(f"{fg.RED}Unexpected error on {refreshArtists.__name__}: {err}")


def searchArtistInfo(key, keyword):
    """
    The function that searches artists by artist name / genres using the specified keyword
    :param str key: Key in mongodb
    :param str keyword: Keyword to search for artist name / generes
    :return list artist_list: List of artists that matches the keyword
    """
    try:
        database = dbconnect.getDBConnection()
        artist_info_col = database["artist_info"]
        artist_list = artist_info_col.find({key: {"$regex": ".*" + keyword + ".*", "$options": "i"}}, {"_id": 0})

    except Exception as err:
        print(f"{fg.RED}Unexpected error {searchArtistInfo.__name__}: {err}")
        artist_list = []

    return artist_list


def searchDeactivatedArtistInfo():
    try:
        database = dbconnect.getDBConnection()
        artist_info_col = database["artist_info"]
        artist_list = artist_info_col.find({"status": "I"}, {"_id": 0})

    except Exception as err:
        print(f"{fg.RED}Unexpected error {searchDeactivatedArtistInfo.__name__}: {err}")
        artist_list = []

    return artist_list


def deactivateArtistInfo(artist_id, flag):
    try:
        database = dbconnect.getDBConnection()
        artist_info_col = database["artist_info"]
        artist_info_col.update_one({"id": artist_id}, {"$set": {"status": "I" if flag else "A"}})

    except Exception as err:
        print(f"{fg.RED}Unexpected error {deactivateArtistInfo.__name__}: {err}")
        return False

    return True

def getArtistInfo(artist_id):
    try:
        database = dbconnect.getDBConnection()
        artist_info_col = database["artist_info"]
        artist_info = artist_info_col.find({"id": artist_id}, {"_id": 0})

    except Exception as err:
        print(f"{fg.RED}Unexpected error {getArtistInfo.__name__}: {err}")
        artist_info = None

    return artist_info


def getAllArtistsByFollowers():
    try:
        database = dbconnect.getDBConnection()
        artist_info_col = database["artist_info"]
        artist_list = artist_info_col.find({"status": {"$ne": "I"}}, {"_id": 0}).sort("followers", -1)

    except Exception as err:
        print(f"{fg.RED}Unexpected error {getAllArtistsByFollowers.__name__}: {err}")
        artist_list = None

    return artist_list


def getAllArtistsByPopularity():
    try:
        database = dbconnect.getDBConnection()
        artist_info_col = database["artist_info"]
        artist_list = artist_info_col.find({"status": {"$ne": "I"}}, {"_id": 0}).sort("popularity", -1)

    except Exception as err:
        print(f"{fg.RED}Unexpected error {getAllArtistsByPopularity.__name__}: {err}")
        artist_list = None

    return artist_list


def getDeactivatedArtists():
    try:
        database = dbconnect.getDBConnection()
        artist_info_col = database["artist_info"]
        deactivated_artists = artist_info_col.find({"status": "I"}, {"_id": 0, "id": 1, "name": 1, "status": 1})

    except Exception as err:
        print(f"{fg.RED}Unexpected error {getDeactivatedArtists.__name__}: {err}")
        deactivated_artists = None

    return deactivated_artists
