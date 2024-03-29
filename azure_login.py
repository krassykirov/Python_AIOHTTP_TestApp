import urllib,adal,uuid,os
import json, requests,datetime
from jose import jws
import urllib.parse
import aiohttp_jinja2
from aiohttp import web
from msrestazure.azure_active_directory import AADTokenCredentials
from aiohttp_session import get_session
from helper_db import get_app_config_data_from_key_vault

conn_str,data = get_app_config_data_from_key_vault()

CLIENT_ID = data['CLIENT_ID']
CLIENT_SECRET = data['CLIENT_SECRET']
REDIRECT_URI = data['REDIRECT_URI']
TENANT = data['TENANT']
AUTHORITY_URL = 'https://login.microsoftonline.com/common'
AUTH_ENDPOINT = '/oauth2/v2.0/authorize'
TOKEN_ENDPOINT = '/oauth2/v2.0/token'
RESOURCE = 'https://graph.microsoft.com/'
API_VERSION = 'beta'
SCOPES = ['User.ReadAll','openid','profile','email']
keys_url = f'https://login.microsoftonline.com/{TENANT}/discovery/keys'
keys_raw = requests.get(keys_url).text
keys = json.loads(keys_raw)

async def login(request):
    session = await get_session(request)
    try:
        auth_state = str(uuid.uuid4())
        print('auth_state',auth_state)
        session['auth_state'] = auth_state
        prompt_behavior = 'select_account'  # prompt_behavior = 'login' select_account
        params = urllib.parse.urlencode({'response_type': 'code id_token',
                                         'client_id': CLIENT_ID,
                                         'redirect_uri': REDIRECT_URI,
                                         'state': auth_state,
                                         'nonce': str(uuid.uuid4()),
                                         'scope': 'openid email',
                                         'prompt': prompt_behavior,
                                         'response_mode': 'form_post'})

        print(AUTHORITY_URL + '/oauth2/v2.0/authorize?' + params)
        return web.HTTPFound(AUTHORITY_URL + '/oauth2/v2.0/authorize?' + params)

    except Exception as error:
        return str(error)

async def authorized(request):
    session = await get_session(request)
    data = await request.post()
    if data['state'] != session['auth_state']:
        raise Exception('state returned to redirect URL does not match!')
    try:
        code = data['code']
        id_token = data['id_token']
        id_token_decoded = json.loads(jws.verify(id_token, keys, algorithms=['RS256']))
        email = id_token_decoded['email'].split('@')[0]

        auth_context = adal.AuthenticationContext(AUTHORITY_URL, api_version=None)
        token_response = auth_context.acquire_token_with_authorization_code(
            code, REDIRECT_URI, RESOURCE, CLIENT_ID, CLIENT_SECRET)

        session['access_token'] = token_response['accessToken']
        session['last_visit'] = str(datetime.datetime.now())
        session['email'] = id_token_decoded['email']
        expires_in = datetime.datetime.now() + datetime.timedelta(seconds=token_response.get('expires_in', 3599))
        expires_in = expires_in.strftime("%m/%d/%Y, %H:%M:%S")
        session['expires_in'] = str(expires_in)
        session['username'] = id_token_decoded['email']
        session['last_visit'] = str(datetime.datetime.now())
        with open('token.txt','a') as file:
            file.write(str(session)+'\n')
        context = {"id_token" : id_token, "id_token_decoded" : id_token_decoded,'token_exp': expires_in,'email':email,
                   'email2':id_token_decoded['email'],'time' : datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),'username':session['username']}
        return aiohttp_jinja2.render_template("graphcall.html", request, context=context)

    except Exception as error:
            return error

def login_required(fn):
    async def wrapped(request, *args, **kwargs):
        session = await get_session(request)
        if not 'username' in session:
            return web.HTTPFound('/auth') # return web.HTTPFound(request.rel_url) not working
        return await fn(request, *args, **kwargs)

    return wrapped

async def authenticate_client_key(request):
    authority_host_uri = 'https://login.microsoftonline.com'
    authority_uri = authority_host_uri + '/' + TENANT

    context = adal.AuthenticationContext(authority_uri, api_version=None)
    mgmt_token = context.acquire_token_with_client_credentials(RESOURCE, CLIENT_ID, CLIENT_SECRET)
    credentials = AADTokenCredentials(mgmt_token, CLIENT_ID)
    token = credentials.token['access_token']
    uri = "https://graph.microsoft.com/beta/users?$filter=startsWith(userPrincipalName,'dron')&$select=UserPrincipalName"
    headers = {'Authorization': 'Bearer {}'.format(token)}
    r = requests.get(uri, headers=headers).json()
    users  = r['value']
    return aiohttp_jinja2.render_template("azure-users.html", request, context= {'users':users})


