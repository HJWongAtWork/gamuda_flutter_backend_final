from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
from .settings import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET

# Social Media OAuth Configuration
config = Config('.env')
oauth = OAuth(config)

# Google OAuth setup
oauth.register(
    name='google',
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)
