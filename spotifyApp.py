"""
Get first 1000 Spotify tracks and their corresponding artist for year 2022.
Data extracted from Spotify are stored in MongoDB Atlas.
Create data visualization on artist's popularity and followers, and tracks popularity.

Project Fall 2022 (BDM-11123)
Submitted by:
- Auradee Castro
- Olivia Deguit
- Bhumika Rajendra Babu
"""
import pickle

import spotifyconnect
import dbconnect
import visualization
from enum import Enum
from colorama import Fore as fg, Back as bg, Style as ef, init
from collections import Counter

init(autoreset=True)


class Command(Enum):
    Search = "1"
    View = "2"
    Refresh = "3"
    Deactivate = "4"
    Delete = "5"
    Exit = "6"


class Info(Enum):
    Artist = "1"
    Genres = "2"
    Track = "3"
    Deactivated = "4"


class Report(Enum):
    Artist_Follower = "1"
    Artist_Popularity = "2"
    Track_Popularity = "3"
    Num_Artist_Popularity = "4"
    Num_Track_Popularity = "5"

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
        print("4. Deactivate/Activate Artist Profile")
        print("5. Delete All Artist Profiles")
        print("6. Exit Application")

        req_command = input(f"\n{ef.BRIGHT}Select one option from the list (1, 2, 3, 4, 5 or 6): ").strip()

        if req_command not in [elem.value for elem in Command]:
            print("Invalid selection. Try again.")
        elif req_command == Command.Exit.value:
            print(f"\n{bg.GREEN}{fg.BLACK} Thank you for using the application! ")
        else:
            if req_command == Command.Search.value:
                print()
                print("1. Search for Artists (by Name)")
                print("2. Search for Artists (by Genre)")
                print("3. Search for Tracks (by Track Name)")
                print("4. List Deactivated Artist Profile")

                req_search = input(f"\n{ef.BRIGHT}Select one option from the list (1, 2, 3 or 4): ").strip()
                if req_search not in [elem.value for elem in Info]:
                    print(f"{fg.RED}Invalid selection")
                else:
                    has_result = searchArtistInfo(req_search)
                    if not has_result:
                        print("No record found")

            elif req_command == Command.View.value:
                print()
                print("1. Top 10 Artists with Most Number of Followers")
                print("2. Top 10 Artists with Highest Popularity Index")
                print("3. Top 10 Tracks with Highest Popularity Index")
                print("4. Number of Artists by Popularity Index (80 to 100)")
                print("5. Number of Tracks by Popularity Index (80 to 100)")

                req_report = input(f"\n{ef.BRIGHT}Select one option from the list (1, 2, 3, 4 or 5): ").strip()
                if req_report not in [elem.value for elem in Report]:
                    print(f"{fg.RED}Invalid selection")
                else:
                    print("Generating the report...")
                    has_report = viewReport(req_report)
                    if not has_report:
                        print("No record found")

            elif req_command == Command.Refresh.value:
                refreshArtistInfo()

            elif req_command == Command.Deactivate.value:
                artist_id = input("\nEnter Artist ID: ").strip()
                has_result = deactivateArtistInfo(artist_id)
                if not has_result:
                    print(f"{fg.RED}Invalid artist ID")

            elif req_command == Command.Delete.value:
                is_login = loginAccount()
                if is_login:
                    req_delete = input(f"\n{ef.BRIGHT}Are you sure you want to delete all the records? [y/Y]: ").lower().strip()
                    if req_delete == 'y':
                        dbconnect.deleteAllArtistProfiles()
                    else:
                        print("No changes done")

            is_continue = ""
            while is_continue != "n" and is_continue != "y":
                is_continue = input(f"\n{ef.BRIGHT}Do you want to continue? [y/n]: ").strip().lower()
                if is_continue != "n" and is_continue != "y":
                    print(f"{fg.RED}Invalid input. Type 'y' for yes or 'n' for no.")
            else:
                if is_continue == 'n':
                    print(f"\n{bg.GREEN}{fg.BLACK} Thank you for using the application! ")
                    break


def searchArtistInfo(selection):
    """
    The function that search for artists or tracks
    :param str selection: A for Artist. G for Genres. T for Tracks.
    """
    match selection:
        case Info.Artist.value:
            keyword = input("\nEnter keyword to search for artist (by name): ").lower().strip()
            artist_list = list(dbconnect.searchArtistInfo("name", keyword))
        case Info.Genres.value:
            keyword = input("\nEnter keyword to search for artist (by genre): ").lower().strip()
            artist_list = list(dbconnect.searchArtistInfo("genres", keyword))
        case Info.Track.value:
            keyword = input("\nEnter keyword to search for track (by name): ").lower().strip()
            artist_list = list(dbconnect.searchArtistInfo("tracks.name", keyword))
        case Info.Deactivated.value:
            artist_list = list(dbconnect.getDeactivatedArtists())

    if len(artist_list) == 0:
        return False

    for artist in artist_list:
        if selection == Info.Track.value:
            for track in artist['tracks']:
                if keyword in str(track['name']).lower():
                    deactivated = popular = ""
                    if artist['status'] == 'I':
                        deactivated = "(DEACTIVATED)"
                    if track['popularity'] > 80:
                        popular = "\u2606"

                    print()
                    print(f"{fg.MAGENTA}{ef.BRIGHT}Track Name: {track['name']} {deactivated}{fg.YELLOW}{popular}")
                    print(f"Track ID: {track['id']}")
                    print(f"Artist Name: {artist['name']}")
                    print(f"Album: {track['album']}")
                    print(f"Popularity: {track['popularity']}")
        else:
            deactivated = popular = ""
            if artist['status'] == 'I':
                deactivated = "(DEACTIVATED)"
            if artist['popularity'] > 80:
                popular = "\u2606"

            print()
            print(f"{fg.MAGENTA}{ef.BRIGHT}Artist Name: {artist['name']} {deactivated}{fg.YELLOW}{popular}")
            print(f"Artist ID: {artist['id']}")
            print(f"Genres: {', '.join(artist['genres'])}")
            print(f"Popularity: {artist['popularity']}")
            print(f"Followers: {artist['followers']}")

    return True


def viewReport(report_type):
    """
    The function that creates different types of report
    :param str report_type: Type of report
    """
    match report_type:
        case Report.Artist_Follower.value:

            artist_list = list(dbconnect.getAllArtistsByFollowers())
            if len(artist_list) == 0:
                return False

            artist_names = [artist_list[idx]['name'] for idx in range(10)]
            artist_followers = [artist_list[idx]['followers'] for idx in range(10)]

            visualization.showBarGraph(artist_followers,
                                       artist_names,
                                       x_label='Number of Followers (in millions)',
                                       title='Top 10 Artists with Most Number of Followers')

        case Report.Artist_Popularity.value:

            artist_list = list(dbconnect.getAllArtistsByPopularity())
            if len(artist_list) == 0:
                return False

            artist_names = [artist_list[idx]['name'] for idx in range(10)]
            artist_popularity = [artist_list[idx]['popularity'] for idx in range(10)]

            visualization.showBarGraph(artist_popularity,
                                       artist_names,
                                       add_val=True,
                                       x_label='Popularity Index',
                                       title='Top 10 Artists with Highest Popularity Index')

        case Report.Track_Popularity.value:

            track_list = list(dbconnect.getAllTracksByPopularity())
            if len(track_list) == 0:
                return False

            track_list = [track_list[idx]['tracks'][0] for idx in range(10)]
            track_names = [track['name'] for track in track_list]
            track_popularity = [track['popularity'] for track in track_list]

            visualization.showBarGraph(track_popularity,
                                       track_names,
                                       add_val=True,
                                       x_label='Popularity Index',
                                       title='Top 10 Tracks with Highest Popularity Index')

        case Report.Num_Artist_Popularity.value:

            artist_list = list(dbconnect.getAllArtistsByPopularity())
            if len(artist_list) == 0:
                return False

            popularity_counter = Counter([artist['popularity'] for artist in artist_list if artist['popularity'] >= 80])
            popularity_list = [i for i in range(80, 101)]
            popularity_count_list = popularityCounter(popularity_list, popularity_counter)

            visualization.showLineGraph(popularity_list,
                                        popularity_count_list,
                                        x_label='Popularity Index',
                                        y_label='Number of Artists',
                                        title='Number of Artists per Popularity Index')

        case Report.Num_Track_Popularity.value:

            track_list = list(dbconnect.getAllTracksByPopularity())
            if len(track_list) == 0:
                return False

            track_list = [track['tracks'][0] for track in track_list]

            popularity_counter = Counter([track['popularity'] for track in track_list if track['popularity'] >= 80])
            popularity_list = [i for i in range(80, 101)]
            popularity_count_list = popularityCounter(popularity_list, popularity_counter)

            visualization.showLineGraph(popularity_list,
                                        popularity_count_list,
                                        x_label='Popularity Index',
                                        y_label='Number of Tracks',
                                        title='Number of Tracks per Popularity Index')
    return True


def refreshArtistInfo():
    print(f"\n{bg.YELLOW}{fg.BLACK} WARNING: All active artist profiles will be replaced by records from Spotify ")

    req_enable = input(f"{ef.BRIGHT}Are you sure you want to refresh the data? [y/Y]: ").lower().strip()
    if req_enable == 'y':
        print("Connecting to Spotify to get artist records...")
        artists = spotifyconnect.getSpotifyArtists('2022')
        print("Saving artist records...")
        dbconnect.refreshArtists(artists)
    else:
        print("No changes done")


def deactivateArtistInfo(artist_id):
    """
    The function that deactivate or inactivate artist profile
    :param str artist_id: ID of the artist
    :return bool: True if successful action. False if ID does not exist.
    """
    artist_info = list(dbconnect.getArtistInfo(artist_id))
    if len(artist_info) == 0:
        return False

    print(f"Artist Name: {artist_info[0]['name']}")

    if artist_info[0]['status'] == 'I':
        req_enable = input(f"{ef.BRIGHT}Would you like to activate this artist profile? [y/Y]: ").lower().strip()
        if req_enable == 'y':
            is_activated = dbconnect.changeArtistInfoStatus(artist_id, False)
            if is_activated:
                print(f"{fg.GREEN}Successfully activated")
        else:
            print("No changes done")
    else:
        req_disabled = input(f"{ef.BRIGHT}Are you sure you want to deactivate this artist profile? [y/Y]: ").lower().strip()
        if req_disabled == 'y':
            is_deactivated = dbconnect.changeArtistInfoStatus(artist_id, True)
            if is_deactivated:
                print(f"{fg.GREEN}Successfully deactivated")
        else:
            print("No changes done")

    return True


def loginAccount():
    """
    The function that prompts authorized users to log into the application
    :return bool: True for successful login. False otherwise.
    """
    login_attempt = 0
    is_login_account = False
    max_login_attempt = 3

    account_list = readFile("config/accounts")

    # If there are no errors reading the account file
    if account_list is not None:

        print(f"\n{bg.YELLOW}{fg.BLACK} Only authorized users are allowed to delete all artist profiles ")
        username = input("Username: ")
        password = input("Password: ")

        for account in account_list:
            if username == account[0] and password == account[1]:
                is_login_account = True
                break
        else:
            login_attempt += 1
            if login_attempt < max_login_attempt:
                print(f"{fg.RED}{ef.BRIGHT}Invalid username and/or password")

        if is_login_account:
            print(f"{fg.GREEN}{ef.BRIGHT}Log In Successful")

    return is_login_account


def readFile(filename):
    """
    The function that reads content from a file
    :param str filename: Filename
    :return list: File content
    """
    try:
        with open(filename, "rb") as file:
            content_list = pickle.load(file)
    except EOFError:
        content_list = []
    except Exception as err:
        print(f"{fg.RED}Unexpected error: {err}")
        content_list = None

    return content_list


def popularityCounter(popularity_list, popularity_counter):
    """
    The function that counts the number of elements exist in the list
    :param list popularity_list: Complete list of popularity index (81 to 100)
    :param map popularity_counter: Map of popularity index with respective count
    :return list: Complete list of popularity index with count
    """
    popularity_count_list = []
    for popularity in popularity_list:
        if popularity in popularity_counter.keys():
            popularity_count_list.append(popularity_counter[popularity])
        else:
            popularity_count_list.append(0)
    return popularity_count_list


if __name__ == "__main__":
    startApplication()
