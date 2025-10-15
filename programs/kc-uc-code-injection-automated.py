import sconekc as kc
import os

SERVER=os.environ['KEYCLOAK']
REALM=os.environ['MBOLREALM']
CLIENT=os.environ['MBOLCLIENT']
USERNAME=os.environ['MBOLUSER']
PASSWORD=os.environ['MBOLPASS']

UC_CODE_INJECTION=os.getenv('UC_CODE_INJECTION', None)

try:
    AT=kc.get_access_token(SERVER, REALM, CLIENT, USERNAME, PASSWORD, cert='cert.pem', key='key.pem')
    VT=kc.get_validation_token(SERVER, REALM, AT, cert='cert.pem', key='key.pem')
    if VT['preferred_username'] == USERNAME:
        if UC_CODE_INJECTION != None:
            exec(UC_CODE_INJECTION)
except Exception as e:
    print(f'Exception: {e}')
