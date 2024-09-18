<b>Spotify Data Tracker</b>

This project is a web application that uses the Spotify API to retrieve and store the recently played tracks of a Spotify user. The app is built with Flask, Spotipy (a Python library to interact with Spotify's API), and stores the data in a local SQLite database.

<b>Features</b>

<b></b>
<i></i>
<b>Spotify Authentication:</b>

- Uses OAuth2 to authenticate the user via Spotify.

- User session management is handled using FlaskSessionCacheHandler.

<b>Retrieve Recently Played Tracks:</b>


- Fetches the tracks a user has played over the last 30 days using the Spotify API.

- The tracks are stored in a SQLite database after validating that there are no duplicates or null values.

<b>List Playlists:</b>

- Allows the user to retrieve a list of their playlists and access them through the app.

<b>Track Storage:</b>

- Recently played tracks are stored in a local SQLite database for future reference. The database ensures no duplicate records by using the played_at field as the primary key.

<b>Code Structure</b>

<b>Dependencies</b>

<i>requests</i>: For making HTTP requests.

<i>datetime</i>: To handle date and time.

<i>os</i>: To manage system variables and configuration.

<i>pandas</i>: For managing and processing data in DataFrames.

<i>sqlalchemy</i> and <i>sqlite3</i>: To interact with the SQLite database.

<i>Flask</i>: To create the web application.

<i>Spotipy</i>: To connect to the Spotify API.

<b>Main Components</b>

<b>Spotify Authentication:</b>
 The authentication flow is managed by SpotifyOAuth, with session-based caching to prevent repeated authentication prompts.

<b>Data Validation:</b>
 The check_if_valid_data function ensures that the data retrieved from the Spotify API:

- Is not empty.

- Does not contain null values.

- Does not have duplicate entries, using the played_at field as the primary key.

<b>Key Routes:</b>


- /: Starts the Spotify authentication process if needed.

- /get_user_recently_played_songs: Retrieves and stores the user’s recently played tracks in the database.

- /get_playlists: Retrieves the user’s playlists.

- /logout: Logs the user out of the session.

<b>Database:</b>


- SQLite is used to store recently played tracks. The database is created if it doesn't exist, and it ensures new tracks aren’t duplicated before being saved.
