# Spotify Playlist Color Analyzer

This Python script analyzes the colors of album covers in a Spotify playlist and displays the dominant colors along with the closest rainbow color for each track.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your_username/spotify-playlist-color-analyzer.git
    ```

2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Replace the placeholders in the script (`spotify_playlist_color_analyzer.py`) with your Spotify API credentials:

    ```python
    SPOTIPY_CLIENT_ID = 'your_client_id'
    SPOTIPY_CLIENT_SECRET = 'your_client_secret'
    SPOTIPY_REDIRECT_URI = 'your_redirect_uri'
    username = 'your_username'
    ```

2. Run the script:

    ```bash
    python spotify_playlist_color_analyzer.py
    ```

3. Follow the prompts to authenticate with Spotify and enter the playlist URL to analyze.

## Features

- Retrieves tracks from a Spotify playlist using the Spotipy library.
- Extracts the dominant color of album covers using the ColorThief library.
- Converts RGB colors to their closest rainbow color names.
- Displays track names, artist names, dominant colors, and closest rainbow colors.

## Contributing

Contributions are welcome! If you have any suggestions, bug reports, or feature requests, please open an issue or submit a pull request.

## License

This project is licensed under the Creative Commons License.

___
