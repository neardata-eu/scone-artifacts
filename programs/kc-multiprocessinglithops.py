from werkzeug.serving import make_server
import threading
from flask import Flask, session, request, jsonify, abort
import logging as log
import time
import sconekc as kc
import json
import os


###
# based on the works by Ruben Decrop at https://stackoverflow.com/a/45017691
class ServerThread(threading.Thread):

    def __init__(self, app):
        threading.Thread.__init__(self)
        self.server = make_server('127.0.0.1', 4443, app)
        self.ctx = app.app_context()
        self.ctx.push()

    def run(self):
        log.info('starting server')
        self.server.serve_forever()

    def shutdown(self):
        self.server.shutdown()


###
# start server thread
def start_server():
    global server
    app = Flask('neardatawebapp')

    # App routes defined here

    ###
    # callback endpoint in localhost to get the access token when Keycloak goes to redirect_uri
    @app.route("/callback")
    def callback():
        return kc.callback_endpoint(kcsession, request, AUTH_SERVER, REALM, CLIENT_ID, REDIRECT_URI)

    server = ServerThread(app)
    server.start()
    print('logging into Keycloak')
    log.info('server started')


###
# start server thread
def stop_server():
    global server
    server.shutdown()


###
# main

###
# global variables
AUTH_SERVER = os.environ['KEYCLOAK']
REALM = os.environ['MBOLREALM']
CLIENT_ID = os.environ['MBOLCLIENT']
ROLE = os.environ['MBOLROLE']
REDIRECT_URI = "http://127.0.0.1:4443/callback"
BROWSER = "/usr/bin/opera"
BROWSER_PARAMS = "--private"

server = threading.Thread
kcsession = kc.KeycloakSession()
browser_t = threading.Thread


if __name__ == "__main__":
    start_server()

    x=lambda: kc.login_browser_auth(kcsession, AUTH_SERVER, REALM, CLIENT_ID, REDIRECT_URI, BROWSER, BROWSER_PARAMS)
    t=threading.Thread(target=x)
    t.start()
    t.join()

    sl = 3
    rd = 10
    print(f'wait {rd} x {sl} secs = {sl*rd}. to login or abort execution')
    while rd > 0:
        if kcsession.touch is True:
            break
        rd = rd-1
        time.sleep(sl)
    stop_server()
    if kcsession.proceed:
        try:
            print(f"Performing verification: RBAC access={ROLE}")
            access_token_json=json.loads(kcsession.access_token_json)
            header, access_token, signature, issued, started, validto = kc.sliceJWT(access_token_json["access_token"])
            if ROLE in access_token['realm_access']['roles']:
                print("User IS AUTHORIZED to proceed with computation")
                print(f"Authorization is valid until {validto}")
                header, payload, signature, issued, started, validto = kc.sliceJWT(access_token_json["access_token"])

                print(f"...")

                print(f"kc.get_validation_token=(AUTH_SERVER, REALM, access_token)")
                VT=kc.get_validation_token(AUTH_SERVER, REALM, access_token_json['access_token'])
                print(f"validation_token={VT}")
                print(f"validation_token.name={VT['name']}")
                if VT['name'] != "":
                    # Lithops execution authorized
                    from lithops.multiprocessing import Pool
                    def double(i):
                        return i * 2
                    with Pool() as pool:
                        result = pool.map(double, [1, 2, 3, 4])
                        print(result)
            else:
                print("User IS FORBIDEN to proceed with computation")
            kc.logout_session(kcsession, AUTH_SERVER, REALM)
        except Exception as e:
            print(f"Exception: {e}")
            kc.logout_session(kcsession, AUTH_SERVER, REALM)
    else:
        kcsession = None
        print(f"Abort execution")
