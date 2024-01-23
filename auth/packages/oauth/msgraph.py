import os
from authlib.integrations.flask_client import OAuth

msgraph = OAuth()


msgraph.register(
    name='msgraph',
    client_id=os.getenv('CLIENT_ID'),
    client_secret=os.getenv('CLIENT_SECRET'),
    access_token_url='https://login.microsoftonline.com/organizations/oauth2/v2.0/token',
    access_token_params=None,
    authorize_url='https://login.microsoftonline.com/organizations/oauth2/v2.0/authorize',
    authorize_params=None,
    api_base_url='https://graph.microsoft.com/v1.0/',
    client_kwargs={'scope': 'offline_access User.Read Directory.AccessAsUser.All', 'response_mode': 'query'}
)
