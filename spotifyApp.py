"""
Search and get Spotify tracks and artists

Submitted by:
Auradee Castro
Olivia Deguit
"""
import spotifyconnect
import dbconnect
from datetime import datetime
from enum import Enum
from colorama import Fore as fg, Back as bg, Style as ef, init

init(autoreset=True)


class Command(Enum):
    Search_Artist = "1"
    Search_Track = "2"
    Refresh = "3"
    Exit = "4"


def startApplication():
    print("SPOTIFY TRACKS AND ARTISTS (2022)")
    print("1. Search for Artists")
    print("2. Search for Tracks")
    print("3. Refresh Artists and Tracks")
    print("4. Exit Application")

    req_command = None
    while req_command != Command.Exit.value:

        req_command = input(f"\n{ef.BRIGHT}Select one option from the list (1, 2 or 3): ").strip()

        if req_command not in [item.value for item in Command]:
            print("Invalid selection. Try again.")
        elif req_command == Command.Exit.value:
            print(f"\n{bg.GREEN} Thank you for using the application! ")
        else:
            if req_command == Command.Search_Artist.value:
                print("1. Search Artist by Name")
                print("2. Search Artist by Genre")

            elif req_command == Command.Search_Track.value:
                keyword = input("Enter keyword to search for track: ")
                track_list = dbconnect.searchByTrackName(keyword)

                for track in track_list:
                    print(f"Track ID: {track['id']}")
                    print(f"Track Name: {track['name']}")
                    print(f"Artist: {track['artist_name']}")

            elif req_command == Command.Refresh.value:
                print(f"{bg.YELLOW}{ef.BRIGHT} WARNING: All tracks in the collection will be deleted. They will replaced by tracks extracted from Spotify ")
                is_continue = input("Do you want to continue? [y/Y]: ").strip().lower()

                if is_continue == 'y':
                    curr_datetime = datetime.now()

                    #tracks = spotifyconnect.getSpotifyTracks('2022', curr_datetime)
                    #dbconnect.refreshTracks(tracks)

                    artists = spotifyconnect.getSpotifyArtists('2022', curr_datetime)
                    dbconnect.refreshArtists(artists)


if __name__ == "__main__":
    startApplication()
