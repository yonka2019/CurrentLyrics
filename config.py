import SpotifyAuth

SPOTIFY_REFRESH_TOKEN = "-"

spotify_auth_info = dict(
	CLIENT_ID='-',
	CLIENT_SECRET='-',
	REDIRECT_URI='-'
)

access_tokens = dict(
	ACCESS_TOKEN_GENIUS='-',
	ACCESS_TOKEN_SPOTIFY=SpotifyAuth.get_auth_token(SPOTIFY_REFRESH_TOKEN)
)
