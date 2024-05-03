import pyodbc,requests
import os,json

def get_app_config_data_from_key_vault():

    msi_endpoint = os.environ.get("MSI_ENDPOINT")
    msi_secret = os.environ.get("MSI_SECRET")
    token_auth_uri = f"{msi_endpoint}?resource=https://vault.azure.net&api-version=2017-09-01"
    head_msi = {'Secret': msi_secret}
    resp = requests.get(token_auth_uri, headers=head_msi)
    access_token = resp.json()['access_token']
    con_str = "https://krassykeyvault.vault.azure.net/secrets/connstr?api-version=2016-10-01"
    app_config = "https://krassykeyvault.vault.azure.net/secrets/data?api-version=2016-10-01"
    headers = {'Authorization': 'Bearer {}'.format(access_token)}
    constr = requests.get(con_str, headers=headers).json()
    app_data = requests.get(app_config, headers=headers).json()
    constr = constr.get('value')
    app_data = json.loads(app_data.get('value'))
    return constr, app_data

conn_str, data = get_app_config_data_from_key_vault()

async def db_connect():
    try:
        conn = pyodbc.connect(conn_str)
        return conn
    except pyodbc.Error as error:
        raise Exception("Unable to connect to the Database server ",error)


