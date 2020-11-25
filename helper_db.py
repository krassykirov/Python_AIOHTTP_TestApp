import pyodbc,requests
import os,json



async def db_connect():
    try:
        con = pyodbc.connect(conn_str)
        return con
    except pyodbc.Error as e:
        print(e)

def get_app_config_data_from_key_vault():
    msi_endpoint = os.environ.get("MSI_ENDPOINT")
    msi_secret = os.environ.get("MSI_SECRET")
    token_auth_uri = f"{msi_endpoint}?resource=https://vault.azure.net&api-version=2017-09-01"
    head_msi = {'Secret': msi_secret}
    resp = requests.get(token_auth_uri, headers=head_msi)
    access_token = resp.json()['access_token']
    con_str = "https://krassykeyvault.vault.azure.net/secrets/constr?api-version=2016-10-01"
    app_config = "https://krassykeyvault.vault.azure.net/secrets/kr9data?api-version=2016-10-01"
    headers = {'Authorization': 'Bearer {}'.format(access_token)}
    constr = requests.get(con_str, headers=headers).json()
    app_data = requests.get(app_config, headers=headers).json()
    constr = constr.get('value')  # str_to_dict => d1 = eval('string_value')
    app_data = app_data.get('value')
    app_data = json.loads(app_data)
    return constr, app_data
