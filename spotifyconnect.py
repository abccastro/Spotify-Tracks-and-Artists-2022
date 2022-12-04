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


def getSpotifyTracks(year, curr_datetime):
    track_list = []
    try:
        sp = spotifyconnect.getSpotifyConnection()

        for i in range(0, 1000, 50):
            track_results = sp.search(q='year:' + year, type='track', limit=50, offset=i, market="US")
            for t in track_results['tracks']['items']:
                track = {"id": t['id'],
                         "name": t['name'],
                         "album": t['album']['name'],
                         "popularity": t['popularity'],
                         "update_datetime": curr_datetime.strftime("%d/%m/%Y %H:%M:%S")
                         }
                track_list.append(track)
        else:
            print(f"{fg.GREEN}Successfully retrieved {len(track_list)} tracks from Spotify")

    except Exception as err:
        print(f"{fg.RED}Unexpected error {getSpotifyTracks.__name__}: {err}")

    return track_list

def getSpotifyArtists(year, curr_datetime):
    artist_list = []
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
                print(f"{fg.GREEN}Retrieved {len(artist_list)} records")
        else:
            print(f"{fg.GREEN}Total artists retrieved from Spotify: {len(artist_list)}")

    except Exception as err:
        print(f"{fg.RED}Unexpected error {getSpotifyArtists.__name__}: {err}")

    return artist_list

'''
def getSpotifyArtists(curr_datetime):
    artist_list = []
    try:
        sp = spotifyconnect.getSpotifyConnection()
        artist_id_list = dbconnect.getArtistIDsFromTrack()

        for artist_id in artist_id_list:
            a = sp.artist(artist_id)
            artist = {"id": artist_id,
                      "name": a['name'],
                      "genres": a['genres'],
                      "popularity": a['popularity'],
                      "followers": a['followers']['total'],
                      "update_datetime": curr_datetime.strftime("%d/%m/%Y %H:%M:%S")
                      }
            artist_list.append(artist)
        else:
            print(f"{fg.GREEN}Successfully retrieved {len(artist_list)} artists from Spotify")

    except Exception as err:
        print(f"{fg.RED}Unexpected error {getSpotifyArtists.__name__}: {err}")

    return artist_list
'''


#getSpotifyArtists("2022", datetime.now())
