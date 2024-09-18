<b>Spotify Data Tracker</b>
This project is a web application that uses the Spotify API to retrieve and store the recently played tracks of a Spotify user. The app is built with Flask, Spotipy (a Python library to interact with Spotify's API), and stores the data in a local SQLite database.

Features
Spotify Authentication:

Uses OAuth2 to authenticate the user via Spotify.
User session management is handled using FlaskSessionCacheHandler.
Retrieve Recently Played Tracks:

Fetches the tracks a user has played over the last 30 days using the Spotify API.
The tracks are stored in a SQLite database after validating that there are no duplicates or null values.
List Playlists:

Allows the user to retrieve a list of their playlists and access them through the app.
Track Storage:

Recently played tracks are stored in a local SQLite database for future reference. The database ensures no duplicate records by using the played_at field as the primary key.
Code Structure
Dependencies
requests: For making HTTP requests.
datetime: To handle date and time.
os: To manage system variables and configuration.
pandas: For managing and processing data in DataFrames.
sqlalchemy and sqlite3: To interact with the SQLite database.
Flask: To create the web application.
Spotipy: To connect to the Spotify API.
Main Components
Spotify Authentication: The authentication flow is managed by SpotifyOAuth, with session-based caching to prevent repeated authentication prompts.

Data Validation: The check_if_valid_data function ensures that the data retrieved from the Spotify API:

Is not empty.
Does not contain null values.
Does not have duplicate entries, using the played_at field as the primary key.
Key Routes:

/: Starts the Spotify authentication process if needed.
/get_user_recently_played_songs: Retrieves and stores the user’s recently played tracks in the database.
/get_playlists: Retrieves the user’s playlists.
/logout: Logs the user out of the session.
Database:

SQLite is used to store recently played tracks. The database is created if it doesn't exist, and it ensures new tracks aren’t duplicated before being saved.
