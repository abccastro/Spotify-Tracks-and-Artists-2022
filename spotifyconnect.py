import pickle

import pymongo as pymongo
import spotipy
from spotipy import SpotifyClientCredentials


def getSpotifyConnection():

    try:
        with open("config", "rb") as output_file:
            config = pickle.load(output_file)

        client_credentials_manager = SpotifyClientCredentials(client_id=config["sp_client_id"],
                                                              client_secret=config["sp_client_secret"])
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    except FileNotFoundError as err:
        print(f"Missing config file: {err}")
    except Exception as err:
        print(f"Unexpected error: {err}")
        sp = None

    return sp
