import os
from authlib.integrations.flask_client import OAuth

github = OAuth()


github.register(
    name='github',
    client_id=os.getenv('GITHUB_CLIENT_ID'),
    client_secret=os.getenv('GITHUB_CLIENT_SECRET'),
    access_token_url='https://github.com/login/oauth/access_token',
    access_token_params=None,
    authorize_url='https://github.com/login/oauth/authorize',
    authorize_params=None,
    api_base_url='https://api.github.com/user',
    client_kwargs={'scope': 'read:user', 'response_mode': 'query'}
)
