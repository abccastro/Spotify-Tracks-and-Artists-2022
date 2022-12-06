"""
Search and get Spotify tracks and artists

Submitted by:
Auradee Castro
Olivia Deguit
"""
import spotifyconnect
import dbconnect
from enum import Enum
from colorama import Fore as fg, Back as bg, Style as ef, init
import matplotlib.pyplot as plt

init(autoreset=True)


class Command(Enum):
    Search = "1"
    View = "2"
    Refresh = "3"
    Deactivate = "4"
    Exit = "5"


class Info(Enum):
    Artist = "1"
    Genres = "2"
    Track = "3"


def startApplication():
    print(f"{fg.CYAN}+++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print(f"{fg.CYAN}+         SPOTIFY ARTISTS AND TRACKS (2022)         +")
    print(f"{fg.CYAN}+++++++++++++++++++++++++++++++++++++++++++++++++++++")

    req_command = None
    while req_command != Command.Exit.value:
        print()
        print("1. Search for Artists or Tracks")
        print("2. View Reports")
        print("3. Refresh Artists and Tracks")
        print("4. Deactivate Artist Info")
        print("5. Exit Application")

        req_command = input(f"\n{ef.BRIGHT}Select one option from the list (1, 2, 3 or 4): ").strip()

        if req_command not in [item.value for item in Command]:
            print("Invalid selection. Try again.")
        elif req_command == Command.Exit.value:
            print(f"\n{bg.GREEN} Thank you for using the application! ")
        else:
            if req_command == Command.Search.value:
                print()
                print("1. Search for Artists (by Name)")
                print("2. Search for Artists (by Genre)")
                print("3. Search for Tracks (by Track Name)")

                req_search = input(f"\n{ef.BRIGHT}Select one option from the list (1, 2 or 3): ").strip()

                if req_search not in [item.value for item in Info]:
                    print(f"{fg.RED}Invalid selection")
                else:
                    has_result = searchArtistInfo(req_search)
                    if not has_result:
                        print("No record found")

            elif req_command == Command.Refresh.value:
                refreshArtistInfo('2022')

            elif req_command == Command.Deactivate.value:
                artist_id = input("\nEnter Artist ID: ").strip()
                has_result = deactivateArtistInfo(artist_id)
                if not has_result:
                    print(f"{fg.RED}Invalid artist ID")

            is_continue = displayPromptToContinue()
            if not is_continue:
                print(f"\n{bg.GREEN} Thank you for using the application! ")
                break


def refreshArtistInfo(year):
    """
    The function that updates artist and track info based from records in Spotify
    :param str year: Year
    """
    print(
        f"{bg.YELLOW}{ef.BRIGHT} WARNING: All artists information in the collection will be replaced by records extracted from Spotify ")

    is_continue = displayPromptToContinue()
    if is_continue:
        artists = spotifyconnect.getSpotifyArtists(year)
        dbconnect.refreshArtists(artists)


def searchArtistInfo(selection):
    """
    The function that search for artists or tracks
    :param str selection: A for Artist. G for Genres. T for Tracks.
    """
    match selection:
        case Info.Artist.value:
            keyword = input("\nEnter keyword to search for artist (by name): ").lower().strip()
            artist_list = dbconnect.searchArtistInfo("name", keyword)
        case Info.Genres.value:
            keyword = input("\nEnter keyword to search for artist (by genre): ").lower().strip()
            artist_list = dbconnect.searchArtistInfo("genres", keyword)
        case Info.Track.value:
            keyword = input("\nEnter keyword to search for track (by name): ").lower().strip()
            artist_list = dbconnect.searchArtistInfo("tracks.name", keyword)

    if len(list(artist_list)) == 0:
        return False
    else:
        artist_list.rewind()

    for artist in artist_list:
        if selection == Info.Track.value:
            for track in artist['tracks']:
                if keyword in str(track['name']).lower():
                    print()
                    print(f"{fg.MAGENTA}{ef.BRIGHT}Track Name: {track['name']}")
                    print(f"Track ID: {track['id']}")
                    print(f"Artist Name: {artist['name']}")
                    print(f"Album: {track['album']}")
                    if track['popularity'] >= 80:
                        print(f"{fg.YELLOW}Popularity: {track['popularity']}")
                    else:
                        print(f"Popularity: {track['popularity']}")
        else:
            print()
            print(f"{fg.MAGENTA}{ef.BRIGHT}Artist Name: {artist['name']}")
            print(f"Artist ID: {artist['id']}")
            print(f"Genres: {', '.join(artist['genres'])}")
            if artist['popularity'] >= 80:
                print(f"{fg.YELLOW}Popularity: {artist['popularity']}")
            else:
                print(f"Popularity: {artist['popularity']}")
            print(f"Followers: {artist['followers']}")

    return True

def deactivateArtistInfo(artist_id):

    artist_info = dbconnect.getArtistInfo(artist_id)
    if len(list(artist_info)) == 0:
        return False

    artist_info.rewind()
    print(f"Artist Name: {artist_info[0]['name']}")

    if artist_info[0]['status'] == 'I':
        req_enable = input(f"{fg.YELLOW}{ef.BRIGHT}It is already deactivated. Do you want to activate this artist? [y/Y]: ").lower().strip()
        if req_enable == 'y':
            is_activated = dbconnect.deactivateArtistInfo(artist_id, False)
            if is_activated:
                print(f"{fg.GREEN}Successfully activated")
    else:
        req_disabled = input(f"{fg.YELLOW}{ef.BRIGHT}Do you want to deactivate this artist? [y/Y]: ").lower().strip()
        if req_disabled == 'y':
            is_deactivated = dbconnect.deactivateArtistInfo(artist_id, True)
            if is_deactivated:
                print(f"{fg.GREEN}Successfully deactivated")

    return True

def displayPromptToContinue():
    """
    The function that prompts the user is he wants to continue
    :return bool: True if continue. False otherwise.
    """
    is_continue = ""
    while is_continue != "n" and is_continue != "y":
        is_continue = input(f"\n{ef.BRIGHT}Do you want to continue? [y/n]: ").strip().lower()
        if is_continue != "n" and is_continue != "y":
            print(f"{fg.RED}Invalid input. Type 'y' for yes or 'n' for no.")
    return True if is_continue == 'y' else False


if __name__ == "__main__":
    startApplication()
