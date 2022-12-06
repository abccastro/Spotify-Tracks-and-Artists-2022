"""
Connect to Spotify API

Submitted by:
Auradee Castro
Olivia Deguit
"""
from datetime import datetime
import dbconnect
import spotifyconnect
import spotipy
from spotipy import SpotifyClientCredentials
from colorama import Fore as fg, Back as bg, Style as ef, init

init(autoreset=True)


def getSpotifyConnection():
    """
    The function that connects to Spotify using the valid client credentials
    :return Spotify: Spotify validated instance connection
    """
    try:
        spotify_config = dbconnect.getSpotifyConfig()

        if spotify_config:
            client_credentials_manager = SpotifyClientCredentials(client_id=spotify_config["client_id"],
                                                                  client_secret=spotify_config["client_secret"])
            sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    except Exception as err:
        print(f"{fg.RED}Unexpected error {getSpotifyConnection.__name__}: {err}")
        sp = None

    return sp


def getSpotifyArtists(year):
    """
    The function that gets tracks and artists from Spotify
    :param str year: Year
    :return: List of the artists with tracks
    """
    artist_list = []
    curr_datetime = datetime.now()

    try:
        sp = spotifyconnect.getSpotifyConnection()

        for i in range(0, 1000, 50):
            track_artist_list = sp.search(q='year:' + year, type='track', limit=50, offset=i, market="US")

            for t in track_artist_list['tracks']['items']:
                track = {"id": t['id'],
                         "name": t['name'],
                         "album": t['album']['name'],
                         "popularity": t['popularity'],
                         "update_datetime": curr_datetime.strftime("%d/%m/%Y %H:%M:%S")
                         }

                idx_artist = [idx for idx, e in enumerate(artist_list) if t['artists'][0]['id'] == e['id']]

                if len(idx_artist) == 0:
                    a = sp.artist(t['artists'][0]['id'])

                    artist = {"id": t['artists'][0]['id'],
                              "name": a['name'],
                              "genres": a['genres'],
                              "popularity": a['popularity'],
                              "followers": a['followers']['total'],
                              "tracks": [track],
                              "update_datetime": curr_datetime.strftime("%d/%m/%Y %H:%M:%S")
                              }
                    artist_list.append(artist)

                else:
                    track_list = artist_list[idx_artist[0]]['tracks']
                    track_list.append(track)
                    artist_list[idx_artist[0]]['tracks'] = track_list
            else:
                print(f"\tRetrieved {len(artist_list)} artists")
        else:
            print(f"{fg.GREEN}Total artists retrieved from Spotify: {len(artist_list)}")

    except Exception as err:
        print(f"{fg.RED}Unexpected error {getSpotifyArtists.__name__}: {err}")

    return artist_list
