import sconekc as kc
import os

SERVER=os.environ['KEYCLOAK']
REALM=os.environ['MBOLREALM']
CLIENT=os.environ['MBOLCLIENT']
USERNAME=os.environ['MBOLUSER']
PASSWORD=os.environ['MBOLPASS']

try:
    AT=kc.get_access_token(SERVER, REALM, CLIENT, USERNAME, PASSWORD, cert='cert.pem', key='key.pem')
    print("Access Token")
    kc.showJWT(AT)
    VT=kc.get_validation_token(SERVER, REALM, AT, cert='cert.pem', key='key.pem')
    print("Validation Token")
    print(VT)
except Exception as e:
    print(f'Exception: {e}')
