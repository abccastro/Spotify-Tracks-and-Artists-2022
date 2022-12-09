# Spotify Artist and Tracks (2022)

The application data is currently limited to first 1000 Spotify tracks in 2022 and their corresponding artist. Data extracted from Spotify are stored in MongoDB Atlas.

[Instructions to connect to Spotify API](https://cran.r-project.org/web/packages/spotidy/vignettes/Connecting-with-the-Spotify-API.html)

## Application Features
1. Search for Artists or Tracks
* Search for Artists (by Name)
* Search for Artists (by Genre)
* Search for Tracks (by Track Name)
* List Deactivated Artist Profile
2. View Reports
* Top 10 Artists with Most Number of Followers
* Top 10 Artists with Highest Popularity Index
* Top 10 Tracks with Highest Popularity Index
* Number of Artists by Popularity Index (80 to 100)
* Number of Tracks by Popularity Index (80 to 100)
3. Refresh Artists and Tracks
4. Deactivate/Activate Artist Profile
5. Delete All Artist Profiles

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the following packages
```bash
pip install pymongo
pip install enum
pip install colorama
pip install collections
pip install pickle
pip install datetime
pip install spotipy
```

## Program Execution
```bash
python spotifyApp.py
```

## Contributors

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## References

* https://developer.spotify.com/documentation/web-api/reference/#/operations/get-track
