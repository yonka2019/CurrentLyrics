import requests
import webbrowser
import ctypes
import re
import config

# genius consts
GENIUS_API_URL = "https://api.genius.com"
GENIUS_URL = "https://genius.com"

# spotify consts
SPOTIFY_GET_CURRENT_TRACK_URL = 'https://api.spotify.com/v1/me/player/currently-playing'


def main():
	song_title, artist_name = get_current_playing_track()
	to_open_url = get_track_lyrics_url(song_title, artist_name)

	if to_open_url is None:
		ctypes.windll.user32.MessageBoxW(0, f"Can't find lyrics:\n{song_title} - {artist_name}", "Genius API - Error",
										 0x00000010)
		exit(1)

	webbrowser.open(to_open_url)


def get_track_lyrics_url(song_title, artist_name):
	search_url = GENIUS_API_URL + "/search"

	response = requests.get(
		search_url,
		data={
			"q": f"{song_title} {artist_name}"
		},
		headers={
			"Authorization": f"Bearer {config.tokens['GENIUS']}"
		}
	)
	json = response.json()

	song_info = None

	for hit in json["response"]["hits"]:
		if artist_name in hit["result"]["primary_artist"]["name"]:
			song_info = hit
			break

	if song_info:
		web_open_url = GENIUS_URL + song_info["result"]["path"]
		return web_open_url


def get_current_playing_track():
	response = requests.get(
		SPOTIFY_GET_CURRENT_TRACK_URL,
		headers={
			"Authorization": f"Bearer {config.tokens['SPOTIFY']}"
		}
	)

	json_resp = response.json()
	track_name = json_resp['item']['name']
	artist = [artist for artist in json_resp['item']['artists']][0]['name']

	# remove "SONG_NAME -->> (feat. some) <<--"
	matches = re.search(r"^(.+) \(.+\)$", track_name)
	if matches is not None:
		track_name = matches.group(1)

	return track_name, artist


if __name__ == '__main__':
	main()
