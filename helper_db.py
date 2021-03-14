import pyodbc,requests
import os,json

def get_app_config_data_from_key_vault():
    token_endpoint = "https://login.microsoftonline.com/krassykirovoutlook.onmicrosoft.com/oauth2/v2.0/token"
    data = {
        'grant_type': 'client_credentials',
        'client_id': '8ff7301f-cb19-43d7-968d-9530f85339b7',
        'client_secret': "ZVE_jyer5354AZd19SjnnAnH_qVmbQeI--",
        'scope': 'https://vault.azure.net/.default'
    }
    # VAULT_URL must be in the format 'https://<vaultname>.vault.azure.net'
    uri = "https://krassykeyvault.vault.azure.net/secrets/connstr?api-version=2016-10-01"
    uri2 = "https://krassykeyvault.vault.azure.net/secrets/data?api-version=2016-10-01"
    r = requests.post(token_endpoint, data=data)
    token = r.json().get('access_token')
    headers = {'Authorization': 'Bearer {}'.format(token)}
    constr = requests.get(uri, headers=headers).json()
    app_data = requests.get(uri2, headers=headers).json()

    constr = constr.get('value')  # str_to_dict => d1 = eval('string_value')
    app_data = app_data.get('value')
    app_data = json.loads(app_data)
    return constr, app_data

conn_str,data = get_app_config_data_from_key_vault()

async def db_connect():
    try:
        conn = pyodbc.connect(conn_str)
        return conn
    except pyodbc.Error as error:
        raise Exception("Unable to connect to the Database server ",error)


