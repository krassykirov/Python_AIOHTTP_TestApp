# import pyodbc,requests
# import os,json
#
# async def db_connect():
#     conn_str = get_connstr_from_key_vault()
#     con = pyodbc.connect(conn_str)
#     return con

# def get_connstr_from_key_vault():
#     msi_endpoint = os.environ.get("MSI_ENDPOINT")
#     msi_secret = os.environ.get("MSI_SECRET")
#     token_auth_uri = f"{msi_endpoint}?resource=https://vault.azure.net&api-version=2017-09-01"
#     head_msi = {'Secret': msi_secret}
#     resp = requests.get(token_auth_uri, headers=head_msi)
#     access_token = resp.json()['access_token']
#     endpoint = "https://krassykeyvault.vault.azure.net/secrets/constr?api-version=2016-10-01"
#     headers = {"Authorization": 'Bearer {}'.format(access_token)}
#     response = requests.get(endpoint, headers=headers).json()
#     conn_str = response.get('value')
#     return conn_str

