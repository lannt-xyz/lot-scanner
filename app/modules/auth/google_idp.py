from httpx_oauth.clients.google import GoogleOAuth2

from config import settings

# OAuth2 with Google
GOOGLE_CLIENT_ID = settings.google_client_id
GOOGLE_CLIENT_SECRET = settings.google_client_secret

google_oauth_client = GoogleOAuth2(
    GOOGLE_CLIENT_ID,
    GOOGLE_CLIENT_SECRET,
    scopes=["openid", "email", "profile"],
)

