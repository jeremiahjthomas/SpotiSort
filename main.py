import spotipy
from spotipy.oauth2 import SpotifyOAuth
from colorthief import ColorThief
from PIL import Image
from io import BytesIO
import requests
import webcolors

# Spotify API credentials
SPOTIPY_CLIENT_ID = ""
SPOTIPY_CLIENT_SECRET = ""
SPOTIPY_REDIRECT_URI = ""
username = ""

# Get Spotify API credentials
while not SPOTIPY_CLIENT_ID:
    SPOTIPY_CLIENT_ID = input("Enter Spotify Client ID: ")
while not SPOTIPY_CLIENT_SECRET:
    SPOTIPY_CLIENT_SECRET = input("Enter Spotify Client Secret ID: ")
while not SPOTIPY_REDIRECT_URI:
    SPOTIPY_REDIRECT_URI = input("Redirect URL (If applicable): ")
while not username:
    username = input("Username: ")

# Set up Spotipy client
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope=["playlist-modify-public"],
                                               open_browser=False))

def get_dominant_color(image_url):
    try:
        if image_url:
            response = requests.get(image_url)
            img = Image.open(BytesIO(response.content))
            img_bytes = BytesIO()
            img.save(img_bytes, format='JPEG')  # Save the image in JPEG format
            img_bytes = img_bytes.getvalue()

            color_thief = ColorThief(BytesIO(img_bytes))
            dominant_color = color_thief.get_color(quality=1)
            return dominant_color
        else:
            return None
    except Exception as e:
        print(f"Error getting dominant color: {e}")
        return None


def get_color_order(color):
    # Define the custom order of colors
    color_order = {'W': 0, 'R': 1, 'O': 2, 'Y': 3, 'G': 4, 'B': 5, 'I': 6, 'V': 7, 'Brown': 8, 'Black': 9}

    # Check if the color is in the custom order, otherwise assign a high value
    return color_order.get(color, float('inf'))

def get_playlist_tracks(playlist_url):
    # Extract playlist ID from the URL
    playlist_id = playlist_url.split('/')[-1].split('?')[0]

    # Get tracks from the playlist
    results = sp.playlist_tracks(playlist_id)
    tracks = results['items']

    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])

    return tracks

def get_track_dominant_color(track):
    try:
        album_url = track['track']['album']['external_urls']['spotify']
        color = get_dominant_color(get_album_cover_url(album_url))
        return color
    except (KeyError, TypeError):
        # Handle the case where the necessary information is missing
        return None

def get_album_color(album_url):
    # Extract album ID from the URL
    album_id = album_url.split('/')[-1]

    try:
        album_details = sp.album(album_id)

        # Check if 'images' key is present and not empty
        if 'images' in album_details and album_details['images']:
            image_url = album_details['images'][0]['url']

            # Get color palette from album cover image
            response = requests.get(image_url)
            img = Image.open(BytesIO(response.content))

            # Convert the Image object to bytes
            img_bytes = BytesIO()
            img.save(img_bytes, format='JPEG')
            img_bytes = img_bytes.getvalue()

            # Get color palette using ColorThief
            color_thief = ColorThief(BytesIO(img_bytes))
            dominant_color = color_thief.get_color(quality=1)

            return dominant_color

    except spotipy.SpotifyException as e:
        print(f"Error getting album details: {e}")
    
    # If album details are incomplete or missing, return None
    return None


def rgb_to_color_name(rgb):
    try:
        color_name = webcolors.rgb_to_name(rgb)
        return color_name.lower()
    except ValueError:
        return None

def sort_tracks_by_color(tracks):
    # Sort the tracks based on the dominant color RGB values
    sorted_tracks = sorted(tracks, key=lambda track: get_track_dominant_color(track))

    return sorted_tracks

def create_spotify_playlist(username, playlist_name, playlist_description, tracks):
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                                   client_secret=SPOTIPY_CLIENT_SECRET,
                                                   redirect_uri=SPOTIPY_REDIRECT_URI,
                                                   scope=["playlist-modify-public"],
                                                   open_browser=False))
    playlist = sp.user_playlist_create(username, playlist_name, public=True, description=playlist_description)

    try:
        print("Adding tracks to the playlist:")
        for track in tracks:
            track_uri = f"spotify:track:{track['track']['id']}"
            print(f"Adding track: {track_uri}")
            sp.playlist_add_items(playlist['id'], [track_uri])

        print(f"\nPlaylist created: {playlist['external_urls']['spotify']}")
    except spotipy.SpotifyException as e:
        print(f"Error adding tracks to the playlist: {e}")

def get_album_cover_url(album_url):
    album_id = album_url.split('/')[-1]
    
    try:
        album_details = sp.album(album_id)
        if 'images' in album_details and album_details['images']:
            return album_details['images'][0]['url']
        else:
            return None
    except spotipy.SpotifyException as e:
        print(f"Error getting album details: {e}")
        return None


if __name__ == "__main__":
    # Hardcoded playlist URL for testing
    #playlist_url = "https://open.spotify.com/playlist/5n4zd8QcbhSj0bSInLn4Tr?si=03d38cd0c10a41e3"
    playlist_url = "https://open.spotify.com/playlist/0gy9vRucjaqWnYhEiDL2M1?si=79bd85b0fcac49b3"
    #playlist_url = "https://open.spotify.com/playlist/27Gcj1WBlGD4JaEWXeN9hz?si=5fa501697ef64781"
    # Print playlist URL for verification
    print("Playlist URL:", playlist_url)

    # Get tracks from the playlist
    playlist_tracks = get_playlist_tracks(playlist_url)

    # Print number of tracks for verification
    print("Number of tracks:", len(playlist_tracks))

    # Sort tracks by album color
    sorted_tracks = sort_tracks_by_color(playlist_tracks)

    # Display the sorted tracks
    for track in sorted_tracks:
        print(f"{track['track']['name']} - {track['track']['artists'][0]['name']}")

    # Create a new playlist and add the sorted tracks to it
    create_spotify_playlist(username, "Color Sorted Playlist", "A playlist sorted by album color", sorted_tracks)
