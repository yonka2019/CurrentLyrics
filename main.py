import sys
import webbrowser
import requests
import ctypes
import config
import re

# genius urls
GENIUS_API_URL = "https://api.genius.com"
GENIUS_URL = "https://genius.com"

# spotify urls
SPOTIFY_GET_CURRENT_TRACK_URL = 'https://api.spotify.com/v1/me/player/currently-playing'


def main():
	song_title, artist_name = get_current_playing_track_info()
	print(f"[Spotify]\nCurrently playing:\nSong: {song_title}\nArtist: {artist_name}\n")
	to_open_url = get_track_lyrics_url(song_title, artist_name)
	webbrowser.open(to_open_url)  # Genius lyrics of the current playing song


def get_track_lyrics_url(song_title, artist_name):
	search_url = GENIUS_API_URL + "/search"

	payload = {
		"q": f"{song_title} {artist_name}"
	}
	headers = {
		"Authorization": f"Bearer {config.access_tokens['ACCESS_TOKEN_GENIUS']}"
	}

	response = requests.get(url=search_url, headers=headers, data=payload)
	json = response.json()

	if len(json["response"]["hits"]) == 0:  # If no matches => no lyrics in genius DB
		ctypes.windll.user32.MessageBoxW(
			0, f"Lyrics doesn't exist\n―――――――――\nName: {song_title}\nArtist: {artist_name}", "Genius API - Error", 0x00000010)
		sys.exit("No lyrics match")  # terminate program
	print(f"[Genius]\nLyrics have been successfully found!\n")

	song_info = json["response"]["hits"][0]  # first match

	for hit in json["response"]["hits"]:
		if artist_name in hit["result"]["primary_artist"]["name"]:  # If better match exist (by artist name)
			song_info = hit
			break

	if song_info:
		web_open_url = GENIUS_URL + song_info["result"]["path"]
		return web_open_url


def get_current_playing_track_info():
	headers = {
		"Authorization": f"Bearer {config.access_tokens['ACCESS_TOKEN_SPOTIFY']}"
	}

	response = requests.get(url=SPOTIFY_GET_CURRENT_TRACK_URL, headers=headers)
	json_resp = response.json()

	track_name = json_resp['item']['name']
	artist = [artist for artist in json_resp['item']['artists']][0]['name']

	track_name = remove_addons(track_name)
	return track_name, artist


def remove_addons(track_name):
	# removes "SONG_NAME -->> [feat. some1] <<--"
	matches = re.search(r"^(.+) \[.+]", track_name)
	if matches is not None:
		track_name = matches.group(1)
		return track_name  # leave function

	# removes "SONG_NAME -->> (feat. some1) <<--"
	matches = re.search(r"^(.+) \(.+\)", track_name)
	if matches is not None:
		track_name = matches.group(1)

	# removes "SONG_NAME -->> - lalala <<--"
	matches = re.search(r"^(.+) -", track_name)
	if matches is not None:
		track_name = matches.group(1)

	return track_name


if __name__ == '__main__':
	main()
