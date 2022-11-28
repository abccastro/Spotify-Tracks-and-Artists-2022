import pymongo as pymongo
import spotipy
from spotipy import SpotifyClientCredentials


def getSpotifyConnection():

    client_id = "ffa385b304ab4d5db995a3f894c2bd34"
    client_secret = "d2b26d4f06664fed8a7a5f2f7243e35f"

    try:
        client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    except Exception as err:
        print(f"Unexpected error: {err}")
        sp = None

    return sp
