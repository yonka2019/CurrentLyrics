from urllib.parse import quote
import webbrowser
import requests
import base64
import config
import re

# URLS
AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'


def main():
	code = get_auth_code()
	refresh_token = get_refresh_token(code)
	print(f"Refresh Token - {refresh_token}")  # refresh & view the 'refresh_token'


def get_auth_code():
	open_url = f"{AUTH_URL}?client_id={config.spotify_auth_info['CLIENT_ID']}&response_type=code&redirect_uri={quote(config.spotify_auth_info['REDIRECT_URI'])}&scope=user-read-currently-playing"
	webbrowser.open(open_url)

	redirected_url = input("Input redirected url: ")
	matches = re.search("code=(.+)$", redirected_url)

	if matches is not None:
		return matches.group(1)
	else:
		print("Wrong redirected url =//")
		exit(1)


def get_refresh_token(code):
	payload = {
		"grant_type": "authorization_code",
		"code": code,
		"redirect_uri": config.spotify_auth_info['REDIRECT_URI'],
		"client_id": config.spotify_auth_info['CLIENT_ID'],
		"client_secret": config.spotify_auth_info['CLIENT_SECRET'],
	}

	# Make a request to the /token endpoint to get an access token
	response = requests.post(url=TOKEN_URL, data=payload)

	# convert the response to JSON
	response_data = response.json()

	return response_data["refresh_token"]


def get_auth_token(refresh_token):
	headers = {
		"Authorization": f"Basic {str(base64.urlsafe_b64encode(bytes(config.spotify_auth_info['CLIENT_ID'] + ':' + config.spotify_auth_info['CLIENT_SECRET'], 'ascii')), 'ascii')}"
	}
	payload = {
		"grant_type": "refresh_token",
		"refresh_token": refresh_token
	}

	response_data = requests.post(url=TOKEN_URL, headers=headers, data=payload).json()
	data_access_token = response_data["access_token"]

	return data_access_token


if __name__ == '__main__':
	main()
