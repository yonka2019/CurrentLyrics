import SpotifyAuth

SPOTIFY_REFRESH_TOKEN = "-"

spotify_auth_info = dict(
	CLIENT_ID='-',
	CLIENT_SECRET='-',
	REDIRECT_URI='https://google.co.il'
)

access_tokens = dict(
	ACCESS_TOKEN_GENIUS='KqPm_maXDj8OaCd1_a0MKx3TCleHg8oW8BEnYgJq2MSbBjJ7xdltLI3qHatAGc7y',
	ACCESS_TOKEN_SPOTIFY=SpotifyAuth.get_auth_token(SPOTIFY_REFRESH_TOKEN)
)
