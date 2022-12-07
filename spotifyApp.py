"""
Search and get Spotify tracks and artists

Submitted by:
Auradee Castro
Olivia Deguit
"""
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
    Exit = "5"


class Info(Enum):
    Artist = "1"
    Genres = "2"
    Track = "3"
    Deactivated = "4"


class Report(Enum):
    Artist_Follower = "1"
    Artist_Popularity = "2"
    Track_Popularity = "3"

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
        print("5. Exit Application")

        req_command = input(f"\n{ef.BRIGHT}Select one option from the list (1, 2, 3, 4 or 5): ").strip()

        if req_command not in [elem.value for elem in Command]:
            print("Invalid selection. Try again.")
        elif req_command == Command.Exit.value:
            print(f"\n{bg.GREEN} Thank you for using the application! ")
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
                print("1. Top 20 Artists with Most Number of Followers")
                print("2. Top 10 Artists with Highest Popularity Rating")
                print("3. Top 10 Tracks with Highest Popularity Rating")

                req_report = input(f"\n{ef.BRIGHT}Select one option from the list (1, 2 or 3): ").strip()
                if req_report not in [elem.value for elem in Report]:
                    print(f"{fg.RED}Invalid selection")
                else:
                    viewReport(req_report)

            elif req_command == Command.Refresh.value:
                refreshArtistInfo()

            elif req_command == Command.Deactivate.value:
                artist_id = input("\nEnter Artist ID: ").strip()
                has_result = deactivateArtistInfo(artist_id)
                if not has_result:
                    print(f"{fg.RED}Invalid artist ID")

            is_continue = ""
            while is_continue != "n" and is_continue != "y":
                is_continue = input(f"\n{ef.BRIGHT}Do you want to continue? [y/n]: ").strip().lower()
                if is_continue != "n" and is_continue != "y":
                    print(f"{fg.RED}Invalid input. Type 'y' for yes or 'n' for no.")
            else:
                if is_continue == 'n':
                    print(f"\n{bg.GREEN} Thank you for using the application! ")
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
            artist_list = list(dbconnect.searchDeactivatedArtistInfo())

    if len(artist_list) == 0:
        return False

    for artist in artist_list:
        if selection == Info.Track.value:
            for track in artist['tracks']:
                if keyword in str(track['name']).lower():
                    print()
                    print(f"{fg.MAGENTA}{ef.BRIGHT}Track Name: {track['name']}")
                    print(f"Track ID: {track['id']}")
                    if artist['status'] == 'A':
                        print(f"Artist Name: {artist['name']} (DEACTIVATED)")
                    else:
                        print(f"Artist Name: {artist['name']}")
                    print(f"Album: {track['album']}")
                    print(f"Popularity: {track['popularity']}")
        else:
            print()
            if artist['status'] == 'A':
                print(f"{fg.MAGENTA}{ef.BRIGHT}Artist Name: {artist['name']}")
            else:
                print(f"{fg.MAGENTA}{ef.BRIGHT}Artist Name: {artist['name']} (DEACTIVATED)")
            print(f"Artist ID: {artist['id']}")
            print(f"Genres: {', '.join(artist['genres'])}")
            print(f"Popularity: {artist['popularity']}")
            print(f"Followers: {artist['followers']}")

    return True


def viewReport(report_type):

    match report_type:
        case Report.Artist_Follower.value:

            artist_list = list(dbconnect.getAllArtistsByFollowers())
            artist_names = [artist_list[idx]['name'] for idx in range(10)]
            artist_followers = [artist_list[idx]['followers'] for idx in range(10)]

            visualization.showBarGraph(artist_followers,
                                       artist_names,
                                       x_label='Number of Followers (in millions)',
                                       title='Top 10 Artists with Most Number of Followers')

        case Report.Artist_Popularity.value:

            artist_list = list(dbconnect.getAllArtistsByPopularity())
            artist_names = [artist_list[idx]['name'] for idx in range(10)]
            artist_popularity = [artist_list[idx]['popularity'] for idx in range(10)]

            visualization.showBarGraph(artist_popularity,
                                       artist_names,
                                       add_val=True,
                                       x_label='Popularity Index',
                                       title='Top 10 Artists with Highest Popularity Index')

            popularity_counter = Counter([artist['popularity'] for artist in artist_list if artist['popularity'] > 80])
            popularity_list = [i for i in range(81, 101)]
            popularity_count_list = []

            for popularity in popularity_list:
                if popularity in popularity_counter.keys():
                    popularity_count_list.append(popularity_counter[popularity])
                else:
                    popularity_count_list.append(0)

            visualization.showLineGraph(popularity_list,
                                        popularity_count_list,
                                        x_label='Popularity Index',
                                        y_label='Number of Artists',
                                        title='Number of Artists per Popularity Index')

        case Report.Track_Popularity.value:
            pass

def refreshArtistInfo():
    print(f"\n{bg.YELLOW}{fg.BLACK} WARNING: All active artist profiles will be replaced by records from Spotify ")

    req_enable = input(f"{ef.BRIGHT}Are you sure you want to refresh the data? [y/Y]: ").lower().strip()
    if req_enable == 'y':
        print("Connecting to Spotify to get artist records...")
        artists = spotifyconnect.getSpotifyArtists('2022')
        print("Saving artist records..")
        dbconnect.refreshArtists(artists)
    else:
        print("No changes done")


def deactivateArtistInfo(artist_id):

    artist_info = list(dbconnect.getArtistInfo(artist_id))
    if len(artist_info) == 0:
        return False

    print(f"Artist Name: {artist_info[0]['name']}")

    if artist_info[0]['status'] == 'I':
        req_enable = input(f"{ef.BRIGHT}Would you like to activate this artist profile? [y/Y]: ").lower().strip()
        if req_enable == 'y':
            is_activated = dbconnect.deactivateArtistInfo(artist_id, False)
            if is_activated:
                print(f"{fg.GREEN}Successfully activated")
        else:
            print("No changes done")
    else:
        req_disabled = input(f"{ef.BRIGHT}Are you sure you want to deactivate this artist profile? [y/Y]: ").lower().strip()
        if req_disabled == 'y':
            is_deactivated = dbconnect.deactivateArtistInfo(artist_id, True)
            if is_deactivated:
                print(f"{fg.GREEN}Successfully deactivated")
        else:
            print("No changes done")

    return True


if __name__ == "__main__":
    #startApplication()
    viewReport(Report.Artist_Popularity.value)
