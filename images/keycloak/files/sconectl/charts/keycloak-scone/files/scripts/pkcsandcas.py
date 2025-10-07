# -----------------------------------------------------------------------------
# The MIT License (MIT)
# Copyright (c) 2018 Robbie Coenmans
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# -----------------------------------------------------------------------------

import argparse
import OpenSSL

def read_certificate(ca_cert):
    with open(ca_cert, mode='rb') as file:
        return OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, file.read())

def read_private_key(ca_key, passphrase=None):
    with open(ca_key, mode='rb') as file:
        return OpenSSL.crypto.load_privatekey(OpenSSL.crypto.FILETYPE_PEM, file.read(), passphrase=passphrase)

def export_to_pkcs12(filename, key, cert, passphrase=None):
    pkcs = OpenSSL.crypto.PKCS12()
    pkcs.set_privatekey(key)
    pkcs.set_certificate(cert)
    with open(filename, 'wb') as file:
        file.write(pkcs.export(passphrase=passphrase))

''' #########
# The following is added by mig at Scontain GmbH* upload session to CAS

'''
import json, requests
import os
import io
import binascii
import sys


def validate_envvar(envvar):
    try:
        _validate=os.environ[envvar]
        return _validate
    except KeyError: 
        print(f"..:ERR:You must set a valid {envvar} environment")
        sys.exit(1)


def fail_message_exit(message: str, payload: any):
    print(message)
    print(payload)
    exit(1)


###
# Global variables

# PKCS=validate_envvar("PKCS") #os.environ.get("PKCS", "/ChangeThisNameDynamically.pkcs12")
PKCSPWD=validate_envvar("PKCSPWD") #os.environ.get("PKCSPWD", "TUDciamSCONE")
PKCSALIAS=validate_envvar("PKCSALIAS") #os.environ.get("PKCSALIAS", "MARIADB_CLIENT_CERT")
PKCSCACRT=validate_envvar("PKCSCACRT") #os.environ.get("PKCSCACRT", "/tls/i_mariadb-ca.crt")
PKCSCERT=validate_envvar("PKCSCERT") #os.environ.get("PKCSCERT", "/tls/i_mariadb-client.crt")
PKCSCERTPRIV=validate_envvar("PKCSCERTPRIV") #os.environ.get("PKCSCERTPRIV", "/tls/i_mariadb-client.key")
CASCLICERT=validate_envvar("CASCLICERT") #os.environ.get("CASCLICERT", "/python/cert.pem")
CASCLIKEY=validate_envvar("CASCLIKEY") #os.environ.get("CASCLIKEY", "/python/key.pem")
# CASCLICERTSUBJ=validate_envvar("CASCLICERTSUBJ") #os.environ.get("CASCLICERTSUBJ", "/C=DE/ST=SA/L=Dresden/O=Scontain/OU=Sconectl/CN=ciam")
POLTMPL=validate_envvar("POLTMPL") #os.environ.get("POLTMPL", "/python/pol.template.yaml")
# POLHASHES=validate_envvar("POLHASHES") #os.environ.get("POLHASHES", "/python/hashespkcs.list")
# POLREG=validate_envvar("POLREG") #os.environ.get("POLREG", "/polpkcs.yaml")
SECRETSTORE=validate_envvar("SECRETSTORE") #os.environ.get("SECRETSTORE", "MariadbPkcs12")

CAS_URL=validate_envvar("CAS_URL") #""
CAS_SESSION=validate_envvar("CAS_SESSION") #""
SFX_PKCS_SESSION=validate_envvar("SFX_PKCS_SESSION") #""
EXPSESS=CAS_SESSION.split('/')[0]+'/'+CAS_SESSION.split('/')[1]
KEYBIN=""
# memPOLREG=io.StringIO("")
memPOLREG=io.BytesIO(None)

POLNAME=CAS_SESSION[0:CAS_SESSION.find("/")]+"-"+SFX_PKCS_SESSION



def export_to_pkcs12_memfile(key, cert, friendlyname, passphrase=None):
    pkcs = OpenSSL.crypto.PKCS12()
    pkcs.set_privatekey(key)
    pkcs.set_certificate(cert)
    pkcs.set_friendlyname(friendlyname)
    pkcsbincontent=pkcs.export(passphrase=passphrase)
    pkcsbytecontent = binascii.hexlify(pkcsbincontent).decode()
    global KEYBIN
    KEYBIN=str(pkcsbytecontent)


def build_policies(predecessor):
    global memPOLREG
    with open(POLTMPL, 'r') as pol:
        polcontent=pol.read().replace("POLNAME", POLNAME).replace("KEYBIN", KEYBIN).replace("EXPSESS", EXPSESS).replace("SECRETSTORE", SECRETSTORE)
        memPOLREG=binascii.unhexlify(binascii.hexlify(bytes(polcontent.encode())).decode())
        if predecessor != "":
            polcontent="predecessor: "+predecessor+"\n"+polcontent
            memPOLREG=binascii.unhexlify(binascii.hexlify(bytes(polcontent.encode())).decode())


def register_policies():
    sessionCAS = requests.Session()
    sessionCAS.verify = False
    sessionCAS.cert=(CASCLICERT, CASCLIKEY)

    try:
        response = sessionCAS.get("https://"+CAS_URL+":8081/v1/sessions/"+POLNAME
                                  , headers={"Content-Type":"application/x-www-form-urlencoded"}
                                  )
        body=response.json()
        try:
            if str(body['msg'][0]).find('Session not found') != -1:
                response = sessionCAS.post("https://"+CAS_URL+":8081/session"
                                    , headers={'Content-Type': 'application/octet-stream'}
                                    , data=memPOLREG
                                    )
                body=response.json()
                try:
                    sessionhash=str(body['hash'])
                    print("..:DBG:new session's hash="+sessionhash)
                except KeyError: 
                    fail_message_exit("..:ERR:session registration failed", body)
            else:
                fail_message_exit("..:ERR:unexpected error registering new session", body)
        except KeyError: 
            try:
                sessionexistent=body['session']
                sessionhash=body['hash']
                print("..:DBG:existing session's hash="+sessionhash)
                print("..:DBG:recreate policies file")
                build_policies(sessionhash)
                response = sessionCAS.post("https://"+CAS_URL+":8081/session"
                                    , headers={'Content-Type': 'application/octet-stream'}
                                    , data=memPOLREG
                                    ) #, 
                body=response.json()
                sessionhash=str(body['hash'])
                print("..:DBG:updated session's hash="+sessionhash)
            except KeyError: 
                fail_message_exit("..:ERR:unexpected error updating existing session", body)
    except requests.exceptions.ConnectionError as errcnx:
        print("[ERR]Exception:", errcnx.strerror)
        print("[ERR]Exception:", errcnx)
        exit(1)
        



if __name__ == '__main__':
    key_path   = PKCSCERTPRIV
    cert_path  = PKCSCERT
    passphrase = PKCSPWD
    friendlyname = PKCSALIAS

    if len(passphrase) == 0:
        passphrase = None
    else:
        passphrase = passphrase.encode()

    if len(friendlyname) == 0:
        friendlyname = None
    else:
        friendlyname = friendlyname.encode()

    key  = read_private_key(key_path, passphrase)
    cert = read_certificate(cert_path)
    export_to_pkcs12_memfile(key, cert, friendlyname, passphrase)
    build_policies("")
    register_policies()
